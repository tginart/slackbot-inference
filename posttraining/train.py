import os
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from torch.utils.tensorboard import SummaryWriter
from torch.utils.data import DataLoader
import argparse

from dataset_prep import load_and_prepare_dataset, create_collate_fn

# -----------------------#
# Configurable parameters#
# -----------------------#
parser = argparse.ArgumentParser(description="Fine-tune Whisper on Genshin Voice dataset")
parser.add_argument("--model_id", type=str, default="openai/whisper-large-v3-turbo",
                    help="Hugging Face model name or path for Whisper.")
parser.add_argument("--dataset_name", type=str, default="simon3000/genshin-voice",
                    help="Dataset name on HuggingFace Hub or local path to a HuggingFace dataset directory.")
parser.add_argument("--dataset_path", type=str, default=None,
                    help="(Alias for --dataset_name) Local path to a HuggingFace dataset directory. "
                         "Supports raw audio format (audio, context, transcription, language) "
                         "or preprocessed format (input_features, labels).")
parser.add_argument("--language_option", choices=["auto", "dataset"], default="auto",
                    help="How to handle language tokens: 'auto' for no explicit language (auto-detect), 'dataset' to use dataset's language for each sample.")
parser.add_argument("--output_dir", type=str, default="checkpoints", help="Directory to save checkpoints.")
parser.add_argument("--log_dir", type=str, default="logs", help="Directory for TensorBoard logs.")
parser.add_argument("--batch_size", type=int, default=16, help="Batch size per GPU (effective batch size will be batch_size * num_GPUs).")
parser.add_argument("--learning_rate", type=float, default=1e-5, help="Learning rate for AdamW optimizer.")
parser.add_argument("--num_epochs", type=int, default=3, help="Number of training epochs (used if max_steps is not set).")
parser.add_argument("--max_steps", type=int, default=None, help="Total training steps to run. If set, training will stop after this many steps, overriding num_epochs.")
parser.add_argument("--save_steps", type=int, default=1000, help="Save checkpoint every N steps.")
parser.add_argument("--logging_steps", type=int, default=100, help="Log training loss to TensorBoard every N steps.")
parser.add_argument("--resume_from", type=str, default=None, help="Path to a checkpoint file to resume training from.")
parser.add_argument("--max_label_length", type=int, default=448,
                    help="Maximum allowed label length (in tokens). Longer labels are dropped by default.")
parser.add_argument("--drop_long_labels", action=argparse.BooleanOptionalAction, default=True,
                    help="Drop examples with labels longer than --max_label_length.")


def train(args: argparse.Namespace) -> None:
    model_id = args.model_id
    # dataset_path takes precedence if provided, otherwise use dataset_name
    dataset_name = args.dataset_path if args.dataset_path else args.dataset_name
    language_option = args.language_option
    output_dir = args.output_dir
    log_dir = args.log_dir
    batch_size = args.batch_size
    learning_rate = args.learning_rate
    num_epochs = args.num_epochs
    max_steps = args.max_steps
    save_steps = args.save_steps
    logging_steps = args.logging_steps
    resume_from = args.resume_from
    max_label_length = args.max_label_length
    drop_long_labels = args.drop_long_labels

    # Create output and log directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    # --------------------#
    # Load model & processor
    # --------------------#
    print(f"Loading model {model_id}...")
    model = WhisperForConditionalGeneration.from_pretrained(model_id)
    # For fine-tuning, use float32 or float16 if GPU memory is a concern (fp16 speeds up training on GPU).
    # model = WhisperForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.float16)

    # Load the processor (feature extractor + tokenizer)
    if language_option == "auto":
        # Auto mode: do not set a fixed language, let model detect. We still set task to transcribe by default.
        processor = WhisperProcessor.from_pretrained(model_id, task="transcribe")
    else:
        # Dataset mode: We'll insert language tokens ourselves, so just load processor without fixed language.
        processor = WhisperProcessor.from_pretrained(model_id, task="transcribe", language="auto")
        # (Setting language="auto" means the tokenizer won't prepend any specific language token on its own.)

    # --------------------#
    # Load and prepare dataset BEFORE CUDA initialization
    # (multiprocessing with fork doesn't work after CUDA init)
    # --------------------#
    train_dataset = load_and_prepare_dataset(
        dataset_name=dataset_name,
        processor=processor,
        model=model,  # model is still on CPU here
        language_option=language_option,
    )
    if drop_long_labels and max_label_length is not None:
        before_count = len(train_dataset)
        train_dataset = train_dataset.filter(
            lambda x: len(x["labels"]) <= max_label_length,
            desc=f"Dropping labels longer than {max_label_length}",
        )
        after_count = len(train_dataset)
        dropped = before_count - after_count
        if dropped > 0:
            print(f"Dropped {dropped} samples with labels longer than {max_label_length}.", flush=True)

    # Send model to GPU(s) - AFTER dataset processing
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    # If multiple GPUs are available, use DataParallel for simple data-parallel training
    if torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs for data-parallel training.")
        model = torch.nn.DataParallel(model)

    # Setup optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    # If resuming, load checkpoint
    start_step = 0
    start_epoch = 0
    if resume_from:
        print(f"Resuming from checkpoint {resume_from}...")
        checkpoint = torch.load(resume_from, map_location=device)
        # DataParallel wraps model, so state_dict keys might start with 'module.' if saved that way
        model_state = checkpoint.get("model_state", None)
        if model_state:
            # If using DataParallel, load into model.module if available
            if isinstance(model, torch.nn.DataParallel):
                model.module.load_state_dict(model_state)
            else:
                model.load_state_dict(model_state)
        if "optimizer_state" in checkpoint:
            optimizer.load_state_dict(checkpoint["optimizer_state"])
        start_step = checkpoint.get("step", 0)
        start_epoch = checkpoint.get("epoch", 0)
        print(f"Resumed at epoch {start_epoch}, step {start_step}.")

    # DataLoader creation
    collate_fn = create_collate_fn(processor)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)

    # --------------------#
    # Training loop
    # --------------------#
    writer = SummaryWriter(log_dir=log_dir)
    total_steps = max_steps if max_steps is not None else (num_epochs * len(train_dataloader))
    global_step = start_step
    model.train()  # set model to training mode

    print("Starting training...")
    stop_training = False
    for epoch in range(start_epoch, num_epochs):
        if stop_training:
            break
        print(f"Epoch {epoch+1}/{num_epochs}")
        # If resuming and we are at start_epoch, skip batches already processed in that epoch
        batch_start = 0
        if epoch == start_epoch and start_step > 0:
            batch_start = start_step % len(train_dataloader)
        for batch_idx, batch in enumerate(train_dataloader):
            if batch_idx < batch_start:
                continue  # skip this batch because it was processed before checkpoint
            # Move batch to GPU
            inputs = batch["input_features"].to(device)
            labels = batch["labels"].to(device)
            # Forward pass
            outputs = model(input_features=inputs, labels=labels)
            loss = outputs.loss if hasattr(outputs, "loss") else outputs[0]  # model returns loss in .loss
            # If using DataParallel, the loss might be a tensor on the default device for each replica, so ensure it's a scalar
            if loss.dim() > 0:
                loss = loss.mean()  # average loss from multiple GPUs
            # Backpropagation
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            global_step += 1

            # Logging
            if global_step % logging_steps == 0:
                avg_loss = loss.item()
                writer.add_scalar("train_loss", avg_loss, global_step)
                print(f"Step {global_step}/{total_steps}: loss = {avg_loss:.4f}")

            # Save checkpoint periodically
            if global_step % save_steps == 0:
                ckpt_path = os.path.join(output_dir, f"checkpoint_step{global_step}.pt")
                # Save model, optimizer, and current positions
                # If DataParallel, save the underlying model's state_dict for easier loading
                state_dict = model.module.state_dict() if isinstance(model, torch.nn.DataParallel) else model.state_dict()
                torch.save({
                    "model_state": state_dict,
                    "optimizer_state": optimizer.state_dict(),
                    "step": global_step,
                    "epoch": epoch
                }, ckpt_path)
                # Also update a "last checkpoint" link for convenience
                torch.save({
                    "model_state": state_dict,
                    "optimizer_state": optimizer.state_dict(),
                    "step": global_step,
                    "epoch": epoch
                }, os.path.join(output_dir, "checkpoint_last.pt"))
                print(f"Saved checkpoint to {ckpt_path}")

            # Stop if we've reached the total training steps (if max_steps is set)
            if max_steps is not None and global_step >= max_steps:
                stop_training = True
                break
        # End of epoch
        # If using max_steps and we've already reached the limit, break out of outer loop as well
        if max_steps is not None and global_step >= max_steps:
            break

    # Training finished
    print("Training completed.")

    # Save final model checkpoint
    final_ckpt = os.path.join(output_dir, "checkpoint_final.pt")
    state_dict = model.module.state_dict() if isinstance(model, torch.nn.DataParallel) else model.state_dict()
    torch.save({
        "model_state": state_dict,
        "optimizer_state": optimizer.state_dict(),
        "step": global_step,
        "epoch": epoch
    }, final_ckpt)
    print(f"Saved final checkpoint to {final_ckpt}")


def main(argv: list[str] | None = None) -> None:
    args = parser.parse_args(argv)
    train(args)


if __name__ == "__main__":
    main()

# (Optional) Save model in Hugging Face format for easy re-loading or sharing
# model_to_save = model.module if isinstance(model, torch.nn.DataParallel) else model
# model_to_save.save_pretrained(output_dir)
# processor.save_pretrained(output_dir)

writer.close()

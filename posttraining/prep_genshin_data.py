import datasets
ds = datasets.load_dataset('simon3000/genshin-voice')
# randomly subsample 5000 rows from the 'train' split (DatasetDict object)
import random
ds = ds["train"].select(random.sample(range(len(ds["train"])), 5000))

# filter to those with non-empty 'transcription' field
ds = ds.filter(lambda x: bool(x.get('transcription', '').strip()))

# save to disk
ds.save_to_disk('genshin_voice_5000.jsonl')

# save as HF dataset format
#TODO
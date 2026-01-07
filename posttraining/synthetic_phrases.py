# formatted vs unformatted
PHRASES = [
    {
        'formatted': 'I would like 3 things from you:\n\n- A hug.\n- A kiss.\n- A cuddle.',
        'unformatted': 'I would like 3 things from you, a hug, a kiss, a cuddle.',
    },
    {
        'formatted': 'Please remember to:\n\n- Turn off the oven.\n- Feed the cat.\n- Water the fern.',
        'unformatted': 'Please remember to turn off the oven, feed the cat, and water the fern.',
    },
    {
        'formatted': 'Meeting agenda:\n\n- Review last sprint.\n- Demo the prototype.\n- Plan the release.',
        'unformatted': 'Meeting agenda: review last sprint, demo the prototype, plan the release.',
    },
    {
        'formatted': 'My weekend plan:\n\n- Sleep in.\n- Make pancakes.\n- Call my grandma.',
        'unformatted': 'My weekend plan is to sleep in, make pancakes, and call my grandma.',
    },
    {
        'formatted': 'Shopping list:\n\n- Fresh basil.\n- Olive oil.\n- Sourdough bread.',
        'unformatted': 'Shopping list: fresh basil, olive oil, sourdough bread.',
    },
    {
        'formatted': 'Today I learned:\n\n- Bees can recognize faces.\n- Bananas are berries.\n- Penguins have knees.',
        'unformatted': 'Today I learned that bees can recognize faces, bananas are berries, and penguins have knees.',
    },
    {
        'formatted': 'Before bed I will:\n\n- Brush my teeth.\n- Stretch for ten minutes.\n- Read a chapter.',
        'unformatted': 'Before bed I will brush my teeth, stretch for ten minutes, and read a chapter.',
    },
    {
        'formatted': 'Favorite movie snacks:\n\n- Popcorn with butter.\n- Peanut M&Ms.\n- Sparkling water.',
        'unformatted': 'My favorite movie snacks are popcorn with butter, peanut M&Ms, and sparkling water.',
    },
    {
        'formatted': 'Travel checklist:\n\n- Passport.\n- Phone charger.\n- Comfortable shoes.',
        'unformatted': 'Travel checklist includes passport, phone charger, and comfortable shoes.',
    },
    {
        'formatted': 'Workout circuit:\n\n- 15 push-ups.\n- 20 squats.\n- 30-second plank.',
        'unformatted': 'Workout circuit: 15 push-ups, 20 squats, 30-second plank.',
    },
    {
        'formatted': 'Coffee order:\n\n- One oat milk latte.\n- Extra hot.\n- No foam.',
        'unformatted': 'Coffee order is one oat milk latte, extra hot, no foam.',
    },
    {
        'formatted': 'Gratitude list:\n\n- A sunny morning.\n- A good book.\n- A text from a friend.',
        'unformatted': 'Gratitude list: a sunny morning, a good book, a text from a friend.',
    },
    {
        'formatted': 'Road trip rules:\n\n- Driver picks the music.\n- Passenger picks the snacks.\n- Everyone sings.',
        'unformatted': 'Road trip rules: driver picks the music, passenger picks the snacks, everyone sings.',
    },
    {
        'formatted': 'Bug repro steps:\n\n- Open the settings page.\n- Toggle dark mode twice.\n- Observe the flicker.',
        'unformatted': 'Bug repro steps: open the settings page, toggle dark mode twice, observe the flicker.',
    },
    {
        'formatted': 'Morning routine:\n\n- Drink water.\n- Write three thoughts.\n- Step outside for air.',
        'unformatted': 'Morning routine: drink water, write three thoughts, step outside for air.',
    },
    {
        'formatted': 'Birthday wishes:\n\n- Good health.\n- Laughter with friends.\n- Time to rest.',
        'unformatted': 'Birthday wishes: good health, laughter with friends, time to rest.',
    },
    {
        'formatted': 'Packing for the beach:\n\n- Sunscreen.\n- A wide hat.\n- A paperback novel.',
        'unformatted': 'Packing for the beach: sunscreen, a wide hat, a paperback novel.',
    },
    {
        'formatted': 'Kitchen reminders:\n\n- Label leftovers.\n- Sharpen knives.\n- Wipe the stove.',
        'unformatted': 'Kitchen reminders: label leftovers, sharpen knives, wipe the stove.',
    },
    {
        'formatted': 'Interview prep:\n\n- Research the company.\n- Practice two stories.\n- Charge the laptop.',
        'unformatted': 'Interview prep includes researching the company, practicing two stories, and charging the laptop.',
    },
    {
        'formatted': 'Daily affirmations:\n\n- I can solve hard problems.\n- I listen before I speak.\n- I finish what I start.',
        'unformatted': 'Daily affirmations: I can solve hard problems, I listen before I speak, I finish what I start.',
    },
    {
        'formatted': 'Garden tasks:\n\n- Pull weeds.\n- Add compost.\n- Check the tomatoes.',
        'unformatted': 'Garden tasks: pull weeds, add compost, check the tomatoes.',
    },
    {
        'formatted': '# Weekly Report\n\nEverything is on track.',
        'unformatted': 'Weekly Report: Everything is on track.',
    },
    {
        'formatted': '## Chapter 1: The Beginning\n\nIt was a dark and stormy night.',
        'unformatted': 'Chapter 1: The Beginning. It was a dark and stormy night.',
    },
    {
        'formatted': 'The **quick** brown fox jumps *over* the lazy dog.',
        'unformatted': 'The quick brown fox jumps over the lazy dog.',
    },
    {
        'formatted': '> "Be the change you wish to see in the world."\n> - Mahatma Gandhi',
        'unformatted': '"Be the change you wish to see in the world." - Mahatma Gandhi',
    },
    {
        'formatted': '> She whispered:\n>> "Is anyone there?"',
        'unformatted': 'She whispered: "Is anyone there?"',
    },
    {
        'formatted': 'To install the package, run `pip install numpy` in your terminal.',
        'unformatted': 'To install the package, run pip install numpy in your terminal.',
    },
    {
        'formatted': 'Here is a simple python function:\n\n```python\ndef hello():\n    print("Hello world")\n```',
        'unformatted': 'Here is a simple python function: def hello(): print("Hello world")',
    },
    {
        'formatted': 'Config settings:\n\n```json\n{\n  "debug": true,\n  "version": "1.0"\n}\n```',
        'unformatted': 'Config settings: { "debug": true, "version": "1.0" }',
    },
    {
        'formatted': 'Introduction\n\n---\n\nMain Content',
        'unformatted': 'Introduction. Main Content.',
    },
    {
        'formatted': 'Please visit [OpenAI](https://openai.com) for more information.',
        'unformatted': 'Please visit OpenAI (https://openai.com) for more information.',
    },
    {
        'formatted': '![Sunset over the ocean](image.jpg)',
        'unformatted': '[Image: Sunset over the ocean]',
    },
    {
        'formatted': '| Rank | Player |\n|---|---|\n| 1 | Alice |\n| 2 | Bob |',
        'unformatted': 'Rank: 1 is Alice, 2 is Bob.',
    },
    {
        'formatted': 'The meeting is ~~cancelled~~ postponed to Friday.',
        'unformatted': 'The meeting is cancelled (crossed out) postponed to Friday.',
    },
    {
        'formatted': 'Todo:\n- [x] Buy milk\n- [ ] Walk the dog',
        'unformatted': 'Todo: Buy milk (done), Walk the dog (todo).',
    },
    {
        'formatted': '**HTML**: HyperText Markup Language\n**CSS**: Cascading Style Sheets',
        'unformatted': 'HTML: HyperText Markup Language. CSS: Cascading Style Sheets.',
    },
    {
        'formatted': 'The formula is $E = mc^2$.',
        'unformatted': 'The formula is E equals m c squared.',
    },
    {
        'formatted': 'Roses are red,\nViolets are blue,\nSugar is sweet,\nAnd so are you.',
        'unformatted': 'Roses are red, Violets are blue, Sugar is sweet, And so are you.',
    },
    {
        'formatted': 'Alice: Are you coming?\nBob: I will be there in 5.',
        'unformatted': 'Alice: Are you coming? Bob: I will be there in 5.',
    },
    {
        'formatted': '1234 Elm Street\nSpringfield, IL 62704',
        'unformatted': '1234 Elm Street, Springfield, IL 62704.',
    },
    {
        'formatted': 'Check the `status` field in the **API response**.',
        'unformatted': 'Check the status field in the API response.',
    },
    {
        'formatted': '# Project Omega Status Update\n\nWe are currently moving into the final phase of development, which involves rigorous testing and quality assurance checks to ensure stability before the public launch.\n\nThe team has made significant progress on the core features, including:\n\n- **User Authentication**: Secure login flows are now fully operational with 2FA support.\n- **Database Migration**: All legacy data has been successfully ported to the new PostgreSQL cluster.\n- **API Documentation**: The Swagger UI is live and covers 95% of endpoints.\n\nNext week, we will focus on load testing and fixing any high-priority bugs that emerge.',
        'unformatted': 'Project Omega Status Update. We are currently moving into the final phase of development, which involves rigorous testing and quality assurance checks to ensure stability before the public launch. The team has made significant progress on the core features, including: User Authentication (secure login flows are now fully operational with 2FA support), Database Migration (all legacy data has been successfully ported to the new PostgreSQL cluster), and API Documentation (the Swagger UI is live and covers 95% of endpoints). Next week, we will focus on load testing and fixing any high-priority bugs that emerge.',
    },
    {
        'formatted': '## Classic Chocolate Chip Cookies\n\nThere is nothing quite like the smell of fresh cookies baking in the oven on a rainy Sunday afternoon. The secret to the perfect texture lies in using melted butter and chilling the dough for at least an hour.\n\n### Ingredients\n\n*   1 cup *unsalted butter*, melted\n*   1 cup white sugar\n*   1 cup packed brown sugar\n*   2 large eggs\n*   2 cups semisweet chocolate chips\n\n> "Cooking is like love. It should be entered into with abandon or not at all."\n\nMake sure to preheat your oven to 350°F (175°C) and line your baking sheets with parchment paper for easy cleanup.',
        'unformatted': 'Classic Chocolate Chip Cookies. There is nothing quite like the smell of fresh cookies baking in the oven on a rainy Sunday afternoon. The secret to the perfect texture lies in using melted butter and chilling the dough for at least an hour. Ingredients: 1 cup unsalted butter (melted), 1 cup white sugar, 1 cup packed brown sugar, 2 large eggs, 2 cups semisweet chocolate chips. "Cooking is like love. It should be entered into with abandon or not at all." Make sure to preheat your oven to 350 degrees Fahrenheit (175 degrees Celsius) and line your baking sheets with parchment paper for easy cleanup.',
    },
    {
        'formatted': '### Understanding Recursion\n\nRecursion is a method where the solution to a problem depends on solutions to smaller instances of the same problem. It is often used in computer science for tasks like tree traversal or sorting algorithms.\n\nHere is a classic example of calculating a factorial using Python:\n\n```python\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n```\n\nKey concepts to remember:\n\n1.  **Base Case**: The condition under which the function stops calling itself.\n2.  **Recursive Step**: The part where the function calls itself with modified arguments.\n3.  **Stack Overflow**: What happens if you forget the base case!',
        'unformatted': 'Understanding Recursion. Recursion is a method where the solution to a problem depends on solutions to smaller instances of the same problem. It is often used in computer science for tasks like tree traversal or sorting algorithms. Here is a classic example of calculating a factorial using Python: def factorial(n): if n equals 0: return 1 else: return n times factorial(n minus 1). Key concepts to remember: 1. Base Case: The condition under which the function stops calling itself. 2. Recursive Step: The part where the function calls itself with modified arguments. 3. Stack Overflow: What happens if you forget the base case!',
    },
    {
        'formatted': 'Dear Hiring Manager,\n\nI am writing to express my strong interest in the Senior Software Engineer position at *TechCorp*, as advertised on LinkedIn. With over 8 years of experience in full-stack development, I believe my skills in distributed systems and cloud architecture would be a great asset to your team.\n\nMy core competencies include:\n\n-   `React` & `Node.js` ecosystem\n-   AWS infrastructure management (EC2, S3, Lambda)\n-   CI/CD pipeline optimization\n\n> "Innovation distinguishes between a leader and a follower."\n\nI have attached my resume for your review and would welcome the opportunity to discuss how I can contribute to TechCorp’s upcoming initiatives.\n\nSincerely,\nJane Doe',
        'unformatted': 'Dear Hiring Manager, I am writing to express my strong interest in the Senior Software Engineer position at TechCorp, as advertised on LinkedIn. With over 8 years of experience in full-stack development, I believe my skills in distributed systems and cloud architecture would be a great asset to your team. My core competencies include: React and Node.js ecosystem, AWS infrastructure management (EC2, S3, Lambda), and CI/CD pipeline optimization. "Innovation distinguishes between a leader and a follower." I have attached my resume for your review and would welcome the opportunity to discuss how I can contribute to TechCorp’s upcoming initiatives. Sincerely, Jane Doe',
    },
    {
        'formatted': '# Quarterly Business Review: Q3 2023\n\nThe third quarter has been a period of rapid growth and strategic realignment for our department. Despite some initial headwinds in the supply chain, we managed to exceed our revenue targets by 15%.\n\n**Performance Highlights:**\n\n*   **Revenue**: $1.2M (vs $1.0M forecast)\n*   **Customer Acquisition**: +200 net new clients\n*   ~~Churn Rate~~: Decreased to < 2%\n\nMoving forward into Q4, our primary objectives are:\n\n1.  Expand into the APAC market.\n2.  Launch the mobile application beta.\n3.  Hire 5 new support specialists.\n\nPlease review the attached dashboard for a granular breakdown of these metrics.',
        'unformatted': 'Quarterly Business Review: Q3 2023. The third quarter has been a period of rapid growth and strategic realignment for our department. Despite some initial headwinds in the supply chain, we managed to exceed our revenue targets by 15%. Performance Highlights: Revenue was $1.2M (versus $1.0M forecast), Customer Acquisition saw +200 net new clients, and Churn Rate decreased to less than 2%. Moving forward into Q4, our primary objectives are: 1. Expand into the APAC market. 2. Launch the mobile application beta. 3. Hire 5 new support specialists. Please review the attached dashboard for a granular breakdown of these metrics.',
    },
    {
        'formatted': '### Patient: John Doe (DOB: 01/01/1980)\n\n**Chief Complaint**: Persistent cough and fatigue.\n\n**Vitals**:\n- BP: 120/80\n- HR: 72 bpm\n- Temp: 98.6°F\n\n**Plan**:\n1. Prescribe rest and fluids.\n2. Follow up in 1 week if symptoms persist.',
        'unformatted': 'Patient: John Doe (DOB: 01/01/1980). Chief Complaint: Persistent cough and fatigue. Vitals: BP 120/80, HR 72 bpm, Temp 98.6 degrees Fahrenheit. Plan: 1. Prescribe rest and fluids. 2. Follow up in 1 week if symptoms persist.',
    },
    {
        'formatted': '## The Raven\n\nOnce upon a midnight dreary, while I pondered, weak and weary,\nOver many a quaint and curious volume of forgotten lore—\n\n*   While I nodded, nearly napping,\n*   Suddenly there came a tapping,\n*   As of some one gently rapping,\n*   Rapping at my chamber door.\n\n> "Tis some visitor," I muttered, "tapping at my chamber door—\n> Only this and nothing more."',
        'unformatted': 'The Raven. Once upon a midnight dreary, while I pondered, weak and weary, Over many a quaint and curious volume of forgotten lore. While I nodded, nearly napping, Suddenly there came a tapping, As of some one gently rapping, Rapping at my chamber door. "Tis some visitor," I muttered, "tapping at my chamber door, Only this and nothing more."',
    },
    {
        'formatted': 'To fix the `git` merge conflict:\n\n1. Open the file with conflicts.\n2. Look for `<<<<<<< HEAD` markers.\n3. Edit the code to resolve differences.\n4. Run:\n   ```bash\n   git add .\n   git commit -m "Resolved merge conflict"\n   ```',
        'unformatted': 'To fix the git merge conflict: 1. Open the file with conflicts. 2. Look for HEAD markers. 3. Edit the code to resolve differences. 4. Run: git add ., then git commit -m "Resolved merge conflict".',
    },
    {
        'formatted': '## Inventory Stats\n\n| Item | Qty | Value |\n|---|---|---|\n| Potion | 10 | 50g |\n| Sword | 1 | 200g |\n| Shield | 1 | 150g |\n\n**Total Value**: 400g',
        'unformatted': 'Inventory Stats. Item: Potion (Qty 10, Value 50g), Sword (Qty 1, Value 200g), Shield (Qty 1, Value 150g). Total Value: 400g.',
    },
    {
        'formatted': '### Weather Forecast\n\n**Monday**: Sunny ☀️\n- High: 75°F\n- Low: 60°F\n\n**Tuesday**: Cloudy ☁️\n- High: 70°F\n- Low: 58°F\n\n> Note: Chance of rain in the evening.',
        'unformatted': 'Weather Forecast. Monday: Sunny. High: 75°F, Low: 60°F. Tuesday: Cloudy. High: 70°F, Low: 58°F. Note: Chance of rain in the evening.',
    },
    {
        'formatted': '## Terms of Service\n\n1.  **Acceptance**: By using this service, you agree to these terms.\n2.  **Privacy**: We respect your privacy.\n    *   We do not sell your data.\n    *   We use cookies for analytics.\n3.  **Termination**: We may terminate your account at any time.',
        'unformatted': 'Terms of Service. 1. Acceptance: By using this service, you agree to these terms. 2. Privacy: We respect your privacy. We do not sell your data. We use cookies for analytics. 3. Termination: We may terminate your account at any time.',
    },
    {
        'formatted': '### Chat Log\n\n**Alice** (10:00 AM): Hey, did you see the *memo*?\n\n**Bob** (10:05 AM): No, what did it say?\n\n**Alice** (10:06 AM): It said:\n> "All employees must wear hats on Fridays."\n\n**Bob** (10:07 AM): You\'re joking, right?',
        'unformatted': 'Chat Log. Alice (10:00 AM): Hey, did you see the memo? Bob (10:05 AM): No, what did it say? Alice (10:06 AM): It said: "All employees must wear hats on Fridays." Bob (10:07 AM): You\'re joking, right?',
    },
    {
        'formatted': '## Algebra Homework\n\nSolve for $x$:\n\n$$ 2x + 5 = 15 $$\n\nSteps:\n1. Subtract 5 from both sides: $2x = 10$\n2. Divide by 2: $x = 5$\n\n**Answer**: $x = 5$',
        'unformatted': 'Algebra Homework. Solve for x: 2x + 5 = 15. Steps: 1. Subtract 5 from both sides: 2x = 10. 2. Divide by 2: x = 5. Answer: x = 5.',
    },
    {
        'formatted': '### Movie Review: *The Great Adventure*\n\n**Rating**: ★★★★☆\n\nI really enjoyed this movie. The **visuals** were stunning, and the acting was top-notch.\n\n*   **Pros**:\n    *   Great story.\n    *   Amazing effects.\n*   **Cons**:\n    *   A bit long.\n\n> "A must-watch for adventure fans!"',
        'unformatted': 'Movie Review: The Great Adventure. Rating: 4 out of 5 stars. I really enjoyed this movie. The visuals were stunning, and the acting was top-notch. Pros: Great story, Amazing effects. Cons: A bit long. "A must-watch for adventure fans!"',
    },
    {
        'formatted': "## SQL Query\n\nSelect all users who signed up in 2023:\n\n```sql\nSELECT * FROM users\nWHERE signup_date >= '2023-01-01'\nAND signup_date <= '2023-12-31';\n```\n\nExpected output: A list of 500 users.",
        'unformatted': "SQL Query. Select all users who signed up in 2023: SELECT * FROM users WHERE signup_date >= '2023-01-01' AND signup_date <= '2023-12-31';. Expected output: A list of 500 users.",
    },
    {
        'formatted': '### Flight Itinerary\n\n**Flight**: UA123\n**Date**: Oct 15, 2023\n\n*   **Departs**: SFO at 08:00 AM\n*   **Arrives**: JFK at 04:30 PM\n\n> Please arrive at the airport 2 hours early.',
        'unformatted': 'Flight Itinerary. Flight: UA123. Date: Oct 15, 2023. Departs: SFO at 08:00 AM. Arrives: JFK at 04:30 PM. Please arrive at the airport 2 hours early.',
    },
    {
        'formatted': '## Release Notes v2.0\n\nWe are excited to announce version 2.0!\n\n### New Features\n- Dark mode support.\n- Improved performance.\n\n### Bug Fixes\n- Fixed crash on startup.\n- Resolved login issue.\n\nDownload it now from the [App Store](https://apple.com/app-store).',
        'unformatted': 'Release Notes v2.0. We are excited to announce version 2.0! New Features: Dark mode support, Improved performance. Bug Fixes: Fixed crash on startup, Resolved login issue. Download it now from the App Store (https://apple.com/app-store).',
    },
    {
        'formatted': '### Yoga Sequence\n\n1.  **Mountain Pose**: Stand tall, feet together.\n2.  **Forward Fold**: Exhale and hinge at hips.\n3.  **Downward Dog**: Step back and lift hips.\n\n> Breathe deeply and hold each pose for 5 breaths.',
        'unformatted': 'Yoga Sequence. 1. Mountain Pose: Stand tall, feet together. 2. Forward Fold: Exhale and hinge at hips. 3. Downward Dog: Step back and lift hips. Breathe deeply and hold each pose for 5 breaths.',
    },
    {
        'formatted': '## Cafe Menu\n\n| Drink | Price |\n|---|---|\n| Espresso | $2.50 |\n| Latte | $4.00 |\n| Tea | $3.00 |\n\n**Extras**:\n- Oat milk (+$0.50)\n- Flavor shot (+$0.50)',
        'unformatted': 'Cafe Menu. Drink: Espresso ($2.50), Latte ($4.00), Tea ($3.00). Extras: Oat milk (+$0.50), Flavor shot (+$0.50).',
    },
    {
        'formatted': '### Error Log\n\n**Timestamp**: 2023-10-27 14:23:01\n**Level**: ERROR\n\nMessage:\n```\nNullPointerException at com.example.Main.run(Main.java:42)\n```\n\nAction: Restart the service.',
        'unformatted': 'Error Log. Timestamp: 2023-10-27 14:23:01. Level: ERROR. Message: NullPointerException at com.example.Main.run(Main.java:42). Action: Restart the service.',
    },
    {
        'formatted': '## Social Media Post\n\nJust finished a 5k run! 🏃\u200d♂️💨\n\nFeeling great and energized.\n\n#running #fitness #health\n\n- Time: 25:30\n- Pace: 8:12/mile',
        'unformatted': 'Social Media Post. Just finished a 5k run! Feeling great and energized. #running #fitness #health. Time: 25:30, Pace: 8:12/mile.',
    },
    {
        'formatted': '### Product Description\n\n**SuperGadget 3000**\n\nThe ultimate tool for your daily needs.\n\n*   **Battery Life**: 24 hours\n*   **Weight**: 150g\n*   **Warranty**: 1 year\n\n~~Was: $99.99~~\n**Now: $79.99**',
        'unformatted': 'Product Description. SuperGadget 3000. The ultimate tool for your daily needs. Battery Life: 24 hours. Weight: 150g. Warranty: 1 year. Was: $99.99. Now: $79.99.',
    },
    {
        'formatted': '## Debate Arguments\n\n**Topic**: Should homework be banned?\n\n**Affirmative**:\n1. Reduces stress.\n2. More free time.\n\n**Negative**:\n1. Reinforces learning.\n2. Develops discipline.\n\n> Conclusion: A balanced approach is best.',
        'unformatted': 'Debate Arguments. Topic: Should homework be banned? Affirmative: 1. Reduces stress. 2. More free time. Negative: 1. Reinforces learning. 2. Develops discipline. Conclusion: A balanced approach is best.',
    },
    {
        'formatted': '### Music Playlist\n\n1.  **Bohemian Rhapsody** - Queen\n2.  **Imagine** - John Lennon\n3.  **Billie Jean** - Michael Jackson\n\nTotal duration: *15 minutes*',
        'unformatted': 'Music Playlist. 1. Bohemian Rhapsody - Queen. 2. Imagine - John Lennon. 3. Billie Jean - Michael Jackson. Total duration: 15 minutes.',
    },
    {
        'formatted': 'Hey @channel, quick reminder that the *all-hands meeting* is starting in 15 minutes. Please join via the Zoom link in the invite.',
        'unformatted': 'Hey channel, quick reminder that the all-hands meeting is starting in 15 minutes. Please join via the Zoom link in the invite.',
    },
    {
        'formatted': 'Can someone review my PR when they get a chance? It includes:\n- Fix for the login bug\n- Updated unit tests\n- Documentation changes',
        'unformatted': 'Can someone review my PR when they get a chance? It includes fix for the login bug, updated unit tests, and documentation changes.',
    },
    {
        'formatted': 'I am running into an issue with the build script. It fails with:\n```\nError: module "utils" not found\n```\nHas anyone seen this before?',
        'unformatted': 'I am running into an issue with the build script. It fails with "Error: module utils not found". Has anyone seen this before?',
    },
    {
        'formatted': "FYI: I will be OOO tomorrow for a doctor's appointment. Please ping @Sarah if anything urgent comes up.",
        'unformatted': "FYI: I will be OOO tomorrow for a doctor's appointment. Please ping Sarah if anything urgent comes up.",
    },
    {
        'formatted': 'The new design mocks are ready for review. You can find them [here](https://figma.com/file/123). Let me know your thoughts!',
        'unformatted': 'The new design mocks are ready for review. You can find them here (https://figma.com/file/123). Let me know your thoughts!',
    },
    {
        'formatted': 'Great job on the presentation today, **Team**! The client was really impressed with the roadmap.',
        'unformatted': 'Great job on the presentation today, Team! The client was really impressed with the roadmap.',
    },
    {
        'formatted': 'Could we schedule a quick sync to discuss the Q4 goals? I am free:\n- Monday 2-4 PM\n- Tuesday 10-12 AM\n- Wednesday 1-3 PM',
        'unformatted': 'Could we schedule a quick sync to discuss the Q4 goals? I am free Monday 2-4 PM, Tuesday 10-12 AM, or Wednesday 1-3 PM.',
    },
    {
        'formatted': 'Updates on the server outage:\n1. Root cause identified (database lock).\n2. Fix deployed to staging.\n3. Verifying stability now.',
        'unformatted': 'Updates on the server outage: 1. Root cause identified (database lock). 2. Fix deployed to staging. 3. Verifying stability now.',
    },
    {
        'formatted': 'Does anyone know where the *brand assets* are stored? I need the high-res logo for a deck.',
        'unformatted': 'Does anyone know where the brand assets are stored? I need the high-res logo for a deck.',
    },
    {
        'formatted': 'Please make sure to update your JIRA tickets before the end of the day. We have sprint planning tomorrow morning.',
        'unformatted': 'please make sure to update your jira tickets before the end of the day we have sprint planning tomorrow morning',
    },
    {
        'formatted': "I'm getting a 403 Forbidden error when trying to access the admin panel. Is my account permission set up correctly?",
        'unformatted': 'im getting a 403 forbidden error when trying to access the admin panel is my account permission set up correctly',
    },
    {
        'formatted': 'Here are the action items from the retro:\n*   Improve code coverage.\n*   Update onboarding docs.\n*   Set up alerting for API errors.',
        'unformatted': 'Here are the action items from the retro: improve code coverage, update onboarding docs, and set up alerting for API errors.',
    },
    {
        'formatted': 'Happy work anniversary @Mike! 🥳 Thanks for all your hard work over the last 3 years.',
        'unformatted': 'Happy work anniversary Mike! Thanks for all your hard work over the last 3 years.',
    },
    {
        'formatted': 'Just a heads up, we are freezing code at 5 PM PST today for the release candidate.',
        'unformatted': 'just a heads up we are freezing code at 5 pm pst today for the release candidate',
    },
    {
        'formatted': 'I found a helpful article about optimizing React performance: [link](https://blog.example.com/react-perf). Worth a read!',
        'unformatted': 'I found a helpful article about optimizing React performance: link (https://blog.example.com/react-perf). Worth a read!',
    },
    {
        'formatted': 'Question: Are we using `redux` or `context` for state management in the new dashboard component?',
        'unformatted': 'Question: Are we using redux or context for state management in the new dashboard component?',
    },
    {
        'formatted': 'The latest metrics show a **10% increase** in user engagement since the last update. Great work everyone!',
        'unformatted': 'The latest metrics show a 10% increase in user engagement since the last update. Great work everyone!',
    },
    {
        'formatted': 'Can you please sign the new security policy by Friday? It is mandatory for all employees.',
        'unformatted': 'can you please sign the new security policy by friday it is mandatory for all employees',
    },
    {
        'formatted': 'I will be working remotely from a coffee shop this afternoon, so my response time might be slightly slower.',
        'unformatted': 'i will be working remotely from a coffee shop this afternoon so my response time might be slightly slower',
    },
    {
        'formatted': 'Looking for a volunteer to take notes during the client meeting. Any takers?',
        'unformatted': 'looking for a volunteer to take notes during the client meeting any takers',
    },
    {
        'formatted': 'The cafeteria menu for today is:\n- Grilled Salmon\n- Roasted Vegetables\n- Quinoa Salad',
        'unformatted': 'The cafeteria menu for today is Grilled Salmon, Roasted Vegetables, and Quinoa Salad.',
    },
    {
        'formatted': 'I think we should prioritize the *search feature* over the *profile customization* for the MVP.',
        'unformatted': 'I think we should prioritize the search feature over the profile customization for the MVP.',
    },
    {
        'formatted': 'Welcome to the team, @Anna! We are excited to have you on board.',
        'unformatted': 'Welcome to the team, Anna! We are excited to have you on board.',
    },
    {
        'formatted': "Reminder: Timesheets are due by 12 PM. Please don't forget to submit them.",
        'unformatted': 'reminder timesheets are due by 12 pm please dont forget to submit them',
    },
    {
        'formatted': 'Is anyone else experiencing lag with the VPN today? It has been really slow for me.',
        'unformatted': 'is anyone else experiencing lag with the vpn today it has been really slow for me',
    },
    {
        'formatted': 'I updated the `README.md` file with instructions on how to run the project locally.',
        'unformatted': 'I updated the README.md file with instructions on how to run the project locally.',
    },
    {
        'formatted': "Let's aim to have the *feature spec* finalized by end of week so we can start estimation.",
        'unformatted': "Let's aim to have the feature spec finalized by end of week so we can start estimation.",
    },
    {
        'formatted': 'I baked some cookies and left them in the kitchen. Help yourselves! 🍪',
        'unformatted': 'I baked some cookies and left them in the kitchen. Help yourselves!',
    },
    {
        'formatted': 'The API endpoint `/users/{id}` is returning a 500 error for some IDs. Investigating now.',
        'unformatted': 'The API endpoint /users/{id} is returning a 500 error for some IDs. Investigating now.',
    },
    {
        'formatted': 'Please review the attached PDF for the new HR benefits for 2024.',
        'unformatted': 'please review the attached pdf for the new hr benefits for 2024',
    },
    {
        'formatted': 'We need to renew our SSL certificate for `example.com` before it expires on Monday.',
        'unformatted': 'We need to renew our SSL certificate for example.com before it expires on Monday.',
    },
    {
        'formatted': 'Big shoutout to the **DevOps team** for handling the traffic spike so smoothly!',
        'unformatted': 'Big shoutout to the DevOps team for handling the traffic spike so smoothly!',
    },
    {
        'formatted': 'Can we push back the daily standup by 30 minutes? I have a conflict.',
        'unformatted': 'can we push back the daily standup by 30 minutes i have a conflict',
    },
    {
        'formatted': 'I propose we use a library like `moment.js` or `date-fns` instead of writing custom date parsing logic.',
        'unformatted': 'I propose we use a library like moment.js or date-fns instead of writing custom date parsing logic.',
    },
    {
        'formatted': 'The office will be closed on Monday for the holiday. Enjoy the long weekend!',
        'unformatted': 'the office will be closed on monday for the holiday enjoy the long weekend',
    },
    {
        'formatted': 'Does the new laptop policy apply to contractors as well, or just full-time employees?',
        'unformatted': 'does the new laptop policy apply to contractors as well or just fulltime employees',
    },
    {
        'formatted': 'I am stuck on this SQL query. Can anyone help me optimize it?\n```sql\nSELECT * FROM large_table ...\n```',
        'unformatted': 'I am stuck on this SQL query. Can anyone help me optimize it? SELECT * FROM large_table ...',
    },
    {
        'formatted': "Don't forget to sign up for the company hackathon! Registration closes tomorrow.",
        'unformatted': 'dont forget to sign up for the company hackathon registration closes tomorrow',
    },
    {
        'formatted': 'I will be late to the meeting, stuck in traffic. Start without me.',
        'unformatted': 'i will be late to the meeting stuck in traffic start without me',
    },
    {
        'formatted': 'We are looking for feedback on the new *internal tool*. Please fill out this survey.',
        'unformatted': 'We are looking for feedback on the new internal tool. Please fill out this survey.',
    },
    {
        'formatted': 'The client wants to change the color scheme to match their new branding guidelines.',
        'unformatted': 'the client wants to change the color scheme to match their new branding guidelines',
    },
    {
        'formatted': 'I successfully deployed the hotfix to production. Monitoring logs now.',
        'unformatted': 'i successfully deployed the hotfix to production monitoring logs now',
    },
    {
        'formatted': 'Can you update the invite list for the "Quarterly Planning" meeting? We need to add the marketing leads.',
        'unformatted': 'can you update the invite list for the quarterly planning meeting we need to add the marketing leads',
    },
    {
        'formatted': "I'll be focusing on the *payment gateway integration* for the rest of the sprint.",
        'unformatted': "I'll be focusing on the payment gateway integration for the rest of the sprint.",
    },
    {
        'formatted': 'The wifi password for the guest network has been changed to `GuestPass2023!`.',
        'unformatted': 'The wifi password for the guest network has been changed to GuestPass2023!.',
    },
    {
        'formatted': 'Please refrain from deploying to production on Fridays unless it is critical.',
        'unformatted': 'please refrain from deploying to production on fridays unless it is critical',
    },
    {
        'formatted': 'I have some ideas for improving our onboarding process:\n1. Create a checklist.\n2. Assign a buddy.\n3. Schedule intro meetings.',
        'unformatted': 'I have some ideas for improving our onboarding process: create a checklist, assign a buddy, and schedule intro meetings.',
    },
    {
        'formatted': 'Did we decide on a date for the team offsite? I need to book my flights.',
        'unformatted': 'did we decide on a date for the team offsite i need to book my flights',
    },
    {
        'formatted': "I'm having trouble setting up the local environment. The `docker-compose up` command keeps failing.",
        'unformatted': "I'm having trouble setting up the local environment. The docker-compose up command keeps failing.",
    },
    {
        'formatted': 'Thanks for the quick turnaround on this task! Really appreciate it.',
        'unformatted': 'thanks for the quick turnaround on this task really appreciate it',
    },
]


'''
This script is a "data as code" approach to generating synthetic names and phrases for training.
The point is for the names to be included as additional context for the ASR model.
This enables the ASR model to get the right spelling.

PATTERN & VARIATIONAL ELEMENTS ANALYSIS:

1. CORRECTION PATTERNS
The primary goal is to map phonetically similar but orthographically different names based on the "Context" (the names list).
- Phonetic Spelling Correction: Correcting common names that sound the same but have different spellings (e.g., Mark -> Marc, Jeff -> Geoff).
- Hyphenation and Spacing: Handling names with specific punctuation or internal spaces (e.g., Ka Mun -> Kah Mun, Susan-Lori -> Suzan-Lori).
- Transliteration/International Variations: Correcting Westernized versions of international names to match the specific list (e.g., Alexei -> Alexey, Bharat -> Bharath).
- Reverse Direction: Testing if the model can "undo" a common spelling if the context dictates the alternative (e.g., Charlie -> Charly if Charly is in the name list).
- Multi-Name Correction: Phrases where two or more names are misspelled simultaneously.

2. NAME LIST (CONTEXT) VARIATIONS
The names list provides the "Ground Truth" for that specific sample.
- Small Context (1-2 names): Simple 1:1 mapping.
- Large Context (5-10 names): Simulated "meeting" or "team" lists where only some names are actually mentioned.
- Distractor Names: Including names in the list that are phonetically similar to each other (e.g., Yingbo Zhou vs Yingbo Li).
- Full Names vs. First Names: The list contains full names, but the phrase might only use the first name.

3. LINGUISTIC & PHRASE VARIATIONS
These patterns ensure the model understands sentence structure, not just name matches.
- Negative Examples (No Correction): Phrases where names are already correct or not mentioned at all.
- Varied Speaker Intents: Direct address ("Hey [Name]"), third-person reference, possessives, and coordination ("X and Y").
- Noise/Generic Content: Unrelated sentences (e.g., "The weather is nice today") to ensure stability.
- Ordinary vs. Famous Contexts: Mixing mundane office talk with pop-culture references to vary phonetic distribution.

4. SPECIAL CHARACTERS AND DIACRITICS
- Diacritics: Handling names like Beyoncé, Kylian Mbappé, etc.
- Mononyms vs. Multi-part: Handling mononyms (Rihanna) vs. complex names (X Æ A-12).
'''


NAMES_PHRASES = [
    # Contains a list of names of people in a conversation
    # Corrects an ASR dictation that does not have this name list


    {
        'names': ['Alice Wang', 'Bob Smith', 'Charly Davis'],
        'raw_phrase': "Hey Charlie, can you help me with this project?",
        "corrected_phrase": "Hey Charly, can you help me with this project?"
    },
    {
        'names': ['Jon Doe', 'Jane Smith'],
        'raw_phrase': "I think John is handling the deployment today.",
        "corrected_phrase": "I think Jon is handling the deployment today."
    },
    {
        'names': ['Sara Connor', 'Kyle Reese'],
        'raw_phrase': "Did you send the invite to Sarah yet?",
        "corrected_phrase": "Did you send the invite to Sara yet?"
    },
    {
        'names': ['Marc Jacobs', 'Louis Vuitton'],
        'raw_phrase': "Mark is leading the design team meeting.",
        "corrected_phrase": "Marc is leading the design team meeting."
    },
    {
        'names': ['Caitlin Snow', 'Barry Allen'],
        'raw_phrase': "Kaitlyn needs access to the repository.",
        "corrected_phrase": "Caitlin needs access to the repository."
    },
    {
        'names': ['Geoff Bezos', 'Elon Musk'],
        'raw_phrase': "Jeff suggested we pivot the strategy.",
        "corrected_phrase": "Geoff suggested we pivot the strategy."
    },
    {
        'names': ['Kristina Pimenova', 'Anastasia Bezrukova'],
        'raw_phrase': "Please ask Christina to review the document.",
        "corrected_phrase": "Please ask Kristina to review the document."
    },
    {
        'names': ['Steven Spielberg', 'George Lucas'],
        'raw_phrase': "Stephen is directing the new commercial.",
        "corrected_phrase": "Steven is directing the new commercial."
    },
    {
        'names': ['Elisabeth Moss', 'June Osborne'],
        'raw_phrase': "Elizabeth will be late for the standup.",
        "corrected_phrase": "Elisabeth will be late for the standup."
    },
    {
        'names': ['Rachael Ray', 'Gordon Ramsay'],
        'raw_phrase': "Rachel brought donuts for everyone.",
        "corrected_phrase": "Rachael brought donuts for everyone."
    },
    {
        'names': ['Bryan Cranston', 'Aaron Paul'],
        'raw_phrase': "Brian is cooking something in the lab.",
        "corrected_phrase": "Bryan is cooking something in the lab."
    },
    {
        'names': ['Cate Blanchett', 'Rooney Mara'],
        'raw_phrase': "Kate won the award for best performance.",
        "corrected_phrase": "Cate won the award for best performance."
    },
    {
        'names': ['Micheal Keaton', 'Jack Nicholson'],
        'raw_phrase': "Michael is Batman in this version.",
        "corrected_phrase": "Micheal is Batman in this version."
    },
    {
        'names': ['Jaimie Alexander', 'Chris Hemsworth'],
        'raw_phrase': "Jamie is fighting on the front lines.",
        "corrected_phrase": "Jaimie is fighting on the front lines."
    },
    {
        'names': ['Mathew Perry', 'Courteney Cox'],
        'raw_phrase': "Matthew made a funny joke during the break.",
        "corrected_phrase": "Mathew made a funny joke during the break."
    },
    {
        'names': ['Erik Magneto', 'Charles Xavier'],
        'raw_phrase': "Eric can control metal with his mind.",
        "corrected_phrase": "Erik can control metal with his mind."
    },
    {
        'names': ['Sofia Vergara', 'Julie Bowen'],
        'raw_phrase': "Sophia is very loud and funny.",
        "corrected_phrase": "Sofia is very loud and funny."
    },
    {
        'names': ['Lynda Carter', 'Gal Gadot'],
        'raw_phrase': "Linda was the original Wonder Woman.",
        "corrected_phrase": "Lynda was the original Wonder Woman."
    },
    {
        'names': ['Gerry Lane', 'Brad Pitt'],
        'raw_phrase': "Jerry is trying to survive the zombie apocalypse.",
        "corrected_phrase": "Gerry is trying to survive the zombie apocalypse."
    },
    {
        'names': ['Dianne Wiest', 'Edward Scissorhands'],
        'raw_phrase': "Diane is very caring and motherly.",
        "corrected_phrase": "Dianne is very caring and motherly."
    },
    {
        'names': ['Teresa Lisbon', 'Patrick Jane'],
        'raw_phrase': "Theresa is the boss of the CBI unit.",
        "corrected_phrase": "Teresa is the boss of the CBI unit."
    },
    {
        'names': ['Bharath Ram'],
        'raw_phrase': "Bharat is debugging the latency issue on the production server.",
        "corrected_phrase": "Bharath is debugging the latency issue on the production server."
    },
    {
        'names': ['Bharath Kumar', 'Sanjay Gupta'],
        'raw_phrase': "I spoke with Barath about the API integration, and he thinks we should use gRPC instead of REST.",
        "corrected_phrase": "I spoke with Bharath about the API integration, and he thinks we should use gRPC instead of REST."
    },
    {
        'names': ['Silvio Dante', 'Tony Soprano'],
        'raw_phrase': "Sylvio is managing the club effectively while Tony is away.",
        "corrected_phrase": "Silvio is managing the club effectively while Tony is away."
    },
    {
        'names': ['Silvio Berlusconi'],
        'raw_phrase': "The news article mentioned Sylvio's recent political comments.",
        "corrected_phrase": "The news article mentioned Silvio's recent political comments."
    },
    {
        'names': ['Alexey Navalny'],
        'raw_phrase': "Alexei has been a prominent figure in the opposition movement for years.",
        "corrected_phrase": "Alexey has been a prominent figure in the opposition movement for years."
    },
    {
        'names': ['Alexey Pajitnov', 'Vladimir Pokhilko'],
        'raw_phrase': "Did you know that Alexi created Tetris while working at the Dorodnitsyn Computing Centre?",
        "corrected_phrase": "Did you know that Alexey created Tetris while working at the Dorodnitsyn Computing Centre?"
    },
    {
        'names': ['Kah Mun Wong'],
        'raw_phrase': "Kahmun suggested we optimize the SQL query to reduce the load time.",
        "corrected_phrase": "Kah Mun suggested we optimize the SQL query to reduce the load time."
    },
    {
        'names': ['Kah Mun Lee', 'Wei Ling'],
        'raw_phrase': "I'm scheduling a sync with Ka Mun and Wei Ling to discuss the frontend architecture.",
        "corrected_phrase": "I'm scheduling a sync with Kah Mun and Wei Ling to discuss the frontend architecture."
    },
    {
        'names': ['Krystle Carrington', 'Blake Carrington'],
        'raw_phrase': "Crystal is planning a huge charity gala at the estate next weekend.",
        "corrected_phrase": "Krystle is planning a huge charity gala at the estate next weekend."
    },
    {
        'names': ['Jhonny Depp', 'Amber Heard'],
        'raw_phrase': "Johnny is starring in a new independent film about a jazz musician.",
        "corrected_phrase": "Jhonny is starring in a new independent film about a jazz musician."
    },
    {
        'names': ['Aleksander Ceferin'],
        'raw_phrase': "Alexander announced the new regulations for the upcoming tournament season.",
        "corrected_phrase": "Aleksander announced the new regulations for the upcoming tournament season."
    },
    {
        'names': ['Jayne Cobb', 'Malcolm Reynolds'],
        'raw_phrase': "Jane is the muscle of the crew, often carrying the biggest guns.",
        "corrected_phrase": "Jayne is the muscle of the crew, often carrying the biggest guns."
    },
    {
        'names': ['Antony Starr', 'Erin Moriarty'],
        'raw_phrase': "Anthony plays a terrifying villain in that superhero series.",
        "corrected_phrase": "Antony plays a terrifying villain in that superhero series."
    },
    {
        'names': ['Suzan-Lori Parks'],
        'raw_phrase': "Susan-Lori is a playwright who won the Pulitzer Prize for Drama.",
        "corrected_phrase": "Suzan-Lori is a playwright who won the Pulitzer Prize for Drama."
    },
    {
        'names': ['Barbra Streisand'],
        'raw_phrase': "Barbara is going on tour one last time to say goodbye to her fans.",
        "corrected_phrase": "Barbra is going on tour one last time to say goodbye to her fans."
    },
    {
        'names': ['Lukas Graham'],
        'raw_phrase': "Lucas sang that popular song about being seven years old.",
        "corrected_phrase": "Lukas sang that popular song about being seven years old."
    },
    {
        'names': ['Mikhail Baryshnikov'],
        'raw_phrase': "Michael is considered one of the greatest ballet dancers of the 20th century.",
        "corrected_phrase": "Mikhail is considered one of the greatest ballet dancers of the 20th century."
    },
    {
        'names': ['Dwyane Wade'],
        'raw_phrase': "Dwayne retired from basketball after a legendary career with the Heat.",
        "corrected_phrase": "Dwyane retired from basketball after a legendary career with the Heat."
    },
    {
        'names': ['Scarlett Johansson'],
        'raw_phrase': "Scarlet was nominated for two Academy Awards in the same year.",
        "corrected_phrase": "Scarlett was nominated for two Academy Awards in the same year."
    },
    {
        'names': ['Gwenyth Paltrow'],
        'raw_phrase': "Gwenith launched a new wellness brand that became very controversial.",
        "corrected_phrase": "Gwenyth launched a new wellness brand that became very controversial."
    },
    {
        'names': ['Zack Snyder'],
        'raw_phrase': "Zach released his director's cut of the movie on the streaming platform.",
        "corrected_phrase": "Zack released his director's cut of the movie on the streaming platform."
    },
    {
        'names': ['Caryn Johnson', 'Whoopi Goldberg'],
        'raw_phrase': "Karen changed her name to Whoopi before she became famous.",
        "corrected_phrase": "Caryn changed her name to Whoopi before she became famous."
    },
    {
        'names': ['Jian Yang', 'Erlich Bachman'],
        'raw_phrase': "Jiang Yang is trying to clone the app to sell it in the Chinese market.",
        "corrected_phrase": "Jian Yang is trying to clone the app to sell it in the Chinese market."
    },
    {
        'names': ['Dinesh Chugtai', 'Bertram Gilfoyle'],
        'raw_phrase': "Denish is always arguing with Gilfoyle about the server architecture.",
        "corrected_phrase": "Dinesh is always arguing with Gilfoyle about the server architecture."
    },
    {
        'names': ['Siobhan Roy', 'Logan Roy'],
        'raw_phrase': "Shivon is maneuvering to take over the company from her father.",
        "corrected_phrase": "Siobhan is maneuvering to take over the company from her father."
    },
    {
        'names': ['Daenerys Targaryen'],
        'raw_phrase': "Danaerys commands the dragons with a single word in High Valyrian.",
        "corrected_phrase": "Daenerys commands the dragons with a single word in High Valyrian."
    },
    {
        'names': ['Hermione Granger'],
        'raw_phrase': "Hermy-own is the brightest witch of her age and saved her friends countless times.",
        "corrected_phrase": "Hermione is the brightest witch of her age and saved her friends countless times."
    },
    {
        'names': ['Saoirse Ronan'],
        'raw_phrase': "Sersha gave a stunning performance in the historical drama.",
        "corrected_phrase": "Saoirse gave a stunning performance in the historical drama."
    },
    {
        'names': ['Joaquin Phoenix'],
        'raw_phrase': "Wakeen won the Oscar for his portrayal of the troubled comedian.",
        "corrected_phrase": "Joaquin won the Oscar for his portrayal of the troubled comedian."
    },
    {
        'names': ['Chiwetel Ejiofor'],
        'raw_phrase': "Chewetel is starring in the new sci-fi blockbuster coming out this summer.",
        "corrected_phrase": "Chiwetel is starring in the new sci-fi blockbuster coming out this summer."
    },
    {
        'names': ['Nikolaj Coster-Waldau'],
        'raw_phrase': "Nikolai plays the Kingslayer in the popular fantasy series.",
        "corrected_phrase": "Nikolaj plays the Kingslayer in the popular fantasy series."
    },
    {
        'names': ['Domhnall Gleeson'],
        'raw_phrase': "Donal played the general in the space opera sequel trilogy.",
        "corrected_phrase": "Domhnall played the general in the space opera sequel trilogy."
    },
    {
        'names': ['Ralph Fiennes'],
        'raw_phrase': "Ray Fines is known for playing villains, including the Dark Lord.",
        "corrected_phrase": "Ralph Fiennes is known for playing villains, including the Dark Lord."
    },
    {
        'names': ['Srini Iyer'],
        'raw_phrase': "Sreeni has been optimizing the data pipeline all week.",
        "corrected_phrase": "Srini has been optimizing the data pipeline all week."
    },
    {
        'names': ['Srini Narayanan'],
        'raw_phrase': "Please check with Sriny before merging that pull request.",
        "corrected_phrase": "Please check with Srini before merging that pull request."
    },
    {
        'names': ['Yingbo Zhou'],
        'raw_phrase': "Ying Bo presented the new model architecture at the conference.",
        "corrected_phrase": "Yingbo presented the new model architecture at the conference."
    },
    {
        'names': ['Yingbo Li'],
        'raw_phrase': "I'm not sure if Yinbo is available for a meeting right now.",
        "corrected_phrase": "I'm not sure if Yingbo is available for a meeting right now."
    },
    {
        'names': ['Caiming Xiong'],
        'raw_phrase': "Kai Ming led the research on large language models.",
        "corrected_phrase": "Caiming led the research on large language models."
    },
    {
        'names': ['Caiming Zhang'],
        'raw_phrase': "We need to get approval from Cai Ming for the budget increase.",
        "corrected_phrase": "We need to get approval from Caiming for the budget increase."
    },
    # Longer name lists with only some (or none) used
    {
        'names': ['Alexander Hamilton', 'George Washington', 'Thomas Jefferson', 'James Madison', 'John Adams', 'Benjamin Franklin', 'John Jay', 'Aaron Burr'],
        'raw_phrase': "I was reading about how Aaron killed Alexander in a duel.",
        'corrected_phrase': "I was reading about how Aaron killed Alexander in a duel."
    },
    {
        'names': ['Luke Skywalker', 'Leia Organa', 'Han Solo', 'Chewbacca', 'C-3PO', 'R2-D2', 'Lando Calrissian', 'Yoda', 'Obi-Wan Kenobi'],
        'raw_phrase': "Hans and Chewy are flying the Falcon.",
        'corrected_phrase': "Han and Chewbacca are flying the Falcon."
    },
    {
        'names': ['Frodo Baggins', 'Samwise Gamgee', 'Meriadoc Brandybuck', 'Peregrin Took', 'Aragorn', 'Legolas Greenleaf', 'Gimli', 'Boromir', 'Gandalf the Grey'],
        'raw_phrase': "Sam and Frodo are walking to Mordor alone.",
        'corrected_phrase': "Sam and Frodo are walking to Mordor alone."
    },
    {
        'names': ['Harry Potter', 'Ron Weasley', 'Hermione Granger', 'Neville Longbottom', 'Ginny Weasley', 'Luna Lovegood', 'Draco Malfoy', 'Severus Snape', 'Albus Dumbledore'],
        'raw_phrase': "Hary and Ron missed the train to Hogwarts.",
        'corrected_phrase': "Harry and Ron missed the train to Hogwarts."
    },
    {
        'names': ['Tony Stark', 'Steve Rogers', 'Thor Odinson', 'Bruce Banner', 'Natasha Romanoff', 'Clint Barton', 'Wanda Maximoff', 'Vision', 'Sam Wilson', 'Bucky Barnes'],
        'raw_phrase': "Tony and Steve argued about the accords.",
        'corrected_phrase': "Tony and Steve argued about the accords."
    },
    {
        'names': ['Michael Scott', 'Dwight Schrute', 'Jim Halpert', 'Pam Beesly', 'Ryan Howard', 'Andy Bernard', 'Angela Martin', 'Kevin Malone', 'Oscar Martinez'],
        'raw_phrase': "Dwight tried to get Jim fired again.",
        'corrected_phrase': "Dwight tried to get Jim fired again."
    },
    {
        'names': ['Rachel Green', 'Monica Geller', 'Phoebe Buffay', 'Joey Tribbiani', 'Chandler Bing', 'Ross Geller'],
        'raw_phrase': "Pheebe sang a weird song at the coffee house.",
        'corrected_phrase': "Phoebe sang a weird song at the coffee house."
    },
    {
        'names': ['Walter White', 'Jesse Pinkman', 'Skyler White', 'Hank Schrader', 'Marie Schrader', 'Saul Goodman', 'Mike Ehrmantraut', 'Gustavo Fring'],
        'raw_phrase': "Jesse is cooking in the RV with Mr. White.",
        'corrected_phrase': "Jesse is cooking in the RV with Mr. White."
    },
    {
        'names': ['Rick Grimes', 'Daryl Dixon', 'Glenn Rhee', 'Maggie Greene', 'Carol Peletier', 'Michonne', 'Carl Grimes', 'Hershel Greene'],
        'raw_phrase': "Darryl found a motorcycle on the road.",
        'corrected_phrase': "Daryl found a motorcycle on the road."
    },
    {
        'names': ['Buffy Summers', 'Willow Rosenberg', 'Xander Harris', 'Rupert Giles', 'Angel', 'Spike', 'Cordelia Chase', 'Oz'],
        'raw_phrase': "Buffie is patrolling the cemetery tonight.",
        'corrected_phrase': "Buffy is patrolling the cemetery tonight."
    },
    # Examples where names are NOT used in the phrase (No correction needed or different context)
    {
        'names': ['Alice Wang', 'Bob Smith'],
        'raw_phrase': "The weather is really nice today.",
        'corrected_phrase': "The weather is really nice today."
    },
    {
        'names': ['Jon Doe', 'Jane Smith'],
        'raw_phrase': "Can you pass me the salt please?",
        'corrected_phrase': "Can you pass me the salt please?"
    },
    {
        'names': ['Sara Connor', 'Kyle Reese'],
        'raw_phrase': "I need to restart my computer.",
        'corrected_phrase': "I need to restart my computer."
    },
    {
        'names': ['Marc Jacobs', 'Louis Vuitton'],
        'raw_phrase': "This coffee is too hot to drink.",
        'corrected_phrase': "This coffee is too hot to drink."
    },
    {
        'names': ['Caitlin Snow', 'Barry Allen'],
        'raw_phrase': "Where did you park the car?",
        'corrected_phrase': "Where did you park the car?"
    },
    {
        'names': ['Geoff Bezos', 'Elon Musk'],
        'raw_phrase': "Let's meet at the library at 5 PM.",
        'corrected_phrase': "Let's meet at the library at 5 PM."
    },
    {
        'names': ['Kristina Pimenova', 'Anastasia Bezrukova'],
        'raw_phrase': "Did you see the game last night?",
        'corrected_phrase': "Did you see the game last night?"
    },
    {
        'names': ['Steven Spielberg', 'George Lucas'],
        'raw_phrase': "I forgot to bring my charger.",
        'corrected_phrase': "I forgot to bring my charger."
    },
    {
        'names': ['Elisabeth Moss', 'June Osborne'],
        'raw_phrase': "The printer is out of paper again.",
        'corrected_phrase': "The printer is out of paper again."
    },
    {
        'names': ['Rachael Ray', 'Gordon Ramsay'],
        'raw_phrase': "Please turn off the lights when you leave.",
        'corrected_phrase': "Please turn off the lights when you leave."
    },
    {
        'names': ['Bryan Cranston', 'Aaron Paul'],
        'raw_phrase': "Have you finished reading the report?",
        'corrected_phrase': "Have you finished reading the report?"
    },
    {
        'names': ['Cate Blanchett', 'Rooney Mara'],
        'raw_phrase': "We are going to be late for the movie.",
        'corrected_phrase': "We are going to be late for the movie."
    },
    {
        'names': ['Micheal Keaton', 'Jack Nicholson'],
        'raw_phrase': "What time is the bus arriving?",
        'corrected_phrase': "What time is the bus arriving?"
    },
    {
        'names': ['Jaimie Alexander', 'Chris Hemsworth'],
        'raw_phrase': "I need to buy some groceries.",
        'corrected_phrase': "I need to buy some groceries."
    },
    {
        'names': ['Mathew Perry', 'Courteney Cox'],
        'raw_phrase': "Don't forget to water the plants.",
        'corrected_phrase': "Don't forget to water the plants."
    },
    {
        'names': ['Erik Magneto', 'Charles Xavier'],
        'raw_phrase': "The internet connection is down.",
        'corrected_phrase': "The internet connection is down."
    },
    {
        'names': ['Sofia Vergara', 'Julie Bowen'],
        'raw_phrase': "Could you open the window?",
        'corrected_phrase': "Could you open the window?"
    },
    {
        'names': ['Lynda Carter', 'Gal Gadot'],
        'raw_phrase': "My phone battery is dying.",
        'corrected_phrase': "My phone battery is dying."
    },
    {
        'names': ['Gerry Lane', 'Brad Pitt'],
        'raw_phrase': "I have a dentist appointment tomorrow.",
        'corrected_phrase': "I have a dentist appointment tomorrow."
    },
    {
        'names': ['Dianne Wiest', 'Edward Scissorhands'],
        'raw_phrase': "Can you help me move this table?",
        'corrected_phrase': "Can you help me move this table?"
    },
    {
        'names': ['Teresa Lisbon', 'Patrick Jane'],
        'raw_phrase': "It's supposed to rain all week.",
        'corrected_phrase': "It's supposed to rain all week."
    },
    {
        'names': ['Bharath Ram'],
        'raw_phrase': "The server needs to be rebooted.",
        'corrected_phrase': "The server needs to be rebooted."
    },
    {
        'names': ['Bharath Kumar', 'Sanjay Gupta'],
        'raw_phrase': "We should deploy the hotfix immediately.",
        'corrected_phrase': "We should deploy the hotfix immediately."
    },
    {
        'names': ['Silvio Dante', 'Tony Soprano'],
        'raw_phrase': "I ordered pizza for lunch.",
        'corrected_phrase': "I ordered pizza for lunch."
    },
    {
        'names': ['Silvio Berlusconi'],
        'raw_phrase': "The stock market is volatile today.",
        'corrected_phrase': "The stock market is volatile today."
    },
    {
        'names': ['Alexey Navalny'],
        'raw_phrase': "Did you watch the debate last night?",
        'corrected_phrase': "Did you watch the debate last night?"
    },
    {
        'names': ['Alexey Pajitnov', 'Vladimir Pokhilko'],
        'raw_phrase': "Video games are a great way to relax.",
        'corrected_phrase': "Video games are a great way to relax."
    },
    {
        'names': ['Kah Mun Wong'],
        'raw_phrase': "The meeting room is double booked.",
        'corrected_phrase': "The meeting room is double booked."
    },
    {
        'names': ['Kah Mun Lee', 'Wei Ling'],
        'raw_phrase': "We need to update the documentation.",
        'corrected_phrase': "We need to update the documentation."
    },
    {
        'names': ['Krystle Carrington', 'Blake Carrington'],
        'raw_phrase': "The party was a huge success.",
        'corrected_phrase': "The party was a huge success."
    },
    {
        'names': ['Jhonny Depp', 'Amber Heard'],
        'raw_phrase': "The court case is finally over.",
        'corrected_phrase': "The court case is finally over."
    },
    {
        'names': ['Luke Skywalker', 'Han Solo'],
        'raw_phrase': "The hyperdrive is broken again.",
        'corrected_phrase': "The hyperdrive is broken again."
    },
    # Reverse direction examples
    {
        'names': ['Charlie Davis', 'Bob Smith'],
        'raw_phrase': 'Hey Charly, can you help me with this project?',
        'corrected_phrase': 'Hey Charlie, can you help me with this project?'
    },
    {
        'names': ['John Doe', 'Jane Smith'],
        'raw_phrase': 'I think Jon is handling the deployment today.',
        'corrected_phrase': 'I think John is handling the deployment today.'
    },
    {
        'names': ['Sarah Connor', 'Kyle Reese'],
        'raw_phrase': 'Did you send the invite to Sara yet?',
        'corrected_phrase': 'Did you send the invite to Sarah yet?'
    },
    {
        'names': ['Mark Jacobs', 'Louis Vuitton'],
        'raw_phrase': 'Marc is leading the design team meeting.',
        'corrected_phrase': 'Mark is leading the design team meeting.'
    },
    {
        'names': ['Kaitlyn Snow', 'Barry Allen'],
        'raw_phrase': 'Caitlin needs access to the repository.',
        'corrected_phrase': 'Kaitlyn needs access to the repository.'
    },
    {
        'names': ['Jeff Bezos', 'Elon Musk'],
        'raw_phrase': 'Geoff suggested we pivot the strategy.',
        'corrected_phrase': 'Jeff suggested we pivot the strategy.'
    },
    {
        'names': ['Christina Pimenova', 'Anastasia Bezrukova'],
        'raw_phrase': 'Please ask Kristina to review the document.',
        'corrected_phrase': 'Please ask Christina to review the document.'
    },
    {
        'names': ['Stephen Spielberg', 'George Lucas'],
        'raw_phrase': 'Steven is directing the new commercial.',
        'corrected_phrase': 'Stephen is directing the new commercial.'
    },
    {
        'names': ['Elizabeth Moss', 'June Osborne'],
        'raw_phrase': 'Elisabeth will be late for the standup.',
        'corrected_phrase': 'Elizabeth will be late for the standup.'
    },
    {
        'names': ['Rachel Ray', 'Gordon Ramsay'],
        'raw_phrase': 'Rachael brought donuts for everyone.',
        'corrected_phrase': 'Rachel brought donuts for everyone.'
    },
    {
        'names': ['Brian Cranston', 'Aaron Paul'],
        'raw_phrase': 'Bryan is cooking something in the lab.',
        'corrected_phrase': 'Brian is cooking something in the lab.'
    },
    {
        'names': ['Kate Blanchett', 'Rooney Mara'],
        'raw_phrase': 'Cate won the award for best performance.',
        'corrected_phrase': 'Kate won the award for best performance.'
    },
    {
        'names': ['Michael Keaton', 'Jack Nicholson'],
        'raw_phrase': 'Micheal is Batman in this version.',
        'corrected_phrase': 'Michael is Batman in this version.'
    },
    {
        'names': ['Jamie Alexander', 'Chris Hemsworth'],
        'raw_phrase': 'Jaimie is fighting on the front lines.',
        'corrected_phrase': 'Jamie is fighting on the front lines.'
    },
    {
        'names': ['Matthew Perry', 'Courteney Cox'],
        'raw_phrase': 'Mathew made a funny joke during the break.',
        'corrected_phrase': 'Matthew made a funny joke during the break.'
    },
    {
        'names': ['Eric Magneto', 'Charles Xavier'],
        'raw_phrase': 'Erik can control metal with his mind.',
        'corrected_phrase': 'Eric can control metal with his mind.'
    },
    {
        'names': ['Sophia Vergara', 'Julie Bowen'],
        'raw_phrase': 'Sofia is very loud and funny.',
        'corrected_phrase': 'Sophia is very loud and funny.'
    },
    {
        'names': ['Linda Carter', 'Gal Gadot'],
        'raw_phrase': 'Lynda was the original Wonder Woman.',
        'corrected_phrase': 'Linda was the original Wonder Woman.'
    },
    {
        'names': ['Jerry Lane', 'Brad Pitt'],
        'raw_phrase': 'Gerry is trying to survive the zombie apocalypse.',
        'corrected_phrase': 'Jerry is trying to survive the zombie apocalypse.'
    },
    {
        'names': ['Diane Wiest', 'Edward Scissorhands'],
        'raw_phrase': 'Dianne is very caring and motherly.',
        'corrected_phrase': 'Diane is very caring and motherly.'
    },
    {
        'names': ['Theresa Lisbon', 'Patrick Jane'],
        'raw_phrase': 'Teresa is the boss of the CBI unit.',
        'corrected_phrase': 'Theresa is the boss of the CBI unit.'
    },
    {
        'names': ['Bharat Ram'],
        'raw_phrase': 'Bharath is debugging the latency issue on the production server.',
        'corrected_phrase': 'Bharat is debugging the latency issue on the production server.'
    },
    # Examples with no name usage but present name list
    {
        'names': ['Alice Wang', 'Bob Smith'],
        'raw_phrase': "I'm thinking about taking a vacation to Italy next summer, maybe visit Rome and Florence.",
        'corrected_phrase': "I'm thinking about taking a vacation to Italy next summer, maybe visit Rome and Florence."
    },
    {
        'names': ['Jon Doe', 'Jane Smith'],
        'raw_phrase': 'The quarterly financial report is due by the end of the week, so we need to finalize the numbers.',
        'corrected_phrase': 'The quarterly financial report is due by the end of the week, so we need to finalize the numbers.'
    },
    {
        'names': ['Sara Connor', 'Kyle Reese'],
        'raw_phrase': 'Can you believe that the new restaurant downtown has a three-month waiting list?',
        'corrected_phrase': 'Can you believe that the new restaurant downtown has a three-month waiting list?'
    },
    {
        'names': ['Marc Jacobs', 'Louis Vuitton'],
        'raw_phrase': 'I need to schedule a maintenance appointment for my car before the long road trip.',
        'corrected_phrase': 'I need to schedule a maintenance appointment for my car before the long road trip.'
    },
    {
        'names': ['Caitlin Snow', 'Barry Allen'],
        'raw_phrase': 'The presentation went really well, and the client seemed impressed with our proposal.',
        'corrected_phrase': 'The presentation went really well, and the client seemed impressed with our proposal.'
    },
    {
        'names': ['Geoff Bezos', 'Elon Musk'],
        'raw_phrase': "It's important to double-check the code before deploying it to the production environment.",
        'corrected_phrase': "It's important to double-check the code before deploying it to the production environment."
    },
    {
        'names': ['Kristina Pimenova', 'Anastasia Bezrukova'],
        'raw_phrase': "I've been trying to learn how to play the guitar, but my fingers hurt after practicing.",
        'corrected_phrase': "I've been trying to learn how to play the guitar, but my fingers hurt after practicing."
    },
    {
        'names': ['Steven Spielberg', 'George Lucas'],
        'raw_phrase': 'The traffic was terrible this morning, so I was twenty minutes late to the meeting.',
        'corrected_phrase': 'The traffic was terrible this morning, so I was twenty minutes late to the meeting.'
    },
    {
        'names': ['Elisabeth Moss', 'June Osborne'],
        'raw_phrase': 'Please remember to submit your expense reports by 5 PM on Friday.',
        'corrected_phrase': 'Please remember to submit your expense reports by 5 PM on Friday.'
    },
    {
        'names': ['Rachael Ray', 'Gordon Ramsay'],
        'raw_phrase': "I'm looking for a recipe for a vegan chocolate cake that actually tastes good.",
        'corrected_phrase': "I'm looking for a recipe for a vegan chocolate cake that actually tastes good."
    },
    {
        'names': ['Bryan Cranston', 'Aaron Paul'],
        'raw_phrase': 'The server is down again, and IT says it might take a few hours to fix.',
        'corrected_phrase': 'The server is down again, and IT says it might take a few hours to fix.'
    },
    {
        'names': ['Cate Blanchett', 'Rooney Mara'],
        'raw_phrase': 'We should organize a team-building event to boost morale after the busy season.',
        'corrected_phrase': 'We should organize a team-building event to boost morale after the busy season.'
    },
    {
        'names': ['Micheal Keaton', 'Jack Nicholson'],
        'raw_phrase': 'Did you hear about the new policy regarding remote work options?',
        'corrected_phrase': 'Did you hear about the new policy regarding remote work options?'
    },
    {
        'names': ['Jaimie Alexander', 'Chris Hemsworth'],
        'raw_phrase': "I'm running low on coffee beans, so I need to stop by the roastery.",
        'corrected_phrase': "I'm running low on coffee beans, so I need to stop by the roastery."
    },
    {
        'names': ['Mathew Perry', 'Courteney Cox'],
        'raw_phrase': 'The movie we watched last night had a really unexpected plot twist at the end.',
        'corrected_phrase': 'The movie we watched last night had a really unexpected plot twist at the end.'
    },
    {
        'names': ['Erik Magneto', 'Charles Xavier'],
        'raw_phrase': 'Make sure to backup your data regularly to avoid losing important files.',
        'corrected_phrase': 'Make sure to backup your data regularly to avoid losing important files.'
    },
    {
        'names': ['Sofia Vergara', 'Julie Bowen'],
        'raw_phrase': "I'm thinking of adopting a dog from the local shelter this weekend.",
        'corrected_phrase': "I'm thinking of adopting a dog from the local shelter this weekend."
    },
    {
        'names': ['Lynda Carter', 'Gal Gadot'],
        'raw_phrase': "The concert tickets sold out in minutes, so we'll have to find another way to go.",
        'corrected_phrase': "The concert tickets sold out in minutes, so we'll have to find another way to go."
    },
    {
        'names': ['Gerry Lane', 'Brad Pitt'],
        'raw_phrase': 'I need to get my passport renewed before my trip abroad next month.',
        'corrected_phrase': 'I need to get my passport renewed before my trip abroad next month.'
    },
    {
        'names': ['Dianne Wiest', 'Edward Scissorhands'],
        'raw_phrase': 'Can you recommend a good book for reading on the plane?',
        'corrected_phrase': 'Can you recommend a good book for reading on the plane?'
    },
    {
        'names': ['Teresa Lisbon', 'Patrick Jane'],
        'raw_phrase': 'The weather forecast predicts heavy rain and thunderstorms for the entire weekend.',
        'corrected_phrase': 'The weather forecast predicts heavy rain and thunderstorms for the entire weekend.'
    },
    {
        'names': ['Bharath Ram'],
        'raw_phrase': 'We need to optimize the database queries to improve application performance.',
        'corrected_phrase': 'We need to optimize the database queries to improve application performance.'
    },
    {
        'names': ['Bharath Kumar', 'Sanjay Gupta'],
        'raw_phrase': "I'm going to take a personal day on Monday to catch up on some errands.",
        'corrected_phrase': "I'm going to take a personal day on Monday to catch up on some errands."
    },
    {
        'names': ['Silvio Dante', 'Tony Soprano'],
        'raw_phrase': "The marketing campaign didn't yield the results we were hoping for.",
        'corrected_phrase': "The marketing campaign didn't yield the results we were hoping for."
    },
    {
        'names': ['Silvio Berlusconi'],
        'raw_phrase': "I've been experiencing some issues with my laptop freezing randomly.",
        'corrected_phrase': "I've been experiencing some issues with my laptop freezing randomly."
    },
    # EXTENDED ENTRIES
    {
        'names': ['Rhaenyra Targaryen', 'Alicent Hightower', 'Daemon Targaryen'],
        'raw_phrase': 'Raniera and Alison are fighting for the throne.',
        'corrected_phrase': 'Rhaenyra and Alicent are fighting for the throne.'
    },
    {
        'names': ['Kendall Roy', 'Roman Roy', 'Gerri Kellman'],
        'raw_phrase': 'Kendle and Geri discussed the merger.',
        'corrected_phrase': 'Kendall and Gerri discussed the merger.'
    },
    {
        'names': ['Beyoncé Knowles', 'Jay-Z'],
        'raw_phrase': 'Bee-yonce released a new album.',
        'corrected_phrase': 'Beyoncé released a new album.'
    },
    {
        'names': ['Rihanna', 'A$AP Rocky'],
        'raw_phrase': 'Rhianna is performing at the halftime show.',
        'corrected_phrase': 'Rihanna is performing at the halftime show.'
    },
    {
        'names': ['Kanye West', 'Kim Kardashian'],
        'raw_phrase': 'Kayne interrupted the speech.',
        'corrected_phrase': 'Kanye interrupted the speech.'
    },
    {
        'names': ['Satya Nadella', 'Bill Gates'],
        'raw_phrase': 'Sacha announced the new AI integration.',
        'corrected_phrase': 'Satya announced the new AI integration.'
    },
    {
        'names': ['Sundar Pichai', 'Larry Page'],
        'raw_phrase': 'Sunder is testifying before Congress.',
        'corrected_phrase': 'Sundar is testifying before Congress.'
    },
    {
        'names': ['Elon Musk', 'Grimes', 'X Æ A-12'],
        'raw_phrase': 'Grimez and Elon named their child something unique.',
        'corrected_phrase': 'Grimes and Elon named their child something unique.'
    },
    {
        'names': ['Cillian Murphy', 'Robert Downey Jr'],
        'raw_phrase': 'Killian won best actor for Oppenheimer.',
        'corrected_phrase': 'Cillian won best actor for Oppenheimer.'
    },
    {
        'names': ['Saoirse Ronan', 'Timothée Chalamet'],
        'raw_phrase': 'Sersha and Timothy are in the new adaptation.',
        'corrected_phrase': 'Saoirse and Timothée are in the new adaptation.'
    },
    {
        'names': ['Thierry Henry', 'Zinedine Zidane'],
        'raw_phrase': 'Terry Henry was unstoppable in his prime.',
        'corrected_phrase': 'Thierry Henry was unstoppable in his prime.'
    },
    {
        'names': ['Kylian Mbappé', 'Lionel Messi'],
        'raw_phrase': 'Killian Mbappe is the future of football.',
        'corrected_phrase': 'Kylian Mbappé is the future of football.'
    },
    {
        'names': ['Siobhan', 'Sinead', 'Niamh'],
        'raw_phrase': 'Shavon and Sinead are going to the concert.',
        'corrected_phrase': 'Siobhan and Sinead are going to the concert.'
    },
    {
        'names': ['Caoimhe', 'Tadhg', 'Saoirse'],
        'raw_phrase': 'Keeva and Tige are classic Irish names.',
        'corrected_phrase': 'Caoimhe and Tadhg are classic Irish names.'
    },
    {
        'names': ['Jian-Yang', 'Erlich Bachman'],
        'raw_phrase': 'Jian Yang is pitching a new app.',
        'corrected_phrase': 'Jian-Yang is pitching a new app.'
    },
    {
        'names': ['Dinesh Chugtai', 'Bertram Gilfoyle'],
        'raw_phrase': 'Gilfoil hacked the smart fridge.',
        'corrected_phrase': 'Gilfoyle hacked the smart fridge.'
    },
    {
        'names': ['Leslie Knope', 'Ben Wyatt'],
        'raw_phrase': 'Lesley organized the harvest festival.',
        'corrected_phrase': 'Leslie organized the harvest festival.'
    },
    {
        'names': ['Ron Swanson', 'April Ludgate'],
        'raw_phrase': 'Ron and Aprel hate meetings.',
        'corrected_phrase': 'Ron and April hate meetings.'
    },
    {
        'names': ['Jake Peralta', 'Amy Santiago'],
        'raw_phrase': 'Jack and Amie are solving the case.',
        'corrected_phrase': 'Jake and Amy are solving the case.'
    },
    {
        'names': ['Rosa Diaz', 'Terry Jeffords'],
        'raw_phrase': 'Roza and Teri are at the gym.',
        'corrected_phrase': 'Rosa and Terry are at the gym.'
    },
    {
        'names': ['Eleven', 'Mike Wheeler'],
        'raw_phrase': 'El and Mick are communicating via walkie-talkie.',
        'corrected_phrase': 'Eleven and Mike are communicating via walkie-talkie.'
    },
    {
        'names': ['Dustin Henderson', 'Steve Harrington'],
        'raw_phrase': 'Dustan and Steeve are fighting demodogs.',
        'corrected_phrase': 'Dustin and Steve are fighting demodogs.'
    },
    {
        'names': ['Bruce Wayne', 'Clark Kent'],
        'raw_phrase': 'Clark and Bruce are forming a league.',
        'corrected_phrase': 'Clark and Bruce are forming a league.'
    },
    {
        'names': ['Diana Prince', 'Arthur Curry'],
        'raw_phrase': 'Diane and Arther are protecting the box.',
        'corrected_phrase': 'Diana and Arthur are protecting the box.'
    },
    {
        'names': ['Scott Summers', 'Jean Grey'],
        'raw_phrase': 'Jeane can read minds.',
        'corrected_phrase': 'Jean can read minds.'
    },
    {
        'names': ['Logan', 'Ororo Munroe'],
        'raw_phrase': 'Logen and Aurora are leading the mission.',
        'corrected_phrase': 'Logan and Ororo are leading the mission.'
    },
    {
        'names': ['Homer Simpson', 'Marge Simpson'],
        'raw_phrase': 'Homar is at the power plant.',
        'corrected_phrase': 'Homer is at the power plant.'
    },
    {
        'names': ['Bart Simpson', 'Lisa Simpson'],
        'raw_phrase': 'Burt and Leesa are arguing.',
        'corrected_phrase': 'Bart and Lisa are arguing.'
    },
    {
        'names': ['Peter Griffin', 'Lois Griffin'],
        'raw_phrase': 'Loius is teaching piano.',
        'corrected_phrase': 'Lois is teaching piano.'
    },
    {
        'names': ['Stan Marsh', 'Kyle Broflovski'],
        'raw_phrase': 'Kile and Stann are waiting for the bus.',
        'corrected_phrase': 'Kyle and Stan are waiting for the bus.'
    },
    {
        'names': ['Kathryn Janeway', 'Chakotay'],
        'raw_phrase': 'Catherine is the captain of Voyager.',
        'corrected_phrase': 'Kathryn is the captain of Voyager.'
    },
    {
        'names': ['Shawn Spencer', 'Burton Guster'],
        'raw_phrase': 'Sean and Gus are consulting detectives.',
        'corrected_phrase': 'Shawn and Gus are consulting detectives.'
    },
    {
        'names': ['Shaun of the Dead', 'Ed'],
        'raw_phrase': 'Sean needs to sort his life out.',
        'corrected_phrase': 'Shaun needs to sort his life out.'
    },
    {
        'names': ['Geoff Peterson', 'Craig Ferguson'],
        'raw_phrase': 'Jeff is the robot skeleton sidekick.',
        'corrected_phrase': 'Geoff is the robot skeleton sidekick.'
    },
    {
        'names': ['Marc Anthony', 'Jennifer Lopez'],
        'raw_phrase': 'Mark sang a duet with Jennifer.',
        'corrected_phrase': 'Marc sang a duet with Jennifer.'
    },
    {
        'names': ['Jon Snow', 'Arya Stark'],
        'raw_phrase': 'John knows nothing.',
        'corrected_phrase': 'Jon knows nothing.'
    },
    {
        'names': ['Sara Bareilles', 'Ingrid Michaelson'],
        'raw_phrase': 'Sarah is writing a musical.',
        'corrected_phrase': 'Sara is writing a musical.'
    },
    {
        'names': ['Krysten Ritter', 'David Tennant'],
        'raw_phrase': 'Kristen played a private investigator.',
        'corrected_phrase': 'Krysten played a private investigator.'
    },
    {
        'names': ['Isobel Crawley', 'Violet Crawley'],
        'raw_phrase': 'Isabel and Violet are having tea.',
        'corrected_phrase': 'Isobel and Violet are having tea.'
    },
    {
        'names': ['Zoe Saldana', 'Chris Pratt'],
        'raw_phrase': 'Zoey is green in that movie.',
        'corrected_phrase': 'Zoe is green in that movie.'
    },
    {
        'names': ['Kaia Gerber', 'Cindy Crawford'],
        'raw_phrase': 'Kaya looks just like her mother.',
        'corrected_phrase': 'Kaia looks just like her mother.'
    },
    {
        'names': ['Gisele Bündchen', 'Tom Brady'],
        'raw_phrase': 'Giselle is a supermodel.',
        'corrected_phrase': 'Gisele is a supermodel.'
    },
    {
        'names': ['Cate Blanchett', 'Andrew Upton'],
        'raw_phrase': 'Kate is starring in a new play.',
        'corrected_phrase': 'Cate is starring in a new play.'
    },
    {
        'names': ['Layne Staley', 'Jerry Cantrell'],
        'raw_phrase': 'Lane was the lead singer of Alice in Chains.',
        'corrected_phrase': 'Layne was the lead singer of Alice in Chains.'
    },
    {
        'names': ['Dwyane Wade', 'Gabrielle Union'],
        'raw_phrase': 'Dwayne scored 30 points.',
        'corrected_phrase': 'Dwyane scored 30 points.'
    },
    {
        'names': ['Antony Starr', 'Karl Urban'],
        'raw_phrase': 'Anthony plays Homelander.',
        'corrected_phrase': 'Antony plays Homelander.'
    },
    {
        'names': ['Rami Malek', 'Christian Slater'],
        'raw_phrase': 'Ramy won an Oscar for Bohemian Rhapsody.',
        'corrected_phrase': 'Rami won an Oscar for Bohemian Rhapsody.'
    },
    {
        'names': ['Shia LaBeouf', 'Megan Fox'],
        'raw_phrase': 'Shya starred in Transformers.',
        'corrected_phrase': 'Shia starred in Transformers.'
    },
    {
        'names': ['Chloë Grace Moretz', 'Brooklyn Beckham'],
        'raw_phrase': 'Chloe is filming a sci-fi thriller.',
        'corrected_phrase': 'Chloë is filming a sci-fi thriller.'
    },
    {
        'names': ['Saoirse Ronan', 'Paul Mescal'],
        'raw_phrase': 'Sersha and Paul are Irish actors.',
        'corrected_phrase': 'Saoirse and Paul are Irish actors.'
    },
    {
        'names': ['Harry Styles', 'Niall Horan', 'Liam Payne', 'Louis Tomlinson', 'Zayn Malik'],
        'raw_phrase': 'Nial and Zane left the band.',
        'corrected_phrase': 'Niall and Zayn left the band.'
    },
    {
        'names': ['John Lennon', 'Paul McCartney', 'George Harrison', 'Ringo Starr'],
        'raw_phrase': 'Ringo and George wrote fewer songs than Paul.',
        'corrected_phrase': 'Ringo and George wrote fewer songs than Paul.'
    },
    {
        'names': ['Mick Jagger', 'Keith Richards', 'Charlie Watts', 'Ronnie Wood'],
        'raw_phrase': 'Keith and Mick have been performing for decades.',
        'corrected_phrase': 'Keith and Mick have been performing for decades.'
    },
    {
        'names': ['Agnetha Fältskog', 'Björn Ulvaeus', 'Benny Andersson', 'Anni-Frid Lyngstad'],
        'raw_phrase': 'Bjorn and Benny wrote the music for Mamma Mia.',
        'corrected_phrase': 'Björn and Benny wrote the music for Mamma Mia.'
    },
    {
        'names': ['Serena Williams', 'Venus Williams', 'Alexis Ohanian'],
        'raw_phrase': 'Venice and Serena dominated tennis.',
        'corrected_phrase': 'Venus and Serena dominated tennis.'
    },
    {
        'names': ['Kourtney Kardashian', 'Kim Kardashian', 'Khloé Kardashian', 'Kendall Jenner', 'Kylie Jenner'],
        'raw_phrase': 'Cloe and Kourtney are fighting again.',
        'corrected_phrase': 'Khloé and Kourtney are fighting again.'
    },
    {
        'names': ['Luke Hemsworth', 'Chris Hemsworth', 'Liam Hemsworth'],
        'raw_phrase': 'Laim is the youngest of the brothers.',
        'corrected_phrase': 'Liam is the youngest of the brothers.'
    },
    {
        'names': ['Alec Baldwin', 'Daniel Baldwin', 'William Baldwin', 'Stephen Baldwin'],
        'raw_phrase': 'Steven is the youngest Baldwin brother.',
        'corrected_phrase': 'Stephen is the youngest Baldwin brother.'
    },
    {
        'names': ['Groucho Marx', 'Harpo Marx', 'Chico Marx', 'Zeppo Marx'],
        'raw_phrase': 'Harpo never speaks in the movies.',
        'corrected_phrase': 'Harpo never speaks in the movies.'
    },
    {
        'names': ['Leonardo', 'Michelangelo', 'Donatello', 'Raphael'],
        'raw_phrase': 'Michaelangelo paints the Sistine Chapel.',
        'corrected_phrase': 'Michelangelo paints the Sistine Chapel.'
    },
    {
        'names': ['Athos', 'Porthos', 'Aramis', "d'Artagnan"],
        'raw_phrase': 'Porthos and Aramis are musketeers.',
        'corrected_phrase': 'Porthos and Aramis are musketeers.'
    },
    {
        'names': ['Huey', 'Dewey', 'Louie', 'Donald Duck'],
        'raw_phrase': "Dewey and Louis are Donald's nephews.",
        'corrected_phrase': "Dewey and Louie are Donald's nephews."
    },
    {
        'names': ['Blossom', 'Bubbles', 'Buttercup', 'Professor Utonium'],
        'raw_phrase': 'Bubles fits the cute stereotype.',
        'corrected_phrase': 'Bubbles fits the cute stereotype.'
    },
    {
        'names': ['Ed', 'Edd', 'Eddy'],
        'raw_phrase': 'Ed and Eddie are trying to get jawbreakers.',
        'corrected_phrase': 'Ed and Eddy are trying to get jawbreakers.'
    },
    {
        'names': ['Yakko', 'Wakko', 'Dot'],
        'raw_phrase': 'Wacko and Dot are the Warner siblings.',
        'corrected_phrase': 'Wakko and Dot are the Warner siblings.'
    },
    {
        'names': ['Mickey Mouse', 'Minnie Mouse', 'Donald Duck', 'Daisy Duck', 'Goofy', 'Pluto'],
        'raw_phrase': 'Minny and Daisy are best friends.',
        'corrected_phrase': 'Minnie and Daisy are best friends.'
    },
    {
        'names': ['Fred Jones', 'Daphne Blake', 'Velma Dinkley', 'Shaggy Rogers', 'Scooby-Doo'],
        'raw_phrase': 'Daphnee and Vilma found a clue.',
        'corrected_phrase': 'Daphne and Velma found a clue.'
    },
    {
        'names': ['Spongebob Squarepants', 'Patrick Star', 'Squidward Tentacles', 'Sandy Cheeks'],
        'raw_phrase': 'Squidward hates living next to Spongebob.',
        'corrected_phrase': 'Squidward hates living next to Spongebob.'
    },
    {
        'names': ['Tommy Pickles', 'Chuckie Finster', 'Phil DeVille', 'Lil DeVille', 'Angelica Pickles'],
        'raw_phrase': 'Chucky is afraid of everything.',
        'corrected_phrase': 'Chuckie is afraid of everything.'
    },
    {
        'names': ['Arnold Shortman', 'Helga Pataki', 'Gerald Johanssen'],
        'raw_phrase': 'Gerald and Helgah are in the same class.',
        'corrected_phrase': 'Gerald and Helga are in the same class.'
    },
    {
        'names': ['Alice Wang', 'Bob Smith'],
        'raw_phrase': 'The project deadline has been extended.',
        'corrected_phrase': 'The project deadline has been extended.'
    },
    {
        'names': ['Jon Doe', 'Jane Smith'],
        'raw_phrase': 'Please update the spreadsheet by EOD.',
        'corrected_phrase': 'Please update the spreadsheet by EOD.'
    },
    {
        'names': ['Marc Jacobs', 'Louis Vuitton'],
        'raw_phrase': 'Fashion week starts in September.',
        'corrected_phrase': 'Fashion week starts in September.'
    },
    {
        'names': ['Caitlin Snow', 'Barry Allen'],
        'raw_phrase': 'Running unit tests before the merge.',
        'corrected_phrase': 'Running unit tests before the merge.'
    },
    {
        'names': ['Geoff Bezos', 'Elon Musk'],
        'raw_phrase': 'Space exploration is expensive.',
        'corrected_phrase': 'Space exploration is expensive.'
    },
    {
        'names': ['Kristina Pimenova', 'Anastasia Bezrukova'],
        'raw_phrase': 'Photography requires good lighting.',
        'corrected_phrase': 'Photography requires good lighting.'
    },
    {
        'names': ['Steven Spielberg', 'George Lucas'],
        'raw_phrase': 'Visual effects have come a long way.',
        'corrected_phrase': 'Visual effects have come a long way.'
    },
    {
        'names': ['Elisabeth Moss', 'June Osborne'],
        'raw_phrase': 'Dystopian novels are very popular.',
        'corrected_phrase': 'Dystopian novels are very popular.'
    },
    {
        'names': ['Rachael Ray', 'Gordon Ramsay'],
        'raw_phrase': 'Cooking competitions are intense.',
        'corrected_phrase': 'Cooking competitions are intense.'
    },
    {
        'names': ['Bryan Cranston', 'Aaron Paul'],
        'raw_phrase': 'Chemistry is a fascinating subject.',
        'corrected_phrase': 'Chemistry is a fascinating subject.'
    },
    {
        'names': ['Cate Blanchett', 'Rooney Mara'],
        'raw_phrase': 'Rooney is reading the script.',
        'corrected_phrase': 'Rooney is reading the script.'
    },
    {
        'names': ['Micheal Keaton', 'Jack Nicholson'],
        'raw_phrase': 'Jack is a legendary actor.',
        'corrected_phrase': 'Jack is a legendary actor.'
    },
    {
        'names': ['Jaimie Alexander', 'Chris Hemsworth'],
        'raw_phrase': 'Chris is training for the role.',
        'corrected_phrase': 'Chris is training for the role.'
    },
    {
        'names': ['Mathew Perry', 'Courteney Cox'],
        'raw_phrase': 'Courteney invited us to dinner.',
        'corrected_phrase': 'Courteney invited us to dinner.'
    },
    {
        'names': ['Erik Magneto', 'Charles Xavier'],
        'raw_phrase': 'Charles is founding a school.',
        'corrected_phrase': 'Charles is founding a school.'
    },
    {
        'names': ['Sofia Vergara', 'Julie Bowen'],
        'raw_phrase': 'Julie won an Emmy.',
        'corrected_phrase': 'Julie won an Emmy.'
    },
    {
        'names': ['Lynda Carter', 'Gal Gadot'],
        'raw_phrase': 'Gal is filming the sequel.',
        'corrected_phrase': 'Gal is filming the sequel.'
    },
    {
        'names': ['Gerry Lane', 'Brad Pitt'],
        'raw_phrase': 'Brad produced the film.',
        'corrected_phrase': 'Brad produced the film.'
    },
    {
        'names': ['Dianne Wiest', 'Edward Scissorhands'],
        'raw_phrase': 'Edward has scissor hands.',
        'corrected_phrase': 'Edward has scissor hands.'
    },
    {
        'names': ['Teresa Lisbon', 'Patrick Jane'],
        'raw_phrase': 'Patrick solved the mystery.',
        'corrected_phrase': 'Patrick solved the mystery.'
    },
    {
        'names': ['Bharath Ram', 'Sanjay Gupta'],
        'raw_phrase': 'Sanjay is looking into the logs.',
        'corrected_phrase': 'Sanjay is looking into the logs.'
    },
    {
        'names': ['Silvio Dante', 'Tony Soprano'],
        'raw_phrase': 'Silvio is handling the money.',
        'corrected_phrase': 'Silvio is handling the money.'
    },
    {
        'names': ['Alexey Navalny', 'Vladimir Putin'],
        'raw_phrase': 'Alexey is a political activist.',
        'corrected_phrase': 'Alexey is a political activist.'
    },
    {
        'names': ['Kah Mun Wong', 'Wei Ling'],
        'raw_phrase': 'Wei Ling is updating the UI.',
        'corrected_phrase': 'Wei Ling is updating the UI.'
    },
    {
        'names': ['Krystle Carrington', 'Blake Carrington'],
        'raw_phrase': 'Blake is buying a new oil rig.',
        'corrected_phrase': 'Blake is buying a new oil rig.'
    },
    {
        'names': ['Jhonny Depp', 'Amber Heard'],
        'raw_phrase': 'Amber testified yesterday.',
        'corrected_phrase': 'Amber testified yesterday.'
    },
    {
        'names': ['Aleksander Ceferin'],
        'raw_phrase': 'Aleksander gave a press conference.',
        'corrected_phrase': 'Aleksander gave a press conference.'
    },
    {
        'names': ['Jayne Cobb', 'Malcolm Reynolds'],
        'raw_phrase': 'Malcolm is the captain.',
        'corrected_phrase': 'Malcolm is the captain.'
    },
    {
        'names': ['Antony Starr', 'Erin Moriarty'],
        'raw_phrase': 'Erin plays Starlight.',
        'corrected_phrase': 'Erin plays Starlight.'
    },
    {
        'names': ['Suzan-Lori Parks'],
        'raw_phrase': 'Suzan-Lori wrote a new play.',
        'corrected_phrase': 'Suzan-Lori wrote a new play.'
    },
    # MORE ORDINARY NAMES
    {
        'names': ['Gerry Jones', 'Jon Garcia', 'Erik Davis'],
        'raw_phrase': 'Hey Jerry, have you seen John or Eric today?',
        'corrected_phrase': 'Hey Gerry, have you seen Jon or Erik today?'
    },
    {
        'names': ['Caitlin Johnson', 'Stephen Jones', 'Aleksander Brown'],
        'raw_phrase': 'I think Katelyn and Steven are already in the meeting.',
        'corrected_phrase': 'I think Caitlin and Stephen are already in the meeting.'
    },
    {
        'names': ['Jon Miller', 'Geoffrey Martinez', 'Michaela Jones'],
        'raw_phrase': 'I think John and Jeffrey are already in the meeting.',
        'corrected_phrase': 'I think Jon and Geoffrey are already in the meeting.'
    },
    {
        'names': ['Jon Martinez', 'Bryan Miller', 'Aimee Miller'],
        'raw_phrase': 'Could you ask Brian to send the file to Amy?',
        'corrected_phrase': 'Could you ask Bryan to send the file to Aimee?'
    },
    {
        'names': ['Aimee Rodriguez', 'Lynda Smith', 'Lynda Garcia'],
        'raw_phrase': 'Hey Amy, have you seen Linda or Linda today?',
        'corrected_phrase': 'Hey Aimee, have you seen Lynda or Lynda today?'
    },
    {
        'names': ['Nikolas Rodriguez', 'Teresa Miller', 'Marc Miller'],
        'raw_phrase': 'Could you ask Theresa to send the file to Mark?',
        'corrected_phrase': 'Could you ask Teresa to send the file to Marc?'
    },
    {
        'names': ['Marc Davis', 'Sara Miller', 'Suzan Rodriguez'],
        'raw_phrase': 'Could you ask Sarah to send the file to Susan?',
        'corrected_phrase': 'Could you ask Sara to send the file to Suzan?'
    },
    {
        'names': ['Sara Garcia', 'Lynda Brown', 'Stephen Jones'],
        'raw_phrase': 'I think Sarah and Linda are already in the meeting.',
        'corrected_phrase': 'I think Sara and Lynda are already in the meeting.'
    },
    {
        'names': ['Dianne Davis', 'Aleksander Brown', 'Caitlin Martinez'],
        'raw_phrase': 'Hey Diane, have you seen Alexander or Katelyn today?',
        'corrected_phrase': 'Hey Dianne, have you seen Aleksander or Caitlin today?'
    },
    {
        'names': ['Kristina Rodriguez', 'Kristina Jones', 'Marc Brown'],
        'raw_phrase': 'I think Christina and Christina are already in the meeting.',
        'corrected_phrase': 'I think Kristina and Kristina are already in the meeting.'
    },
    {
        'names': ['Gerry Brown', 'Lukas Garcia', 'Aimee Jones'],
        'raw_phrase': 'Hey Jerry, have you seen Lucas or Amy today?',
        'corrected_phrase': 'Hey Gerry, have you seen Lukas or Aimee today?'
    },
    {
        'names': ['Stephen Johnson', 'Nikolas Williams', 'Michaela Smith'],
        'raw_phrase': 'Could you ask Nicholas to send the file to Makayla?',
        'corrected_phrase': 'Could you ask Nikolas to send the file to Michaela?'
    },
    {
        'names': ['Nikolas Jones', 'Mathew Johnson', 'Geoffrey Johnson'],
        'raw_phrase': 'I think Nicholas and Matthew are already in the meeting.',
        'corrected_phrase': 'I think Nikolas and Mathew are already in the meeting.'
    },
    {
        'names': ['Katherine Miller', 'Dianne Miller', 'Nikolas Martinez'],
        'raw_phrase': 'I think Catherine and Diane are already in the meeting.',
        'corrected_phrase': 'I think Katherine and Dianne are already in the meeting.'
    },
    {
        'names': ['Phillip Martinez', 'Jon Davis', 'Antony Brown'],
        'raw_phrase': 'I think Philip and John are already in the meeting.',
        'corrected_phrase': 'I think Phillip and Jon are already in the meeting.'
    },
    {
        'names': ['Aleksander Williams', 'Caryn Miller', 'Sofia Martinez'],
        'raw_phrase': 'Hey Alexander, have you seen Karen or Sophia today?',
        'corrected_phrase': 'Hey Aleksander, have you seen Caryn or Sofia today?'
    },
    {
        'names': ['Caitlin Miller', 'Bryan Garcia', 'Aleksander Garcia'],
        'raw_phrase': 'Hey Katelyn, have you seen Brian or Alexander today?',
        'corrected_phrase': 'Hey Caitlin, have you seen Bryan or Aleksander today?'
    },
    {
        'names': ['Bryan Martinez', 'Antony Smith', 'Kristina Rodriguez'],
        'raw_phrase': 'Hey Brian, have you seen Anthony or Christina today?',
        'corrected_phrase': 'Hey Bryan, have you seen Antony or Kristina today?'
    },
    {
        'names': ['Bryan Johnson', 'Aimee Brown', 'Aleksander Johnson'],
        'raw_phrase': 'Hey Brian, have you seen Amy or Alexander today?',
        'corrected_phrase': 'Hey Bryan, have you seen Aimee or Aleksander today?'
    },
    {
        'names': ['Aimee Jones', 'Antony Rodriguez', 'Kristina Garcia'],
        'raw_phrase': 'Could you ask Anthony to send the file to Christina?',
        'corrected_phrase': 'Could you ask Antony to send the file to Kristina?'
    },
    {
        'names': ['Caryn Martinez', 'Stephen Brown', 'Michaela Rodriguez'],
        'raw_phrase': 'I think Karen and Steven are already in the meeting.',
        'corrected_phrase': 'I think Caryn and Stephen are already in the meeting.'
    },
    {
        'names': ['Lukas Martinez', 'Lukas Smith', 'Phillip Martinez'],
        'raw_phrase': 'I think Lucas and Lucas are already in the meeting.',
        'corrected_phrase': 'I think Lukas and Lukas are already in the meeting.'
    },
    {
        'names': ['Sofia Martinez', 'Isabel Smith', 'Lynda Martinez'],
        'raw_phrase': 'I think Sophia and Isobel are already in the meeting.',
        'corrected_phrase': 'I think Sofia and Isabel are already in the meeting.'
    },
    {
        'names': ['Aleksander Brown', 'Aimee Rodriguez', 'Elisabeth Garcia'],
        'raw_phrase': 'I think Alexander and Amy are already in the meeting.',
        'corrected_phrase': 'I think Aleksander and Aimee are already in the meeting.'
    },
    {
        'names': ['Antony Davis', 'Stephen Brown', 'Elisabeth Jones'],
        'raw_phrase': 'Hey Anthony, have you seen Steven or Elizabeth today?',
        'corrected_phrase': 'Hey Antony, have you seen Stephen or Elisabeth today?'
    },
    {
        'names': ['Suzan Jones', 'Lynda Smith', 'Dianne Williams'],
        'raw_phrase': 'I think Susan and Linda are already in the meeting.',
        'corrected_phrase': 'I think Suzan and Lynda are already in the meeting.'
    },
    {
        'names': ['Jon Jones', 'Dianne Garcia', 'Antony Williams'],
        'raw_phrase': 'Hey John, have you seen Diane or Anthony today?',
        'corrected_phrase': 'Hey Jon, have you seen Dianne or Antony today?'
    },
    {
        'names': ['Gerry Rodriguez', 'Nikolas Johnson', 'Elisabeth Johnson'],
        'raw_phrase': 'I think Jerry and Nicholas are already in the meeting.',
        'corrected_phrase': 'I think Gerry and Nikolas are already in the meeting.'
    },
    {
        'names': ['Marc Johnson', 'Aleksander Brown', 'Marc Brown'],
        'raw_phrase': 'Hey Mark, have you seen Alexander or Mark today?',
        'corrected_phrase': 'Hey Marc, have you seen Aleksander or Marc today?'
    },
    {
        'names': ['Caitlin Martinez', 'Marc Williams', 'Lynda Miller'],
        'raw_phrase': 'I think Katelyn and Mark are already in the meeting.',
        'corrected_phrase': 'I think Caitlin and Marc are already in the meeting.'
    },
    {
        'names': ['Caryn Brown', 'Marc Rodriguez', 'Bryan Garcia'],
        'raw_phrase': 'Could you ask Mark to send the file to Brian?',
        'corrected_phrase': 'Could you ask Marc to send the file to Bryan?'
    },
    {
        'names': ['Rachael Williams', 'Elisabeth Johnson', 'Isabel Miller'],
        'raw_phrase': 'Hey Rachel, have you seen Elizabeth or Isobel today?',
        'corrected_phrase': 'Hey Rachael, have you seen Elisabeth or Isabel today?'
    },
    {
        'names': ['Stephen Miller', 'Lukas Mirror'],
        'raw_phrase': 'Hey Steven, have you seen Lucas today?',
        'corrected_phrase': 'Hey Stephen, have you seen Lukas today?'
    },
    {
        'names': ['Katherine Smith', 'Michaela Jones', 'Michaela Williams'],
        'raw_phrase': 'I think Catherine and Makayla are already in the meeting.',
        'corrected_phrase': 'I think Katherine and Michaela are already in the meeting.'
    },
    {
        'names': ['Bryan Garcia', 'Nikolas Miller', 'Lukas Martinez'],
        'raw_phrase': 'I think Brian and Nicholas are already in the meeting.',
        'corrected_phrase': 'I think Bryan and Nikolas are already in the meeting.'
    },
    {
        'names': ['Katherine Davis', 'Antony Garcia', 'Caitlin Davis'],
        'raw_phrase': 'I think Catherine and Anthony are already in the meeting.',
        'corrected_phrase': 'I think Katherine and Antony are already in the meeting.'
    },
    {
        'names': ['Jon Garcia', 'Kristina Garcia', 'Lynda Rodriguez'],
        'raw_phrase': 'Hey John, have you seen Christina or Linda today?',
        'corrected_phrase': 'Hey Jon, have you seen Kristina or Lynda today?'
    },
    {
        'names': ['Jon Davis', 'Jon Williams', 'Elisabeth Smith'],
        'raw_phrase': 'Could you ask John to send the file to Elizabeth?',
        'corrected_phrase': 'Could you ask Jon to send the file to Elisabeth?'
    },
    {
        'names': ['Katherine Johnson', 'Dianne Brown', 'Phillip Rodriguez'],
        'raw_phrase': 'I think Catherine and Diane are already in the meeting.',
        'corrected_phrase': 'I think Katherine and Dianne are already in the meeting.'
    },
    {
        'names': ['Sara Smith', 'Sara Martinez', 'Geoffrey Garcia'],
        'raw_phrase': 'I think Sarah and Sarah are already in the meeting.',
        'corrected_phrase': 'I think Sara and Sara are already in the meeting.'
    },
    {
        'names': ['Priya Sharma', 'Anil Kumar', 'Suresh Patel', 'Meena Iyer'],
        'raw_phrase': 'Preeya and Suresh are working on the backend.',
        'corrected_phrase': 'Priya and Suresh are working on the backend.'
    },
    {
        'names': ['Wei Chen', 'Li Wang', 'Jun Zhao', 'Yan Liu'],
        'raw_phrase': 'Lee and June will handle the client presentation.',
        'corrected_phrase': 'Li and Jun will handle the client presentation.'
    },
    {
        'names': ['Mateo Garcia', 'Elena Rodriguez', 'Diego Martinez', 'Lucia Fernandez'],
        'raw_phrase': 'Elana and Deego are joining the sync later.',
        'corrected_phrase': 'Elena and Diego are joining the sync later.'
    },
    {
        'names': ['Hans Schmidt', 'Lukas Weber', 'Petra Mueller', 'Stefan Wagner'],
        'raw_phrase': 'Lucas and Stephan are looking at the logs.',
        'corrected_phrase': 'Lukas and Stefan are looking at the logs.'
    },
    {
        'names': ['Chiara Rossi', 'Giuseppe Bianchi', 'Alessia Romano', 'Luca Ricci'],
        'raw_phrase': 'Kiara and Luka are reviewing the PR.',
        'corrected_phrase': 'Chiara and Luca are reviewing the PR.'
    },
    {
        'names': ['Aarav Singh', 'Ishaan Gupta', 'Vihaan Sharma', 'Ananya Reddy'],
        'raw_phrase': 'Ishan and Vihan discussed the roadmap.',
        'corrected_phrase': 'Ishaan and Vihaan discussed the roadmap.'
    },
    {
        'names': ['Yuki Tanaka', 'Kenji Sato', 'Hana Suzuki', 'Hiroshi Ito'],
        'raw_phrase': 'Ken-jee and Hanna are coordinating the release.',
        'corrected_phrase': 'Kenji and Hana are coordinating the release.'
    },
    {
        'names': ['Fatima Zahra', 'Ahmed Hassan', 'Zainab Ali', 'Omar Khalid'],
        'raw_phrase': 'Zaynab and Amhed finished the documentation.',
        'corrected_phrase': 'Zainab and Ahmed finished the documentation.'
    },
    {
        'names': ['Dmitry Ivanov', 'Olga Petrov', 'Svetlana Kuznetsov', 'Igor Smirnov'],
        'raw_phrase': 'Dimitri and Svetlana are at the onsite.',
        'corrected_phrase': 'Dmitry and Svetlana are at the onsite.'
    },
    {
        'names': ['Clara Dubois', 'Julien Martin', 'Amelie Bernard', 'Pierre Thomas'],
        'raw_phrase': 'Amelee and Peere signed off on the design.',
        'corrected_phrase': 'Amelie and Pierre signed off on the design.'
    },
    {
        'names': ['Priya Sharma', 'Anil Kumar', 'Suresh Patel', 'Meena Iyer'],
        'raw_phrase': 'Preeya and Suresh are working on the backend.',
        'corrected_phrase': 'Priya and Suresh are working on the backend.'
    },
    {
        'names': ['Wei Chen', 'Li Wang', 'Jun Zhao', 'Yan Liu'],
        'raw_phrase': 'Lee and June will handle the client presentation.',
        'corrected_phrase': 'Li and Jun will handle the client presentation.'
    },
    {
        'names': ['Mateo Garcia', 'Elena Rodriguez', 'Diego Martinez', 'Lucia Fernandez'],
        'raw_phrase': 'Elana and Deego are joining the sync later.',
        'corrected_phrase': 'Elena and Diego are joining the sync later.'
    },
    {
        'names': ['Hans Schmidt', 'Lukas Weber', 'Petra Mueller', 'Stefan Wagner'],
        'raw_phrase': 'Lucas and Stephan are looking at the logs.',
        'corrected_phrase': 'Lukas and Stefan are looking at the logs.'
    },
    {
        'names': ['Chiara Rossi', 'Giuseppe Bianchi', 'Alessia Romano', 'Luca Ricci'],
        'raw_phrase': 'Kiara and Luka are reviewing the PR.',
        'corrected_phrase': 'Chiara and Luca are reviewing the PR.'
    },
    {
        'names': ['Aarav Singh', 'Ishaan Gupta', 'Vihaan Sharma', 'Ananya Reddy'],
        'raw_phrase': 'Ishan and Vihan discussed the roadmap.',
        'corrected_phrase': 'Ishaan and Vihaan discussed the roadmap.'
    },
    {
        'names': ['Yuki Tanaka', 'Kenji Sato', 'Hana Suzuki', 'Hiroshi Ito'],
        'raw_phrase': 'Ken-jee and Hanna are coordinating the release.',
        'corrected_phrase': 'Kenji and Hana are coordinating the release.'
    },
    {
        'names': ['Fatima Zahra', 'Ahmed Hassan', 'Zainab Ali', 'Omar Khalid'],
        'raw_phrase': 'Zaynab and Amhed finished the documentation.',
        'corrected_phrase': 'Zainab and Ahmed finished the documentation.'
    },
    {
        'names': ['Dmitry Ivanov', 'Olga Petrov', 'Svetlana Kuznetsov', 'Igor Smirnov'],
        'raw_phrase': 'Dimitri and Svetlana are at the onsite.',
        'corrected_phrase': 'Dmitry and Svetlana are at the onsite.'
    },
    {
        'names': ['Clara Dubois', 'Julien Martin', 'Amelie Bernard', 'Pierre Thomas'],
        'raw_phrase': 'Amelee and Peere signed off on the design.',
        'corrected_phrase': 'Amelie and Pierre signed off on the design.'
    },
    {
        'names': ['Gerry Garcia', 'Aleksander Martinez'],
        'raw_phrase': "Let's grab lunch at 12:30.",
        'corrected_phrase': "Let's grab lunch at 12:30."
    },
    {
        'names': ['Katherine Garcia', 'Sara Smith'],
        'raw_phrase': 'Thanks for the update, Katherine.',
        'corrected_phrase': 'Thanks for the update, Katherine.'
    },
    {
        'names': ['Erik Smith', 'Aimee Martinez'],
        'raw_phrase': 'We need to order more office supplies.',
        'corrected_phrase': 'We need to order more office supplies.'
    },
    {
        'names': ['Jaimie Jones', 'Suzan Jones'],
        'raw_phrase': 'Thanks for the update, Jaimie.',
        'corrected_phrase': 'Thanks for the update, Jaimie.'
    },
    {
        'names': ['Lynda Williams', 'Nikolas Davis'],
        'raw_phrase': 'Thanks for the update, Lynda.',
        'corrected_phrase': 'Thanks for the update, Lynda.'
    },
    {
        'names': ['Antony Miller', 'Caryn Johnson'],
        'raw_phrase': 'Has anyone seen the spare monitor?',
        'corrected_phrase': 'Has anyone seen the spare monitor?'
    },
    {
        'names': ['Gerry Johnson', 'Isabel Brown'],
        'raw_phrase': 'We need to order more office supplies.',
        'corrected_phrase': 'We need to order more office supplies.'
    },
    {
        'names': ['Aimee Garcia', 'Caitlin Jones'],
        'raw_phrase': 'We need to order more office supplies.',
        'corrected_phrase': 'We need to order more office supplies.'
    },
    {
        'names': ['Rachael Johnson', 'Lukas Brown'],
        'raw_phrase': 'The Wi-Fi is acting up again.',
        'corrected_phrase': 'The Wi-Fi is acting up again.'
    },
    {
        'names': ['Sofia Brown', 'Caryn Brown'],
        'raw_phrase': 'Thanks for the update, Sofia.',
        'corrected_phrase': 'Thanks for the update, Sofia.'
    },
    {
        'names': ['Bryan Johnson', 'Isabel Smith'],
        'raw_phrase': 'The Wi-Fi is acting up again.',
        'corrected_phrase': 'The Wi-Fi is acting up again.'
    },
    {
        'names': ['Rachael Jones', 'Caitlin Brown'],
        'raw_phrase': 'Has anyone seen the spare monitor?',
        'corrected_phrase': 'Has anyone seen the spare monitor?'
    },
    {
        'names': ['Mathew Davis', 'Sofia Smith'],
        'raw_phrase': "Let's grab lunch at 12:30.",
        'corrected_phrase': "Let's grab lunch at 12:30."
    },
    {
        'names': ['Marc Brown', 'Dianne Miller'],
        'raw_phrase': 'Thanks for the update, Marc.',
        'corrected_phrase': 'Thanks for the update, Marc.'
    },
    {
        'names': ['Nikolas Martinez', 'Katherine Davis'],
        'raw_phrase': 'We need to order more office supplies.',
        'corrected_phrase': 'We need to order more office supplies.'
    },
    {
        'names': ['Rachael Smith', 'Dianne Brown'],
        'raw_phrase': 'Thanks for the update, Rachael.',
        'corrected_phrase': 'Thanks for the update, Rachael.'
    },
    {
        'names': ['Sofia Martinez', 'Gerry Jones'],
        'raw_phrase': 'The Wi-Fi is acting up again.',
        'corrected_phrase': 'The Wi-Fi is acting up again.'
    },
    {
        'names': ['Dianne Williams', 'Suzan Johnson'],
        'raw_phrase': "Let's grab lunch at 12:30.",
        'corrected_phrase': "Let's grab lunch at 12:30."
    },
    {
        'names': ['Jon Brown', 'Elisabeth Smith'],
        'raw_phrase': 'Thanks for the update, Jon.',
        'corrected_phrase': 'Thanks for the update, Jon.'
    },
    {
        'names': ['Katherine Rodriguez', 'Kristina Davis'],
        'raw_phrase': "Let's grab lunch at 12:30.",
        'corrected_phrase': "Let's grab lunch at 12:30."
    },
    {
        'names': ['Mathew Garcia', 'Bryan Jones'],
        'raw_phrase': 'The office will be closed on Monday.',
        'corrected_phrase': 'The office will be closed on Monday.'
    },
    {
        'names': ['Sofia Williams', 'Gerry Brown'],
        'raw_phrase': 'Thanks for the update, Sofia.',
        'corrected_phrase': 'Thanks for the update, Sofia.'
    },
    {
        'names': ['Mathew Johnson', 'Gerry Davis'],
        'raw_phrase': 'Thanks for the update, Mathew.',
        'corrected_phrase': 'Thanks for the update, Mathew.'
    },
    {
        'names': ['Marc Smith', 'Marc Davis'],
        'raw_phrase': 'We need to order more office supplies.',
        'corrected_phrase': 'We need to order more office supplies.'
    },
    {
        'names': ['Zack Martinez', 'Nikolas Martinez'],
        'raw_phrase': 'Thanks for the update, Zack.',
        'corrected_phrase': 'Thanks for the update, Zack.'
    },
    {
        'names': ['Rachael Johnson', 'Bryan Smith'],
        'raw_phrase': "Let's grab lunch at 12:30.",
        'corrected_phrase': "Let's grab lunch at 12:30."
    },
    {
        'names': ['Elisabeth Davis', 'Aleksander Johnson'],
        'raw_phrase': 'Has anyone seen the spare monitor?',
        'corrected_phrase': 'Has anyone seen the spare monitor?'
    },
    {
        'names': ['Caitlin Davis', 'Geoffrey Williams'],
        'raw_phrase': 'The Wi-Fi is acting up again.',
        'corrected_phrase': 'The Wi-Fi is acting up again.'
    },
    {
        'names': ['Katherine Smith', 'Caryn Williams'],
        'raw_phrase': 'Thanks for the update, Katherine.',
        'corrected_phrase': 'Thanks for the update, Katherine.'
    },
    {
        'names': ['Sara Davis', 'Geoffrey Miller'],
        'raw_phrase': 'Thanks for the update, Sara.',
        'corrected_phrase': 'Thanks for the update, Sara.'
    },
    # POSSESSIVES, TITLES, AND CORPORATE NAMES
    {
        'names': ['Marc Jacobs', 'Louis Vuitton'],
        'raw_phrase': "Mark's laptop is always overheating.",
        'corrected_phrase': "Marc's laptop is always overheating."
    },
    {
        'names': ['Geoff Bezos', 'Elon Musk'],
        'raw_phrase': "Jeff'll be joining the call in five minutes.",
        'corrected_phrase': "Geoff'll be joining the call in five minutes."
    },
    {
        'names': ['Sara Connor', 'Kyle Reese'],
        'raw_phrase': "Is this Sarah's desk or Kyle's?",
        'corrected_phrase': "Is this Sara's desk or Kyle's?"
    },
    {
        'names': ['Bryan Cranston', 'Aaron Paul'],
        'raw_phrase': "Brian's cooking some lunch in the breakroom.",
        'corrected_phrase': "Bryan's cooking some lunch in the breakroom."
    },
    {
        'names': ['Caitlin Snow', 'Barry Allen'],
        'raw_phrase': "Katelyn'll handle the deployment tonight.",
        'corrected_phrase': "Caitlin'll handle the deployment tonight."
    },
    {
        'names': ['Elisabeth Moss', 'June Osborne'],
        'raw_phrase': "Elizabeth's feedback was actually quite helpful.",
        'corrected_phrase': "Elisabeth's feedback was actually quite helpful."
    },
    {
        'names': ['Rachael Ray', 'Gordon Ramsay'],
        'raw_phrase': "Rachel'll be the lead on the new project.",
        'corrected_phrase': "Rachael'll be the lead on the new project."
    },
    {
        'names': ['Mathew Perry', 'Courteney Cox'],
        'raw_phrase': "Matthew's joke went over everyone's head.",
        'corrected_phrase': "Mathew's joke went over everyone's head."
    },
    {
        'names': ['Sofia Vergara', 'Julie Bowen'],
        'raw_phrase': "Sophia's presentation is scheduled for Tuesday.",
        'corrected_phrase': "Sofia's presentation is scheduled for Tuesday."
    },
    {
        'names': ['Jon Doe', 'Jane Smith'],
        'raw_phrase': "John'll be out of the office next week.",
        'corrected_phrase': "Jon'll be out of the office next week."
    },
    {
        'names': ['Stephen Spielberg', 'George Lucas'],
        'raw_phrase': "Steven'll direct the opening sequence.",
        'corrected_phrase': "Stephen'll direct the opening sequence."
    },
    {
        'names': ['Katherine Smith', 'Philip Brown'],
        'raw_phrase': "Catherine's report is still missing some data.",
        'corrected_phrase': "Katherine's report is still missing some data."
    },
    {
        'names': ['Zack Martinez', 'Zachary Taylor'],
        'raw_phrase': "Zach'll take care of the server migration.",
        'corrected_phrase': "Zack'll take care of the server migration."
    },
    {
        'names': ['Aimee Rodriguez', 'Amy Johnson'],
        'raw_phrase': "Amy's PR has already been merged.",
        'corrected_phrase': "Aimee's PR has already been merged."
    },
    {
        'names': ['Nikolas Jones', 'Nicholas Cage'],
        'raw_phrase': "Nicholas'll be the one to present the results.",
        'corrected_phrase': "Nikolas'll be the one to present the results."
    },
    {
        'names': ['Prof. Zhang', 'Dr. Li'],
        'raw_phrase': 'Professor Zhang is teaching the machine learning course.',
        'corrected_phrase': 'Prof. Zhang is teaching the machine learning course.'
    },
    {
        'names': ['Mister Rogers', 'Ms. Smith'],
        'raw_phrase': 'Mr. Rogers invited us to the neighborhood meeting.',
        'corrected_phrase': 'Mister Rogers invited us to the neighborhood meeting.'
    },
    {
        'names': ['Dr. Fischer', 'Prof. Miller'],
        'raw_phrase': "Doctor Fischer'll be performing the surgery.",
        'corrected_phrase': "Dr. Fischer'll be performing the surgery."
    },
    {
        'names': ['Ms. Davis', 'Mister Johnson'],
        'raw_phrase': 'Miss Davis is the new department head.',
        'corrected_phrase': 'Ms. Davis is the new department head.'
    },
    {
        'names': ['Prof. Thompson', 'Dr. Watson'],
        'raw_phrase': "Professor Thompson's research is groundbreaking.",
        'corrected_phrase': "Prof. Thompson's research is groundbreaking."
    },
    {
        'names': ['Mister Anderson', 'Ms. Parker'],
        'raw_phrase': "Mr. Anderson'll see you now.",
        'corrected_phrase': "Mister Anderson'll see you now."
    },
    {
        'names': ['Dr. Gregory House', 'Dr. James Wilson'],
        'raw_phrase': "Doctor House's methods are quite unconventional.",
        'corrected_phrase': "Dr. Gregory House's methods are quite unconventional."
    },
    {
        'names': ['Ms. Marvel', 'Captain America'],
        'raw_phrase': "Miss Marvel'll be at the convention this year.",
        'corrected_phrase': "Ms. Marvel'll be at the convention this year."
    },
    {
        'names': ['Prof. X', 'Magneto'],
        'raw_phrase': "Professor X'll be leading the school for gifted youngsters.",
        'corrected_phrase': "Prof. X'll be leading the school for gifted youngsters."
    },
    {
        'names': ['Dr. Strange', 'Wong'],
        'raw_phrase': "Doctor Strange's cape has a mind of its own.",
        'corrected_phrase': "Dr. Strange's cape has a mind of its own."
    },
    {
        'names': ['Ms. Pac-Man', 'Mister Game & Watch'],
        'raw_phrase': 'Miss Pacman is a classic arcade character.',
        'corrected_phrase': 'Ms. Pac-Man is a classic arcade character.'
    },
    {
        'names': ['Prof. Dumbledore', 'Prof. McGonagall'],
        'raw_phrase': "Professor Dumbledore's office is hidden behind a statue.",
        'corrected_phrase': "Prof. Dumbledore's office is hidden behind a statue."
    },
    {
        'names': ['Dr. Evil', 'Mini-Me'],
        'raw_phrase': "Doctor Evil's plan is to hold the world ransom.",
        'corrected_phrase': "Dr. Evil's plan is to hold the world ransom."
    },
    {
        'names': ['Ms. Frizzle', 'The Magic School Bus'],
        'raw_phrase': "Miss Frizzle'll take the class on a trip inside a volcano.",
        'corrected_phrase': "Ms. Frizzle'll take the class on a trip inside a volcano."
    },
    {
        'names': ['Prof. Oak', 'Ash Ketchum'],
        'raw_phrase': "Professor Oak'll give you your first Pokemon.",
        'corrected_phrase': "Prof. Oak'll give you your first Pokemon."
    },
    {
        'names': ['PagerDuty', 'Opsgenie'],
        'raw_phrase': 'The pager duty alert woke me up at 3 AM.',
        'corrected_phrase': 'The PagerDuty alert woke me up at 3 AM.'
    },
    {
        'names': ['Giphy', 'Slack'],
        'raw_phrase': 'Send a gifty to celebrate the launch.',
        'corrected_phrase': 'Send a Giphy to celebrate the launch.'
    },
    {
        'names': ['Salesforce', 'HubSpot'],
        'raw_phrase': 'Check the sales force dashboard for the latest leads.',
        'corrected_phrase': 'Check the Salesforce dashboard for the latest leads.'
    },
    {
        'names': ['Datadog', 'New Relic'],
        'raw_phrase': 'Data dog is showing a spike in latency.',
        'corrected_phrase': 'Datadog is showing a spike in latency.'
    },
    {
        'names': ['Kubernetes', 'Docker'],
        'raw_phrase': 'The coobernetes cluster needs a restart.',
        'corrected_phrase': 'The Kubernetes cluster needs a restart.'
    },
    {
        'names': ['Grafana', 'Prometheus'],
        'raw_phrase': 'I updated the griffana dashboard with new metrics.',
        'corrected_phrase': 'Grafana updated the dashboard with new metrics.'
    },
    {
        'names': ['Snowflake', 'BigQuery'],
        'raw_phrase': 'The snow flake query is taking too long to run.',
        'corrected_phrase': 'The Snowflake query is taking too long to run.'
    },
    {
        'names': ['GitHub', 'GitLab'],
        'raw_phrase': 'I pushed the changes to git hub this morning.',
        'corrected_phrase': 'I pushed the changes to GitHub this morning.'
    },
    {
        'names': ['Bitbucket', 'Jira'],
        'raw_phrase': 'Check the bit bucket repository for the source code.',
        'corrected_phrase': 'Bitbucket repository has the source code.'
    },
    {
        'names': ['Sentry', 'LogRocket'],
        'raw_phrase': 'Century caught a new exception in the frontend.',
        'corrected_phrase': 'Sentry caught a new exception in the frontend.'
    },
    {
        'names': ['Postman', 'Insomnia'],
        'raw_phrase': "I'm testing the API using post man.",
        'corrected_phrase': "I'm testing the API using Postman."
    },
    {
        'names': ['Splunk', 'Sumo Logic'],
        'raw_phrase': 'Search the splunck logs for the error message.',
        'corrected_phrase': 'Search the Splunk logs for the error message.'
    },
    {
        'names': ['Confluence', 'Notion'],
        'raw_phrase': 'The documentation is on the confluents page.',
        'corrected_phrase': 'The Confluence page has the documentation.'
    },
    {
        'names': ['Tableau', 'Looker'],
        'raw_phrase': 'The tablow report shows a decrease in churn.',
        'corrected_phrase': 'The Tableau report shows a decrease in churn.'
    },
    {
        'names': ['Cloudflare', 'Akamai'],
        'raw_phrase': 'Cloud flare is blocking some legitimate traffic.',
        'corrected_phrase': 'Cloudflare is blocking some legitimate traffic.'
    },
    {
        'names': ['Trello', 'Asana'],
        'raw_phrase': 'Add a new card to the trelow board.',
        'corrected_phrase': 'Add a new card to the Trello board.'
    },
    {
        'names': ['Zoom', 'Microsoft Teams'],
        'raw_phrase': "I'll start the zoom meeting in ten minutes.",
        'corrected_phrase': "I'll start the Zoom meeting in ten minutes."
    },
    {
        'names': ['Dropbox', 'Google Drive'],
        'raw_phrase': 'Upload the file to drop box and share the link.',
        'corrected_phrase': 'Upload the file to Dropbox and share the link.'
    },
    {
        'names': ['Intercom', 'Zendesk'],
        'raw_phrase': 'The inter-com chat is very busy today.',
        'corrected_phrase': 'The Intercom chat is very today.'
    },
    {
        'names': ['CircleCI', 'Jenkins'],
        'raw_phrase': 'The circle c-i build failed due to a timeout.',
        'corrected_phrase': 'The CircleCI build failed due to a timeout.'
    },

    # HIGH-QUALITY DIVERSE NAMES & COMPLEX GRAMMAR
    {
        'names': ['Beatrix Moore', 'Kieran Wilson', 'Aarav Moore', 'Priya Johnson', 'Siobhan Taylor'],
        'raw_phrase': "I'll ask Beatrice to double check the spreadsheet.",
        'corrected_phrase': "I'll ask Beatrix to double check the spreadsheet."
    },
    {
        'names': ['Elliott Anderson', 'Thuy Rodriguez', 'Qasim Hernandez', 'Zahra Davis'],
        'raw_phrase': "Could you see if Kasim's laptop is in the office?",
        'corrected_phrase': "Could you see if Qasim's laptop is in the office?"
    },
    {
        'names': ['Prof. Zhang', 'Dr. Li', 'Professor Miller', 'Mister Anderson'],
        'raw_phrase': "Professor Miller'll be leading the sync today.",
        'corrected_phrase': "Professor Miller'll be leading the sync today."
    },
    {
        'names': ['Ishaan Thomas', 'Vihaan Brown', 'Ananya Jackson', 'Bhavya Lopez'],
        'raw_phrase': "I think Ishan and Vihan's proposal was the strongest.",
        'corrected_phrase': "I think Ishaan and Vihaan's proposal was the strongest."
    },
    {
        'names': ['Juliet Williams', 'Laurence Thomas', 'Francesca Lopez', 'Oscar Rodriguez'],
        'raw_phrase': "Please send the notes to Juliette, Lawrence, and Francheska.",
        'corrected_phrase': "Please send the notes to Juliet, Laurence, and Francesca."
    },
    {
        'names': ['Nikolas Smith', 'Lukas Brown', 'Gillian Wilson', 'Sara Lopez'],
        'raw_phrase': "Nicholas'll handle the frontend, while Lucas focuses on the API.",
        'corrected_phrase': "Nikolas'll handle the frontend, while Lukas focuses on the API."
    },
    {
        'names': ['PagerDuty', 'Sentry', 'Grafana', 'Datadog'],
        'raw_phrase': "Check the page or duty logs for any century errors.",
        'corrected_phrase': "Check the PagerDuty logs for any Sentry errors."
    },
    {
        'names': ['GitHub', 'CircleCI', 'Kubernetes', 'Docker'],
        'raw_phrase': "The circle c-i build triggered the coobernetes deployment.",
        'corrected_phrase': "The CircleCI build triggered the Kubernetes deployment."
    },
    {
        'names': ['Beatrix Garcia', 'Beatrix Taylor', 'Rachael Gonzalez', 'Siobhan Rodriguez'],
        'raw_phrase': "Sarah and Shavon are working with Beatrice on the roadmap.",
        'corrected_phrase': "Sara and Siobhan are working with Beatrix on the roadmap."
    },
    {
        'names': ['Tomas Thomas', 'Vivian Jackson', 'Juliet Thomas', 'Laurence Thomas'],
        'raw_phrase': "Thomas'll be out, so Vivien is taking his place.",
        'corrected_phrase': "Tomas'll be out, so Vivian is taking his place."
    },
    {
        'names': ['Aarav Singh', 'Ishaan Gupta', 'Vihaan Sharma', 'Ananya Reddy'],
        'raw_phrase': "I spoke with Arav about Ishan's feedback.",
        'corrected_phrase': "I spoke with Aarav about Ishaan's feedback."
    },
    {
        'names': ['Chen Hernandez', 'Mei-ling Wilson', 'Wei Williams', 'Xuan Davis'],
        'raw_phrase': "Way and Meiling will present the results to the team.",
        'corrected_phrase': "Wei and Mei-ling will present the results to the team."
    },
    {
        'names': ['Oksana Martin', 'Damian Moore', 'Yosef Martinez', 'Zahra Davis'],
        'raw_phrase': "Oxana and Joseph'll be at the onsite next week.",
        'corrected_phrase': "Oksana and Yosef'll be at the onsite next week."
    },
    {
        'names': ['Dr. Fischer', 'Prof. Thompson', 'Professor Dumbledore'],
        'raw_phrase': "Doctor Fischer's research was cited by Professor Thompson.",
        'corrected_phrase': "Dr. Fischer's research was cited by Prof. Thompson."
    },
    {
        'names': ['Giphy', 'Slack', 'Zoom', 'Intercom'],
        'raw_phrase': "I'll start the zoom call and post the link in the inter-com chat.",
        'corrected_phrase': "I'll start the Zoom call and post the link in the Intercom chat."
    },
    {
        'names': ['Beatrix Moore', 'Elliott Anderson', 'Thuy Rodriguez', 'Qasim Hernandez'],
        'raw_phrase': "We're using Elliot's approach for the Twee project.",
        'corrected_phrase': "We're using Elliott's approach for the Thuy project."
    },
    {
        'names': ['Siobhan Taylor', 'Kieran Wilson', 'Aimee Johnson', 'Nikolas Smith'],
        'raw_phrase': "Hey Shavon, did you hear about Nicholas'll promotion?",
        'corrected_phrase': "Hey Siobhan, did you hear about Nikolas's promotion?"
    },
    {
        'names': ['Marc Jacobs', 'Louis Vuitton', 'Caryn Johnson', 'Sofia Vergara'],
        'raw_phrase': "Mark'll be at the fashion show with Karen and Sophia.",
        'corrected_phrase': "Marc'll be at the fashion show with Caryn and Sofia."
    },
    {
        'names': ['Bryan Cranston', 'Aaron Paul', 'Rachael Ray', 'Gordon Ramsay'],
        'raw_phrase': "Brian and Rachel'll be cooking for the gala.",
        'corrected_phrase': "Bryan and Rachael'll be cooking for the gala."
    },
    {
        'names': ['Prof. Zhang', 'Dr. Li', 'Professor Miller', 'Mister Anderson'],
        'raw_phrase': "Professor Zhang'll be there, but Mr. Anderson might be late.",
        'corrected_phrase': "Prof. Zhang'll be there, but Mister Anderson might be late."
    },
    {
        'names': ['Ishaan Thomas', 'Vihaan Brown', 'Ananya Jackson', 'Bhavya Lopez'],
        'raw_phrase': "Ishan's laptop is broken, so he's using Vihan's.",
        'corrected_phrase': "Ishaan's laptop is broken, so he's using Vihaan's."
    },
    {
        'names': ['Juliet Williams', 'Laurence Thomas', 'Francesca Lopez', 'Oscar Rodriguez'],
        'raw_phrase': "Juliette'll send the file to Lawrence later today.",
        'corrected_phrase': "Juliet'll send the file to Laurence later today."
    },
    {
        'names': ['Nikolas Smith', 'Lukas Brown', 'Gillian Wilson', 'Sara Lopez'],
        'raw_phrase': "Nicholas and Jillian'll be at the standup.",
        'corrected_phrase': "Nikolas and Gillian'll be at the standup."
    },
    {
        'names': ['Aarav Singh', 'Ishaan Gupta', 'Vihaan Sharma', 'Ananya Reddy'],
        'raw_phrase': "Arav'll sync with Anania tomorrow morning.",
        'corrected_phrase': "Aarav'll sync with Ananya tomorrow morning."
    },
    {
        'names': ['Chen Hernandez', 'Mei-ling Wilson', 'Wei Williams', 'Xuan Davis'],
        'raw_phrase': "Chun's and Way'll handle the documentation.",
        'corrected_phrase': "Chen's and Wei'll handle the documentation."
    },

    # AUTOMATED REGULAR NAME SAMPLES
    {
        "names": [
                "Shawn Thomas"
        ],
        "raw_phrase": "Sean's PR is ready for review.",
        "corrected_phrase": "Shawn's PR is ready for review."
},
    {
        "names": [
                "Shawn Thomas"
        ],
        "raw_phrase": "Sean mentioned the deadline was moved.",
        "corrected_phrase": "Shawn mentioned the deadline was moved."
},
    {
        "names": [
                "Sean Smith"
        ],
        "raw_phrase": "Hey Shawn, can you check the logs?",
        "corrected_phrase": "Hey Sean, can you check the logs?"
},
    {
        "names": [
                "Shawn Martinez"
        ],
        "raw_phrase": "Can you ask Shaun to join the Zoom?",
        "corrected_phrase": "Can you ask Shawn to join the Zoom?"
},
    {
        "names": [
                "Shawn Thomas"
        ],
        "raw_phrase": "Please send the invite to Shaun.",
        "corrected_phrase": "Please send the invite to Shawn."
},
    {
        "names": [
                "Shaun Smith"
        ],
        "raw_phrase": "Hey Shawn, can you check the logs?",
        "corrected_phrase": "Hey Shaun, can you check the logs?"
},
    {
        "names": [
                "Megan Moore"
        ],
        "raw_phrase": "Check with Meagan about the API credentials.",
        "corrected_phrase": "Check with Megan about the API credentials."
},
    {
        "names": [
                "Megan Rodriguez"
        ],
        "raw_phrase": "I think Meagan is handling the project.",
        "corrected_phrase": "I think Megan is handling the project."
},
    {
        "names": [
                "Meagan Taylor"
        ],
        "raw_phrase": "Hey Megan, can you check the logs?",
        "corrected_phrase": "Hey Meagan, can you check the logs?"
},
    {
        "names": [
                "Megan Taylor"
        ],
        "raw_phrase": "Wait for Meghan before starting the meeting.",
        "corrected_phrase": "Wait for Megan before starting the meeting."
},
    {
        "names": [
                "Megan Smith"
        ],
        "raw_phrase": "Is Meghan on the call?",
        "corrected_phrase": "Is Megan on the call?"
},
    {
        "names": [
                "Meghan Smith"
        ],
        "raw_phrase": "Hey Megan, can you check the logs?",
        "corrected_phrase": "Hey Meghan, can you check the logs?"
},
    {
        "names": [
                "Eric Williams"
        ],
        "raw_phrase": "Check with Erik about the API credentials.",
        "corrected_phrase": "Check with Eric about the API credentials."
},
    {
        "names": [
                "Eric Brown"
        ],
        "raw_phrase": "I think Erik is handling the project.",
        "corrected_phrase": "I think Eric is handling the project."
},
    {
        "names": [
                "Erik Jones"
        ],
        "raw_phrase": "Hey Eric, can you check the logs?",
        "corrected_phrase": "Hey Erik, can you check the logs?"
},
    {
        "names": [
                "Sara Martinez"
        ],
        "raw_phrase": "Did Sarah send the report yet?",
        "corrected_phrase": "Did Sara send the report yet?"
},
    {
        "names": [
                "Sara Smith"
        ],
        "raw_phrase": "I'll sync with Sarah later today.",
        "corrected_phrase": "I'll sync with Sara later today."
},
    {
        "names": [
                "Sarah Smith"
        ],
        "raw_phrase": "Hey Sara, can you check the logs?",
        "corrected_phrase": "Hey Sarah, can you check the logs?"
},
    {
        "names": [
                "Geoff Garcia"
        ],
        "raw_phrase": "Jeff mentioned the deadline was moved.",
        "corrected_phrase": "Geoff mentioned the deadline was moved."
},
    {
        "names": [
                "Geoff Miller"
        ],
        "raw_phrase": "Can you ask Jeff to join the Zoom?",
        "corrected_phrase": "Can you ask Geoff to join the Zoom?"
},
    {
        "names": [
                "Jeff Rodriguez"
        ],
        "raw_phrase": "Hey Geoff, can you check the logs?",
        "corrected_phrase": "Hey Jeff, can you check the logs?"
},
    {
        "names": [
                "Marc Taylor"
        ],
        "raw_phrase": "Please send the invite to Mark.",
        "corrected_phrase": "Please send the invite to Marc."
},
    {
        "names": [
                "Marc Miller"
        ],
        "raw_phrase": "Did Mark send the report yet?",
        "corrected_phrase": "Did Marc send the report yet?"
},
    {
        "names": [
                "Mark Davis"
        ],
        "raw_phrase": "Hey Marc, can you check the logs?",
        "corrected_phrase": "Hey Mark, can you check the logs?"
},
    {
        "names": [
                "Jon Jones"
        ],
        "raw_phrase": "Check with John about the API credentials.",
        "corrected_phrase": "Check with Jon about the API credentials."
},
    {
        "names": [
                "Jon Brown"
        ],
        "raw_phrase": "Can you ask John to join the Zoom?",
        "corrected_phrase": "Can you ask Jon to join the Zoom?"
},
    {
        "names": [
                "John Brown"
        ],
        "raw_phrase": "Hey Jon, can you check the logs?",
        "corrected_phrase": "Hey John, can you check the logs?"
},
    {
        "names": [
                "Caitlin Brown"
        ],
        "raw_phrase": "Check with Kaitlyn about the API credentials.",
        "corrected_phrase": "Check with Caitlin about the API credentials."
},
    {
        "names": [
                "Caitlin Rodriguez"
        ],
        "raw_phrase": "Kaitlyn mentioned the deadline was moved.",
        "corrected_phrase": "Caitlin mentioned the deadline was moved."
},
    {
        "names": [
                "Kaitlyn Rodriguez"
        ],
        "raw_phrase": "Hey Caitlin, can you check the logs?",
        "corrected_phrase": "Hey Kaitlyn, can you check the logs?"
},
    {
        "names": [
                "Caitlin Martinez"
        ],
        "raw_phrase": "Katelyn's PR is ready for review.",
        "corrected_phrase": "Caitlin's PR is ready for review."
},
    {
        "names": [
                "Caitlin Miller"
        ],
        "raw_phrase": "Please send the invite to Katelyn.",
        "corrected_phrase": "Please send the invite to Caitlin."
},
    {
        "names": [
                "Katelyn Davis"
        ],
        "raw_phrase": "Hey Caitlin, can you check the logs?",
        "corrected_phrase": "Hey Katelyn, can you check the logs?"
},
    {
        "names": [
                "Caitlin Johnson"
        ],
        "raw_phrase": "Can you ask Katelynn to join the Zoom?",
        "corrected_phrase": "Can you ask Caitlin to join the Zoom?"
},
    {
        "names": [
                "Caitlin Jones"
        ],
        "raw_phrase": "Wait for Katelynn before starting the meeting.",
        "corrected_phrase": "Wait for Caitlin before starting the meeting."
},
    {
        "names": [
                "Katelynn Anderson"
        ],
        "raw_phrase": "Hey Caitlin, can you check the logs?",
        "corrected_phrase": "Hey Katelynn, can you check the logs?"
},
    {
        "names": [
                "Bryan Garcia"
        ],
        "raw_phrase": "I'll sync with Brian later today.",
        "corrected_phrase": "I'll sync with Bryan later today."
},
    {
        "names": [
                "Bryan Jones"
        ],
        "raw_phrase": "Wait for Brian before starting the meeting.",
        "corrected_phrase": "Wait for Bryan before starting the meeting."
},
    {
        "names": [
                "Brian Rodriguez"
        ],
        "raw_phrase": "Hey Bryan, can you check the logs?",
        "corrected_phrase": "Hey Brian, can you check the logs?"
},
    {
        "names": [
                "Stephen Jones"
        ],
        "raw_phrase": "Wait for Steven before starting the meeting.",
        "corrected_phrase": "Wait for Stephen before starting the meeting."
},
    {
        "names": [
                "Stephen Brown"
        ],
        "raw_phrase": "I'll sync with Steven later today.",
        "corrected_phrase": "I'll sync with Stephen later today."
},
    {
        "names": [
                "Steven Johnson"
        ],
        "raw_phrase": "Hey Stephen, can you check the logs?",
        "corrected_phrase": "Hey Steven, can you check the logs?"
},
    {
        "names": [
                "Mathew Anderson"
        ],
        "raw_phrase": "Matthew's PR is ready for review.",
        "corrected_phrase": "Mathew's PR is ready for review."
},
    {
        "names": [
                "Mathew Martinez"
        ],
        "raw_phrase": "I think Matthew is handling the project.",
        "corrected_phrase": "I think Mathew is handling the project."
},
    {
        "names": [
                "Matthew Taylor"
        ],
        "raw_phrase": "Hey Mathew, can you check the logs?",
        "corrected_phrase": "Hey Matthew, can you check the logs?"
},
    {
        "names": [
                "Aimee Davis"
        ],
        "raw_phrase": "I think Amy is handling the project.",
        "corrected_phrase": "I think Aimee is handling the project."
},
    {
        "names": [
                "Aimee Davis"
        ],
        "raw_phrase": "I'll sync with Amy later today.",
        "corrected_phrase": "I'll sync with Aimee later today."
},
    {
        "names": [
                "Amy Thomas"
        ],
        "raw_phrase": "Hey Aimee, can you check the logs?",
        "corrected_phrase": "Hey Amy, can you check the logs?"
},
    {
        "names": [
                "Aimee Martinez"
        ],
        "raw_phrase": "I'll sync with Amie later today.",
        "corrected_phrase": "I'll sync with Aimee later today."
},
    {
        "names": [
                "Aimee Smith"
        ],
        "raw_phrase": "I'll sync with Amie later today.",
        "corrected_phrase": "I'll sync with Aimee later today."
},
    {
        "names": [
                "Amie Brown"
        ],
        "raw_phrase": "Hey Aimee, can you check the logs?",
        "corrected_phrase": "Hey Amie, can you check the logs?"
},
    {
        "names": [
                "Nikolas Brown"
        ],
        "raw_phrase": "Is Nicholas on the call?",
        "corrected_phrase": "Is Nikolas on the call?"
},
    {
        "names": [
                "Nikolas Taylor"
        ],
        "raw_phrase": "Nicholas mentioned the deadline was moved.",
        "corrected_phrase": "Nikolas mentioned the deadline was moved."
},
    {
        "names": [
                "Nicholas Davis"
        ],
        "raw_phrase": "Hey Nikolas, can you check the logs?",
        "corrected_phrase": "Hey Nicholas, can you check the logs?"
},
    {
        "names": [
                "Nikolas Jones"
        ],
        "raw_phrase": "I'll sync with Nickolas later today.",
        "corrected_phrase": "I'll sync with Nikolas later today."
},
    {
        "names": [
                "Nikolas Thomas"
        ],
        "raw_phrase": "Nickolas's PR is ready for review.",
        "corrected_phrase": "Nikolas's PR is ready for review."
},
    {
        "names": [
                "Nickolas Taylor"
        ],
        "raw_phrase": "Hey Nikolas, can you check the logs?",
        "corrected_phrase": "Hey Nickolas, can you check the logs?"
},
    {
        "names": [
                "Jayne Thomas"
        ],
        "raw_phrase": "Jane mentioned the deadline was moved.",
        "corrected_phrase": "Jayne mentioned the deadline was moved."
},
    {
        "names": [
                "Jayne Thomas"
        ],
        "raw_phrase": "Did Jane send the report yet?",
        "corrected_phrase": "Did Jayne send the report yet?"
},
    {
        "names": [
                "Jane Moore"
        ],
        "raw_phrase": "Hey Jayne, can you check the logs?",
        "corrected_phrase": "Hey Jane, can you check the logs?"
},
    {
        "names": [
                "Antony Brown"
        ],
        "raw_phrase": "Did Anthony send the report yet?",
        "corrected_phrase": "Did Antony send the report yet?"
},
    {
        "names": [
                "Antony Martinez"
        ],
        "raw_phrase": "Please send the invite to Anthony.",
        "corrected_phrase": "Please send the invite to Antony."
},
    {
        "names": [
                "Anthony Anderson"
        ],
        "raw_phrase": "Hey Antony, can you check the logs?",
        "corrected_phrase": "Hey Anthony, can you check the logs?"
},
    {
        "names": [
                "Barbra Martinez"
        ],
        "raw_phrase": "I think Barbara is handling the project.",
        "corrected_phrase": "I think Barbra is handling the project."
},
    {
        "names": [
                "Barbra Thomas"
        ],
        "raw_phrase": "Barbara mentioned the deadline was moved.",
        "corrected_phrase": "Barbra mentioned the deadline was moved."
},
    {
        "names": [
                "Barbara Garcia"
        ],
        "raw_phrase": "Hey Barbra, can you check the logs?",
        "corrected_phrase": "Hey Barbara, can you check the logs?"
},
    {
        "names": [
                "Lukas Smith"
        ],
        "raw_phrase": "I'll sync with Lucas later today.",
        "corrected_phrase": "I'll sync with Lukas later today."
},
    {
        "names": [
                "Lukas Davis"
        ],
        "raw_phrase": "Did Lucas send the report yet?",
        "corrected_phrase": "Did Lukas send the report yet?"
},
    {
        "names": [
                "Lucas Martinez"
        ],
        "raw_phrase": "Hey Lukas, can you check the logs?",
        "corrected_phrase": "Hey Lucas, can you check the logs?"
},
    {
        "names": [
                "Mikhail Jones"
        ],
        "raw_phrase": "I think Michael is handling the project.",
        "corrected_phrase": "I think Mikhail is handling the project."
},
    {
        "names": [
                "Mikhail Williams"
        ],
        "raw_phrase": "Did Michael send the report yet?",
        "corrected_phrase": "Did Mikhail send the report yet?"
},
    {
        "names": [
                "Michael Williams"
        ],
        "raw_phrase": "Hey Mikhail, can you check the logs?",
        "corrected_phrase": "Hey Michael, can you check the logs?"
},
    {
        "names": [
                "Dwyane Williams"
        ],
        "raw_phrase": "Check with Dwayne about the API credentials.",
        "corrected_phrase": "Check with Dwyane about the API credentials."
},
    {
        "names": [
                "Dwyane Moore"
        ],
        "raw_phrase": "Please send the invite to Dwayne.",
        "corrected_phrase": "Please send the invite to Dwyane."
},
    {
        "names": [
                "Dwayne Brown"
        ],
        "raw_phrase": "Hey Dwyane, can you check the logs?",
        "corrected_phrase": "Hey Dwayne, can you check the logs?"
},
    {
        "names": [
                "Scarlett Miller"
        ],
        "raw_phrase": "Can you ask Scarlet to join the Zoom?",
        "corrected_phrase": "Can you ask Scarlett to join the Zoom?"
},
    {
        "names": [
                "Scarlett Moore"
        ],
        "raw_phrase": "Scarlet mentioned the deadline was moved.",
        "corrected_phrase": "Scarlett mentioned the deadline was moved."
},
    {
        "names": [
                "Scarlet Martinez"
        ],
        "raw_phrase": "Hey Scarlett, can you check the logs?",
        "corrected_phrase": "Hey Scarlet, can you check the logs?"
},
    {
        "names": [
                "Gwenyth Miller"
        ],
        "raw_phrase": "Please send the invite to Gwenith.",
        "corrected_phrase": "Please send the invite to Gwenyth."
},
    {
        "names": [
                "Gwenyth Smith"
        ],
        "raw_phrase": "Gwenith's PR is ready for review.",
        "corrected_phrase": "Gwenyth's PR is ready for review."
},
    {
        "names": [
                "Gwenith Davis"
        ],
        "raw_phrase": "Hey Gwenyth, can you check the logs?",
        "corrected_phrase": "Hey Gwenith, can you check the logs?"
},
    {
        "names": [
                "Zack Anderson"
        ],
        "raw_phrase": "Check with Zach about the API credentials.",
        "corrected_phrase": "Check with Zack about the API credentials."
},
    {
        "names": [
                "Zack Brown"
        ],
        "raw_phrase": "Zach mentioned the deadline was moved.",
        "corrected_phrase": "Zack mentioned the deadline was moved."
},
    {
        "names": [
                "Zach Jones"
        ],
        "raw_phrase": "Hey Zack, can you check the logs?",
        "corrected_phrase": "Hey Zach, can you check the logs?"
},
    {
        "names": [
                "Hanna Garcia"
        ],
        "raw_phrase": "Please send the invite to Hannah.",
        "corrected_phrase": "Please send the invite to Hanna."
},
    {
        "names": [
                "Hanna Miller"
        ],
        "raw_phrase": "Can you ask Hannah to join the Zoom?",
        "corrected_phrase": "Can you ask Hanna to join the Zoom?"
},
    {
        "names": [
                "Hannah Thomas"
        ],
        "raw_phrase": "Hey Hanna, can you check the logs?",
        "corrected_phrase": "Hey Hannah, can you check the logs?"
},
    {
        "names": [
                "Mateo Thomas"
        ],
        "raw_phrase": "Matteo's PR is ready for review.",
        "corrected_phrase": "Mateo's PR is ready for review."
},
    {
        "names": [
                "Mateo Thomas"
        ],
        "raw_phrase": "Check with Matteo about the API credentials.",
        "corrected_phrase": "Check with Mateo about the API credentials."
},
    {
        "names": [
                "Matteo Johnson"
        ],
        "raw_phrase": "Hey Mateo, can you check the logs?",
        "corrected_phrase": "Hey Matteo, can you check the logs?"
},
    {
        "names": [
                "Yosef Johnson"
        ],
        "raw_phrase": "Youssef mentioned the deadline was moved.",
        "corrected_phrase": "Yosef mentioned the deadline was moved."
},
    {
        "names": [
                "Yosef Martinez"
        ],
        "raw_phrase": "Youssef's PR is ready for review.",
        "corrected_phrase": "Yosef's PR is ready for review."
},
    {
        "names": [
                "Youssef Martinez"
        ],
        "raw_phrase": "Hey Yosef, can you check the logs?",
        "corrected_phrase": "Hey Youssef, can you check the logs?"
},
    {
        "names": [
                "Yosef Martinez"
        ],
        "raw_phrase": "Joseph's PR is ready for review.",
        "corrected_phrase": "Yosef's PR is ready for review."
},
    {
        "names": [
                "Yosef Garcia"
        ],
        "raw_phrase": "Joseph mentioned the deadline was moved.",
        "corrected_phrase": "Yosef mentioned the deadline was moved."
},
    {
        "names": [
                "Joseph Anderson"
        ],
        "raw_phrase": "Hey Yosef, can you check the logs?",
        "corrected_phrase": "Hey Joseph, can you check the logs?"
},
    {
        "names": [
                "Sanjay Davis"
        ],
        "raw_phrase": "Sanjai's PR is ready for review.",
        "corrected_phrase": "Sanjay's PR is ready for review."
},
    {
        "names": [
                "Sanjay Martinez"
        ],
        "raw_phrase": "Sanjai mentioned the deadline was moved.",
        "corrected_phrase": "Sanjay mentioned the deadline was moved."
},
    {
        "names": [
                "Sanjai Jones"
        ],
        "raw_phrase": "Hey Sanjay, can you check the logs?",
        "corrected_phrase": "Hey Sanjai, can you check the logs?"
},
    {
        "names": [
                "Alexey Taylor"
        ],
        "raw_phrase": "Please send the invite to Alexei.",
        "corrected_phrase": "Please send the invite to Alexey."
},
    {
        "names": [
                "Alexey Taylor"
        ],
        "raw_phrase": "Wait for Alexei before starting the meeting.",
        "corrected_phrase": "Wait for Alexey before starting the meeting."
},
    {
        "names": [
                "Alexei Williams"
        ],
        "raw_phrase": "Hey Alexey, can you check the logs?",
        "corrected_phrase": "Hey Alexei, can you check the logs?"
},
    {
        "names": [
                "Alexey Miller"
        ],
        "raw_phrase": "Alexi mentioned the deadline was moved.",
        "corrected_phrase": "Alexey mentioned the deadline was moved."
},
    {
        "names": [
                "Alexey Anderson"
        ],
        "raw_phrase": "Alexi mentioned the deadline was moved.",
        "corrected_phrase": "Alexey mentioned the deadline was moved."
},
    {
        "names": [
                "Alexi Garcia"
        ],
        "raw_phrase": "Hey Alexey, can you check the logs?",
        "corrected_phrase": "Hey Alexi, can you check the logs?"
},
    {
        "names": [
                "Bharath Rodriguez"
        ],
        "raw_phrase": "Did Bharat send the report yet?",
        "corrected_phrase": "Did Bharath send the report yet?"
},
    {
        "names": [
                "Bharath Taylor"
        ],
        "raw_phrase": "Please send the invite to Bharat.",
        "corrected_phrase": "Please send the invite to Bharath."
},
    {
        "names": [
                "Bharat Brown"
        ],
        "raw_phrase": "Hey Bharath, can you check the logs?",
        "corrected_phrase": "Hey Bharat, can you check the logs?"
},
    {
        "names": [
                "Bharath Davis"
        ],
        "raw_phrase": "Wait for Barath before starting the meeting.",
        "corrected_phrase": "Wait for Bharath before starting the meeting."
},
    {
        "names": [
                "Bharath Garcia"
        ],
        "raw_phrase": "Barath mentioned the deadline was moved.",
        "corrected_phrase": "Bharath mentioned the deadline was moved."
},
    {
        "names": [
                "Barath Moore"
        ],
        "raw_phrase": "Hey Bharath, can you check the logs?",
        "corrected_phrase": "Hey Barath, can you check the logs?"
},
    {
        "names": [
                "Sofia Rodriguez"
        ],
        "raw_phrase": "Is Sophia on the call?",
        "corrected_phrase": "Is Sofia on the call?"
},
    {
        "names": [
                "Sofia Johnson"
        ],
        "raw_phrase": "Please send the invite to Sophia.",
        "corrected_phrase": "Please send the invite to Sofia."
},
    {
        "names": [
                "Sophia Johnson"
        ],
        "raw_phrase": "Hey Sofia, can you check the logs?",
        "corrected_phrase": "Hey Sophia, can you check the logs?"
},
    {
        "names": [
                "Kristina Thomas"
        ],
        "raw_phrase": "Wait for Christina before starting the meeting.",
        "corrected_phrase": "Wait for Kristina before starting the meeting."
},
    {
        "names": [
                "Kristina Williams"
        ],
        "raw_phrase": "Wait for Christina before starting the meeting.",
        "corrected_phrase": "Wait for Kristina before starting the meeting."
},
    {
        "names": [
                "Christina Moore"
        ],
        "raw_phrase": "Hey Kristina, can you check the logs?",
        "corrected_phrase": "Hey Christina, can you check the logs?"
},
    {
        "names": [
                "Kristina Martinez"
        ],
        "raw_phrase": "Cristina's PR is ready for review.",
        "corrected_phrase": "Kristina's PR is ready for review."
},
    {
        "names": [
                "Kristina Moore"
        ],
        "raw_phrase": "Check with Cristina about the API credentials.",
        "corrected_phrase": "Check with Kristina about the API credentials."
},
    {
        "names": [
                "Cristina Brown"
        ],
        "raw_phrase": "Hey Kristina, can you check the logs?",
        "corrected_phrase": "Hey Cristina, can you check the logs?"
},
    {
        "names": [
                "Priya Davis"
        ],
        "raw_phrase": "Did Preeya send the report yet?",
        "corrected_phrase": "Did Priya send the report yet?"
},
    {
        "names": [
                "Priya Brown"
        ],
        "raw_phrase": "I'll sync with Preeya later today.",
        "corrected_phrase": "I'll sync with Priya later today."
},
    {
        "names": [
                "Preeya Smith"
        ],
        "raw_phrase": "Hey Priya, can you check the logs?",
        "corrected_phrase": "Hey Preeya, can you check the logs?"
},
    {
        "names": [
                "Li Davis"
        ],
        "raw_phrase": "I'll sync with Lee later today.",
        "corrected_phrase": "I'll sync with Li later today."
},
    {
        "names": [
                "Li Williams"
        ],
        "raw_phrase": "Wait for Lee before starting the meeting.",
        "corrected_phrase": "Wait for Li before starting the meeting."
},
    {
        "names": [
                "Lee Brown"
        ],
        "raw_phrase": "Hey Li, can you check the logs?",
        "corrected_phrase": "Hey Lee, can you check the logs?"
},
    {
        "names": [
                "Wei Davis"
        ],
        "raw_phrase": "Wait for Way before starting the meeting.",
        "corrected_phrase": "Wait for Wei before starting the meeting."
},
    {
        "names": [
                "Wei Thomas"
        ],
        "raw_phrase": "Way's PR is ready for review.",
        "corrected_phrase": "Wei's PR is ready for review."
},
    {
        "names": [
                "Way Miller"
        ],
        "raw_phrase": "Hey Wei, can you check the logs?",
        "corrected_phrase": "Hey Way, can you check the logs?"
},
    {
        "names": [
                "Kah Mun Davis"
        ],
        "raw_phrase": "Did Ka Mun send the report yet?",
        "corrected_phrase": "Did Kah Mun send the report yet?"
},
    {
        "names": [
                "Kah Mun Moore"
        ],
        "raw_phrase": "Please send the invite to Ka Mun.",
        "corrected_phrase": "Please send the invite to Kah Mun."
},
    {
        "names": [
                "Ka Mun Anderson"
        ],
        "raw_phrase": "Hey Kah Mun, can you check the logs?",
        "corrected_phrase": "Hey Ka Mun, can you check the logs?"
},
    {
        "names": [
                "Kah Mun Smith"
        ],
        "raw_phrase": "I think Kahmun is handling the project.",
        "corrected_phrase": "I think Kah Mun is handling the project."
},
    {
        "names": [
                "Kah Mun Brown"
        ],
        "raw_phrase": "Kahmun's PR is ready for review.",
        "corrected_phrase": "Kah Mun's PR is ready for review."
},
    {
        "names": [
                "Kahmun Jones"
        ],
        "raw_phrase": "Hey Kah Mun, can you check the logs?",
        "corrected_phrase": "Hey Kahmun, can you check the logs?"
},
    {
        "names": [
                "Silvio Miller"
        ],
        "raw_phrase": "Is Sylvio on the call?",
        "corrected_phrase": "Is Silvio on the call?"
},
    {
        "names": [
                "Silvio Anderson"
        ],
        "raw_phrase": "Check with Sylvio about the API credentials.",
        "corrected_phrase": "Check with Silvio about the API credentials."
},
    {
        "names": [
                "Sylvio Miller"
        ],
        "raw_phrase": "Hey Silvio, can you check the logs?",
        "corrected_phrase": "Hey Sylvio, can you check the logs?"
},

    # LARGE BATCH AUTOMATED REGULAR NAME SAMPLES
    {
        "names": [
                "Caitlin Cooper",
                "Oleksandr Williams",
                "Aimee Roberts",
                "Elisabeth Martinez",
                "Susannah Carter"
        ],
        "raw_phrase": "Amy is the point of contact for this.",
        "corrected_phrase": "Aimee is the point of contact for this."
},
    {
        "names": [
                "Chiwetel Scott",
                "Susannah Williams",
                "Thierry Green",
                "Aimee Harris"
        ],
        "raw_phrase": "Amy is leading the research on machine learning.",
        "corrected_phrase": "Aimee is leading the research on machine learning."
},
    {
        "names": [
                "Claire Dubois",
                "Sofia Anderson",
                "Aimee Schmidt",
                "Beatrix Garcia"
        ],
        "raw_phrase": "Amy is taking the lead on the frontend refactor.",
        "corrected_phrase": "Aimee is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Aimee Smith",
                "Qasim Khan",
                "Marc Green"
        ],
        "raw_phrase": "Wait for Amy before starting the meeting.",
        "corrected_phrase": "Wait for Aimee before starting the meeting."
},
    {
        "names": [
                "Aimee Turner",
                "Damian Green",
                "Vivian Tan"
        ],
        "raw_phrase": "Can Amy join the sync tomorrow morning?",
        "corrected_phrase": "Can Aimee join the sync tomorrow morning?"
},
    {
        "names": [
                "Amy Collins"
        ],
        "raw_phrase": "Hey Aimee, can you check the logs?",
        "corrected_phrase": "Hey Amy, can you check the logs?"
},
    {
        "names": [
                "Aimee Harris"
        ],
        "raw_phrase": "I'm looking at Amy's latest update.",
        "corrected_phrase": "I'm looking at Aimee's latest update."
},
    {
        "names": [
                "Dmitry Morris",
                "Vivian Ramirez",
                "Aimee Thomas"
        ],
        "raw_phrase": "I'll follow up with Amie after the meeting.",
        "corrected_phrase": "I'll follow up with Aimee after the meeting."
},
    {
        "names": [
                "Abhishek Brown",
                "Aimee Rossi",
                "Alexey Stewart",
                "Rhaenyra Ivanov"
        ],
        "raw_phrase": "Please make sure Amie has access to the repository.",
        "corrected_phrase": "Please make sure Aimee has access to the repository."
},
    {
        "names": [
                "Aimee Nguyen",
                "Li Singh"
        ],
        "raw_phrase": "Wait for Amie before starting the meeting.",
        "corrected_phrase": "Wait for Aimee before starting the meeting."
},
    {
        "names": [
                "Susannah Khan",
                "Vihaan Green",
                "Hassan Phillips",
                "Aimee Carter"
        ],
        "raw_phrase": "I think Amie is handling the project.",
        "corrected_phrase": "I think Aimee is handling the project."
},
    {
        "names": [
                "Ishaan Adams",
                "Aimee White",
                "Scarlett Phillips",
                "Chiwetel Lee",
                "Isabelle Lefebvre"
        ],
        "raw_phrase": "Is Amie joining the happy hour tonight?",
        "corrected_phrase": "Is Aimee joining the happy hour tonight?"
},
    {
        "names": [
                "Amie Bailey"
        ],
        "raw_phrase": "Hey Aimee, can you check the logs?",
        "corrected_phrase": "Hey Amie, can you check the logs?"
},
    {
        "names": [
                "Aimee Ivanov"
        ],
        "raw_phrase": "I'm looking at Amie's latest update.",
        "corrected_phrase": "I'm looking at Aimee's latest update."
},
    {
        "names": [
                "Aimee Edwards",
                "Krysten Santos"
        ],
        "raw_phrase": "Please add Ami to the email thread.",
        "corrected_phrase": "Please add Aimee to the email thread."
},
    {
        "names": [
                "Aimee Scott",
                "Aimee Evans",
                "Yuki Kim",
                "Hanna Ramirez"
        ],
        "raw_phrase": "Wait for Ami before starting the meeting.",
        "corrected_phrase": "Wait for Aimee before starting the meeting."
},
    {
        "names": [
                "Aimee Lefebvre",
                "Vivian Roberts",
                "Megan Rossi",
                "Li Nelson"
        ],
        "raw_phrase": "I'll sync with Ami later today.",
        "corrected_phrase": "I'll sync with Aimee later today."
},
    {
        "names": [
                "Aimee Patel",
                "Katarina Miller",
                "Silvio Carter",
                "Ulysses Rossi"
        ],
        "raw_phrase": "Has Ami reviewed the security policy yet?",
        "corrected_phrase": "Has Aimee reviewed the security policy yet?"
},
    {
        "names": [
                "Aimee Nelson",
                "Xavier Hill",
                "Susannah Ivanov",
                "Hanna Harris",
                "Kieran Hill"
        ],
        "raw_phrase": "Ami is taking the lead on the frontend refactor.",
        "corrected_phrase": "Aimee is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Ami Tan"
        ],
        "raw_phrase": "Hey Aimee, can you check the logs?",
        "corrected_phrase": "Hey Ami, can you check the logs?"
},
    {
        "names": [
                "Aimee Morales"
        ],
        "raw_phrase": "I'm looking at Ami's latest update.",
        "corrected_phrase": "I'm looking at Aimee's latest update."
},
    {
        "names": [
                "Sofia Stewart",
                "Fatima Patel",
                "Teresa Rogers",
                "Antony Campbell"
        ],
        "raw_phrase": "Anthony is currently out of office until Monday.",
        "corrected_phrase": "Antony is currently out of office until Monday."
},
    {
        "names": [
                "Lukas Harris",
                "Marc Patel",
                "Teresa Jones",
                "Antony Jackson"
        ],
        "raw_phrase": "Has Anthony updated their ticket?",
        "corrected_phrase": "Has Antony updated their ticket?"
},
    {
        "names": [
                "Megan Carter",
                "Antony Ivanov",
                "Chen Stewart",
                "Chen Tan"
        ],
        "raw_phrase": "Anthony is the point of contact for this.",
        "corrected_phrase": "Antony is the point of contact for this."
},
    {
        "names": [
                "Antony Adams",
                "Sundar Davis"
        ],
        "raw_phrase": "Please make sure Anthony has access to the repository.",
        "corrected_phrase": "Please make sure Antony has access to the repository."
},
    {
        "names": [
                "Sofia Scott",
                "Katarina Singh",
                "Chiwetel Mitchell",
                "Antony White"
        ],
        "raw_phrase": "Is Anthony on the call?",
        "corrected_phrase": "Is Antony on the call?"
},
    {
        "names": [
                "Anthony Bailey"
        ],
        "raw_phrase": "Hey Antony, can you check the logs?",
        "corrected_phrase": "Hey Anthony, can you check the logs?"
},
    {
        "names": [
                "Antony Patel"
        ],
        "raw_phrase": "I'm looking at Anthony's latest update.",
        "corrected_phrase": "I'm looking at Antony's latest update."
},
    {
        "names": [
                "Barbra Anderson",
                "Dmitry Miller",
                "Yosef Taylor"
        ],
        "raw_phrase": "Barbara is the best person to talk to about this.",
        "corrected_phrase": "Barbra is the best person to talk to about this."
},
    {
        "names": [
                "Oksana Bailey",
                "Barbra Adams",
                "Barbra Thomas",
                "Thierry Brown",
                "Shawn Morgan"
        ],
        "raw_phrase": "Barbara is first on the standup list.",
        "corrected_phrase": "Barbra is first on the standup list."
},
    {
        "names": [
                "Dwyane Morales",
                "Barbra King"
        ],
        "raw_phrase": "I saw a comment from Barbara on the design doc.",
        "corrected_phrase": "I saw a comment from Barbra on the design doc."
},
    {
        "names": [
                "Barbra Carter",
                "Jayne Phillips",
                "Mateo Anderson"
        ],
        "raw_phrase": "I think Barbara is handling the project.",
        "corrected_phrase": "I think Barbra is handling the project."
},
    {
        "names": [
                "Qasim Moore",
                "Barbra Torres",
                "Lukas Cook",
                "Rachael Khan",
                "Kieran Turner"
        ],
        "raw_phrase": "Barbara is presenting their findings at the all-hands.",
        "corrected_phrase": "Barbra is presenting their findings at the all-hands."
},
    {
        "names": [
                "Barbara Martinez"
        ],
        "raw_phrase": "Hey Barbra, can you check the logs?",
        "corrected_phrase": "Hey Barbara, can you check the logs?"
},
    {
        "names": [
                "Barbra Silva"
        ],
        "raw_phrase": "I'm looking at Barbara's latest update.",
        "corrected_phrase": "I'm looking at Barbra's latest update."
},
    {
        "names": [
                "Krysten Murphy",
                "Isabelle Santos",
                "Arjun Thomas",
                "Damian Johnson",
                "Bryan Lee"
        ],
        "raw_phrase": "Brian suggested we use a different database.",
        "corrected_phrase": "Bryan suggested we use a different database."
},
    {
        "names": [
                "Sanjay Jackson",
                "Bryan Harris"
        ],
        "raw_phrase": "Check with Brian about the API credentials.",
        "corrected_phrase": "Check with Bryan about the API credentials."
},
    {
        "names": [
                "Abhishek Young",
                "Aarav Stewart",
                "Bryan Murphy"
        ],
        "raw_phrase": "Please add Brian to the email thread.",
        "corrected_phrase": "Please add Bryan to the email thread."
},
    {
        "names": [
                "Aimee Harris",
                "Oksana Campbell",
                "Bryan Adams",
                "Marc Murphy"
        ],
        "raw_phrase": "Could you take a look at the PR from Brian?",
        "corrected_phrase": "Could you take a look at the PR from Bryan?"
},
    {
        "names": [
                "Bryan Peterson",
                "Aarav Scott",
                "Krysten Morgan",
                "Sara Kim",
                "Shawn Jackson"
        ],
        "raw_phrase": "Can you pass the message to Brian for me?",
        "corrected_phrase": "Can you pass the message to Bryan for me?"
},
    {
        "names": [
                "Brian Peterson"
        ],
        "raw_phrase": "Hey Bryan, can you check the logs?",
        "corrected_phrase": "Hey Brian, can you check the logs?"
},
    {
        "names": [
                "Bryan Roberts"
        ],
        "raw_phrase": "I'm looking at Brian's latest update.",
        "corrected_phrase": "I'm looking at Bryan's latest update."
},
    {
        "names": [
                "Caitlin Jones",
                "Ulysses Lefebvre",
                "Li Martin"
        ],
        "raw_phrase": "Kaitlyn has a lot of experience with React.",
        "corrected_phrase": "Caitlin has a lot of experience with React."
},
    {
        "names": [
                "Stephen Turner",
                "Caitlin Rossi"
        ],
        "raw_phrase": "I'll sync with Kaitlyn later today.",
        "corrected_phrase": "I'll sync with Caitlin later today."
},
    {
        "names": [
                "Antony Collins",
                "Yuki Morgan",
                "Caitlin Kim",
                "Isabelle Khan",
                "Zainab M\u00fcller"
        ],
        "raw_phrase": "Did Kaitlyn mention anything about the budget?",
        "corrected_phrase": "Did Caitlin mention anything about the budget?"
},
    {
        "names": [
                "Rachael Stewart",
                "Caitlin Morales",
                "Chen Ivanov",
                "Eric Scott"
        ],
        "raw_phrase": "Kaitlyn mentioned the deadline was moved.",
        "corrected_phrase": "Caitlin mentioned the deadline was moved."
},
    {
        "names": [
                "Yosef Taylor",
                "Caitlin Reed"
        ],
        "raw_phrase": "Kaitlyn is currently out of office until Monday.",
        "corrected_phrase": "Caitlin is currently out of office until Monday."
},
    {
        "names": [
                "Kaitlyn Ivanov"
        ],
        "raw_phrase": "Hey Caitlin, can you check the logs?",
        "corrected_phrase": "Hey Kaitlyn, can you check the logs?"
},
    {
        "names": [
                "Caitlin Silva"
        ],
        "raw_phrase": "I'm looking at Kaitlyn's latest update.",
        "corrected_phrase": "I'm looking at Caitlin's latest update."
},
    {
        "names": [
                "Caiming Garcia",
                "Tomas Torres",
                "Krysten Jackson",
                "Caitlin Scott"
        ],
        "raw_phrase": "Has Katelyn updated their ticket?",
        "corrected_phrase": "Has Caitlin updated their ticket?"
},
    {
        "names": [
                "Gwenyth Rodriguez",
                "Caitlin King"
        ],
        "raw_phrase": "Katelyn is the point of contact for this.",
        "corrected_phrase": "Caitlin is the point of contact for this."
},
    {
        "names": [
                "Zack Thomas",
                "Caitlin Kim"
        ],
        "raw_phrase": "Katelyn is currently out of office until Monday.",
        "corrected_phrase": "Caitlin is currently out of office until Monday."
},
    {
        "names": [
                "Juliet Phillips",
                "Sundar Rodriguez",
                "Phillip Thompson",
                "Caitlin Nguyen",
                "Xavier Jackson"
        ],
        "raw_phrase": "Can you pass the message to Katelyn for me?",
        "corrected_phrase": "Can you pass the message to Caitlin for me?"
},
    {
        "names": [
                "Aarav Stewart",
                "Scarlett Santos",
                "Dmitry White",
                "Caitlin Stewart"
        ],
        "raw_phrase": "Ask Katelyn if they have the login for the staging server.",
        "corrected_phrase": "Ask Caitlin if they have the login for the staging server."
},
    {
        "names": [
                "Katelyn Cook"
        ],
        "raw_phrase": "Hey Caitlin, can you check the logs?",
        "corrected_phrase": "Hey Katelyn, can you check the logs?"
},
    {
        "names": [
                "Caitlin Dubois"
        ],
        "raw_phrase": "I'm looking at Katelyn's latest update.",
        "corrected_phrase": "I'm looking at Caitlin's latest update."
},
    {
        "names": [
                "Caitlin Hill",
                "Hassan Scott",
                "Phillip Collins"
        ],
        "raw_phrase": "Please make sure Katelynn has access to the repository.",
        "corrected_phrase": "Please make sure Caitlin has access to the repository."
},
    {
        "names": [
                "Oleksandr Harris",
                "Mei Peterson",
                "Caitlin Collins"
        ],
        "raw_phrase": "Is Katelynn joining the happy hour tonight?",
        "corrected_phrase": "Is Caitlin joining the happy hour tonight?"
},
    {
        "names": [
                "Srini Ramirez",
                "Caitlin Rodriguez",
                "Krysten Nelson"
        ],
        "raw_phrase": "Katelynn is leading the research on machine learning.",
        "corrected_phrase": "Caitlin is leading the research on machine learning."
},
    {
        "names": [
                "Caitlin Martinez",
                "Katarina Torres",
                "Sofia Martin"
        ],
        "raw_phrase": "Did Katelynn mention anything about the budget?",
        "corrected_phrase": "Did Caitlin mention anything about the budget?"
},
    {
        "names": [
                "Nikolas Ivanov",
                "Caitlin Rossi",
                "Ulysses Rogers"
        ],
        "raw_phrase": "Please CC Katelynn on all future updates.",
        "corrected_phrase": "Please CC Caitlin on all future updates."
},
    {
        "names": [
                "Katelynn Kim"
        ],
        "raw_phrase": "Hey Caitlin, can you check the logs?",
        "corrected_phrase": "Hey Katelynn, can you check the logs?"
},
    {
        "names": [
                "Caitlin Bailey"
        ],
        "raw_phrase": "I'm looking at Katelynn's latest update.",
        "corrected_phrase": "I'm looking at Caitlin's latest update."
},
    {
        "names": [
                "Zainab Evans",
                "Caitlin Singh",
                "Isabelle M\u00fcller",
                "Teresa Ramirez"
        ],
        "raw_phrase": "Katelin is the point of contact for this.",
        "corrected_phrase": "Caitlin is the point of contact for this."
},
    {
        "names": [
                "Caiming Nelson",
                "Caitlin Cook",
                "Sanjay Bailey",
                "Qasim Schmidt",
                "Scarlett Cooper"
        ],
        "raw_phrase": "Did Katelin send the report yet?",
        "corrected_phrase": "Did Caitlin send the report yet?"
},
    {
        "names": [
                "Caitlin Bailey",
                "Chiwetel Tan",
                "Juliet Patel"
        ],
        "raw_phrase": "I'll ask Katelin to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Caitlin to walk us through the deployment process."
},
    {
        "names": [
                "Claire Carter",
                "Caitlin M\u00fcller",
                "Zhi Davis",
                "Rachael Carter",
                "Teresa Santos"
        ],
        "raw_phrase": "Check with Katelin about the API credentials.",
        "corrected_phrase": "Check with Caitlin about the API credentials."
},
    {
        "names": [
                "Caitlin Parker",
                "Thierry Ramirez"
        ],
        "raw_phrase": "Is Katelin familiar with this part of the codebase?",
        "corrected_phrase": "Is Caitlin familiar with this part of the codebase?"
},
    {
        "names": [
                "Katelin Phillips"
        ],
        "raw_phrase": "Hey Caitlin, can you check the logs?",
        "corrected_phrase": "Hey Katelin, can you check the logs?"
},
    {
        "names": [
                "Caitlin Morris"
        ],
        "raw_phrase": "I'm looking at Katelin's latest update.",
        "corrected_phrase": "I'm looking at Caitlin's latest update."
},
    {
        "names": [
                "Jayne Adams",
                "Mei Phillips",
                "Claire Bailey"
        ],
        "raw_phrase": "Clare suggested a few improvements to the UI.",
        "corrected_phrase": "Claire suggested a few improvements to the UI."
},
    {
        "names": [
                "Tomas Morris",
                "Giuseppe Jones",
                "Claire Dubois",
                "Ishaan Edwards"
        ],
        "raw_phrase": "Is Clare familiar with this part of the codebase?",
        "corrected_phrase": "Is Claire familiar with this part of the codebase?"
},
    {
        "names": [
                "Zack Lee",
                "Claire Jones",
                "Caitlin Lee",
                "Yosef Nelson",
                "Phillip Jones"
        ],
        "raw_phrase": "Please add Clare to the email thread.",
        "corrected_phrase": "Please add Claire to the email thread."
},
    {
        "names": [
                "Vivian Edwards",
                "Claire Patel",
                "Qasim Rodriguez",
                "Chiwetel Morales"
        ],
        "raw_phrase": "Did Clare mention anything about the budget?",
        "corrected_phrase": "Did Claire mention anything about the budget?"
},
    {
        "names": [
                "Arjun Scott",
                "Claire Morgan",
                "Marc Murphy"
        ],
        "raw_phrase": "Please add Clare to the email thread.",
        "corrected_phrase": "Please add Claire to the email thread."
},
    {
        "names": [
                "Clare Mitchell"
        ],
        "raw_phrase": "Hey Claire, can you check the logs?",
        "corrected_phrase": "Hey Clare, can you check the logs?"
},
    {
        "names": [
                "Claire Campbell"
        ],
        "raw_phrase": "I'm looking at Clare's latest update.",
        "corrected_phrase": "I'm looking at Claire's latest update."
},
    {
        "names": [
                "Chen Cooper",
                "Damian White",
                "Susannah Brown",
                "Ishaan Davis"
        ],
        "raw_phrase": "I'll sync up with Damien to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Damian to make sure we're on the same page."
},
    {
        "names": [
                "Katarina Tan",
                "Damian Phillips"
        ],
        "raw_phrase": "Damien's PR is ready for review.",
        "corrected_phrase": "Damian's PR is ready for review."
},
    {
        "names": [
                "Damian Rossi",
                "Niamh Taylor",
                "Qasim Turner",
                "Nikolas Peterson"
        ],
        "raw_phrase": "I'm going to grab a coffee with Damien later.",
        "corrected_phrase": "I'm going to grab a coffee with Damian later."
},
    {
        "names": [
                "Juliet Lee",
                "Caiming Roberts",
                "Damian Campbell",
                "Yosef Green"
        ],
        "raw_phrase": "Could you take a look at the PR from Damien?",
        "corrected_phrase": "Could you take a look at the PR from Damian?"
},
    {
        "names": [
                "Pavel Moore",
                "Damian Martin"
        ],
        "raw_phrase": "Damien is presenting their findings at the all-hands.",
        "corrected_phrase": "Damian is presenting their findings at the all-hands."
},
    {
        "names": [
                "Damien Johnson"
        ],
        "raw_phrase": "Hey Damian, can you check the logs?",
        "corrected_phrase": "Hey Damien, can you check the logs?"
},
    {
        "names": [
                "Damian Silva"
        ],
        "raw_phrase": "I'm looking at Damien's latest update.",
        "corrected_phrase": "I'm looking at Damian's latest update."
},
    {
        "names": [
                "Arjun Bailey",
                "Dwyane Khan",
                "Elisabeth Scott",
                "Shawn Williams"
        ],
        "raw_phrase": "Did Dwayne finish the documentation for the new API?",
        "corrected_phrase": "Did Dwyane finish the documentation for the new API?"
},
    {
        "names": [
                "Vivian Jackson",
                "Dwyane Thomas"
        ],
        "raw_phrase": "Is Dwayne joining the happy hour tonight?",
        "corrected_phrase": "Is Dwyane joining the happy hour tonight?"
},
    {
        "names": [
                "Alexey Dubois",
                "Dwyane Harris",
                "Abhishek Cook"
        ],
        "raw_phrase": "Could you take a look at the PR from Dwayne?",
        "corrected_phrase": "Could you take a look at the PR from Dwyane?"
},
    {
        "names": [
                "Priya Harris",
                "Ishaan Peterson",
                "Dwyane Carter",
                "Hassan King",
                "Sundar Roberts"
        ],
        "raw_phrase": "Dwayne suggested we use a different database.",
        "corrected_phrase": "Dwyane suggested we use a different database."
},
    {
        "names": [
                "Barbra Rodriguez",
                "Chiwetel Martinez",
                "Dwyane Stewart",
                "Domhnall Lefebvre"
        ],
        "raw_phrase": "I'll be working closely with Dwayne on this feature.",
        "corrected_phrase": "I'll be working closely with Dwyane on this feature."
},
    {
        "names": [
                "Dwayne Collins"
        ],
        "raw_phrase": "Hey Dwyane, can you check the logs?",
        "corrected_phrase": "Hey Dwayne, can you check the logs?"
},
    {
        "names": [
                "Dwyane Peterson"
        ],
        "raw_phrase": "I'm looking at Dwayne's latest update.",
        "corrected_phrase": "I'm looking at Dwyane's latest update."
},
    {
        "names": [
                "Aarav Santos",
                "Ulysses Nguyen",
                "Mathew Silva",
                "Elisabeth Jackson",
                "Shawn Thompson"
        ],
        "raw_phrase": "Elizabeth is the best person to talk to about this.",
        "corrected_phrase": "Elisabeth is the best person to talk to about this."
},
    {
        "names": [
                "Elisabeth Hill",
                "Alexey Kim",
                "Caitlin Lee",
                "Megan Young"
        ],
        "raw_phrase": "Elizabeth is leading the research on machine learning.",
        "corrected_phrase": "Elisabeth is leading the research on machine learning."
},
    {
        "names": [
                "Elisabeth Baker",
                "Giuseppe Moore",
                "Marc Rossi",
                "Dmitry Khan"
        ],
        "raw_phrase": "I'll check the calendar to see when Elizabeth is free.",
        "corrected_phrase": "I'll check the calendar to see when Elisabeth is free."
},
    {
        "names": [
                "Damian White",
                "Dwyane Torres",
                "Pavel Martin",
                "Kieran Morales",
                "Elisabeth Anderson"
        ],
        "raw_phrase": "Did Elizabeth catch that error in the logs?",
        "corrected_phrase": "Did Elisabeth catch that error in the logs?"
},
    {
        "names": [
                "Elisabeth Morales",
                "Thierry Hill",
                "Oleksandr Rossi",
                "Rhaenyra Murphy"
        ],
        "raw_phrase": "Has Elizabeth updated their ticket?",
        "corrected_phrase": "Has Elisabeth updated their ticket?"
},
    {
        "names": [
                "Elizabeth Young"
        ],
        "raw_phrase": "Hey Elisabeth, can you check the logs?",
        "corrected_phrase": "Hey Elizabeth, can you check the logs?"
},
    {
        "names": [
                "Elisabeth Edwards"
        ],
        "raw_phrase": "I'm looking at Elizabeth's latest update.",
        "corrected_phrase": "I'm looking at Elisabeth's latest update."
},
    {
        "names": [
                "Pavel Rogers",
                "Eric Martinez",
                "Chiwetel Cooper",
                "Dwyane Campbell"
        ],
        "raw_phrase": "I saw a comment from Erik on the design doc.",
        "corrected_phrase": "I saw a comment from Eric on the design doc."
},
    {
        "names": [
                "Eric Rodriguez",
                "Dwyane Khan"
        ],
        "raw_phrase": "I sent the draft to Erik for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Eric for some initial thoughts."
},
    {
        "names": [
                "Claire Green",
                "Eric Williams"
        ],
        "raw_phrase": "Could you take a look at the PR from Erik?",
        "corrected_phrase": "Could you take a look at the PR from Eric?"
},
    {
        "names": [
                "Priya Nguyen",
                "Eric Thomas",
                "Dwyane Johnson",
                "Yuki Rogers"
        ],
        "raw_phrase": "Erik's PR is ready for review.",
        "corrected_phrase": "Eric's PR is ready for review."
},
    {
        "names": [
                "Oleksandr Thomas",
                "Rachael Morgan",
                "Eric Campbell",
                "Gwenyth Parker",
                "Zhi Moore"
        ],
        "raw_phrase": "Erik is the best person to talk to about this.",
        "corrected_phrase": "Eric is the best person to talk to about this."
},
    {
        "names": [
                "Erik Anderson"
        ],
        "raw_phrase": "Hey Eric, can you check the logs?",
        "corrected_phrase": "Hey Erik, can you check the logs?"
},
    {
        "names": [
                "Eric Nelson"
        ],
        "raw_phrase": "I'm looking at Erik's latest update.",
        "corrected_phrase": "I'm looking at Eric's latest update."
},
    {
        "names": [
                "Sundar Baker",
                "Mateo Young",
                "Kieran Miller",
                "Abhishek Scott",
                "Geoff Murphy"
        ],
        "raw_phrase": "I'll ask Jeff to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Geoff to walk us through the deployment process."
},
    {
        "names": [
                "Geoff Kim",
                "Wei Phillips",
                "Domhnall Miller",
                "Stephen Ivanov"
        ],
        "raw_phrase": "I'm going to grab a coffee with Jeff later.",
        "corrected_phrase": "I'm going to grab a coffee with Geoff later."
},
    {
        "names": [
                "Yuki Brown",
                "Geoff Silva",
                "Dwyane Martinez",
                "Jian Martinez",
                "Niamh Thompson"
        ],
        "raw_phrase": "Jeff is first on the standup list.",
        "corrected_phrase": "Geoff is first on the standup list."
},
    {
        "names": [
                "Hassan Evans",
                "Geoff Carter"
        ],
        "raw_phrase": "Please CC Jeff on all future updates.",
        "corrected_phrase": "Please CC Geoff on all future updates."
},
    {
        "names": [
                "Ishaan Harris",
                "Susannah Nguyen",
                "Geoff Dubois",
                "Geoff Young"
        ],
        "raw_phrase": "Please add Jeff to the email thread.",
        "corrected_phrase": "Please add Geoff to the email thread."
},
    {
        "names": [
                "Jeff Silva"
        ],
        "raw_phrase": "Hey Geoff, can you check the logs?",
        "corrected_phrase": "Hey Jeff, can you check the logs?"
},
    {
        "names": [
                "Geoff Johnson"
        ],
        "raw_phrase": "I'm looking at Jeff's latest update.",
        "corrected_phrase": "I'm looking at Geoff's latest update."
},
    {
        "names": [
                "Gwenyth Rossi",
                "Geoff Taylor"
        ],
        "raw_phrase": "Did Geoffrey mention anything about the budget?",
        "corrected_phrase": "Did Geoff mention anything about the budget?"
},
    {
        "names": [
                "Abhishek Rogers",
                "Geoff Morris"
        ],
        "raw_phrase": "I'll sync up with Geoffrey to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Geoff to make sure we're on the same page."
},
    {
        "names": [
                "Geoff Cooper",
                "Jian Roberts"
        ],
        "raw_phrase": "Geoffrey's PR is ready for review.",
        "corrected_phrase": "Geoff's PR is ready for review."
},
    {
        "names": [
                "Ishaan Morgan",
                "Geoff Thompson",
                "Damian Silva"
        ],
        "raw_phrase": "Is Geoffrey joining the happy hour tonight?",
        "corrected_phrase": "Is Geoff joining the happy hour tonight?"
},
    {
        "names": [
                "Fatima Carter",
                "Geoff Cooper",
                "Damian Khan"
        ],
        "raw_phrase": "Geoffrey's PR is ready for review.",
        "corrected_phrase": "Geoff's PR is ready for review."
},
    {
        "names": [
                "Geoffrey Parker"
        ],
        "raw_phrase": "Hey Geoff, can you check the logs?",
        "corrected_phrase": "Hey Geoffrey, can you check the logs?"
},
    {
        "names": [
                "Geoff Johnson"
        ],
        "raw_phrase": "I'm looking at Geoffrey's latest update.",
        "corrected_phrase": "I'm looking at Geoff's latest update."
},
    {
        "names": [
                "Caiming Lefebvre",
                "Isabelle Reed",
                "Geoff King",
                "Yosef Adams",
                "Dmitry Johnson"
        ],
        "raw_phrase": "Is Jeffrey on the call?",
        "corrected_phrase": "Is Geoff on the call?"
},
    {
        "names": [
                "Geoff Martin",
                "Mei Dubois"
        ],
        "raw_phrase": "Jeffrey is the best person to talk to about this.",
        "corrected_phrase": "Geoff is the best person to talk to about this."
},
    {
        "names": [
                "Abhishek Edwards",
                "Geoff Lee",
                "Rachael Johnson"
        ],
        "raw_phrase": "Is Jeffrey familiar with this part of the codebase?",
        "corrected_phrase": "Is Geoff familiar with this part of the codebase?"
},
    {
        "names": [
                "Lukas Martin",
                "Eric King",
                "Dwyane Rossi",
                "Geoff Brown"
        ],
        "raw_phrase": "Jeffrey found a bug in the production environment.",
        "corrected_phrase": "Geoff found a bug in the production environment."
},
    {
        "names": [
                "Geoff Anderson",
                "Caiming White",
                "Katherine Rogers"
        ],
        "raw_phrase": "Jeffrey found a bug in the production environment.",
        "corrected_phrase": "Geoff found a bug in the production environment."
},
    {
        "names": [
                "Jeffrey Evans"
        ],
        "raw_phrase": "Hey Geoff, can you check the logs?",
        "corrected_phrase": "Hey Jeffrey, can you check the logs?"
},
    {
        "names": [
                "Geoff Davis"
        ],
        "raw_phrase": "I'm looking at Jeffrey's latest update.",
        "corrected_phrase": "I'm looking at Geoff's latest update."
},
    {
        "names": [
                "Gwenyth Martin",
                "Yosef Cooper"
        ],
        "raw_phrase": "Gwenith has a lot of experience with React.",
        "corrected_phrase": "Gwenyth has a lot of experience with React."
},
    {
        "names": [
                "Gwenyth Bailey",
                "Gwenyth Schmidt"
        ],
        "raw_phrase": "Is Gwenith joining the happy hour tonight?",
        "corrected_phrase": "Is Gwenyth joining the happy hour tonight?"
},
    {
        "names": [
                "Gwenyth Evans",
                "Oleksandr Jackson",
                "Ishaan Singh"
        ],
        "raw_phrase": "Wait for Gwenith before starting the meeting.",
        "corrected_phrase": "Wait for Gwenyth before starting the meeting."
},
    {
        "names": [
                "Oleksandr Hill",
                "Gwenyth Kim",
                "Mathew Khan",
                "Krysten Lefebvre"
        ],
        "raw_phrase": "Is Gwenith on the call?",
        "corrected_phrase": "Is Gwenyth on the call?"
},
    {
        "names": [
                "Phillip Nelson",
                "Alexey Ivanov",
                "Eric Morris",
                "Gwenyth Hill",
                "Bharath Campbell"
        ],
        "raw_phrase": "We should get some feedback from Gwenith on this.",
        "corrected_phrase": "We should get some feedback from Gwenyth on this."
},
    {
        "names": [
                "Gwenith Morgan"
        ],
        "raw_phrase": "Hey Gwenyth, can you check the logs?",
        "corrected_phrase": "Hey Gwenith, can you check the logs?"
},
    {
        "names": [
                "Gwenyth Moore"
        ],
        "raw_phrase": "I'm looking at Gwenith's latest update.",
        "corrected_phrase": "I'm looking at Gwenyth's latest update."
},
    {
        "names": [
                "Gwenyth Morris",
                "Dmitry King",
                "Wei Kim"
        ],
        "raw_phrase": "I'll sync with Gwyneth later today.",
        "corrected_phrase": "I'll sync with Gwenyth later today."
},
    {
        "names": [
                "Isabelle Martin",
                "Gwenyth Kim",
                "Srini Carter"
        ],
        "raw_phrase": "Gwyneth is the one who originally wrote this script.",
        "corrected_phrase": "Gwenyth is the one who originally wrote this script."
},
    {
        "names": [
                "Gwenyth Rossi",
                "Srini Cook"
        ],
        "raw_phrase": "I'll ask Gwyneth to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Gwenyth to walk us through the deployment process."
},
    {
        "names": [
                "Gwenyth Schmidt",
                "Juliet Baker",
                "Chiwetel Anderson"
        ],
        "raw_phrase": "Gwyneth suggested we use a different database.",
        "corrected_phrase": "Gwenyth suggested we use a different database."
},
    {
        "names": [
                "Sundar Jackson",
                "Giuseppe Torres",
                "Ulysses Martin",
                "Gwenyth Jackson"
        ],
        "raw_phrase": "I'll check the calendar to see when Gwyneth is free.",
        "corrected_phrase": "I'll check the calendar to see when Gwenyth is free."
},
    {
        "names": [
                "Gwyneth Smith"
        ],
        "raw_phrase": "Hey Gwenyth, can you check the logs?",
        "corrected_phrase": "Hey Gwyneth, can you check the logs?"
},
    {
        "names": [
                "Gwenyth Lee"
        ],
        "raw_phrase": "I'm looking at Gwyneth's latest update.",
        "corrected_phrase": "I'm looking at Gwenyth's latest update."
},
    {
        "names": [
                "Sundar Torres",
                "Isabelle Martinez"
        ],
        "raw_phrase": "I'll sync with Isabel later today.",
        "corrected_phrase": "I'll sync with Isabelle later today."
},
    {
        "names": [
                "Krysten Nguyen",
                "Oleksandr Nelson",
                "Arjun Jackson",
                "Giuseppe Reed",
                "Isabelle Murphy"
        ],
        "raw_phrase": "Has Isabel updated their ticket?",
        "corrected_phrase": "Has Isabelle updated their ticket?"
},
    {
        "names": [
                "Isabelle Kim",
                "Caitlin Murphy",
                "Zack Scott",
                "Arjun Nguyen",
                "Li Peterson"
        ],
        "raw_phrase": "Isabel's PR is ready for review.",
        "corrected_phrase": "Isabelle's PR is ready for review."
},
    {
        "names": [
                "Caitlin Bailey",
                "Beatrix Parker",
                "Isabelle Bailey"
        ],
        "raw_phrase": "Could you take a look at the PR from Isabel?",
        "corrected_phrase": "Could you take a look at the PR from Isabelle?"
},
    {
        "names": [
                "Isabelle Morales",
                "Krysten Morgan",
                "Bryan Thomas"
        ],
        "raw_phrase": "I'll ask Isabel to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Isabelle to walk us through the deployment process."
},
    {
        "names": [
                "Isabel Smith"
        ],
        "raw_phrase": "Hey Isabelle, can you check the logs?",
        "corrected_phrase": "Hey Isabel, can you check the logs?"
},
    {
        "names": [
                "Isabelle Ramirez"
        ],
        "raw_phrase": "I'm looking at Isabel's latest update.",
        "corrected_phrase": "I'm looking at Isabelle's latest update."
},
    {
        "names": [
                "Sofia Rogers",
                "Dmitry Jones",
                "Isabelle Cook"
        ],
        "raw_phrase": "Isobel has a lot of experience with React.",
        "corrected_phrase": "Isabelle has a lot of experience with React."
},
    {
        "names": [
                "Isabelle Davis",
                "Stephen Santos",
                "Beatrix Khan",
                "Aarav Santos"
        ],
        "raw_phrase": "I'll double check the numbers with Isobel.",
        "corrected_phrase": "I'll double check the numbers with Isabelle."
},
    {
        "names": [
                "Rachael Nguyen",
                "Zainab Carter",
                "Beatrix Lee",
                "Qasim Dubois",
                "Isabelle Thompson"
        ],
        "raw_phrase": "Could you take a look at the PR from Isobel?",
        "corrected_phrase": "Could you take a look at the PR from Isabelle?"
},
    {
        "names": [
                "Katherine Ramirez",
                "Li Morris",
                "Isabelle Carter"
        ],
        "raw_phrase": "Isobel is currently out of office until Monday.",
        "corrected_phrase": "Isabelle is currently out of office until Monday."
},
    {
        "names": [
                "Isabelle Peterson",
                "Domhnall Rodriguez"
        ],
        "raw_phrase": "Isobel is presenting their findings at the all-hands.",
        "corrected_phrase": "Isabelle is presenting their findings at the all-hands."
},
    {
        "names": [
                "Isobel Nelson"
        ],
        "raw_phrase": "Hey Isabelle, can you check the logs?",
        "corrected_phrase": "Hey Isobel, can you check the logs?"
},
    {
        "names": [
                "Isabelle Morales"
        ],
        "raw_phrase": "I'm looking at Isobel's latest update.",
        "corrected_phrase": "I'm looking at Isabelle's latest update."
},
    {
        "names": [
                "Jayne Dubois",
                "Oleksandr Johnson",
                "Shawn Lee",
                "Arjun Collins"
        ],
        "raw_phrase": "I'll follow up with Jane after the meeting.",
        "corrected_phrase": "I'll follow up with Jayne after the meeting."
},
    {
        "names": [
                "Antony Davis",
                "Jayne Schmidt",
                "Niamh Moore",
                "Sanjay Parker",
                "Teresa Ivanov"
        ],
        "raw_phrase": "Please send the invite to Jane.",
        "corrected_phrase": "Please send the invite to Jayne."
},
    {
        "names": [
                "Yosef Mitchell",
                "Xavier Ivanov",
                "Jayne M\u00fcller"
        ],
        "raw_phrase": "Jane is currently out of office until Monday.",
        "corrected_phrase": "Jayne is currently out of office until Monday."
},
    {
        "names": [
                "Zainab Green",
                "Jayne Thompson"
        ],
        "raw_phrase": "Jane is the point of contact for this.",
        "corrected_phrase": "Jayne is the point of contact for this."
},
    {
        "names": [
                "Saoirse Miller",
                "Sundar Ramirez",
                "Claire Khan",
                "Elisabeth Williams",
                "Jayne Peterson"
        ],
        "raw_phrase": "Is Jane familiar with this part of the codebase?",
        "corrected_phrase": "Is Jayne familiar with this part of the codebase?"
},
    {
        "names": [
                "Jane Mitchell"
        ],
        "raw_phrase": "Hey Jayne, can you check the logs?",
        "corrected_phrase": "Hey Jane, can you check the logs?"
},
    {
        "names": [
                "Jayne Thomas"
        ],
        "raw_phrase": "I'm looking at Jane's latest update.",
        "corrected_phrase": "I'm looking at Jayne's latest update."
},
    {
        "names": [
                "Rhaenyra Kim",
                "Jon White",
                "Damian Phillips",
                "Domhnall Reed",
                "Jian Ramirez"
        ],
        "raw_phrase": "Check with John about the API credentials.",
        "corrected_phrase": "Check with Jon about the API credentials."
},
    {
        "names": [
                "Qasim Phillips",
                "Jon Taylor",
                "Yingbo Thomas"
        ],
        "raw_phrase": "Did John mention anything about the budget?",
        "corrected_phrase": "Did Jon mention anything about the budget?"
},
    {
        "names": [
                "Jon Turner",
                "Scarlett Morales"
        ],
        "raw_phrase": "John is presenting their findings at the all-hands.",
        "corrected_phrase": "Jon is presenting their findings at the all-hands."
},
    {
        "names": [
                "Megan Cook",
                "Jon Singh",
                "Hassan Rodriguez",
                "Jayne Brown"
        ],
        "raw_phrase": "I'll check the calendar to see when John is free.",
        "corrected_phrase": "I'll check the calendar to see when Jon is free."
},
    {
        "names": [
                "Jon Parker",
                "Domhnall Santos",
                "Aimee Martinez"
        ],
        "raw_phrase": "John is presenting their findings at the all-hands.",
        "corrected_phrase": "Jon is presenting their findings at the all-hands."
},
    {
        "names": [
                "John Lee"
        ],
        "raw_phrase": "Hey Jon, can you check the logs?",
        "corrected_phrase": "Hey John, can you check the logs?"
},
    {
        "names": [
                "Jon Torres"
        ],
        "raw_phrase": "I'm looking at John's latest update.",
        "corrected_phrase": "I'm looking at Jon's latest update."
},
    {
        "names": [
                "Bharath Dubois",
                "Juliet Smith"
        ],
        "raw_phrase": "Juliette is presenting their findings at the all-hands.",
        "corrected_phrase": "Juliet is presenting their findings at the all-hands."
},
    {
        "names": [
                "Chiwetel Ramirez",
                "Juliet Brown",
                "Rhaenyra King",
                "Eric Johnson"
        ],
        "raw_phrase": "Juliette is the point of contact for this.",
        "corrected_phrase": "Juliet is the point of contact for this."
},
    {
        "names": [
                "Hiroshi Kim",
                "Claire Tan",
                "Phillip Turner",
                "Juliet Thompson"
        ],
        "raw_phrase": "I'll coordinate the meeting with Juliette.",
        "corrected_phrase": "I'll coordinate the meeting with Juliet."
},
    {
        "names": [
                "Kieran Tan",
                "Juliet Peterson",
                "Dmitry Edwards",
                "Beatrix Martin",
                "Saoirse Rossi"
        ],
        "raw_phrase": "I'll follow up with Juliette after the meeting.",
        "corrected_phrase": "I'll follow up with Juliet after the meeting."
},
    {
        "names": [
                "Sara Patel",
                "Hiroshi M\u00fcller",
                "Juliet Carter",
                "Aarav Torres",
                "Beatrix Hill"
        ],
        "raw_phrase": "Is Juliette joining the happy hour tonight?",
        "corrected_phrase": "Is Juliet joining the happy hour tonight?"
},
    {
        "names": [
                "Juliette Torres"
        ],
        "raw_phrase": "Hey Juliet, can you check the logs?",
        "corrected_phrase": "Hey Juliette, can you check the logs?"
},
    {
        "names": [
                "Juliet King"
        ],
        "raw_phrase": "I'm looking at Juliette's latest update.",
        "corrected_phrase": "I'm looking at Juliet's latest update."
},
    {
        "names": [
                "Qasim Smith",
                "Ulysses Parker",
                "Yosef M\u00fcller",
                "Katherine Nguyen"
        ],
        "raw_phrase": "Check with Catherine about the API credentials.",
        "corrected_phrase": "Check with Katherine about the API credentials."
},
    {
        "names": [
                "Qasim Martin",
                "Katherine Taylor",
                "Shawn Murphy",
                "Fatima King"
        ],
        "raw_phrase": "Has Catherine updated their ticket?",
        "corrected_phrase": "Has Katherine updated their ticket?"
},
    {
        "names": [
                "Hiroshi Nguyen",
                "Vihaan Phillips",
                "Katherine Dubois",
                "Yingbo Brown"
        ],
        "raw_phrase": "Let's find a time that works for Catherine.",
        "corrected_phrase": "Let's find a time that works for Katherine."
},
    {
        "names": [
                "Caitlin Williams",
                "Pavel Rodriguez",
                "Chiwetel Morales",
                "Katherine Rossi",
                "Wei M\u00fcller"
        ],
        "raw_phrase": "Catherine suggested we use a different database.",
        "corrected_phrase": "Katherine suggested we use a different database."
},
    {
        "names": [
                "Isabelle Phillips",
                "Katherine Morales",
                "Sara Torres",
                "Silvio Smith",
                "Aimee M\u00fcller"
        ],
        "raw_phrase": "We should get some feedback from Catherine on this.",
        "corrected_phrase": "We should get some feedback from Katherine on this."
},
    {
        "names": [
                "Catherine Lee"
        ],
        "raw_phrase": "Hey Katherine, can you check the logs?",
        "corrected_phrase": "Hey Catherine, can you check the logs?"
},
    {
        "names": [
                "Katherine Bailey"
        ],
        "raw_phrase": "I'm looking at Catherine's latest update.",
        "corrected_phrase": "I'm looking at Katherine's latest update."
},
    {
        "names": [
                "Oksana Harris",
                "Teresa Rogers",
                "Sofia Anderson",
                "Katherine Davis"
        ],
        "raw_phrase": "Can you pass the message to Kathryn for me?",
        "corrected_phrase": "Can you pass the message to Katherine for me?"
},
    {
        "names": [
                "Sundar Davis",
                "Katherine Phillips",
                "Wei Morales"
        ],
        "raw_phrase": "I need to discuss the roadmap with Kathryn.",
        "corrected_phrase": "I need to discuss the roadmap with Katherine."
},
    {
        "names": [
                "Jon Nguyen",
                "Katherine Smith",
                "Chiwetel Patel"
        ],
        "raw_phrase": "Kathryn mentioned the deadline was moved.",
        "corrected_phrase": "Katherine mentioned the deadline was moved."
},
    {
        "names": [
                "Katherine Nelson",
                "Teresa Adams"
        ],
        "raw_phrase": "Kathryn is the one who originally wrote this script.",
        "corrected_phrase": "Katherine is the one who originally wrote this script."
},
    {
        "names": [
                "Katherine Murphy",
                "Hassan Jackson"
        ],
        "raw_phrase": "We should get some feedback from Kathryn on this.",
        "corrected_phrase": "We should get some feedback from Katherine on this."
},
    {
        "names": [
                "Kathryn Singh"
        ],
        "raw_phrase": "Hey Katherine, can you check the logs?",
        "corrected_phrase": "Hey Kathryn, can you check the logs?"
},
    {
        "names": [
                "Katherine Mitchell"
        ],
        "raw_phrase": "I'm looking at Kathryn's latest update.",
        "corrected_phrase": "I'm looking at Katherine's latest update."
},
    {
        "names": [
                "Katherine Taylor",
                "Yingbo Turner",
                "Vivian Green"
        ],
        "raw_phrase": "Katharine is the one who originally wrote this script.",
        "corrected_phrase": "Katherine is the one who originally wrote this script."
},
    {
        "names": [
                "Jon Carter",
                "Katherine Morales"
        ],
        "raw_phrase": "Wait for Katharine before starting the meeting.",
        "corrected_phrase": "Wait for Katherine before starting the meeting."
},
    {
        "names": [
                "Arjun Scott",
                "Katherine Scott",
                "Claire Rossi",
                "Katarina Rogers",
                "Qasim Harris"
        ],
        "raw_phrase": "Katharine is currently out of office until Monday.",
        "corrected_phrase": "Katherine is currently out of office until Monday."
},
    {
        "names": [
                "Krysten Carter",
                "Eric Rogers",
                "Sofia Martin",
                "Megan Collins",
                "Katherine King"
        ],
        "raw_phrase": "I'll ask Katharine to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Katherine to walk us through the deployment process."
},
    {
        "names": [
                "Katarina Bailey",
                "Rachael Smith",
                "Katherine Taylor",
                "Pavel Turner"
        ],
        "raw_phrase": "Is Katharine on the call?",
        "corrected_phrase": "Is Katherine on the call?"
},
    {
        "names": [
                "Katharine Peterson"
        ],
        "raw_phrase": "Hey Katherine, can you check the logs?",
        "corrected_phrase": "Hey Katharine, can you check the logs?"
},
    {
        "names": [
                "Katherine Khan"
        ],
        "raw_phrase": "I'm looking at Katharine's latest update.",
        "corrected_phrase": "I'm looking at Katherine's latest update."
},
    {
        "names": [
                "Krysten Jones",
                "Thierry Thompson",
                "Sofia Williams"
        ],
        "raw_phrase": "Is Kristen joining the happy hour tonight?",
        "corrected_phrase": "Is Krysten joining the happy hour tonight?"
},
    {
        "names": [
                "Krysten Lefebvre",
                "Caitlin Carter",
                "Yingbo Reed"
        ],
        "raw_phrase": "Did Kristen send the report yet?",
        "corrected_phrase": "Did Krysten send the report yet?"
},
    {
        "names": [
                "Caitlin Martinez",
                "Domhnall Young",
                "Krysten Scott"
        ],
        "raw_phrase": "Kristen has a lot of experience with React.",
        "corrected_phrase": "Krysten has a lot of experience with React."
},
    {
        "names": [
                "Juliet Campbell",
                "Chiwetel Edwards",
                "Krysten Morgan"
        ],
        "raw_phrase": "I'll coordinate the meeting with Kristen.",
        "corrected_phrase": "I'll coordinate the meeting with Krysten."
},
    {
        "names": [
                "Scarlett Young",
                "Krysten Williams"
        ],
        "raw_phrase": "Did Kristen catch that error in the logs?",
        "corrected_phrase": "Did Krysten catch that error in the logs?"
},
    {
        "names": [
                "Kristen Anderson"
        ],
        "raw_phrase": "Hey Krysten, can you check the logs?",
        "corrected_phrase": "Hey Kristen, can you check the logs?"
},
    {
        "names": [
                "Krysten Phillips"
        ],
        "raw_phrase": "I'm looking at Kristen's latest update.",
        "corrected_phrase": "I'm looking at Krysten's latest update."
},
    {
        "names": [
                "Krysten Singh",
                "Sanjay Morgan"
        ],
        "raw_phrase": "I'll ask Kristin to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Krysten to walk us through the deployment process."
},
    {
        "names": [
                "Krysten Roberts",
                "Krysten Ramirez",
                "Gwenyth Scott",
                "Li Patel"
        ],
        "raw_phrase": "Kristin is the point of contact for this.",
        "corrected_phrase": "Krysten is the point of contact for this."
},
    {
        "names": [
                "Krysten Williams",
                "Nikolas Tan",
                "Zack Carter",
                "Yosef Singh"
        ],
        "raw_phrase": "Has Kristin updated their ticket?",
        "corrected_phrase": "Has Krysten updated their ticket?"
},
    {
        "names": [
                "Niamh King",
                "Krysten Baker",
                "Sundar Khan",
                "Fatima Patel"
        ],
        "raw_phrase": "Has Kristin updated their ticket?",
        "corrected_phrase": "Has Krysten updated their ticket?"
},
    {
        "names": [
                "Bharath Patel",
                "Krysten Kim"
        ],
        "raw_phrase": "Kristin mentioned the deadline was moved.",
        "corrected_phrase": "Krysten mentioned the deadline was moved."
},
    {
        "names": [
                "Kristin Miller"
        ],
        "raw_phrase": "Hey Krysten, can you check the logs?",
        "corrected_phrase": "Hey Kristin, can you check the logs?"
},
    {
        "names": [
                "Krysten Torres"
        ],
        "raw_phrase": "I'm looking at Kristin's latest update.",
        "corrected_phrase": "I'm looking at Krysten's latest update."
},
    {
        "names": [
                "Jon Williams",
                "Lukas Miller",
                "Sundar Taylor"
        ],
        "raw_phrase": "Lucas is taking the lead on the frontend refactor.",
        "corrected_phrase": "Lukas is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Nikolas Singh",
                "Hiroshi Moore",
                "Lukas Jackson"
        ],
        "raw_phrase": "I'll follow up with Lucas after the meeting.",
        "corrected_phrase": "I'll follow up with Lukas after the meeting."
},
    {
        "names": [
                "Damian Thompson",
                "Dwyane Martin",
                "Lukas Schmidt"
        ],
        "raw_phrase": "Please send the invite to Lucas.",
        "corrected_phrase": "Please send the invite to Lukas."
},
    {
        "names": [
                "Giuseppe Edwards",
                "Aimee Adams",
                "Lukas Morris"
        ],
        "raw_phrase": "Lucas is the best person to talk to about this.",
        "corrected_phrase": "Lukas is the best person to talk to about this."
},
    {
        "names": [
                "Hassan Davis",
                "Lukas Cooper"
        ],
        "raw_phrase": "Lucas has a lot of experience with React.",
        "corrected_phrase": "Lukas has a lot of experience with React."
},
    {
        "names": [
                "Lucas Morris"
        ],
        "raw_phrase": "Hey Lukas, can you check the logs?",
        "corrected_phrase": "Hey Lucas, can you check the logs?"
},
    {
        "names": [
                "Lukas Martinez"
        ],
        "raw_phrase": "I'm looking at Lucas's latest update.",
        "corrected_phrase": "I'm looking at Lukas's latest update."
},
    {
        "names": [
                "Scarlett Jones",
                "Katarina Harris",
                "Priya Hill",
                "Marc Lee",
                "Qasim Garcia"
        ],
        "raw_phrase": "Mark is taking the lead on the frontend refactor.",
        "corrected_phrase": "Marc is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Marc Parker",
                "Scarlett Santos",
                "Arjun Morales"
        ],
        "raw_phrase": "Mark is presenting their findings at the all-hands.",
        "corrected_phrase": "Marc is presenting their findings at the all-hands."
},
    {
        "names": [
                "Marc Cook",
                "Mathew Rossi"
        ],
        "raw_phrase": "I'll ask Mark to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Marc to walk us through the deployment process."
},
    {
        "names": [
                "Nikolas Parker",
                "Jon Morales",
                "Marc Morris",
                "Ulysses Ivanov",
                "Marc Collins"
        ],
        "raw_phrase": "We should get some feedback from Mark on this.",
        "corrected_phrase": "We should get some feedback from Marc on this."
},
    {
        "names": [
                "Abhishek Rossi",
                "Qasim Jones",
                "Elisabeth Singh",
                "Marc Lefebvre",
                "Oksana Roberts"
        ],
        "raw_phrase": "Mark's PR is ready for review.",
        "corrected_phrase": "Marc's PR is ready for review."
},
    {
        "names": [
                "Mark Lefebvre"
        ],
        "raw_phrase": "Hey Marc, can you check the logs?",
        "corrected_phrase": "Hey Mark, can you check the logs?"
},
    {
        "names": [
                "Marc Johnson"
        ],
        "raw_phrase": "I'm looking at Mark's latest update.",
        "corrected_phrase": "I'm looking at Marc's latest update."
},
    {
        "names": [
                "Rhaenyra Silva",
                "Mei Reed",
                "Sundar Roberts",
                "Mathew Parker",
                "Zhi Nguyen"
        ],
        "raw_phrase": "Did Matthew mention anything about the budget?",
        "corrected_phrase": "Did Mathew mention anything about the budget?"
},
    {
        "names": [
                "Mathew Stewart",
                "Lukas Scott",
                "Antony Scott",
                "Zack Green",
                "Mathew Evans"
        ],
        "raw_phrase": "Is Matthew joining the happy hour tonight?",
        "corrected_phrase": "Is Mathew joining the happy hour tonight?"
},
    {
        "names": [
                "Mathew Bailey",
                "Mikhail Carter"
        ],
        "raw_phrase": "Matthew is taking the lead on the frontend refactor.",
        "corrected_phrase": "Mathew is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Antony Thomas",
                "Mathew Rodriguez"
        ],
        "raw_phrase": "Has Matthew updated their ticket?",
        "corrected_phrase": "Has Mathew updated their ticket?"
},
    {
        "names": [
                "Lukas Morgan",
                "Beatrix Jones",
                "Mathew Lefebvre"
        ],
        "raw_phrase": "Matthew is taking the lead on the frontend refactor.",
        "corrected_phrase": "Mathew is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Matthew Rogers"
        ],
        "raw_phrase": "Hey Mathew, can you check the logs?",
        "corrected_phrase": "Hey Matthew, can you check the logs?"
},
    {
        "names": [
                "Mathew Cooper"
        ],
        "raw_phrase": "I'm looking at Matthew's latest update.",
        "corrected_phrase": "I'm looking at Mathew's latest update."
},
    {
        "names": [
                "Hassan Cooper",
                "Megan Parker"
        ],
        "raw_phrase": "Please make sure Meagan has access to the repository.",
        "corrected_phrase": "Please make sure Megan has access to the repository."
},
    {
        "names": [
                "Niamh Schmidt",
                "Megan Lefebvre"
        ],
        "raw_phrase": "I saw a comment from Meagan on the design doc.",
        "corrected_phrase": "I saw a comment from Megan on the design doc."
},
    {
        "names": [
                "Megan Rossi",
                "Priya Brown",
                "Domhnall Martinez"
        ],
        "raw_phrase": "Meagan is the one who originally wrote this script.",
        "corrected_phrase": "Megan is the one who originally wrote this script."
},
    {
        "names": [
                "Eric Reed",
                "Megan Nelson",
                "Eric Ramirez"
        ],
        "raw_phrase": "I saw a comment from Meagan on the design doc.",
        "corrected_phrase": "I saw a comment from Megan on the design doc."
},
    {
        "names": [
                "Beatrix Moore",
                "Sofia Mitchell",
                "Megan Evans",
                "Mathew Nguyen",
                "Abhishek Patel"
        ],
        "raw_phrase": "I'll check the calendar to see when Meagan is free.",
        "corrected_phrase": "I'll check the calendar to see when Megan is free."
},
    {
        "names": [
                "Meagan Thompson"
        ],
        "raw_phrase": "Hey Megan, can you check the logs?",
        "corrected_phrase": "Hey Meagan, can you check the logs?"
},
    {
        "names": [
                "Megan Khan"
        ],
        "raw_phrase": "I'm looking at Meagan's latest update.",
        "corrected_phrase": "I'm looking at Megan's latest update."
},
    {
        "names": [
                "Megan Morgan",
                "Fatima Ivanov",
                "Domhnall Murphy",
                "Sara Campbell",
                "Dwyane Moore"
        ],
        "raw_phrase": "Meghan suggested we use a different database.",
        "corrected_phrase": "Megan suggested we use a different database."
},
    {
        "names": [
                "Megan Ramirez",
                "Hanna Kim",
                "Yuki Silva",
                "Juliet White",
                "Antony Taylor"
        ],
        "raw_phrase": "We should get some feedback from Meghan on this.",
        "corrected_phrase": "We should get some feedback from Megan on this."
},
    {
        "names": [
                "Barbra Williams",
                "Claire Thomas",
                "Megan Jackson"
        ],
        "raw_phrase": "Did Meghan send the report yet?",
        "corrected_phrase": "Did Megan send the report yet?"
},
    {
        "names": [
                "Sara Thomas",
                "Megan Dubois"
        ],
        "raw_phrase": "I need to discuss the roadmap with Meghan.",
        "corrected_phrase": "I need to discuss the roadmap with Megan."
},
    {
        "names": [
                "Kah Mun Morris",
                "Megan Cook"
        ],
        "raw_phrase": "Ask Meghan if they have the login for the staging server.",
        "corrected_phrase": "Ask Megan if they have the login for the staging server."
},
    {
        "names": [
                "Meghan Torres"
        ],
        "raw_phrase": "Hey Megan, can you check the logs?",
        "corrected_phrase": "Hey Meghan, can you check the logs?"
},
    {
        "names": [
                "Megan Smith"
        ],
        "raw_phrase": "I'm looking at Meghan's latest update.",
        "corrected_phrase": "I'm looking at Megan's latest update."
},
    {
        "names": [
                "Damian Adams",
                "Mikhail Reed"
        ],
        "raw_phrase": "Michael is first on the standup list.",
        "corrected_phrase": "Mikhail is first on the standup list."
},
    {
        "names": [
                "Bharath Morgan",
                "Mikhail Schmidt",
                "Mei M\u00fcller",
                "Saoirse Smith"
        ],
        "raw_phrase": "Ask Michael if they have the login for the staging server.",
        "corrected_phrase": "Ask Mikhail if they have the login for the staging server."
},
    {
        "names": [
                "Jian Morales",
                "Mikhail Patel"
        ],
        "raw_phrase": "Did Michael mention anything about the budget?",
        "corrected_phrase": "Did Mikhail mention anything about the budget?"
},
    {
        "names": [
                "Stephen Thomas",
                "Caiming Williams",
                "Chen Cook",
                "Mikhail Brown",
                "Hanna Evans"
        ],
        "raw_phrase": "I sent the draft to Michael for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Mikhail for some initial thoughts."
},
    {
        "names": [
                "Mikhail Morris",
                "Rhaenyra Brown",
                "Caiming Baker",
                "Hiroshi Nelson",
                "Caiming Johnson"
        ],
        "raw_phrase": "I'll follow up with Michael after the meeting.",
        "corrected_phrase": "I'll follow up with Mikhail after the meeting."
},
    {
        "names": [
                "Michael M\u00fcller"
        ],
        "raw_phrase": "Hey Mikhail, can you check the logs?",
        "corrected_phrase": "Hey Michael, can you check the logs?"
},
    {
        "names": [
                "Mikhail Stewart"
        ],
        "raw_phrase": "I'm looking at Michael's latest update.",
        "corrected_phrase": "I'm looking at Mikhail's latest update."
},
    {
        "names": [
                "Nikolas Nguyen",
                "Nikolas Murphy",
                "Xavier Harris"
        ],
        "raw_phrase": "Can you pass the message to Nicholas for me?",
        "corrected_phrase": "Can you pass the message to Nikolas for me?"
},
    {
        "names": [
                "Zhi Schmidt",
                "Yosef Scott",
                "Nikolas Cook"
        ],
        "raw_phrase": "Is Nicholas on the call?",
        "corrected_phrase": "Is Nikolas on the call?"
},
    {
        "names": [
                "Aarav Murphy",
                "Nikolas Tan",
                "Geoff Cooper"
        ],
        "raw_phrase": "Nicholas is first on the standup list.",
        "corrected_phrase": "Nikolas is first on the standup list."
},
    {
        "names": [
                "Chiwetel Edwards",
                "Aimee Tan",
                "Nikolas Murphy",
                "Rhaenyra Evans"
        ],
        "raw_phrase": "Did Nicholas send the report yet?",
        "corrected_phrase": "Did Nikolas send the report yet?"
},
    {
        "names": [
                "Ishaan Peterson",
                "Abhishek Moore",
                "Wei Reed",
                "Aarav Anderson",
                "Nikolas Tan"
        ],
        "raw_phrase": "Has Nicholas reviewed the security policy yet?",
        "corrected_phrase": "Has Nikolas reviewed the security policy yet?"
},
    {
        "names": [
                "Nicholas Ramirez"
        ],
        "raw_phrase": "Hey Nikolas, can you check the logs?",
        "corrected_phrase": "Hey Nicholas, can you check the logs?"
},
    {
        "names": [
                "Nikolas Brown"
        ],
        "raw_phrase": "I'm looking at Nicholas's latest update.",
        "corrected_phrase": "I'm looking at Nikolas's latest update."
},
    {
        "names": [
                "Nikolas Nelson",
                "Yingbo Morales",
                "Phillip Anderson"
        ],
        "raw_phrase": "I'm waiting on Nickolas to approve the changes.",
        "corrected_phrase": "I'm waiting on Nikolas to approve the changes."
},
    {
        "names": [
                "Shawn Kim",
                "Juliet Brown",
                "Wei Patel",
                "Nikolas Young"
        ],
        "raw_phrase": "Can Nickolas join the sync tomorrow morning?",
        "corrected_phrase": "Can Nikolas join the sync tomorrow morning?"
},
    {
        "names": [
                "Xavier Patel",
                "Nikolas Khan",
                "Katherine Bailey"
        ],
        "raw_phrase": "Nickolas is presenting their findings at the all-hands.",
        "corrected_phrase": "Nikolas is presenting their findings at the all-hands."
},
    {
        "names": [
                "Mateo Turner",
                "Mathew Adams",
                "Nikolas Santos"
        ],
        "raw_phrase": "I'll sync with Nickolas later today.",
        "corrected_phrase": "I'll sync with Nikolas later today."
},
    {
        "names": [
                "Nikolas Bailey",
                "Yuki Moore",
                "Antony Patel"
        ],
        "raw_phrase": "I need to discuss the roadmap with Nickolas.",
        "corrected_phrase": "I need to discuss the roadmap with Nikolas."
},
    {
        "names": [
                "Nickolas Cooper"
        ],
        "raw_phrase": "Hey Nikolas, can you check the logs?",
        "corrected_phrase": "Hey Nickolas, can you check the logs?"
},
    {
        "names": [
                "Nikolas Scott"
        ],
        "raw_phrase": "I'm looking at Nickolas's latest update.",
        "corrected_phrase": "I'm looking at Nikolas's latest update."
},
    {
        "names": [
                "Sofia Dubois",
                "Phillip M\u00fcller",
                "Zainab Hill",
                "Wei Collins"
        ],
        "raw_phrase": "I'll double check the numbers with Philip.",
        "corrected_phrase": "I'll double check the numbers with Phillip."
},
    {
        "names": [
                "Aarav White",
                "Chen Bailey",
                "Jon Phillips",
                "Phillip Baker",
                "Mikhail Edwards"
        ],
        "raw_phrase": "Please send the invite to Philip.",
        "corrected_phrase": "Please send the invite to Phillip."
},
    {
        "names": [
                "Ishaan Edwards",
                "Phillip King",
                "Srini Harris",
                "Bryan Thompson"
        ],
        "raw_phrase": "Please send the invite to Philip.",
        "corrected_phrase": "Please send the invite to Phillip."
},
    {
        "names": [
                "Yosef Nelson",
                "Phillip Carter",
                "Arjun Morgan",
                "Juliet Young"
        ],
        "raw_phrase": "I sent the draft to Philip for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Phillip for some initial thoughts."
},
    {
        "names": [
                "Kah Mun Thomas",
                "Mikhail Torres",
                "Phillip Rogers",
                "Stephen Campbell",
                "Claire Edwards"
        ],
        "raw_phrase": "Philip is first on the standup list.",
        "corrected_phrase": "Phillip is first on the standup list."
},
    {
        "names": [
                "Philip Green"
        ],
        "raw_phrase": "Hey Phillip, can you check the logs?",
        "corrected_phrase": "Hey Philip, can you check the logs?"
},
    {
        "names": [
                "Phillip Martin"
        ],
        "raw_phrase": "I'm looking at Philip's latest update.",
        "corrected_phrase": "I'm looking at Phillip's latest update."
},
    {
        "names": [
                "Rachael Moore",
                "Hiroshi Thomas"
        ],
        "raw_phrase": "Has Rachel reviewed the security policy yet?",
        "corrected_phrase": "Has Rachael reviewed the security policy yet?"
},
    {
        "names": [
                "Lukas Jones",
                "Hiroshi Evans",
                "Rachael Carter"
        ],
        "raw_phrase": "Could you take a look at the PR from Rachel?",
        "corrected_phrase": "Could you take a look at the PR from Rachael?"
},
    {
        "names": [
                "Yosef Rodriguez",
                "Geoff Anderson",
                "Rachael Parker",
                "Susannah Santos"
        ],
        "raw_phrase": "Is Rachel familiar with this part of the codebase?",
        "corrected_phrase": "Is Rachael familiar with this part of the codebase?"
},
    {
        "names": [
                "Dwyane Parker",
                "Scarlett Mitchell",
                "Niamh Baker",
                "Antony Bailey",
                "Rachael Jones"
        ],
        "raw_phrase": "I'll sync with Rachel later today.",
        "corrected_phrase": "I'll sync with Rachael later today."
},
    {
        "names": [
                "Chiwetel Edwards",
                "Rachael Harris",
                "Isabelle Taylor",
                "Damian Khan"
        ],
        "raw_phrase": "Please make sure Rachel has access to the repository.",
        "corrected_phrase": "Please make sure Rachael has access to the repository."
},
    {
        "names": [
                "Rachel Morris"
        ],
        "raw_phrase": "Hey Rachael, can you check the logs?",
        "corrected_phrase": "Hey Rachel, can you check the logs?"
},
    {
        "names": [
                "Rachael Dubois"
        ],
        "raw_phrase": "I'm looking at Rachel's latest update.",
        "corrected_phrase": "I'm looking at Rachael's latest update."
},
    {
        "names": [
                "Susannah Dubois",
                "Sara Bailey",
                "Giuseppe Martin"
        ],
        "raw_phrase": "Sarah suggested a few improvements to the UI.",
        "corrected_phrase": "Sara suggested a few improvements to the UI."
},
    {
        "names": [
                "Zhi Adams",
                "Sara Nguyen"
        ],
        "raw_phrase": "I sent the draft to Sarah for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Sara for some initial thoughts."
},
    {
        "names": [
                "Oksana Jackson",
                "Sara Jackson",
                "Caitlin Ramirez"
        ],
        "raw_phrase": "Please send the invite to Sarah.",
        "corrected_phrase": "Please send the invite to Sara."
},
    {
        "names": [
                "Niamh Thomas",
                "Priya Stewart",
                "Sara Rogers"
        ],
        "raw_phrase": "I'll double check the numbers with Sarah.",
        "corrected_phrase": "I'll double check the numbers with Sara."
},
    {
        "names": [
                "Sara Murphy",
                "Stephen Rossi"
        ],
        "raw_phrase": "Sarah found a bug in the production environment.",
        "corrected_phrase": "Sara found a bug in the production environment."
},
    {
        "names": [
                "Sarah Tan"
        ],
        "raw_phrase": "Hey Sara, can you check the logs?",
        "corrected_phrase": "Hey Sarah, can you check the logs?"
},
    {
        "names": [
                "Sara Ivanov"
        ],
        "raw_phrase": "I'm looking at Sarah's latest update.",
        "corrected_phrase": "I'm looking at Sara's latest update."
},
    {
        "names": [
                "Jian Mitchell",
                "Katherine Rogers",
                "Scarlett Turner",
                "Priya Morris",
                "Yosef Reed"
        ],
        "raw_phrase": "I'll sync with Scarlet later today.",
        "corrected_phrase": "I'll sync with Scarlett later today."
},
    {
        "names": [
                "Mikhail Campbell",
                "Scarlett Lee",
                "Scarlett Rogers",
                "Chen Johnson"
        ],
        "raw_phrase": "Scarlet mentioned the deadline was moved.",
        "corrected_phrase": "Scarlett mentioned the deadline was moved."
},
    {
        "names": [
                "Lukas Santos",
                "Scarlett Silva",
                "Niamh Young",
                "Beatrix Nguyen"
        ],
        "raw_phrase": "Scarlet is the best person to talk to about this.",
        "corrected_phrase": "Scarlett is the best person to talk to about this."
},
    {
        "names": [
                "Aimee Schmidt",
                "Zhi Carter",
                "Scarlett Peterson",
                "Vihaan Martinez"
        ],
        "raw_phrase": "I need to discuss the roadmap with Scarlet.",
        "corrected_phrase": "I need to discuss the roadmap with Scarlett."
},
    {
        "names": [
                "Bryan Johnson",
                "Beatrix Baker",
                "Alexey Rossi",
                "Yuki Patel",
                "Scarlett Kim"
        ],
        "raw_phrase": "Scarlet mentioned the deadline was moved.",
        "corrected_phrase": "Scarlett mentioned the deadline was moved."
},
    {
        "names": [
                "Scarlet Williams"
        ],
        "raw_phrase": "Hey Scarlett, can you check the logs?",
        "corrected_phrase": "Hey Scarlet, can you check the logs?"
},
    {
        "names": [
                "Scarlett Thompson"
        ],
        "raw_phrase": "I'm looking at Scarlet's latest update.",
        "corrected_phrase": "I'm looking at Scarlett's latest update."
},
    {
        "names": [
                "Shawn Reed",
                "Eric Thomas",
                "Claire Cook",
                "Niamh Nelson",
                "Qasim Miller"
        ],
        "raw_phrase": "Did Sean send the report yet?",
        "corrected_phrase": "Did Shawn send the report yet?"
},
    {
        "names": [
                "Jon Lee",
                "Shawn Rossi",
                "Kieran Scott",
                "Shawn Green",
                "Aimee Phillips"
        ],
        "raw_phrase": "Sean is first on the standup list.",
        "corrected_phrase": "Shawn is first on the standup list."
},
    {
        "names": [
                "Yingbo Phillips",
                "Shawn Evans",
                "Oleksandr Baker"
        ],
        "raw_phrase": "Can you pass the message to Sean for me?",
        "corrected_phrase": "Can you pass the message to Shawn for me?"
},
    {
        "names": [
                "Sanjay Edwards",
                "Sundar Anderson",
                "Rhaenyra Lee",
                "Shawn Adams",
                "Barbra Smith"
        ],
        "raw_phrase": "Please CC Sean on all future updates.",
        "corrected_phrase": "Please CC Shawn on all future updates."
},
    {
        "names": [
                "Shawn Mitchell",
                "Zack Bailey",
                "Hanna Mitchell"
        ],
        "raw_phrase": "Sean found a bug in the production environment.",
        "corrected_phrase": "Shawn found a bug in the production environment."
},
    {
        "names": [
                "Sean Reed"
        ],
        "raw_phrase": "Hey Shawn, can you check the logs?",
        "corrected_phrase": "Hey Sean, can you check the logs?"
},
    {
        "names": [
                "Shawn Roberts"
        ],
        "raw_phrase": "I'm looking at Sean's latest update.",
        "corrected_phrase": "I'm looking at Shawn's latest update."
},
    {
        "names": [
                "Gwenyth Nguyen",
                "Oksana Carter",
                "Scarlett Scott",
                "Shawn M\u00fcller",
                "Domhnall Green"
        ],
        "raw_phrase": "Shaun is the best person to talk to about this.",
        "corrected_phrase": "Shawn is the best person to talk to about this."
},
    {
        "names": [
                "Shawn Jones",
                "Alexey Williams"
        ],
        "raw_phrase": "Ask Shaun if they have the login for the staging server.",
        "corrected_phrase": "Ask Shawn if they have the login for the staging server."
},
    {
        "names": [
                "Shawn Rodriguez",
                "Scarlett Williams"
        ],
        "raw_phrase": "Shaun is the best person to talk to about this.",
        "corrected_phrase": "Shawn is the best person to talk to about this."
},
    {
        "names": [
                "Shawn Morris",
                "Domhnall Nelson",
                "Tomas Harris"
        ],
        "raw_phrase": "I'll sync with Shaun later today.",
        "corrected_phrase": "I'll sync with Shawn later today."
},
    {
        "names": [
                "Katherine Nelson",
                "Saoirse Harris",
                "Shawn Lefebvre",
                "Aarav Garcia"
        ],
        "raw_phrase": "Shaun is the best person to talk to about this.",
        "corrected_phrase": "Shawn is the best person to talk to about this."
},
    {
        "names": [
                "Shaun Nelson"
        ],
        "raw_phrase": "Hey Shawn, can you check the logs?",
        "corrected_phrase": "Hey Shaun, can you check the logs?"
},
    {
        "names": [
                "Shawn Rodriguez"
        ],
        "raw_phrase": "I'm looking at Shaun's latest update.",
        "corrected_phrase": "I'm looking at Shawn's latest update."
},
    {
        "names": [
                "Stephen Smith",
                "Stephen Moore"
        ],
        "raw_phrase": "Please make sure Steven has access to the repository.",
        "corrected_phrase": "Please make sure Stephen has access to the repository."
},
    {
        "names": [
                "Ishaan Tan",
                "Stephen Kim",
                "Megan Roberts"
        ],
        "raw_phrase": "Steven suggested a few improvements to the UI.",
        "corrected_phrase": "Stephen suggested a few improvements to the UI."
},
    {
        "names": [
                "Alexey Rossi",
                "Beatrix Campbell",
                "Stephen Young",
                "Nikolas Singh",
                "Arjun Harris"
        ],
        "raw_phrase": "Wait for Steven before starting the meeting.",
        "corrected_phrase": "Wait for Stephen before starting the meeting."
},
    {
        "names": [
                "Stephen Torres",
                "Kieran Ivanov",
                "Silvio Thompson",
                "Scarlett Garcia",
                "Srini Stewart"
        ],
        "raw_phrase": "Can Steven join the sync tomorrow morning?",
        "corrected_phrase": "Can Stephen join the sync tomorrow morning?"
},
    {
        "names": [
                "Susannah Nelson",
                "Mikhail Bailey",
                "Stephen Green",
                "Arjun Carter",
                "Scarlett Phillips"
        ],
        "raw_phrase": "Did Steven send the report yet?",
        "corrected_phrase": "Did Stephen send the report yet?"
},
    {
        "names": [
                "Steven Lefebvre"
        ],
        "raw_phrase": "Hey Stephen, can you check the logs?",
        "corrected_phrase": "Hey Steven, can you check the logs?"
},
    {
        "names": [
                "Stephen Scott"
        ],
        "raw_phrase": "I'm looking at Steven's latest update.",
        "corrected_phrase": "I'm looking at Stephen's latest update."
},
    {
        "names": [
                "Zainab Lefebvre",
                "Susannah Collins",
                "Arjun Ramirez"
        ],
        "raw_phrase": "Please send the invite to Susanna.",
        "corrected_phrase": "Please send the invite to Susannah."
},
    {
        "names": [
                "Caiming Patel",
                "Susannah Adams"
        ],
        "raw_phrase": "Please add Susanna to the email thread.",
        "corrected_phrase": "Please add Susannah to the email thread."
},
    {
        "names": [
                "Kieran Ramirez",
                "Fatima Nelson",
                "Susannah Garcia"
        ],
        "raw_phrase": "Please make sure Susanna has access to the repository.",
        "corrected_phrase": "Please make sure Susannah has access to the repository."
},
    {
        "names": [
                "Mateo Nelson",
                "Susannah Moore",
                "Teresa Murphy",
                "Aarav Parker"
        ],
        "raw_phrase": "Susanna is presenting their findings at the all-hands.",
        "corrected_phrase": "Susannah is presenting their findings at the all-hands."
},
    {
        "names": [
                "Sanjay Smith",
                "Bharath Scott",
                "Susannah Nguyen",
                "Saoirse Edwards",
                "Srini Morales"
        ],
        "raw_phrase": "Could you take a look at the PR from Susanna?",
        "corrected_phrase": "Could you take a look at the PR from Susannah?"
},
    {
        "names": [
                "Susanna Santos"
        ],
        "raw_phrase": "Hey Susannah, can you check the logs?",
        "corrected_phrase": "Hey Susanna, can you check the logs?"
},
    {
        "names": [
                "Susannah Collins"
        ],
        "raw_phrase": "I'm looking at Susanna's latest update.",
        "corrected_phrase": "I'm looking at Susannah's latest update."
},
    {
        "names": [
                "Chiwetel Lee",
                "Susannah Baker",
                "Isabelle Stewart",
                "Giuseppe Ivanov",
                "Mathew Harris"
        ],
        "raw_phrase": "Has Susan reviewed the security policy yet?",
        "corrected_phrase": "Has Susannah reviewed the security policy yet?"
},
    {
        "names": [
                "Wei Davis",
                "Susannah Dubois",
                "Geoff Morris",
                "Vihaan King"
        ],
        "raw_phrase": "I'll be working closely with Susan on this feature.",
        "corrected_phrase": "I'll be working closely with Susannah on this feature."
},
    {
        "names": [
                "Aimee Garcia",
                "Marc Peterson",
                "Geoff Young",
                "Susannah Morgan"
        ],
        "raw_phrase": "Please CC Susan on all future updates.",
        "corrected_phrase": "Please CC Susannah on all future updates."
},
    {
        "names": [
                "Susannah King",
                "Hanna Ivanov",
                "Pavel Nguyen"
        ],
        "raw_phrase": "Susan suggested a few improvements to the UI.",
        "corrected_phrase": "Susannah suggested a few improvements to the UI."
},
    {
        "names": [
                "Zainab Hill",
                "Wei Peterson",
                "Susannah Phillips"
        ],
        "raw_phrase": "I'll check the calendar to see when Susan is free.",
        "corrected_phrase": "I'll check the calendar to see when Susannah is free."
},
    {
        "names": [
                "Susan Peterson"
        ],
        "raw_phrase": "Hey Susannah, can you check the logs?",
        "corrected_phrase": "Hey Susan, can you check the logs?"
},
    {
        "names": [
                "Susannah Morales"
        ],
        "raw_phrase": "I'm looking at Susan's latest update.",
        "corrected_phrase": "I'm looking at Susannah's latest update."
},
    {
        "names": [
                "Teresa Morales",
                "Chen Adams",
                "Claire Cook",
                "Ulysses Rossi",
                "Oleksandr Campbell"
        ],
        "raw_phrase": "I think Theresa is handling the project.",
        "corrected_phrase": "I think Teresa is handling the project."
},
    {
        "names": [
                "Teresa Davis",
                "Yingbo Rossi"
        ],
        "raw_phrase": "Theresa is presenting their findings at the all-hands.",
        "corrected_phrase": "Teresa is presenting their findings at the all-hands."
},
    {
        "names": [
                "Wei Taylor",
                "Abhishek Thompson",
                "Teresa Jackson"
        ],
        "raw_phrase": "I'm going to grab a coffee with Theresa later.",
        "corrected_phrase": "I'm going to grab a coffee with Teresa later."
},
    {
        "names": [
                "Teresa Adams",
                "Tomas Roberts",
                "Krysten Cooper",
                "Susannah Martinez",
                "Lukas Brown"
        ],
        "raw_phrase": "Theresa is the point of contact for this.",
        "corrected_phrase": "Teresa is the point of contact for this."
},
    {
        "names": [
                "Bharath Silva",
                "Teresa Rodriguez",
                "Hassan Baker",
                "Zhi Murphy"
        ],
        "raw_phrase": "Theresa is taking the lead on the frontend refactor.",
        "corrected_phrase": "Teresa is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Theresa Turner"
        ],
        "raw_phrase": "Hey Teresa, can you check the logs?",
        "corrected_phrase": "Hey Theresa, can you check the logs?"
},
    {
        "names": [
                "Teresa Garcia"
        ],
        "raw_phrase": "I'm looking at Theresa's latest update.",
        "corrected_phrase": "I'm looking at Teresa's latest update."
},
    {
        "names": [
                "Xavier Reed",
                "Susannah Lee",
                "Fatima Campbell",
                "Tomas Jones",
                "Kah Mun Johnson"
        ],
        "raw_phrase": "Thomas's PR is ready for review.",
        "corrected_phrase": "Tomas's PR is ready for review."
},
    {
        "names": [
                "Tomas Patel",
                "Stephen Rogers",
                "Hanna Smith"
        ],
        "raw_phrase": "Thomas has a lot of experience with React.",
        "corrected_phrase": "Tomas has a lot of experience with React."
},
    {
        "names": [
                "Abhishek Collins",
                "Claire Martin",
                "Tomas Lefebvre",
                "Sofia Evans"
        ],
        "raw_phrase": "Check with Thomas about the API credentials.",
        "corrected_phrase": "Check with Tomas about the API credentials."
},
    {
        "names": [
                "Abhishek Khan",
                "Tomas Peterson"
        ],
        "raw_phrase": "Please add Thomas to the email thread.",
        "corrected_phrase": "Please add Tomas to the email thread."
},
    {
        "names": [
                "Tomas Parker",
                "Dwyane Nguyen"
        ],
        "raw_phrase": "Thomas is leading the research on machine learning.",
        "corrected_phrase": "Tomas is leading the research on machine learning."
},
    {
        "names": [
                "Thomas Rogers"
        ],
        "raw_phrase": "Hey Tomas, can you check the logs?",
        "corrected_phrase": "Hey Thomas, can you check the logs?"
},
    {
        "names": [
                "Tomas Nelson"
        ],
        "raw_phrase": "I'm looking at Thomas's latest update.",
        "corrected_phrase": "I'm looking at Tomas's latest update."
},
    {
        "names": [
                "Nikolas Young",
                "Vivian Patel"
        ],
        "raw_phrase": "Vivien is the one who originally wrote this script.",
        "corrected_phrase": "Vivian is the one who originally wrote this script."
},
    {
        "names": [
                "Vivian Lee",
                "Susannah Morales",
                "Dmitry Ramirez"
        ],
        "raw_phrase": "Please add Vivien to the email thread.",
        "corrected_phrase": "Please add Vivian to the email thread."
},
    {
        "names": [
                "Vivian Cook",
                "Geoff Taylor",
                "Priya Hill"
        ],
        "raw_phrase": "Please make sure Vivien has access to the repository.",
        "corrected_phrase": "Please make sure Vivian has access to the repository."
},
    {
        "names": [
                "Yosef Morgan",
                "Krysten Baker",
                "Vivian Williams",
                "Bryan Hill",
                "Scarlett Martin"
        ],
        "raw_phrase": "Wait for Vivien before starting the meeting.",
        "corrected_phrase": "Wait for Vivian before starting the meeting."
},
    {
        "names": [
                "Jon Turner",
                "Vivian Martinez",
                "Wei Carter",
                "Chiwetel Rodriguez"
        ],
        "raw_phrase": "Vivien has a lot of experience with React.",
        "corrected_phrase": "Vivian has a lot of experience with React."
},
    {
        "names": [
                "Vivien Thompson"
        ],
        "raw_phrase": "Hey Vivian, can you check the logs?",
        "corrected_phrase": "Hey Vivien, can you check the logs?"
},
    {
        "names": [
                "Vivian Garcia"
        ],
        "raw_phrase": "I'm looking at Vivien's latest update.",
        "corrected_phrase": "I'm looking at Vivian's latest update."
},
    {
        "names": [
                "Chen Nelson",
                "Kieran Anderson",
                "Vivian White",
                "Yosef Rogers",
                "Yuki Miller"
        ],
        "raw_phrase": "Is Vivianne joining the happy hour tonight?",
        "corrected_phrase": "Is Vivian joining the happy hour tonight?"
},
    {
        "names": [
                "Oleksandr Rossi",
                "Vivian Khan",
                "Lukas Lefebvre"
        ],
        "raw_phrase": "We should get some feedback from Vivianne on this.",
        "corrected_phrase": "We should get some feedback from Vivian on this."
},
    {
        "names": [
                "Sara Nelson",
                "Eric White",
                "Gwenyth Schmidt",
                "Vivian Patel"
        ],
        "raw_phrase": "Did Vivianne send the report yet?",
        "corrected_phrase": "Did Vivian send the report yet?"
},
    {
        "names": [
                "Ulysses Smith",
                "Yosef King",
                "Hanna Peterson",
                "Vivian Thompson"
        ],
        "raw_phrase": "I need to discuss the roadmap with Vivianne.",
        "corrected_phrase": "I need to discuss the roadmap with Vivian."
},
    {
        "names": [
                "Caiming Mitchell",
                "Dmitry Adams",
                "Oksana Cook",
                "Vivian Davis"
        ],
        "raw_phrase": "Check with Vivianne about the API credentials.",
        "corrected_phrase": "Check with Vivian about the API credentials."
},
    {
        "names": [
                "Vivianne Dubois"
        ],
        "raw_phrase": "Hey Vivian, can you check the logs?",
        "corrected_phrase": "Hey Vivianne, can you check the logs?"
},
    {
        "names": [
                "Vivian Peterson"
        ],
        "raw_phrase": "I'm looking at Vivianne's latest update.",
        "corrected_phrase": "I'm looking at Vivian's latest update."
},
    {
        "names": [
                "Zack Parker",
                "Mei Morris"
        ],
        "raw_phrase": "Can you ask Zach to join the Zoom?",
        "corrected_phrase": "Can you ask Zack to join the Zoom?"
},
    {
        "names": [
                "Yosef Reed",
                "Kieran Khan",
                "Yingbo Turner",
                "Zack Garcia",
                "Elisabeth Rogers"
        ],
        "raw_phrase": "Check with Zach about the API credentials.",
        "corrected_phrase": "Check with Zack about the API credentials."
},
    {
        "names": [
                "Shawn Parker",
                "Qasim Williams",
                "Zack Carter",
                "Oksana Parker"
        ],
        "raw_phrase": "I'll be working closely with Zach on this feature.",
        "corrected_phrase": "I'll be working closely with Zack on this feature."
},
    {
        "names": [
                "Claire Bailey",
                "Zack Phillips"
        ],
        "raw_phrase": "Zach is the point of contact for this.",
        "corrected_phrase": "Zack is the point of contact for this."
},
    {
        "names": [
                "Zack M\u00fcller",
                "Saoirse Scott"
        ],
        "raw_phrase": "I think Zach is handling the project.",
        "corrected_phrase": "I think Zack is handling the project."
},
    {
        "names": [
                "Zach Nelson"
        ],
        "raw_phrase": "Hey Zack, can you check the logs?",
        "corrected_phrase": "Hey Zach, can you check the logs?"
},
    {
        "names": [
                "Zack Lefebvre"
        ],
        "raw_phrase": "I'm looking at Zach's latest update.",
        "corrected_phrase": "I'm looking at Zack's latest update."
},
    {
        "names": [
                "Fatima Phillips",
                "Zack Scott",
                "Vivian Brown",
                "Chen Adams",
                "Dmitry Miller"
        ],
        "raw_phrase": "Please make sure Zachary has access to the repository.",
        "corrected_phrase": "Please make sure Zack has access to the repository."
},
    {
        "names": [
                "Zack Silva",
                "Oksana Morales",
                "Wei Baker",
                "Silvio Baker",
                "Kieran Collins"
        ],
        "raw_phrase": "Zachary is leading the research on machine learning.",
        "corrected_phrase": "Zack is leading the research on machine learning."
},
    {
        "names": [
                "Oleksandr Harris",
                "Sundar Lefebvre",
                "Zack Carter"
        ],
        "raw_phrase": "Is Zachary familiar with this part of the codebase?",
        "corrected_phrase": "Is Zack familiar with this part of the codebase?"
},
    {
        "names": [
                "Mathew Jones",
                "Zack Martin",
                "Rhaenyra Carter"
        ],
        "raw_phrase": "Please add Zachary to the email thread.",
        "corrected_phrase": "Please add Zack to the email thread."
},
    {
        "names": [
                "Zack Nguyen",
                "Gwenyth Collins",
                "Aimee Martin",
                "Isabelle Lee",
                "Beatrix Garcia"
        ],
        "raw_phrase": "Is Zachary on the call?",
        "corrected_phrase": "Is Zack on the call?"
},
    {
        "names": [
                "Zachary Campbell"
        ],
        "raw_phrase": "Hey Zack, can you check the logs?",
        "corrected_phrase": "Hey Zachary, can you check the logs?"
},
    {
        "names": [
                "Zack Nguyen"
        ],
        "raw_phrase": "I'm looking at Zachary's latest update.",
        "corrected_phrase": "I'm looking at Zack's latest update."
},
    {
        "names": [
                "Sofia White",
                "Megan Evans",
                "Alexey Miller",
                "Aarav Smith",
                "Abhishek Jackson"
        ],
        "raw_phrase": "Can you ask Alexei to join the Zoom?",
        "corrected_phrase": "Can you ask Alexey to join the Zoom?"
},
    {
        "names": [
                "Niamh Carter",
                "Alexey Rogers",
                "Wei Dubois",
                "Caitlin Carter",
                "Hiroshi Mitchell"
        ],
        "raw_phrase": "I'm going to grab a coffee with Alexei later.",
        "corrected_phrase": "I'm going to grab a coffee with Alexey later."
},
    {
        "names": [
                "Sanjay Dubois",
                "Megan Santos",
                "Lukas Lee",
                "Alexey Martin",
                "Rhaenyra Nguyen"
        ],
        "raw_phrase": "Alexei has a lot of experience with React.",
        "corrected_phrase": "Alexey has a lot of experience with React."
},
    {
        "names": [
                "Aarav Evans",
                "Alexey Stewart",
                "Dmitry King",
                "Geoff Nguyen",
                "Shawn Bailey"
        ],
        "raw_phrase": "I sent the draft to Alexei for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Alexey for some initial thoughts."
},
    {
        "names": [
                "Saoirse Mitchell",
                "Dwyane Khan",
                "Alexey Silva"
        ],
        "raw_phrase": "Alexei is taking the lead on the frontend refactor.",
        "corrected_phrase": "Alexey is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Alexei Parker"
        ],
        "raw_phrase": "Hey Alexey, can you check the logs?",
        "corrected_phrase": "Hey Alexei, can you check the logs?"
},
    {
        "names": [
                "Alexey Anderson"
        ],
        "raw_phrase": "I'm looking at Alexei's latest update.",
        "corrected_phrase": "I'm looking at Alexey's latest update."
},
    {
        "names": [
                "Phillip Kim",
                "Sara Cooper",
                "Rhaenyra Phillips",
                "Hassan Scott",
                "Alexey Scott"
        ],
        "raw_phrase": "I'm waiting on Alexi to approve the changes.",
        "corrected_phrase": "I'm waiting on Alexey to approve the changes."
},
    {
        "names": [
                "Mei Martin",
                "Alexey Lee"
        ],
        "raw_phrase": "I'm going to grab a coffee with Alexi later.",
        "corrected_phrase": "I'm going to grab a coffee with Alexey later."
},
    {
        "names": [
                "Alexey Stewart",
                "Rachael Stewart",
                "Abhishek Parker",
                "Fatima Martin",
                "Sundar Garcia"
        ],
        "raw_phrase": "I'll double check the numbers with Alexi.",
        "corrected_phrase": "I'll double check the numbers with Alexey."
},
    {
        "names": [
                "Kieran Johnson",
                "Alexey Green",
                "Yosef Martinez",
                "Aarav Patel"
        ],
        "raw_phrase": "Did Alexi catch that error in the logs?",
        "corrected_phrase": "Did Alexey catch that error in the logs?"
},
    {
        "names": [
                "Stephen Garcia",
                "Abhishek Nelson",
                "Alexey Singh",
                "Caitlin Bailey"
        ],
        "raw_phrase": "I'll be working closely with Alexi on this feature.",
        "corrected_phrase": "I'll be working closely with Alexey on this feature."
},
    {
        "names": [
                "Alexi King"
        ],
        "raw_phrase": "Hey Alexey, can you check the logs?",
        "corrected_phrase": "Hey Alexi, can you check the logs?"
},
    {
        "names": [
                "Alexey Phillips"
        ],
        "raw_phrase": "I'm looking at Alexi's latest update.",
        "corrected_phrase": "I'm looking at Alexey's latest update."
},
    {
        "names": [
                "Saoirse Nelson",
                "Arjun Reed",
                "Sara Phillips",
                "Isabelle Garcia",
                "Aimee Carter"
        ],
        "raw_phrase": "Arjoon mentioned the deadline was moved.",
        "corrected_phrase": "Arjun mentioned the deadline was moved."
},
    {
        "names": [
                "Arjun Ramirez",
                "Gwenyth Morales"
        ],
        "raw_phrase": "Let's find a time that works for Arjoon.",
        "corrected_phrase": "Let's find a time that works for Arjun."
},
    {
        "names": [
                "Rhaenyra Torres",
                "Kieran Thomas",
                "Arjun Stewart",
                "Sanjay Thomas"
        ],
        "raw_phrase": "I'll sync with Arjoon later today.",
        "corrected_phrase": "I'll sync with Arjun later today."
},
    {
        "names": [
                "Arjun Lefebvre",
                "Rachael Torres",
                "Priya Silva"
        ],
        "raw_phrase": "I'll sync up with Arjoon to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Arjun to make sure we're on the same page."
},
    {
        "names": [
                "Aarav Green",
                "Arjun Baker"
        ],
        "raw_phrase": "Arjoon has a lot of experience with React.",
        "corrected_phrase": "Arjun has a lot of experience with React."
},
    {
        "names": [
                "Arjoon Cooper"
        ],
        "raw_phrase": "Hey Arjun, can you check the logs?",
        "corrected_phrase": "Hey Arjoon, can you check the logs?"
},
    {
        "names": [
                "Arjun Collins"
        ],
        "raw_phrase": "I'm looking at Arjoon's latest update.",
        "corrected_phrase": "I'm looking at Arjun's latest update."
},
    {
        "names": [
                "Giuseppe Jones",
                "Scarlett Dubois",
                "Shawn Dubois",
                "Bharath Harris"
        ],
        "raw_phrase": "I'll ask Bharat to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Bharath to walk us through the deployment process."
},
    {
        "names": [
                "Bharath Roberts",
                "Qasim Brown"
        ],
        "raw_phrase": "I'll sync up with Bharat to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Bharath to make sure we're on the same page."
},
    {
        "names": [
                "Sanjay Phillips",
                "Bharath Peterson"
        ],
        "raw_phrase": "Bharat suggested a few improvements to the UI.",
        "corrected_phrase": "Bharath suggested a few improvements to the UI."
},
    {
        "names": [
                "Zack Ramirez",
                "Pavel Jackson",
                "Hassan Nelson",
                "Bharath Jackson"
        ],
        "raw_phrase": "Bharat is the one who originally wrote this script.",
        "corrected_phrase": "Bharath is the one who originally wrote this script."
},
    {
        "names": [
                "Bharath Reed",
                "Ishaan Ivanov",
                "Teresa Rogers",
                "Eric Cooper",
                "Claire Taylor"
        ],
        "raw_phrase": "Did Bharat send the report yet?",
        "corrected_phrase": "Did Bharath send the report yet?"
},
    {
        "names": [
                "Bharat Khan"
        ],
        "raw_phrase": "Hey Bharath, can you check the logs?",
        "corrected_phrase": "Hey Bharat, can you check the logs?"
},
    {
        "names": [
                "Bharath Morris"
        ],
        "raw_phrase": "I'm looking at Bharat's latest update.",
        "corrected_phrase": "I'm looking at Bharath's latest update."
},
    {
        "names": [
                "Bharath Reed",
                "Hanna Anderson",
                "Eric Nguyen",
                "Bryan Turner",
                "Barbra Evans"
        ],
        "raw_phrase": "I'll be working closely with Barath on this feature.",
        "corrected_phrase": "I'll be working closely with Bharath on this feature."
},
    {
        "names": [
                "Bharath Campbell",
                "Caitlin Martin"
        ],
        "raw_phrase": "I'm going to grab a coffee with Barath later.",
        "corrected_phrase": "I'm going to grab a coffee with Bharath later."
},
    {
        "names": [
                "Aimee Silva",
                "Bharath Williams"
        ],
        "raw_phrase": "Did Barath mention anything about the budget?",
        "corrected_phrase": "Did Bharath mention anything about the budget?"
},
    {
        "names": [
                "Wei Lee",
                "Bharath Taylor",
                "Pavel Morgan",
                "Ulysses Turner",
                "Sanjay Reed"
        ],
        "raw_phrase": "I'll double check the numbers with Barath.",
        "corrected_phrase": "I'll double check the numbers with Bharath."
},
    {
        "names": [
                "Xavier Peterson",
                "Alexey Brown",
                "Lukas Jones",
                "Bharath Turner"
        ],
        "raw_phrase": "I'll check the calendar to see when Barath is free.",
        "corrected_phrase": "I'll check the calendar to see when Bharath is free."
},
    {
        "names": [
                "Barath Khan"
        ],
        "raw_phrase": "Hey Bharath, can you check the logs?",
        "corrected_phrase": "Hey Barath, can you check the logs?"
},
    {
        "names": [
                "Bharath Patel"
        ],
        "raw_phrase": "I'm looking at Barath's latest update.",
        "corrected_phrase": "I'm looking at Bharath's latest update."
},
    {
        "names": [
                "Damian Peterson",
                "Caiming Cook",
                "Mathew Green",
                "Fatima Edwards"
        ],
        "raw_phrase": "I'm waiting on Kai Ming to approve the changes.",
        "corrected_phrase": "I'm waiting on Caiming to approve the changes."
},
    {
        "names": [
                "Caiming Collins",
                "Saoirse Peterson"
        ],
        "raw_phrase": "Kai Ming is leading the research on machine learning.",
        "corrected_phrase": "Caiming is leading the research on machine learning."
},
    {
        "names": [
                "Gwenyth Ramirez",
                "Caiming Martin"
        ],
        "raw_phrase": "Kai Ming is the best person to talk to about this.",
        "corrected_phrase": "Caiming is the best person to talk to about this."
},
    {
        "names": [
                "Caiming Collins",
                "Arjun Kim"
        ],
        "raw_phrase": "I'll ask Kai Ming to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Caiming to walk us through the deployment process."
},
    {
        "names": [
                "Zack Nelson",
                "Ishaan Cook",
                "Caiming Taylor",
                "Sanjay Johnson",
                "Shawn Green"
        ],
        "raw_phrase": "I'll sync up with Kai Ming to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Caiming to make sure we're on the same page."
},
    {
        "names": [
                "Kai Ming Ivanov"
        ],
        "raw_phrase": "Hey Caiming, can you check the logs?",
        "corrected_phrase": "Hey Kai Ming, can you check the logs?"
},
    {
        "names": [
                "Caiming Garcia"
        ],
        "raw_phrase": "I'm looking at Kai Ming's latest update.",
        "corrected_phrase": "I'm looking at Caiming's latest update."
},
    {
        "names": [
                "Zhi Anderson",
                "Caitlin Harris",
                "Caiming Johnson"
        ],
        "raw_phrase": "Cai Ming is currently out of office until Monday.",
        "corrected_phrase": "Caiming is currently out of office until Monday."
},
    {
        "names": [
                "Isabelle Singh",
                "Caiming Jones"
        ],
        "raw_phrase": "I'll sync up with Cai Ming to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Caiming to make sure we're on the same page."
},
    {
        "names": [
                "Caiming Jones",
                "Antony Stewart",
                "Nikolas Rodriguez"
        ],
        "raw_phrase": "I sent the draft to Cai Ming for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Caiming for some initial thoughts."
},
    {
        "names": [
                "Mathew Turner",
                "Caiming Cook"
        ],
        "raw_phrase": "I'm waiting on Cai Ming to approve the changes.",
        "corrected_phrase": "I'm waiting on Caiming to approve the changes."
},
    {
        "names": [
                "Domhnall Reed",
                "Arjun Silva",
                "Caiming Ramirez"
        ],
        "raw_phrase": "I'll double check the numbers with Cai Ming.",
        "corrected_phrase": "I'll double check the numbers with Caiming."
},
    {
        "names": [
                "Cai Ming Evans"
        ],
        "raw_phrase": "Hey Caiming, can you check the logs?",
        "corrected_phrase": "Hey Cai Ming, can you check the logs?"
},
    {
        "names": [
                "Caiming Santos"
        ],
        "raw_phrase": "I'm looking at Cai Ming's latest update.",
        "corrected_phrase": "I'm looking at Caiming's latest update."
},
    {
        "names": [
                "Chen Campbell",
                "Chen Baker",
                "Sundar King",
                "Rhaenyra Martinez",
                "Sara Thompson"
        ],
        "raw_phrase": "Please make sure Chun has access to the repository.",
        "corrected_phrase": "Please make sure Chen has access to the repository."
},
    {
        "names": [
                "Niamh Cook",
                "Caitlin Roberts",
                "Chen Murphy"
        ],
        "raw_phrase": "Chun is the best person to talk to about this.",
        "corrected_phrase": "Chen is the best person to talk to about this."
},
    {
        "names": [
                "Barbra Edwards",
                "Chen Nelson",
                "Hiroshi Schmidt",
                "Damian Cooper"
        ],
        "raw_phrase": "Chun is the best person to talk to about this.",
        "corrected_phrase": "Chen is the best person to talk to about this."
},
    {
        "names": [
                "Dmitry Adams",
                "Chen Murphy"
        ],
        "raw_phrase": "Can you ask Chun to join the Zoom?",
        "corrected_phrase": "Can you ask Chen to join the Zoom?"
},
    {
        "names": [
                "Chen Rodriguez",
                "Nikolas Edwards"
        ],
        "raw_phrase": "I sent the draft to Chun for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Chen for some initial thoughts."
},
    {
        "names": [
                "Chun Brown"
        ],
        "raw_phrase": "Hey Chen, can you check the logs?",
        "corrected_phrase": "Hey Chun, can you check the logs?"
},
    {
        "names": [
                "Chen Ivanov"
        ],
        "raw_phrase": "I'm looking at Chun's latest update.",
        "corrected_phrase": "I'm looking at Chen's latest update."
},
    {
        "names": [
                "Dmitry Ivanov",
                "Ishaan Reed"
        ],
        "raw_phrase": "Dimitri is the best person to talk to about this.",
        "corrected_phrase": "Dmitry is the best person to talk to about this."
},
    {
        "names": [
                "Dmitry Turner",
                "Antony Scott"
        ],
        "raw_phrase": "Dimitri is first on the standup list.",
        "corrected_phrase": "Dmitry is first on the standup list."
},
    {
        "names": [
                "Damian Campbell",
                "Dmitry Harris",
                "Barbra Williams"
        ],
        "raw_phrase": "Dimitri found a bug in the production environment.",
        "corrected_phrase": "Dmitry found a bug in the production environment."
},
    {
        "names": [
                "Sundar Campbell",
                "Niamh Rodriguez",
                "Dmitry Cook"
        ],
        "raw_phrase": "Check with Dimitri about the API credentials.",
        "corrected_phrase": "Check with Dmitry about the API credentials."
},
    {
        "names": [
                "Niamh Smith",
                "Kieran Silva",
                "Domhnall Mitchell",
                "Dmitry Lee",
                "Vihaan Morgan"
        ],
        "raw_phrase": "Has Dimitri reviewed the security policy yet?",
        "corrected_phrase": "Has Dmitry reviewed the security policy yet?"
},
    {
        "names": [
                "Dimitri Parker"
        ],
        "raw_phrase": "Hey Dmitry, can you check the logs?",
        "corrected_phrase": "Hey Dimitri, can you check the logs?"
},
    {
        "names": [
                "Dmitry Rogers"
        ],
        "raw_phrase": "I'm looking at Dimitri's latest update.",
        "corrected_phrase": "I'm looking at Dmitry's latest update."
},
    {
        "names": [
                "Eric Smith",
                "Caiming Murphy",
                "Chiwetel Cooper",
                "Dmitry Silva",
                "Lukas Morris"
        ],
        "raw_phrase": "I'm going to grab a coffee with Dmitri later.",
        "corrected_phrase": "I'm going to grab a coffee with Dmitry later."
},
    {
        "names": [
                "Dmitry Davis",
                "Tomas Campbell",
                "Saoirse Lefebvre",
                "Dmitry Thompson"
        ],
        "raw_phrase": "Dmitri's PR is ready for review.",
        "corrected_phrase": "Dmitry's PR is ready for review."
},
    {
        "names": [
                "Sara Nguyen",
                "Zainab Morgan",
                "Dmitry Stewart",
                "Jian Young",
                "Jayne Rodriguez"
        ],
        "raw_phrase": "Dmitri suggested we use a different database.",
        "corrected_phrase": "Dmitry suggested we use a different database."
},
    {
        "names": [
                "Phillip Murphy",
                "Dmitry Taylor",
                "Beatrix Nguyen",
                "Stephen Baker",
                "Aimee Jones"
        ],
        "raw_phrase": "Wait for Dmitri before starting the meeting.",
        "corrected_phrase": "Wait for Dmitry before starting the meeting."
},
    {
        "names": [
                "Dmitry Cooper",
                "Priya Ivanov",
                "Dmitry Bailey",
                "Dmitry M\u00fcller",
                "Oleksandr Taylor"
        ],
        "raw_phrase": "Dmitri suggested we use a different database.",
        "corrected_phrase": "Dmitry suggested we use a different database."
},
    {
        "names": [
                "Dmitri Green"
        ],
        "raw_phrase": "Hey Dmitry, can you check the logs?",
        "corrected_phrase": "Hey Dmitri, can you check the logs?"
},
    {
        "names": [
                "Dmitry Evans"
        ],
        "raw_phrase": "I'm looking at Dmitri's latest update.",
        "corrected_phrase": "I'm looking at Dmitry's latest update."
},
    {
        "names": [
                "Hanna Young",
                "Wei Phillips"
        ],
        "raw_phrase": "Is Hannah familiar with this part of the codebase?",
        "corrected_phrase": "Is Hanna familiar with this part of the codebase?"
},
    {
        "names": [
                "Hanna Johnson",
                "Kah Mun King"
        ],
        "raw_phrase": "I'll sync with Hannah later today.",
        "corrected_phrase": "I'll sync with Hanna later today."
},
    {
        "names": [
                "Bryan Jones",
                "Sara M\u00fcller",
                "Hanna Williams",
                "Juliet Tan"
        ],
        "raw_phrase": "I'll follow up with Hannah after the meeting.",
        "corrected_phrase": "I'll follow up with Hanna after the meeting."
},
    {
        "names": [
                "Shawn Patel",
                "Hanna Nguyen",
                "Damian Stewart"
        ],
        "raw_phrase": "Please make sure Hannah has access to the repository.",
        "corrected_phrase": "Please make sure Hanna has access to the repository."
},
    {
        "names": [
                "Aarav Parker",
                "Juliet Nelson",
                "Niamh M\u00fcller",
                "Hanna Morgan",
                "Abhishek Williams"
        ],
        "raw_phrase": "I'm going to grab a coffee with Hannah later.",
        "corrected_phrase": "I'm going to grab a coffee with Hanna later."
},
    {
        "names": [
                "Hannah Murphy"
        ],
        "raw_phrase": "Hey Hanna, can you check the logs?",
        "corrected_phrase": "Hey Hannah, can you check the logs?"
},
    {
        "names": [
                "Hanna Morris"
        ],
        "raw_phrase": "I'm looking at Hannah's latest update.",
        "corrected_phrase": "I'm looking at Hanna's latest update."
},
    {
        "names": [
                "Ishaan Mitchell",
                "Alexey Morales",
                "Ishaan Reed",
                "Teresa Silva"
        ],
        "raw_phrase": "Ishan is the one who originally wrote this script.",
        "corrected_phrase": "Ishaan is the one who originally wrote this script."
},
    {
        "names": [
                "Ishaan Jackson",
                "Nikolas Cook",
                "Vihaan Phillips"
        ],
        "raw_phrase": "Can Ishan join the sync tomorrow morning?",
        "corrected_phrase": "Can Ishaan join the sync tomorrow morning?"
},
    {
        "names": [
                "Zack Phillips",
                "Ishaan Stewart"
        ],
        "raw_phrase": "Could you take a look at the PR from Ishan?",
        "corrected_phrase": "Could you take a look at the PR from Ishaan?"
},
    {
        "names": [
                "Yingbo Roberts",
                "Ishaan Peterson"
        ],
        "raw_phrase": "Ishan is the one who originally wrote this script.",
        "corrected_phrase": "Ishaan is the one who originally wrote this script."
},
    {
        "names": [
                "Zhi Martin",
                "Priya Dubois",
                "Ishaan Miller"
        ],
        "raw_phrase": "I sent the draft to Ishan for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Ishaan for some initial thoughts."
},
    {
        "names": [
                "Ishan Morales"
        ],
        "raw_phrase": "Hey Ishaan, can you check the logs?",
        "corrected_phrase": "Hey Ishan, can you check the logs?"
},
    {
        "names": [
                "Ishaan Patel"
        ],
        "raw_phrase": "I'm looking at Ishan's latest update.",
        "corrected_phrase": "I'm looking at Ishaan's latest update."
},
    {
        "names": [
                "Jian Roberts",
                "Mei Martinez",
                "Ulysses Murphy",
                "Bharath Evans",
                "Geoff Thompson"
        ],
        "raw_phrase": "I'll sync with Gee-an later today.",
        "corrected_phrase": "I'll sync with Jian later today."
},
    {
        "names": [
                "Jian Nguyen",
                "Sundar Green"
        ],
        "raw_phrase": "We should get some feedback from Gee-an on this.",
        "corrected_phrase": "We should get some feedback from Jian on this."
},
    {
        "names": [
                "Zainab Morales",
                "Jian Campbell"
        ],
        "raw_phrase": "Please add Gee-an to the email thread.",
        "corrected_phrase": "Please add Jian to the email thread."
},
    {
        "names": [
                "Priya Campbell",
                "Jian Anderson"
        ],
        "raw_phrase": "Is Gee-an on the call?",
        "corrected_phrase": "Is Jian on the call?"
},
    {
        "names": [
                "Jian Bailey",
                "Rachael Morris"
        ],
        "raw_phrase": "Is Gee-an joining the happy hour tonight?",
        "corrected_phrase": "Is Jian joining the happy hour tonight?"
},
    {
        "names": [
                "Gee-an White"
        ],
        "raw_phrase": "Hey Jian, can you check the logs?",
        "corrected_phrase": "Hey Gee-an, can you check the logs?"
},
    {
        "names": [
                "Jian Collins"
        ],
        "raw_phrase": "I'm looking at Gee-an's latest update.",
        "corrected_phrase": "I'm looking at Jian's latest update."
},
    {
        "names": [
                "Kah Mun Jones",
                "Kah Mun Ramirez",
                "Caitlin Young",
                "Jayne Ivanov",
                "Katarina Harris"
        ],
        "raw_phrase": "Ka Mun has a lot of experience with React.",
        "corrected_phrase": "Kah Mun has a lot of experience with React."
},
    {
        "names": [
                "Kah Mun Martin",
                "Aarav Jones",
                "Yosef Campbell",
                "Jayne Mitchell"
        ],
        "raw_phrase": "Please make sure Ka Mun has access to the repository.",
        "corrected_phrase": "Please make sure Kah Mun has access to the repository."
},
    {
        "names": [
                "Caiming Hill",
                "Kah Mun Morales",
                "Kieran Nelson"
        ],
        "raw_phrase": "Ka Mun is the best person to talk to about this.",
        "corrected_phrase": "Kah Mun is the best person to talk to about this."
},
    {
        "names": [
                "Arjun Schmidt",
                "Yingbo Roberts",
                "Kah Mun Rogers",
                "Silvio Edwards"
        ],
        "raw_phrase": "I'll coordinate the meeting with Ka Mun.",
        "corrected_phrase": "I'll coordinate the meeting with Kah Mun."
},
    {
        "names": [
                "Kah Mun Rossi",
                "Bharath Garcia"
        ],
        "raw_phrase": "Ka Mun is first on the standup list.",
        "corrected_phrase": "Kah Mun is first on the standup list."
},
    {
        "names": [
                "Ka Mun Williams"
        ],
        "raw_phrase": "Hey Kah Mun, can you check the logs?",
        "corrected_phrase": "Hey Ka Mun, can you check the logs?"
},
    {
        "names": [
                "Kah Mun Evans"
        ],
        "raw_phrase": "I'm looking at Ka Mun's latest update.",
        "corrected_phrase": "I'm looking at Kah Mun's latest update."
},
    {
        "names": [
                "Claire Roberts",
                "Saoirse Murphy",
                "Yosef Morales",
                "Kah Mun Carter"
        ],
        "raw_phrase": "I'm going to grab a coffee with Kahmun later.",
        "corrected_phrase": "I'm going to grab a coffee with Kah Mun later."
},
    {
        "names": [
                "Kah Mun Rodriguez",
                "Hiroshi Tan",
                "Antony Anderson"
        ],
        "raw_phrase": "I'll be working closely with Kahmun on this feature.",
        "corrected_phrase": "I'll be working closely with Kah Mun on this feature."
},
    {
        "names": [
                "Kah Mun Santos",
                "Sundar M\u00fcller"
        ],
        "raw_phrase": "I'm waiting on Kahmun to approve the changes.",
        "corrected_phrase": "I'm waiting on Kah Mun to approve the changes."
},
    {
        "names": [
                "Kah Mun Williams",
                "Ulysses Cook"
        ],
        "raw_phrase": "I sent the draft to Kahmun for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Kah Mun for some initial thoughts."
},
    {
        "names": [
                "Juliet Morris",
                "Kah Mun Jones",
                "Juliet Mitchell",
                "Caiming Jones",
                "Mikhail M\u00fcller"
        ],
        "raw_phrase": "Can you ask Kahmun to join the Zoom?",
        "corrected_phrase": "Can you ask Kah Mun to join the Zoom?"
},
    {
        "names": [
                "Kahmun Lee"
        ],
        "raw_phrase": "Hey Kah Mun, can you check the logs?",
        "corrected_phrase": "Hey Kahmun, can you check the logs?"
},
    {
        "names": [
                "Kah Mun Green"
        ],
        "raw_phrase": "I'm looking at Kahmun's latest update.",
        "corrected_phrase": "I'm looking at Kah Mun's latest update."
},
    {
        "names": [
                "Katarina Singh",
                "Katherine White",
                "Yosef Miller",
                "Zainab Young",
                "Sundar Tan"
        ],
        "raw_phrase": "I'm going to grab a coffee with Katrina later.",
        "corrected_phrase": "I'm going to grab a coffee with Katarina later."
},
    {
        "names": [
                "Katarina Johnson",
                "Caiming Reed"
        ],
        "raw_phrase": "Could you take a look at the PR from Katrina?",
        "corrected_phrase": "Could you take a look at the PR from Katarina?"
},
    {
        "names": [
                "Krysten Stewart",
                "Priya Johnson",
                "Katarina Dubois",
                "Xavier Jackson",
                "Mei Santos"
        ],
        "raw_phrase": "Check with Katrina about the API credentials.",
        "corrected_phrase": "Check with Katarina about the API credentials."
},
    {
        "names": [
                "Eric Stewart",
                "Katarina King"
        ],
        "raw_phrase": "Katrina is leading the research on machine learning.",
        "corrected_phrase": "Katarina is leading the research on machine learning."
},
    {
        "names": [
                "Beatrix Torres",
                "Sara Martinez",
                "Rhaenyra Schmidt",
                "Katarina Reed",
                "Elisabeth Jones"
        ],
        "raw_phrase": "Katrina suggested we use a different database.",
        "corrected_phrase": "Katarina suggested we use a different database."
},
    {
        "names": [
                "Katrina Murphy"
        ],
        "raw_phrase": "Hey Katarina, can you check the logs?",
        "corrected_phrase": "Hey Katrina, can you check the logs?"
},
    {
        "names": [
                "Katarina Baker"
        ],
        "raw_phrase": "I'm looking at Katrina's latest update.",
        "corrected_phrase": "I'm looking at Katarina's latest update."
},
    {
        "names": [
                "Mathew Miller",
                "Rhaenyra Moore",
                "Katarina Singh"
        ],
        "raw_phrase": "Is Katerina joining the happy hour tonight?",
        "corrected_phrase": "Is Katarina joining the happy hour tonight?"
},
    {
        "names": [
                "Rhaenyra Mitchell",
                "Katarina Evans",
                "Eric Nguyen",
                "Lukas Tan",
                "Zhi Reed"
        ],
        "raw_phrase": "Katerina is the point of contact for this.",
        "corrected_phrase": "Katarina is the point of contact for this."
},
    {
        "names": [
                "Hiroshi Jackson",
                "Pavel Adams",
                "Beatrix Edwards",
                "Katarina White"
        ],
        "raw_phrase": "Did Katerina finish the documentation for the new API?",
        "corrected_phrase": "Did Katarina finish the documentation for the new API?"
},
    {
        "names": [
                "Aimee Nguyen",
                "Silvio Thompson",
                "Abhishek Turner",
                "Katarina Miller",
                "Claire Thomas"
        ],
        "raw_phrase": "Did Katerina catch that error in the logs?",
        "corrected_phrase": "Did Katarina catch that error in the logs?"
},
    {
        "names": [
                "Beatrix Adams",
                "Katarina Nelson"
        ],
        "raw_phrase": "Katerina is first on the standup list.",
        "corrected_phrase": "Katarina is first on the standup list."
},
    {
        "names": [
                "Katerina Brown"
        ],
        "raw_phrase": "Hey Katarina, can you check the logs?",
        "corrected_phrase": "Hey Katerina, can you check the logs?"
},
    {
        "names": [
                "Katarina Reed"
        ],
        "raw_phrase": "I'm looking at Katerina's latest update.",
        "corrected_phrase": "I'm looking at Katarina's latest update."
},
    {
        "names": [
                "Krysten Campbell",
                "Li Tan",
                "Katherine Morgan"
        ],
        "raw_phrase": "Check with Lee about the API credentials.",
        "corrected_phrase": "Check with Li about the API credentials."
},
    {
        "names": [
                "Katarina Green",
                "Li Garcia"
        ],
        "raw_phrase": "Did Lee catch that error in the logs?",
        "corrected_phrase": "Did Li catch that error in the logs?"
},
    {
        "names": [
                "Oksana Bailey",
                "Domhnall Ivanov",
                "Li Lee",
                "Kah Mun Smith"
        ],
        "raw_phrase": "Lee is currently out of office until Monday.",
        "corrected_phrase": "Li is currently out of office until Monday."
},
    {
        "names": [
                "Rachael Silva",
                "Li Williams"
        ],
        "raw_phrase": "Please CC Lee on all future updates.",
        "corrected_phrase": "Please CC Li on all future updates."
},
    {
        "names": [
                "Li Johnson",
                "Sara Peterson",
                "Caitlin M\u00fcller"
        ],
        "raw_phrase": "Is Lee on the call?",
        "corrected_phrase": "Is Li on the call?"
},
    {
        "names": [
                "Lee Taylor"
        ],
        "raw_phrase": "Hey Li, can you check the logs?",
        "corrected_phrase": "Hey Lee, can you check the logs?"
},
    {
        "names": [
                "Li Martin"
        ],
        "raw_phrase": "I'm looking at Lee's latest update.",
        "corrected_phrase": "I'm looking at Li's latest update."
},
    {
        "names": [
                "Mateo Thompson",
                "Yosef Johnson",
                "Krysten Jackson"
        ],
        "raw_phrase": "Matteo mentioned the deadline was moved.",
        "corrected_phrase": "Mateo mentioned the deadline was moved."
},
    {
        "names": [
                "Rachael Jones",
                "Zhi Rogers",
                "Mateo Rodriguez"
        ],
        "raw_phrase": "Has Matteo reviewed the security policy yet?",
        "corrected_phrase": "Has Mateo reviewed the security policy yet?"
},
    {
        "names": [
                "Vihaan Young",
                "Mateo M\u00fcller",
                "Chen Adams",
                "Caitlin Anderson",
                "Fatima Rossi"
        ],
        "raw_phrase": "I saw a comment from Matteo on the design doc.",
        "corrected_phrase": "I saw a comment from Mateo on the design doc."
},
    {
        "names": [
                "Arjun Moore",
                "Mateo White",
                "Mei Patel"
        ],
        "raw_phrase": "Did Matteo send the report yet?",
        "corrected_phrase": "Did Mateo send the report yet?"
},
    {
        "names": [
                "Hassan Rossi",
                "Isabelle Jones",
                "Mateo Edwards"
        ],
        "raw_phrase": "Did Matteo finish the documentation for the new API?",
        "corrected_phrase": "Did Mateo finish the documentation for the new API?"
},
    {
        "names": [
                "Matteo Lee"
        ],
        "raw_phrase": "Hey Mateo, can you check the logs?",
        "corrected_phrase": "Hey Matteo, can you check the logs?"
},
    {
        "names": [
                "Mateo White"
        ],
        "raw_phrase": "I'm looking at Matteo's latest update.",
        "corrected_phrase": "I'm looking at Mateo's latest update."
},
    {
        "names": [
                "Geoff Jones",
                "Oksana Scott",
                "Mei Campbell"
        ],
        "raw_phrase": "I'll double check the numbers with May.",
        "corrected_phrase": "I'll double check the numbers with Mei."
},
    {
        "names": [
                "Ulysses Miller",
                "Domhnall Lefebvre",
                "Mei Collins",
                "Susannah Schmidt"
        ],
        "raw_phrase": "Did May mention anything about the budget?",
        "corrected_phrase": "Did Mei mention anything about the budget?"
},
    {
        "names": [
                "Thierry Torres",
                "Srini Green",
                "Wei Nguyen",
                "Mei Roberts"
        ],
        "raw_phrase": "May's PR is ready for review.",
        "corrected_phrase": "Mei's PR is ready for review."
},
    {
        "names": [
                "Domhnall Campbell",
                "Mei Harris"
        ],
        "raw_phrase": "Did May send the report yet?",
        "corrected_phrase": "Did Mei send the report yet?"
},
    {
        "names": [
                "Aimee Baker",
                "Srini Cook",
                "Priya Garcia",
                "Mei Scott"
        ],
        "raw_phrase": "I'll coordinate the meeting with May.",
        "corrected_phrase": "I'll coordinate the meeting with Mei."
},
    {
        "names": [
                "May Taylor"
        ],
        "raw_phrase": "Hey Mei, can you check the logs?",
        "corrected_phrase": "Hey May, can you check the logs?"
},
    {
        "names": [
                "Mei Cook"
        ],
        "raw_phrase": "I'm looking at May's latest update.",
        "corrected_phrase": "I'm looking at Mei's latest update."
},
    {
        "names": [
                "Shawn Lee",
                "Tomas Thomas",
                "Shawn Singh",
                "Mei Garcia",
                "Oleksandr Lee"
        ],
        "raw_phrase": "Did Alexander finish the documentation for the new API?",
        "corrected_phrase": "Did Oleksandr finish the documentation for the new API?"
},
    {
        "names": [
                "Chiwetel Davis",
                "Bharath Peterson",
                "Priya Martinez",
                "Oleksandr Murphy"
        ],
        "raw_phrase": "I need to discuss the roadmap with Alexander.",
        "corrected_phrase": "I need to discuss the roadmap with Oleksandr."
},
    {
        "names": [
                "Oleksandr Nguyen",
                "Vihaan Morris"
        ],
        "raw_phrase": "Please CC Alexander on all future updates.",
        "corrected_phrase": "Please CC Oleksandr on all future updates."
},
    {
        "names": [
                "Krysten Peterson",
                "Oleksandr Rossi"
        ],
        "raw_phrase": "Alexander's PR is ready for review.",
        "corrected_phrase": "Oleksandr's PR is ready for review."
},
    {
        "names": [
                "Alexey Martin",
                "Pavel Lefebvre",
                "Elisabeth Anderson",
                "Oleksandr Davis",
                "Aimee Rossi"
        ],
        "raw_phrase": "Wait for Alexander before starting the meeting.",
        "corrected_phrase": "Wait for Oleksandr before starting the meeting."
},
    {
        "names": [
                "Alexander Carter"
        ],
        "raw_phrase": "Hey Oleksandr, can you check the logs?",
        "corrected_phrase": "Hey Alexander, can you check the logs?"
},
    {
        "names": [
                "Oleksandr Scott"
        ],
        "raw_phrase": "I'm looking at Alexander's latest update.",
        "corrected_phrase": "I'm looking at Oleksandr's latest update."
},
    {
        "names": [
                "Rachael Santos",
                "Caitlin Peterson",
                "Stephen Campbell",
                "Mei Reed",
                "Oleksandr Martinez"
        ],
        "raw_phrase": "I'll sync with Olexander later today.",
        "corrected_phrase": "I'll sync with Oleksandr later today."
},
    {
        "names": [
                "Saoirse Baker",
                "Jayne Martinez",
                "Oleksandr Baker",
                "Jayne Bailey"
        ],
        "raw_phrase": "Wait for Olexander before starting the meeting.",
        "corrected_phrase": "Wait for Oleksandr before starting the meeting."
},
    {
        "names": [
                "Saoirse Bailey",
                "Abhishek Parker",
                "Domhnall Martin",
                "Oleksandr Nelson",
                "Jian Ivanov"
        ],
        "raw_phrase": "Please send the invite to Olexander.",
        "corrected_phrase": "Please send the invite to Oleksandr."
},
    {
        "names": [
                "Oleksandr Baker",
                "Priya Turner"
        ],
        "raw_phrase": "Olexander found a bug in the production environment.",
        "corrected_phrase": "Oleksandr found a bug in the production environment."
},
    {
        "names": [
                "Eric Anderson",
                "Mei Martinez",
                "Oleksandr White"
        ],
        "raw_phrase": "I'm going to grab a coffee with Olexander later.",
        "corrected_phrase": "I'm going to grab a coffee with Oleksandr later."
},
    {
        "names": [
                "Olexander Baker"
        ],
        "raw_phrase": "Hey Oleksandr, can you check the logs?",
        "corrected_phrase": "Hey Olexander, can you check the logs?"
},
    {
        "names": [
                "Oleksandr Carter"
        ],
        "raw_phrase": "I'm looking at Olexander's latest update.",
        "corrected_phrase": "I'm looking at Oleksandr's latest update."
},
    {
        "names": [
                "Tomas Morales",
                "Priya Mitchell",
                "Domhnall Adams"
        ],
        "raw_phrase": "Can you ask Preeya to join the Zoom?",
        "corrected_phrase": "Can you ask Priya to join the Zoom?"
},
    {
        "names": [
                "Priya Edwards",
                "Dwyane Brown",
                "Xavier Stewart"
        ],
        "raw_phrase": "Preeya is the point of contact for this.",
        "corrected_phrase": "Priya is the point of contact for this."
},
    {
        "names": [
                "Priya Anderson",
                "Silvio Rogers",
                "Dwyane Bailey"
        ],
        "raw_phrase": "Preeya mentioned the deadline was moved.",
        "corrected_phrase": "Priya mentioned the deadline was moved."
},
    {
        "names": [
                "Jian Singh",
                "Priya Torres",
                "Priya Cook",
                "Kah Mun Edwards",
                "Scarlett Cook"
        ],
        "raw_phrase": "Preeya is currently out of office until Monday.",
        "corrected_phrase": "Priya is currently out of office until Monday."
},
    {
        "names": [
                "Rhaenyra Dubois",
                "Domhnall Thomas",
                "Priya Nguyen",
                "Dwyane Morris",
                "Mateo Phillips"
        ],
        "raw_phrase": "Did Preeya catch that error in the logs?",
        "corrected_phrase": "Did Priya catch that error in the logs?"
},
    {
        "names": [
                "Preeya Evans"
        ],
        "raw_phrase": "Hey Priya, can you check the logs?",
        "corrected_phrase": "Hey Preeya, can you check the logs?"
},
    {
        "names": [
                "Priya Phillips"
        ],
        "raw_phrase": "I'm looking at Preeya's latest update.",
        "corrected_phrase": "I'm looking at Priya's latest update."
},
    {
        "names": [
                "Sanjay Garcia",
                "Qasim Mitchell",
                "Megan M\u00fcller",
                "Xavier Lefebvre"
        ],
        "raw_phrase": "Sanjai is taking the lead on the frontend refactor.",
        "corrected_phrase": "Sanjay is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Sanjay Rogers",
                "Nikolas Santos"
        ],
        "raw_phrase": "Sanjai suggested a few improvements to the UI.",
        "corrected_phrase": "Sanjay suggested a few improvements to the UI."
},
    {
        "names": [
                "Mathew Edwards",
                "Sanjay Morris"
        ],
        "raw_phrase": "Sanjai is currently out of office until Monday.",
        "corrected_phrase": "Sanjay is currently out of office until Monday."
},
    {
        "names": [
                "Chen Rossi",
                "Aimee Edwards",
                "Dmitry Ramirez",
                "Sanjay Ivanov"
        ],
        "raw_phrase": "Wait for Sanjai before starting the meeting.",
        "corrected_phrase": "Wait for Sanjay before starting the meeting."
},
    {
        "names": [
                "Kah Mun Silva",
                "Sanjay Schmidt"
        ],
        "raw_phrase": "Can Sanjai join the sync tomorrow morning?",
        "corrected_phrase": "Can Sanjay join the sync tomorrow morning?"
},
    {
        "names": [
                "Sanjai Taylor"
        ],
        "raw_phrase": "Hey Sanjay, can you check the logs?",
        "corrected_phrase": "Hey Sanjai, can you check the logs?"
},
    {
        "names": [
                "Sanjay Morgan"
        ],
        "raw_phrase": "I'm looking at Sanjai's latest update.",
        "corrected_phrase": "I'm looking at Sanjay's latest update."
},
    {
        "names": [
                "Silvio Thompson",
                "Oleksandr Williams",
                "Barbra Moore",
                "Chiwetel Morales"
        ],
        "raw_phrase": "Sylvio's PR is ready for review.",
        "corrected_phrase": "Silvio's PR is ready for review."
},
    {
        "names": [
                "Silvio Lefebvre",
                "Stephen M\u00fcller"
        ],
        "raw_phrase": "I saw a comment from Sylvio on the design doc.",
        "corrected_phrase": "I saw a comment from Silvio on the design doc."
},
    {
        "names": [
                "Sara Jackson",
                "Silvio Green",
                "Katarina Davis"
        ],
        "raw_phrase": "I think Sylvio is handling the project.",
        "corrected_phrase": "I think Silvio is handling the project."
},
    {
        "names": [
                "Silvio Young",
                "Rhaenyra Evans"
        ],
        "raw_phrase": "Sylvio suggested we use a different database.",
        "corrected_phrase": "Silvio suggested we use a different database."
},
    {
        "names": [
                "Qasim Edwards",
                "Pavel Singh",
                "Silvio Roberts",
                "Vivian Rossi"
        ],
        "raw_phrase": "Please send the invite to Sylvio.",
        "corrected_phrase": "Please send the invite to Silvio."
},
    {
        "names": [
                "Sylvio Garcia"
        ],
        "raw_phrase": "Hey Silvio, can you check the logs?",
        "corrected_phrase": "Hey Sylvio, can you check the logs?"
},
    {
        "names": [
                "Silvio Morgan"
        ],
        "raw_phrase": "I'm looking at Sylvio's latest update.",
        "corrected_phrase": "I'm looking at Silvio's latest update."
},
    {
        "names": [
                "Sofia Patel",
                "Zhi Parker",
                "Aimee Phillips"
        ],
        "raw_phrase": "I saw a comment from Sophia on the design doc.",
        "corrected_phrase": "I saw a comment from Sofia on the design doc."
},
    {
        "names": [
                "Sofia Peterson",
                "Ishaan Thomas",
                "Yingbo Carter"
        ],
        "raw_phrase": "I'll follow up with Sophia after the meeting.",
        "corrected_phrase": "I'll follow up with Sofia after the meeting."
},
    {
        "names": [
                "Sofia Smith",
                "Isabelle Ramirez",
                "Ulysses Rodriguez"
        ],
        "raw_phrase": "I'll coordinate the meeting with Sophia.",
        "corrected_phrase": "I'll coordinate the meeting with Sofia."
},
    {
        "names": [
                "Qasim Peterson",
                "Sofia Carter"
        ],
        "raw_phrase": "Sophia is the best person to talk to about this.",
        "corrected_phrase": "Sofia is the best person to talk to about this."
},
    {
        "names": [
                "Pavel Lee",
                "Hiroshi Dubois",
                "Sofia Rodriguez",
                "Vivian Phillips",
                "Shawn Campbell"
        ],
        "raw_phrase": "Sophia suggested a few improvements to the UI.",
        "corrected_phrase": "Sofia suggested a few improvements to the UI."
},
    {
        "names": [
                "Sophia Rodriguez"
        ],
        "raw_phrase": "Hey Sofia, can you check the logs?",
        "corrected_phrase": "Hey Sophia, can you check the logs?"
},
    {
        "names": [
                "Sofia Garcia"
        ],
        "raw_phrase": "I'm looking at Sophia's latest update.",
        "corrected_phrase": "I'm looking at Sofia's latest update."
},
    {
        "names": [
                "Barbra Khan",
                "Aarav Roberts",
                "Srini Brown"
        ],
        "raw_phrase": "We should get some feedback from Sreeni on this.",
        "corrected_phrase": "We should get some feedback from Srini on this."
},
    {
        "names": [
                "Zack Green",
                "Srini Khan",
                "Hassan Evans"
        ],
        "raw_phrase": "I'm waiting on Sreeni to approve the changes.",
        "corrected_phrase": "I'm waiting on Srini to approve the changes."
},
    {
        "names": [
                "Rachael Young",
                "Srini Peterson"
        ],
        "raw_phrase": "Has Sreeni reviewed the security policy yet?",
        "corrected_phrase": "Has Srini reviewed the security policy yet?"
},
    {
        "names": [
                "Srini Green",
                "Megan Edwards"
        ],
        "raw_phrase": "Can you pass the message to Sreeni for me?",
        "corrected_phrase": "Can you pass the message to Srini for me?"
},
    {
        "names": [
                "Sofia Garcia",
                "Srini Jackson",
                "Scarlett Carter"
        ],
        "raw_phrase": "Sreeni suggested we use a different database.",
        "corrected_phrase": "Srini suggested we use a different database."
},
    {
        "names": [
                "Sreeni Hill"
        ],
        "raw_phrase": "Hey Srini, can you check the logs?",
        "corrected_phrase": "Hey Sreeni, can you check the logs?"
},
    {
        "names": [
                "Srini Kim"
        ],
        "raw_phrase": "I'm looking at Sreeni's latest update.",
        "corrected_phrase": "I'm looking at Srini's latest update."
},
    {
        "names": [
                "Sara Parker",
                "Geoff Cook",
                "Srini Lee"
        ],
        "raw_phrase": "I'll check the calendar to see when Sriny is free.",
        "corrected_phrase": "I'll check the calendar to see when Srini is free."
},
    {
        "names": [
                "Sundar Nelson",
                "Jon Adams",
                "Eric Singh",
                "Srini Kim"
        ],
        "raw_phrase": "I need to discuss the roadmap with Sriny.",
        "corrected_phrase": "I need to discuss the roadmap with Srini."
},
    {
        "names": [
                "Marc Parker",
                "Barbra Khan",
                "Fatima Baker",
                "Srini Martin",
                "Lukas Phillips"
        ],
        "raw_phrase": "I'm going to grab a coffee with Sriny later.",
        "corrected_phrase": "I'm going to grab a coffee with Srini later."
},
    {
        "names": [
                "Katarina Dubois",
                "Srini Davis",
                "Fatima Reed",
                "Thierry Morris",
                "Nikolas Lee"
        ],
        "raw_phrase": "Is Sriny familiar with this part of the codebase?",
        "corrected_phrase": "Is Srini familiar with this part of the codebase?"
},
    {
        "names": [
                "Srini Brown",
                "Alexey Phillips",
                "Caiming Cook",
                "Zack Ivanov"
        ],
        "raw_phrase": "Sriny is the best person to talk to about this.",
        "corrected_phrase": "Srini is the best person to talk to about this."
},
    {
        "names": [
                "Sriny Thomas"
        ],
        "raw_phrase": "Hey Srini, can you check the logs?",
        "corrected_phrase": "Hey Sriny, can you check the logs?"
},
    {
        "names": [
                "Srini Morris"
        ],
        "raw_phrase": "I'm looking at Sriny's latest update.",
        "corrected_phrase": "I'm looking at Srini's latest update."
},
    {
        "names": [
                "Ishaan Reed",
                "Sundar Santos",
                "Sundar Brown",
                "Srini Rogers"
        ],
        "raw_phrase": "Sunder suggested we use a different database.",
        "corrected_phrase": "Sundar suggested we use a different database."
},
    {
        "names": [
                "Sundar Baker",
                "Lukas Rogers",
                "Oleksandr Scott"
        ],
        "raw_phrase": "I need to discuss the roadmap with Sunder.",
        "corrected_phrase": "I need to discuss the roadmap with Sundar."
},
    {
        "names": [
                "Sundar Adams",
                "Arjun Smith"
        ],
        "raw_phrase": "Sunder is the point of contact for this.",
        "corrected_phrase": "Sundar is the point of contact for this."
},
    {
        "names": [
                "Fatima Ramirez",
                "Sundar Taylor"
        ],
        "raw_phrase": "Did Sunder mention anything about the budget?",
        "corrected_phrase": "Did Sundar mention anything about the budget?"
},
    {
        "names": [
                "Sundar Singh",
                "Chen Green",
                "Yosef Johnson"
        ],
        "raw_phrase": "Sunder is the one who originally wrote this script.",
        "corrected_phrase": "Sundar is the one who originally wrote this script."
},
    {
        "names": [
                "Sunder Rodriguez"
        ],
        "raw_phrase": "Hey Sundar, can you check the logs?",
        "corrected_phrase": "Hey Sunder, can you check the logs?"
},
    {
        "names": [
                "Sundar Morales"
        ],
        "raw_phrase": "I'm looking at Sunder's latest update.",
        "corrected_phrase": "I'm looking at Sundar's latest update."
},
    {
        "names": [
                "Qasim Peterson",
                "Thierry Morris",
                "Beatrix Cook",
                "Vihaan Brown"
        ],
        "raw_phrase": "I need to discuss the roadmap with Vihan.",
        "corrected_phrase": "I need to discuss the roadmap with Vihaan."
},
    {
        "names": [
                "Vihaan Miller",
                "Saoirse Miller"
        ],
        "raw_phrase": "Please add Vihan to the email thread.",
        "corrected_phrase": "Please add Vihaan to the email thread."
},
    {
        "names": [
                "Vihaan Young",
                "Vihaan Patel",
                "Geoff Rossi",
                "Stephen Scott"
        ],
        "raw_phrase": "I'll sync up with Vihan to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Vihaan to make sure we're on the same page."
},
    {
        "names": [
                "Chen Schmidt",
                "Vihaan Nguyen",
                "Yuki Torres",
                "Rhaenyra Martinez",
                "Susannah Scott"
        ],
        "raw_phrase": "Please add Vihan to the email thread.",
        "corrected_phrase": "Please add Vihaan to the email thread."
},
    {
        "names": [
                "Vihaan Kim",
                "Oksana Kim",
                "Chen Johnson",
                "Yuki Santos",
                "Krysten Johnson"
        ],
        "raw_phrase": "Vihan is the best person to talk to about this.",
        "corrected_phrase": "Vihaan is the best person to talk to about this."
},
    {
        "names": [
                "Vihan Morris"
        ],
        "raw_phrase": "Hey Vihaan, can you check the logs?",
        "corrected_phrase": "Hey Vihan, can you check the logs?"
},
    {
        "names": [
                "Vihaan Thomas"
        ],
        "raw_phrase": "I'm looking at Vihan's latest update.",
        "corrected_phrase": "I'm looking at Vihaan's latest update."
},
    {
        "names": [
                "Caitlin Turner",
                "Wei Cook",
                "Zhi Thomas"
        ],
        "raw_phrase": "Did Way mention anything about the budget?",
        "corrected_phrase": "Did Wei mention anything about the budget?"
},
    {
        "names": [
                "Vivian Moore",
                "Gwenyth Carter",
                "Wei Hill",
                "Nikolas Morales",
                "Sundar Patel"
        ],
        "raw_phrase": "Way mentioned the deadline was moved.",
        "corrected_phrase": "Wei mentioned the deadline was moved."
},
    {
        "names": [
                "Wei Edwards",
                "Kah Mun Parker",
                "Megan Thomas",
                "Katherine Cook"
        ],
        "raw_phrase": "Has Way updated their ticket?",
        "corrected_phrase": "Has Wei updated their ticket?"
},
    {
        "names": [
                "Wei Adams",
                "Li Turner"
        ],
        "raw_phrase": "I'll sync with Way later today.",
        "corrected_phrase": "I'll sync with Wei later today."
},
    {
        "names": [
                "Wei Rogers",
                "Thierry Peterson",
                "Pavel Jones",
                "Kieran Peterson"
        ],
        "raw_phrase": "Way is first on the standup list.",
        "corrected_phrase": "Wei is first on the standup list."
},
    {
        "names": [
                "Way Ramirez"
        ],
        "raw_phrase": "Hey Wei, can you check the logs?",
        "corrected_phrase": "Hey Way, can you check the logs?"
},
    {
        "names": [
                "Wei Mitchell"
        ],
        "raw_phrase": "I'm looking at Way's latest update.",
        "corrected_phrase": "I'm looking at Wei's latest update."
},
    {
        "names": [
                "Yingbo Williams",
                "Oleksandr Morgan"
        ],
        "raw_phrase": "Yinbo is the one who originally wrote this script.",
        "corrected_phrase": "Yingbo is the one who originally wrote this script."
},
    {
        "names": [
                "Yingbo Davis",
                "Sofia Lefebvre"
        ],
        "raw_phrase": "Yinbo is taking the lead on the frontend refactor.",
        "corrected_phrase": "Yingbo is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Xavier Campbell",
                "Yingbo Campbell"
        ],
        "raw_phrase": "Yinbo found a bug in the production environment.",
        "corrected_phrase": "Yingbo found a bug in the production environment."
},
    {
        "names": [
                "Eric Rogers",
                "Yingbo Collins",
                "Yosef Lefebvre",
                "Ulysses Jones"
        ],
        "raw_phrase": "I need to discuss the roadmap with Yinbo.",
        "corrected_phrase": "I need to discuss the roadmap with Yingbo."
},
    {
        "names": [
                "Yingbo Baker",
                "Caiming Parker"
        ],
        "raw_phrase": "Can you ask Yinbo to join the Zoom?",
        "corrected_phrase": "Can you ask Yingbo to join the Zoom?"
},
    {
        "names": [
                "Yinbo Carter"
        ],
        "raw_phrase": "Hey Yingbo, can you check the logs?",
        "corrected_phrase": "Hey Yinbo, can you check the logs?"
},
    {
        "names": [
                "Yingbo Moore"
        ],
        "raw_phrase": "I'm looking at Yinbo's latest update.",
        "corrected_phrase": "I'm looking at Yingbo's latest update."
},
    {
        "names": [
                "Yingbo Carter",
                "Abhishek Anderson"
        ],
        "raw_phrase": "Ying Bo is presenting their findings at the all-hands.",
        "corrected_phrase": "Yingbo is presenting their findings at the all-hands."
},
    {
        "names": [
                "Phillip Edwards",
                "Geoff Roberts",
                "Yingbo M\u00fcller",
                "Shawn Edwards"
        ],
        "raw_phrase": "I need to discuss the roadmap with Ying Bo.",
        "corrected_phrase": "I need to discuss the roadmap with Yingbo."
},
    {
        "names": [
                "Yingbo Khan",
                "Vihaan Parker",
                "Alexey Cook"
        ],
        "raw_phrase": "Can Ying Bo join the sync tomorrow morning?",
        "corrected_phrase": "Can Yingbo join the sync tomorrow morning?"
},
    {
        "names": [
                "Aimee Martin",
                "Yingbo M\u00fcller"
        ],
        "raw_phrase": "Ying Bo is leading the research on machine learning.",
        "corrected_phrase": "Yingbo is leading the research on machine learning."
},
    {
        "names": [
                "Yosef Scott",
                "Qasim Davis",
                "Yingbo Khan"
        ],
        "raw_phrase": "I'll ask Ying Bo to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Yingbo to walk us through the deployment process."
},
    {
        "names": [
                "Ying Bo Adams"
        ],
        "raw_phrase": "Hey Yingbo, can you check the logs?",
        "corrected_phrase": "Hey Ying Bo, can you check the logs?"
},
    {
        "names": [
                "Yingbo Phillips"
        ],
        "raw_phrase": "I'm looking at Ying Bo's latest update.",
        "corrected_phrase": "I'm looking at Yingbo's latest update."
},
    {
        "names": [
                "Zainab Santos",
                "Yosef Taylor",
                "Wei Bailey",
                "Juliet Adams",
                "Caitlin Morgan"
        ],
        "raw_phrase": "Youssef is first on the standup list.",
        "corrected_phrase": "Yosef is first on the standup list."
},
    {
        "names": [
                "Vivian Peterson",
                "Xavier Torres",
                "Yosef Anderson"
        ],
        "raw_phrase": "Youssef is leading the research on machine learning.",
        "corrected_phrase": "Yosef is leading the research on machine learning."
},
    {
        "names": [
                "Yosef Nguyen",
                "Mateo Rodriguez"
        ],
        "raw_phrase": "Did Youssef send the report yet?",
        "corrected_phrase": "Did Yosef send the report yet?"
},
    {
        "names": [
                "Rhaenyra Stewart",
                "Yosef Smith",
                "Pavel Martinez",
                "Oleksandr Phillips"
        ],
        "raw_phrase": "Youssef has a lot of experience with React.",
        "corrected_phrase": "Yosef has a lot of experience with React."
},
    {
        "names": [
                "Mikhail Thompson",
                "Yosef Peterson",
                "Beatrix Jackson",
                "Mikhail Evans"
        ],
        "raw_phrase": "I'll follow up with Youssef after the meeting.",
        "corrected_phrase": "I'll follow up with Yosef after the meeting."
},
    {
        "names": [
                "Youssef Green"
        ],
        "raw_phrase": "Hey Yosef, can you check the logs?",
        "corrected_phrase": "Hey Youssef, can you check the logs?"
},
    {
        "names": [
                "Yosef Silva"
        ],
        "raw_phrase": "I'm looking at Youssef's latest update.",
        "corrected_phrase": "I'm looking at Yosef's latest update."
},
    {
        "names": [
                "Scarlett Cooper",
                "Yosef Edwards",
                "Abhishek Anderson"
        ],
        "raw_phrase": "Wait for Joseph before starting the meeting.",
        "corrected_phrase": "Wait for Yosef before starting the meeting."
},
    {
        "names": [
                "Yuki Silva",
                "Arjun Green",
                "Yosef Anderson",
                "Aimee Evans"
        ],
        "raw_phrase": "I saw a comment from Joseph on the design doc.",
        "corrected_phrase": "I saw a comment from Yosef on the design doc."
},
    {
        "names": [
                "Yosef Patel",
                "Scarlett Taylor",
                "Jon Scott",
                "Shawn Anderson"
        ],
        "raw_phrase": "Joseph is presenting their findings at the all-hands.",
        "corrected_phrase": "Yosef is presenting their findings at the all-hands."
},
    {
        "names": [
                "Mikhail Morales",
                "Jayne Jones",
                "Yosef Nguyen"
        ],
        "raw_phrase": "Has Joseph reviewed the security policy yet?",
        "corrected_phrase": "Has Yosef reviewed the security policy yet?"
},
    {
        "names": [
                "Sanjay Schmidt",
                "Yosef Nguyen",
                "Zainab Adams",
                "Isabelle Silva"
        ],
        "raw_phrase": "Did Joseph mention anything about the budget?",
        "corrected_phrase": "Did Yosef mention anything about the budget?"
},
    {
        "names": [
                "Joseph Mitchell"
        ],
        "raw_phrase": "Hey Yosef, can you check the logs?",
        "corrected_phrase": "Hey Joseph, can you check the logs?"
},
    {
        "names": [
                "Yosef Johnson"
        ],
        "raw_phrase": "I'm looking at Joseph's latest update.",
        "corrected_phrase": "I'm looking at Yosef's latest update."
},
    {
        "names": [
                "Yuki Bailey",
                "Marc Khan",
                "Bryan Martinez"
        ],
        "raw_phrase": "Can you pass the message to Yuuki for me?",
        "corrected_phrase": "Can you pass the message to Yuki for me?"
},
    {
        "names": [
                "Mikhail Davis",
                "Yuki Adams"
        ],
        "raw_phrase": "I'm going to grab a coffee with Yuuki later.",
        "corrected_phrase": "I'm going to grab a coffee with Yuki later."
},
    {
        "names": [
                "Aimee Lee",
                "Yuki Nguyen"
        ],
        "raw_phrase": "Yuuki is the best person to talk to about this.",
        "corrected_phrase": "Yuki is the best person to talk to about this."
},
    {
        "names": [
                "Wei Martin",
                "Sara Campbell",
                "Katherine King",
                "Juliet Ramirez",
                "Yuki Garcia"
        ],
        "raw_phrase": "Yuuki is currently out of office until Monday.",
        "corrected_phrase": "Yuki is currently out of office until Monday."
},
    {
        "names": [
                "Sanjay Scott",
                "Yuki Morris",
                "Hiroshi Santos",
                "Sanjay Baker",
                "Isabelle Peterson"
        ],
        "raw_phrase": "Did Yuuki send the report yet?",
        "corrected_phrase": "Did Yuki send the report yet?"
},
    {
        "names": [
                "Yuuki M\u00fcller"
        ],
        "raw_phrase": "Hey Yuki, can you check the logs?",
        "corrected_phrase": "Hey Yuuki, can you check the logs?"
},
    {
        "names": [
                "Yuki M\u00fcller"
        ],
        "raw_phrase": "I'm looking at Yuuki's latest update.",
        "corrected_phrase": "I'm looking at Yuki's latest update."
},
    {
        "names": [
                "Zhi Parker",
                "Antony Silva",
                "Qasim Silva",
                "Scarlett Silva",
                "Katarina Campbell"
        ],
        "raw_phrase": "I'm waiting on Gee to approve the changes.",
        "corrected_phrase": "I'm waiting on Zhi to approve the changes."
},
    {
        "names": [
                "Shawn M\u00fcller",
                "Zhi Jackson"
        ],
        "raw_phrase": "I sent the draft to Gee for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Zhi for some initial thoughts."
},
    {
        "names": [
                "Wei Taylor",
                "Zhi Khan"
        ],
        "raw_phrase": "Gee suggested we use a different database.",
        "corrected_phrase": "Zhi suggested we use a different database."
},
    {
        "names": [
                "Zhi Cook",
                "Qasim Lee"
        ],
        "raw_phrase": "Let's find a time that works for Gee.",
        "corrected_phrase": "Let's find a time that works for Zhi."
},
    {
        "names": [
                "Sundar Harris",
                "Xavier Collins",
                "Zhi Santos"
        ],
        "raw_phrase": "Gee is taking the lead on the frontend refactor.",
        "corrected_phrase": "Zhi is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Gee Cooper"
        ],
        "raw_phrase": "Hey Zhi, can you check the logs?",
        "corrected_phrase": "Hey Gee, can you check the logs?"
},
    {
        "names": [
                "Zhi Cook"
        ],
        "raw_phrase": "I'm looking at Gee's latest update.",
        "corrected_phrase": "I'm looking at Zhi's latest update."
},
    {
        "names": [
                "Zhi Johnson",
                "Oleksandr Evans",
                "Claire White"
        ],
        "raw_phrase": "Please CC Zee on all future updates.",
        "corrected_phrase": "Please CC Zhi on all future updates."
},
    {
        "names": [
                "Dmitry Taylor",
                "Zhi Reed",
                "Hassan M\u00fcller",
                "Susannah Collins"
        ],
        "raw_phrase": "Let's find a time that works for Zee.",
        "corrected_phrase": "Let's find a time that works for Zhi."
},
    {
        "names": [
                "Giuseppe Evans",
                "Oksana Adams",
                "Zhi Lefebvre",
                "Domhnall Khan"
        ],
        "raw_phrase": "Did Zee mention anything about the budget?",
        "corrected_phrase": "Did Zhi mention anything about the budget?"
},
    {
        "names": [
                "Zhi Torres",
                "Katarina Torres"
        ],
        "raw_phrase": "I'll ask Zee to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Zhi to walk us through the deployment process."
},
    {
        "names": [
                "Caitlin Roberts",
                "Zhi Dubois",
                "Elisabeth Edwards"
        ],
        "raw_phrase": "Did Zee finish the documentation for the new API?",
        "corrected_phrase": "Did Zhi finish the documentation for the new API?"
},
    {
        "names": [
                "Zee Phillips"
        ],
        "raw_phrase": "Hey Zhi, can you check the logs?",
        "corrected_phrase": "Hey Zee, can you check the logs?"
},
    {
        "names": [
                "Zhi Tan"
        ],
        "raw_phrase": "I'm looking at Zee's latest update.",
        "corrected_phrase": "I'm looking at Zhi's latest update."
},
    {
        "names": [
                "Hanna Thomas",
                "Aarav Tan"
        ],
        "raw_phrase": "Arav mentioned the deadline was moved.",
        "corrected_phrase": "Aarav mentioned the deadline was moved."
},
    {
        "names": [
                "Aarav Baker",
                "Rachael Santos",
                "Wei Reed",
                "Krysten Smith",
                "Kieran Scott"
        ],
        "raw_phrase": "Can you pass the message to Arav for me?",
        "corrected_phrase": "Can you pass the message to Aarav for me?"
},
    {
        "names": [
                "Eric Phillips",
                "Aarav Peterson",
                "Xavier Singh",
                "Rachael Cooper"
        ],
        "raw_phrase": "Arav is the one who originally wrote this script.",
        "corrected_phrase": "Aarav is the one who originally wrote this script."
},
    {
        "names": [
                "Claire Nguyen",
                "Aarav Jackson",
                "Chiwetel Silva",
                "Isabelle Nelson"
        ],
        "raw_phrase": "I'll sync with Arav later today.",
        "corrected_phrase": "I'll sync with Aarav later today."
},
    {
        "names": [
                "Kah Mun Scott",
                "Phillip Evans",
                "Aarav Cook"
        ],
        "raw_phrase": "I'll sync up with Arav to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Aarav to make sure we're on the same page."
},
    {
        "names": [
                "Arav Martin"
        ],
        "raw_phrase": "Hey Aarav, can you check the logs?",
        "corrected_phrase": "Hey Arav, can you check the logs?"
},
    {
        "names": [
                "Aarav Moore"
        ],
        "raw_phrase": "I'm looking at Arav's latest update.",
        "corrected_phrase": "I'm looking at Aarav's latest update."
},
    {
        "names": [
                "Vihaan Schmidt",
                "Srini Davis",
                "Abhishek Tan",
                "Kieran Patel"
        ],
        "raw_phrase": "Did Abishek catch that error in the logs?",
        "corrected_phrase": "Did Abhishek catch that error in the logs?"
},
    {
        "names": [
                "Hiroshi Williams",
                "Abhishek Stewart",
                "Dwyane Anderson",
                "Niamh Collins"
        ],
        "raw_phrase": "We should get some feedback from Abishek on this.",
        "corrected_phrase": "We should get some feedback from Abhishek on this."
},
    {
        "names": [
                "Nikolas Edwards",
                "Abhishek Williams",
                "Dwyane Murphy",
                "Fatima Dubois"
        ],
        "raw_phrase": "I'll coordinate the meeting with Abishek.",
        "corrected_phrase": "I'll coordinate the meeting with Abhishek."
},
    {
        "names": [
                "Abhishek Lefebvre",
                "Caitlin Adams"
        ],
        "raw_phrase": "I'll be working closely with Abishek on this feature.",
        "corrected_phrase": "I'll be working closely with Abhishek on this feature."
},
    {
        "names": [
                "Aarav Reed",
                "Abhishek Carter"
        ],
        "raw_phrase": "I'm going to grab a coffee with Abishek later.",
        "corrected_phrase": "I'm going to grab a coffee with Abhishek later."
},
    {
        "names": [
                "Abishek Young"
        ],
        "raw_phrase": "Hey Abhishek, can you check the logs?",
        "corrected_phrase": "Hey Abishek, can you check the logs?"
},
    {
        "names": [
                "Abhishek Young"
        ],
        "raw_phrase": "I'm looking at Abishek's latest update.",
        "corrected_phrase": "I'm looking at Abhishek's latest update."
},
    {
        "names": [
                "Chiwetel Schmidt",
                "Beatrix Carter",
                "Hanna Edwards",
                "Yuki Parker"
        ],
        "raw_phrase": "Did Beatrice catch that error in the logs?",
        "corrected_phrase": "Did Beatrix catch that error in the logs?"
},
    {
        "names": [
                "Scarlett Patel",
                "Beatrix Davis",
                "Bharath Rodriguez",
                "Kah Mun Johnson",
                "Qasim Jones"
        ],
        "raw_phrase": "Did Beatrice catch that error in the logs?",
        "corrected_phrase": "Did Beatrix catch that error in the logs?"
},
    {
        "names": [
                "Beatrix Evans",
                "Mathew Patel",
                "Zainab Adams",
                "Dwyane White"
        ],
        "raw_phrase": "Beatrice is first on the standup list.",
        "corrected_phrase": "Beatrix is first on the standup list."
},
    {
        "names": [
                "Vihaan Bailey",
                "Jian Anderson",
                "Beatrix Collins",
                "Xavier Cook"
        ],
        "raw_phrase": "Check with Beatrice about the API credentials.",
        "corrected_phrase": "Check with Beatrix about the API credentials."
},
    {
        "names": [
                "Wei Thompson",
                "Arjun Campbell",
                "Beatrix Patel",
                "Ulysses Scott",
                "Teresa Collins"
        ],
        "raw_phrase": "Check with Beatrice about the API credentials.",
        "corrected_phrase": "Check with Beatrix about the API credentials."
},
    {
        "names": [
                "Beatrice Nelson"
        ],
        "raw_phrase": "Hey Beatrix, can you check the logs?",
        "corrected_phrase": "Hey Beatrice, can you check the logs?"
},
    {
        "names": [
                "Beatrix Thompson"
        ],
        "raw_phrase": "I'm looking at Beatrice's latest update.",
        "corrected_phrase": "I'm looking at Beatrix's latest update."
},
    {
        "names": [
                "Caiming Evans",
                "Chiwetel Silva"
        ],
        "raw_phrase": "Ask Chewetel if they have the login for the staging server.",
        "corrected_phrase": "Ask Chiwetel if they have the login for the staging server."
},
    {
        "names": [
                "Bryan Roberts",
                "Caiming Nguyen",
                "Chiwetel Cooper"
        ],
        "raw_phrase": "Please send the invite to Chewetel.",
        "corrected_phrase": "Please send the invite to Chiwetel."
},
    {
        "names": [
                "Chiwetel Anderson",
                "Dmitry Rodriguez",
                "Yuki Davis",
                "Ulysses Moore"
        ],
        "raw_phrase": "I'll sync up with Chewetel to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Chiwetel to make sure we're on the same page."
},
    {
        "names": [
                "Arjun Scott",
                "Chiwetel Thomas",
                "Ishaan Taylor",
                "Aimee Stewart"
        ],
        "raw_phrase": "We should get some feedback from Chewetel on this.",
        "corrected_phrase": "We should get some feedback from Chiwetel on this."
},
    {
        "names": [
                "Chiwetel Torres",
                "Srini Green",
                "Susannah Smith",
                "Nikolas Lee",
                "Yosef Collins"
        ],
        "raw_phrase": "Chewetel suggested a few improvements to the UI.",
        "corrected_phrase": "Chiwetel suggested a few improvements to the UI."
},
    {
        "names": [
                "Chewetel King"
        ],
        "raw_phrase": "Hey Chiwetel, can you check the logs?",
        "corrected_phrase": "Hey Chewetel, can you check the logs?"
},
    {
        "names": [
                "Chiwetel Stewart"
        ],
        "raw_phrase": "I'm looking at Chewetel's latest update.",
        "corrected_phrase": "I'm looking at Chiwetel's latest update."
},
    {
        "names": [
                "Phillip Adams",
                "Priya Evans",
                "Zhi Thomas",
                "Damian Smith",
                "Domhnall Martinez"
        ],
        "raw_phrase": "Please send the invite to Donal.",
        "corrected_phrase": "Please send the invite to Domhnall."
},
    {
        "names": [
                "Kah Mun Hill",
                "Domhnall Jones"
        ],
        "raw_phrase": "Donal is taking the lead on the frontend refactor.",
        "corrected_phrase": "Domhnall is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Domhnall Moore",
                "Qasim Young",
                "Yosef King",
                "Nikolas Garcia"
        ],
        "raw_phrase": "Donal mentioned the deadline was moved.",
        "corrected_phrase": "Domhnall mentioned the deadline was moved."
},
    {
        "names": [
                "Silvio Hill",
                "Domhnall Rodriguez"
        ],
        "raw_phrase": "Donal is currently out of office until Monday.",
        "corrected_phrase": "Domhnall is currently out of office until Monday."
},
    {
        "names": [
                "Jayne Johnson",
                "Domhnall Schmidt"
        ],
        "raw_phrase": "Did Donal send the report yet?",
        "corrected_phrase": "Did Domhnall send the report yet?"
},
    {
        "names": [
                "Donal Turner"
        ],
        "raw_phrase": "Hey Domhnall, can you check the logs?",
        "corrected_phrase": "Hey Donal, can you check the logs?"
},
    {
        "names": [
                "Domhnall Taylor"
        ],
        "raw_phrase": "I'm looking at Donal's latest update.",
        "corrected_phrase": "I'm looking at Domhnall's latest update."
},
    {
        "names": [
                "Jian Phillips",
                "Zhi Dubois",
                "Tomas Patel",
                "Isabelle Nelson",
                "Fatima Roberts"
        ],
        "raw_phrase": "Check with Fateema about the API credentials.",
        "corrected_phrase": "Check with Fatima about the API credentials."
},
    {
        "names": [
                "Aimee Peterson",
                "Fatima Young"
        ],
        "raw_phrase": "Is Fateema familiar with this part of the codebase?",
        "corrected_phrase": "Is Fatima familiar with this part of the codebase?"
},
    {
        "names": [
                "Fatima Carter",
                "Jayne Jackson",
                "Hanna Thompson"
        ],
        "raw_phrase": "I'll sync with Fateema later today.",
        "corrected_phrase": "I'll sync with Fatima later today."
},
    {
        "names": [
                "Fatima Singh",
                "Hanna Morris",
                "Jian White",
                "Yuki Thompson"
        ],
        "raw_phrase": "Fateema is the best person to talk to about this.",
        "corrected_phrase": "Fatima is the best person to talk to about this."
},
    {
        "names": [
                "Giuseppe Lefebvre",
                "Fatima Morales",
                "Hiroshi Khan"
        ],
        "raw_phrase": "Did Fateema send the report yet?",
        "corrected_phrase": "Did Fatima send the report yet?"
},
    {
        "names": [
                "Fateema Morales"
        ],
        "raw_phrase": "Hey Fatima, can you check the logs?",
        "corrected_phrase": "Hey Fateema, can you check the logs?"
},
    {
        "names": [
                "Fatima Hill"
        ],
        "raw_phrase": "I'm looking at Fateema's latest update.",
        "corrected_phrase": "I'm looking at Fatima's latest update."
},
    {
        "names": [
                "Oleksandr Murphy",
                "Katherine Murphy",
                "Giuseppe Nelson"
        ],
        "raw_phrase": "Is Guiseppe on the call?",
        "corrected_phrase": "Is Giuseppe on the call?"
},
    {
        "names": [
                "Nikolas Parker",
                "Giuseppe Mitchell",
                "Xavier Kim",
                "Katarina Cook"
        ],
        "raw_phrase": "I'll check the calendar to see when Guiseppe is free.",
        "corrected_phrase": "I'll check the calendar to see when Giuseppe is free."
},
    {
        "names": [
                "Giuseppe Murphy",
                "Arjun Stewart"
        ],
        "raw_phrase": "Guiseppe suggested a few improvements to the UI.",
        "corrected_phrase": "Giuseppe suggested a few improvements to the UI."
},
    {
        "names": [
                "Chiwetel Rossi",
                "Giuseppe Phillips"
        ],
        "raw_phrase": "I'll coordinate the meeting with Guiseppe.",
        "corrected_phrase": "I'll coordinate the meeting with Giuseppe."
},
    {
        "names": [
                "Silvio Schmidt",
                "Giuseppe Kim"
        ],
        "raw_phrase": "We should get some feedback from Guiseppe on this.",
        "corrected_phrase": "We should get some feedback from Giuseppe on this."
},
    {
        "names": [
                "Guiseppe Turner"
        ],
        "raw_phrase": "Hey Giuseppe, can you check the logs?",
        "corrected_phrase": "Hey Guiseppe, can you check the logs?"
},
    {
        "names": [
                "Giuseppe Rogers"
        ],
        "raw_phrase": "I'm looking at Guiseppe's latest update.",
        "corrected_phrase": "I'm looking at Giuseppe's latest update."
},
    {
        "names": [
                "Kieran Adams",
                "Yosef Nguyen",
                "Hassan Moore"
        ],
        "raw_phrase": "I'll be working closely with Hasan on this feature.",
        "corrected_phrase": "I'll be working closely with Hassan on this feature."
},
    {
        "names": [
                "Hassan Lee",
                "Sofia Campbell",
                "Lukas Lefebvre"
        ],
        "raw_phrase": "Is Hasan familiar with this part of the codebase?",
        "corrected_phrase": "Is Hassan familiar with this part of the codebase?"
},
    {
        "names": [
                "Silvio Rodriguez",
                "Antony Khan",
                "Hassan Ivanov",
                "Oksana King"
        ],
        "raw_phrase": "I'll coordinate the meeting with Hasan.",
        "corrected_phrase": "I'll coordinate the meeting with Hassan."
},
    {
        "names": [
                "Priya Ivanov",
                "Krysten Bailey",
                "Hassan Santos",
                "Rhaenyra Schmidt",
                "Tomas Patel"
        ],
        "raw_phrase": "Can you ask Hasan to join the Zoom?",
        "corrected_phrase": "Can you ask Hassan to join the Zoom?"
},
    {
        "names": [
                "Beatrix Ramirez",
                "Aimee Patel",
                "Hassan Ramirez"
        ],
        "raw_phrase": "I'll sync up with Hasan to make sure we're on the same page.",
        "corrected_phrase": "I'll sync up with Hassan to make sure we're on the same page."
},
    {
        "names": [
                "Hasan Peterson"
        ],
        "raw_phrase": "Hey Hassan, can you check the logs?",
        "corrected_phrase": "Hey Hasan, can you check the logs?"
},
    {
        "names": [
                "Hassan Murphy"
        ],
        "raw_phrase": "I'm looking at Hasan's latest update.",
        "corrected_phrase": "I'm looking at Hassan's latest update."
},
    {
        "names": [
                "Hanna Moore",
                "Kieran Green",
                "Yosef Bailey"
        ],
        "raw_phrase": "I'll double check the numbers with Kieron.",
        "corrected_phrase": "I'll double check the numbers with Kieran."
},
    {
        "names": [
                "Krysten Khan",
                "Rhaenyra Young",
                "Jayne Tan",
                "Kieran Williams",
                "Abhishek Tan"
        ],
        "raw_phrase": "We should get some feedback from Kieron on this.",
        "corrected_phrase": "We should get some feedback from Kieran on this."
},
    {
        "names": [
                "Kieran Carter",
                "Mathew Campbell",
                "Sofia Reed",
                "Antony Morris",
                "Xavier Rossi"
        ],
        "raw_phrase": "Kieron suggested we use a different database.",
        "corrected_phrase": "Kieran suggested we use a different database."
},
    {
        "names": [
                "Zhi Carter",
                "Qasim Nelson",
                "Kieran Garcia",
                "Sara Johnson"
        ],
        "raw_phrase": "Ask Kieron if they have the login for the staging server.",
        "corrected_phrase": "Ask Kieran if they have the login for the staging server."
},
    {
        "names": [
                "Niamh Torres",
                "Kieran Morris",
                "Gwenyth Cooper",
                "Kieran Taylor",
                "Vivian Smith"
        ],
        "raw_phrase": "Kieron is the best person to talk to about this.",
        "corrected_phrase": "Kieran is the best person to talk to about this."
},
    {
        "names": [
                "Kieron Cook"
        ],
        "raw_phrase": "Hey Kieran, can you check the logs?",
        "corrected_phrase": "Hey Kieron, can you check the logs?"
},
    {
        "names": [
                "Kieran Ramirez"
        ],
        "raw_phrase": "I'm looking at Kieron's latest update.",
        "corrected_phrase": "I'm looking at Kieran's latest update."
},
    {
        "names": [
                "Niamh Nelson",
                "Bharath Patel",
                "Jon Lefebvre",
                "Srini Davis"
        ],
        "raw_phrase": "I saw a comment from Nieve on the design doc.",
        "corrected_phrase": "I saw a comment from Niamh on the design doc."
},
    {
        "names": [
                "Xavier Young",
                "Mikhail Brown",
                "Niamh Morgan"
        ],
        "raw_phrase": "Ask Nieve if they have the login for the staging server.",
        "corrected_phrase": "Ask Niamh if they have the login for the staging server."
},
    {
        "names": [
                "Jon Khan",
                "Beatrix Tan",
                "Niamh King",
                "Marc Collins",
                "Mateo Peterson"
        ],
        "raw_phrase": "Did Nieve send the report yet?",
        "corrected_phrase": "Did Niamh send the report yet?"
},
    {
        "names": [
                "Dmitry Dubois",
                "Sundar Dubois",
                "Niamh Silva",
                "Rhaenyra Adams",
                "Yosef Martinez"
        ],
        "raw_phrase": "I'll coordinate the meeting with Nieve.",
        "corrected_phrase": "I'll coordinate the meeting with Niamh."
},
    {
        "names": [
                "Vivian Cooper",
                "Niamh Thompson"
        ],
        "raw_phrase": "I'll follow up with Nieve after the meeting.",
        "corrected_phrase": "I'll follow up with Niamh after the meeting."
},
    {
        "names": [
                "Nieve Dubois"
        ],
        "raw_phrase": "Hey Niamh, can you check the logs?",
        "corrected_phrase": "Hey Nieve, can you check the logs?"
},
    {
        "names": [
                "Niamh Morris"
        ],
        "raw_phrase": "I'm looking at Nieve's latest update.",
        "corrected_phrase": "I'm looking at Niamh's latest update."
},
    {
        "names": [
                "Niamh Rossi",
                "Xavier Patel",
                "Sanjay Davis",
                "Shawn Rogers",
                "Marc Harris"
        ],
        "raw_phrase": "I'll follow up with Neve after the meeting.",
        "corrected_phrase": "I'll follow up with Niamh after the meeting."
},
    {
        "names": [
                "Niamh Davis",
                "Megan Garcia",
                "Dmitry Dubois",
                "Katherine Davis",
                "Jian Jones"
        ],
        "raw_phrase": "I'll double check the numbers with Neve.",
        "corrected_phrase": "I'll double check the numbers with Niamh."
},
    {
        "names": [
                "Saoirse Adams",
                "Kah Mun Rodriguez",
                "Niamh Green",
                "Niamh Jones"
        ],
        "raw_phrase": "Did Neve catch that error in the logs?",
        "corrected_phrase": "Did Niamh catch that error in the logs?"
},
    {
        "names": [
                "Jian Jackson",
                "Niamh Cook",
                "Stephen Davis",
                "Jayne Evans",
                "Fatima Turner"
        ],
        "raw_phrase": "Please send the invite to Neve.",
        "corrected_phrase": "Please send the invite to Niamh."
},
    {
        "names": [
                "Damian Ivanov",
                "Niamh Tan",
                "Kieran Jones"
        ],
        "raw_phrase": "Wait for Neve before starting the meeting.",
        "corrected_phrase": "Wait for Niamh before starting the meeting."
},
    {
        "names": [
                "Neve Khan"
        ],
        "raw_phrase": "Hey Niamh, can you check the logs?",
        "corrected_phrase": "Hey Neve, can you check the logs?"
},
    {
        "names": [
                "Niamh Smith"
        ],
        "raw_phrase": "I'm looking at Neve's latest update.",
        "corrected_phrase": "I'm looking at Niamh's latest update."
},
    {
        "names": [
                "Oksana Thompson",
                "Hiroshi Jackson"
        ],
        "raw_phrase": "I saw a comment from Oxana on the design doc.",
        "corrected_phrase": "I saw a comment from Oksana on the design doc."
},
    {
        "names": [
                "Oksana Jackson",
                "Barbra Thompson",
                "Sofia Harris"
        ],
        "raw_phrase": "Oxana is leading the research on machine learning.",
        "corrected_phrase": "Oksana is leading the research on machine learning."
},
    {
        "names": [
                "Oksana Jones",
                "Alexey Miller",
                "Bharath Harris"
        ],
        "raw_phrase": "Please CC Oxana on all future updates.",
        "corrected_phrase": "Please CC Oksana on all future updates."
},
    {
        "names": [
                "Oksana Hill",
                "Yosef Baker",
                "Hanna Lefebvre"
        ],
        "raw_phrase": "Did Oxana send the report yet?",
        "corrected_phrase": "Did Oksana send the report yet?"
},
    {
        "names": [
                "Geoff Thomas",
                "Caiming Ivanov",
                "Yingbo Young",
                "Vivian Silva",
                "Oksana Patel"
        ],
        "raw_phrase": "I saw a comment from Oxana on the design doc.",
        "corrected_phrase": "I saw a comment from Oksana on the design doc."
},
    {
        "names": [
                "Oxana Reed"
        ],
        "raw_phrase": "Hey Oksana, can you check the logs?",
        "corrected_phrase": "Hey Oxana, can you check the logs?"
},
    {
        "names": [
                "Oksana Hill"
        ],
        "raw_phrase": "I'm looking at Oxana's latest update.",
        "corrected_phrase": "I'm looking at Oksana's latest update."
},
    {
        "names": [
                "Pavel Roberts",
                "Kieran Singh",
                "Yingbo Mitchell",
                "Antony Taylor",
                "Alexey Rodriguez"
        ],
        "raw_phrase": "Did Paul catch that error in the logs?",
        "corrected_phrase": "Did Pavel catch that error in the logs?"
},
    {
        "names": [
                "Megan Brown",
                "Chen Jackson",
                "Pavel Peterson",
                "Sundar Morris",
                "Silvio Patel"
        ],
        "raw_phrase": "I'll ask Paul to walk us through the deployment process.",
        "corrected_phrase": "I'll ask Pavel to walk us through the deployment process."
},
    {
        "names": [
                "Aarav Singh",
                "Pavel Nelson",
                "Qasim Williams"
        ],
        "raw_phrase": "Check with Paul about the API credentials.",
        "corrected_phrase": "Check with Pavel about the API credentials."
},
    {
        "names": [
                "Saoirse Roberts",
                "Stephen Rossi",
                "Susannah Martin",
                "Pavel Scott",
                "Mikhail Williams"
        ],
        "raw_phrase": "Paul is currently out of office until Monday.",
        "corrected_phrase": "Pavel is currently out of office until Monday."
},
    {
        "names": [
                "Pavel King",
                "Alexey Dubois"
        ],
        "raw_phrase": "I'll follow up with Paul after the meeting.",
        "corrected_phrase": "I'll follow up with Pavel after the meeting."
},
    {
        "names": [
                "Paul Williams"
        ],
        "raw_phrase": "Hey Pavel, can you check the logs?",
        "corrected_phrase": "Hey Paul, can you check the logs?"
},
    {
        "names": [
                "Pavel Nguyen"
        ],
        "raw_phrase": "I'm looking at Paul's latest update.",
        "corrected_phrase": "I'm looking at Pavel's latest update."
},
    {
        "names": [
                "Srini Williams",
                "Oleksandr Nguyen",
                "Qasim Patel"
        ],
        "raw_phrase": "Kasim is presenting their findings at the all-hands.",
        "corrected_phrase": "Qasim is presenting their findings at the all-hands."
},
    {
        "names": [
                "Qasim Stewart",
                "Eric Ivanov"
        ],
        "raw_phrase": "Kasim suggested a few improvements to the UI.",
        "corrected_phrase": "Qasim suggested a few improvements to the UI."
},
    {
        "names": [
                "Qasim Evans",
                "Domhnall Dubois"
        ],
        "raw_phrase": "Kasim has a lot of experience with React.",
        "corrected_phrase": "Qasim has a lot of experience with React."
},
    {
        "names": [
                "Zainab Stewart",
                "Qasim White"
        ],
        "raw_phrase": "We should get some feedback from Kasim on this.",
        "corrected_phrase": "We should get some feedback from Qasim on this."
},
    {
        "names": [
                "Jayne Schmidt",
                "Qasim Tan",
                "Vihaan Cook"
        ],
        "raw_phrase": "I'll double check the numbers with Kasim.",
        "corrected_phrase": "I'll double check the numbers with Qasim."
},
    {
        "names": [
                "Kasim Santos"
        ],
        "raw_phrase": "Hey Qasim, can you check the logs?",
        "corrected_phrase": "Hey Kasim, can you check the logs?"
},
    {
        "names": [
                "Qasim Rogers"
        ],
        "raw_phrase": "I'm looking at Kasim's latest update.",
        "corrected_phrase": "I'm looking at Qasim's latest update."
},
    {
        "names": [
                "Rhaenyra M\u00fcller",
                "Vivian Dubois",
                "Megan Thomas"
        ],
        "raw_phrase": "Did Raniera finish the documentation for the new API?",
        "corrected_phrase": "Did Rhaenyra finish the documentation for the new API?"
},
    {
        "names": [
                "Barbra Ivanov",
                "Mathew Hill",
                "Rhaenyra Young"
        ],
        "raw_phrase": "Raniera mentioned the deadline was moved.",
        "corrected_phrase": "Rhaenyra mentioned the deadline was moved."
},
    {
        "names": [
                "Mathew Carter",
                "Rhaenyra Adams",
                "Priya Collins",
                "Megan Khan"
        ],
        "raw_phrase": "Please make sure Raniera has access to the repository.",
        "corrected_phrase": "Please make sure Rhaenyra has access to the repository."
},
    {
        "names": [
                "Shawn Roberts",
                "Rhaenyra Martin",
                "Phillip Murphy",
                "Gwenyth Green",
                "Zhi Hill"
        ],
        "raw_phrase": "Raniera found a bug in the production environment.",
        "corrected_phrase": "Rhaenyra found a bug in the production environment."
},
    {
        "names": [
                "Bharath Scott",
                "Rhaenyra Lefebvre",
                "Ulysses Reed"
        ],
        "raw_phrase": "Raniera suggested we use a different database.",
        "corrected_phrase": "Rhaenyra suggested we use a different database."
},
    {
        "names": [
                "Raniera Mitchell"
        ],
        "raw_phrase": "Hey Rhaenyra, can you check the logs?",
        "corrected_phrase": "Hey Raniera, can you check the logs?"
},
    {
        "names": [
                "Rhaenyra Morgan"
        ],
        "raw_phrase": "I'm looking at Raniera's latest update.",
        "corrected_phrase": "I'm looking at Rhaenyra's latest update."
},
    {
        "names": [
                "Saoirse Kim",
                "Juliet Murphy"
        ],
        "raw_phrase": "Sersha is first on the standup list.",
        "corrected_phrase": "Saoirse is first on the standup list."
},
    {
        "names": [
                "Saoirse Williams",
                "Claire Martin",
                "Stephen Mitchell",
                "Li Stewart"
        ],
        "raw_phrase": "Can Sersha join the sync tomorrow morning?",
        "corrected_phrase": "Can Saoirse join the sync tomorrow morning?"
},
    {
        "names": [
                "Saoirse Morris",
                "Giuseppe Khan",
                "Katherine Moore",
                "Beatrix Stewart",
                "Rachael Edwards"
        ],
        "raw_phrase": "I'm going to grab a coffee with Sersha later.",
        "corrected_phrase": "I'm going to grab a coffee with Saoirse later."
},
    {
        "names": [
                "Gwenyth Adams",
                "Saoirse Bailey",
                "Tomas Kim"
        ],
        "raw_phrase": "Check with Sersha about the API credentials.",
        "corrected_phrase": "Check with Saoirse about the API credentials."
},
    {
        "names": [
                "Mateo Tan",
                "Caiming Rogers",
                "Saoirse Green",
                "Arjun Murphy"
        ],
        "raw_phrase": "Sersha mentioned the deadline was moved.",
        "corrected_phrase": "Saoirse mentioned the deadline was moved."
},
    {
        "names": [
                "Sersha Nelson"
        ],
        "raw_phrase": "Hey Saoirse, can you check the logs?",
        "corrected_phrase": "Hey Sersha, can you check the logs?"
},
    {
        "names": [
                "Saoirse Martin"
        ],
        "raw_phrase": "I'm looking at Sersha's latest update.",
        "corrected_phrase": "I'm looking at Saoirse's latest update."
},
    {
        "names": [
                "Isabelle Carter",
                "Katherine Thompson",
                "Jon Santos",
                "Thierry Green"
        ],
        "raw_phrase": "Terry has a lot of experience with React.",
        "corrected_phrase": "Thierry has a lot of experience with React."
},
    {
        "names": [
                "Aimee Jones",
                "Thierry Harris",
                "Yingbo Mitchell",
                "Mei Hill",
                "Thierry Morgan"
        ],
        "raw_phrase": "Terry found a bug in the production environment.",
        "corrected_phrase": "Thierry found a bug in the production environment."
},
    {
        "names": [
                "Shawn Adams",
                "Thierry Baker",
                "Pavel Hill"
        ],
        "raw_phrase": "Terry suggested we use a different database.",
        "corrected_phrase": "Thierry suggested we use a different database."
},
    {
        "names": [
                "Hanna Carter",
                "Thierry Adams",
                "Yosef Williams"
        ],
        "raw_phrase": "Terry is first on the standup list.",
        "corrected_phrase": "Thierry is first on the standup list."
},
    {
        "names": [
                "Dmitry Schmidt",
                "Thierry Silva"
        ],
        "raw_phrase": "Wait for Terry before starting the meeting.",
        "corrected_phrase": "Wait for Thierry before starting the meeting."
},
    {
        "names": [
                "Terry Morales"
        ],
        "raw_phrase": "Hey Thierry, can you check the logs?",
        "corrected_phrase": "Hey Terry, can you check the logs?"
},
    {
        "names": [
                "Thierry Young"
        ],
        "raw_phrase": "I'm looking at Terry's latest update.",
        "corrected_phrase": "I'm looking at Thierry's latest update."
},
    {
        "names": [
                "Dmitry Green",
                "Tomas Taylor",
                "Ishaan Scott",
                "Ulysses Ramirez",
                "Priya Phillips"
        ],
        "raw_phrase": "Did Ulises catch that error in the logs?",
        "corrected_phrase": "Did Ulysses catch that error in the logs?"
},
    {
        "names": [
                "Ulysses Rogers",
                "Elisabeth Moore",
                "Mathew Johnson",
                "Kah Mun Johnson"
        ],
        "raw_phrase": "Ulises is the one who originally wrote this script.",
        "corrected_phrase": "Ulysses is the one who originally wrote this script."
},
    {
        "names": [
                "Ulysses Tan",
                "Xavier Phillips"
        ],
        "raw_phrase": "Ulises found a bug in the production environment.",
        "corrected_phrase": "Ulysses found a bug in the production environment."
},
    {
        "names": [
                "Mateo Peterson",
                "Ulysses Taylor",
                "Oksana Taylor",
                "Alexey Davis"
        ],
        "raw_phrase": "Ask Ulises if they have the login for the staging server.",
        "corrected_phrase": "Ask Ulysses if they have the login for the staging server."
},
    {
        "names": [
                "Ulysses Thomas",
                "Jian Campbell",
                "Barbra Murphy",
                "Kieran Baker",
                "Priya Taylor"
        ],
        "raw_phrase": "I'll be working closely with Ulises on this feature.",
        "corrected_phrase": "I'll be working closely with Ulysses on this feature."
},
    {
        "names": [
                "Ulises Bailey"
        ],
        "raw_phrase": "Hey Ulysses, can you check the logs?",
        "corrected_phrase": "Hey Ulises, can you check the logs?"
},
    {
        "names": [
                "Ulysses Jones"
        ],
        "raw_phrase": "I'm looking at Ulises's latest update.",
        "corrected_phrase": "I'm looking at Ulysses's latest update."
},
    {
        "names": [
                "Giuseppe Rossi",
                "Hiroshi Johnson",
                "Xavier Turner",
                "Abhishek Davis",
                "Xavier Thompson"
        ],
        "raw_phrase": "Is Zavier joining the happy hour tonight?",
        "corrected_phrase": "Is Xavier joining the happy hour tonight?"
},
    {
        "names": [
                "Xavier Johnson",
                "Katarina Rossi",
                "Susannah Reed"
        ],
        "raw_phrase": "Has Zavier updated their ticket?",
        "corrected_phrase": "Has Xavier updated their ticket?"
},
    {
        "names": [
                "Vihaan Kim",
                "Xavier Williams",
                "Nikolas Reed"
        ],
        "raw_phrase": "I'm waiting on Zavier to approve the changes.",
        "corrected_phrase": "I'm waiting on Xavier to approve the changes."
},
    {
        "names": [
                "Niamh Moore",
                "Xavier Silva",
                "Silvio M\u00fcller",
                "Giuseppe Green",
                "Sanjay Torres"
        ],
        "raw_phrase": "Is Zavier familiar with this part of the codebase?",
        "corrected_phrase": "Is Xavier familiar with this part of the codebase?"
},
    {
        "names": [
                "Abhishek Dubois",
                "Xavier Rossi",
                "Damian Morales",
                "Priya Evans",
                "Srini Turner"
        ],
        "raw_phrase": "Is Zavier familiar with this part of the codebase?",
        "corrected_phrase": "Is Xavier familiar with this part of the codebase?"
},
    {
        "names": [
                "Zavier M\u00fcller"
        ],
        "raw_phrase": "Hey Xavier, can you check the logs?",
        "corrected_phrase": "Hey Zavier, can you check the logs?"
},
    {
        "names": [
                "Xavier Peterson"
        ],
        "raw_phrase": "I'm looking at Zavier's latest update.",
        "corrected_phrase": "I'm looking at Xavier's latest update."
},
    {
        "names": [
                "Yosef Williams",
                "Claire Collins",
                "Bryan Williams",
                "Priya Williams",
                "Alexey Bailey"
        ],
        "raw_phrase": "I sent the draft to Joseph for some initial thoughts.",
        "corrected_phrase": "I sent the draft to Yosef for some initial thoughts."
},
    {
        "names": [
                "Sundar M\u00fcller",
                "Sanjay Dubois",
                "Yosef Smith"
        ],
        "raw_phrase": "Joseph is presenting their findings at the all-hands.",
        "corrected_phrase": "Yosef is presenting their findings at the all-hands."
},
    {
        "names": [
                "Yingbo Jones",
                "Sundar Nguyen",
                "Zainab Jackson",
                "Yosef Turner"
        ],
        "raw_phrase": "I'll coordinate the meeting with Joseph.",
        "corrected_phrase": "I'll coordinate the meeting with Yosef."
},
    {
        "names": [
                "Yosef Jones",
                "Yuki Kim",
                "Arjun Scott",
                "Krysten Parker",
                "Srini Dubois"
        ],
        "raw_phrase": "I need to discuss the roadmap with Joseph.",
        "corrected_phrase": "I need to discuss the roadmap with Yosef."
},
    {
        "names": [
                "Bharath Lee",
                "Yosef Baker",
                "Giuseppe Phillips"
        ],
        "raw_phrase": "Joseph is taking the lead on the frontend refactor.",
        "corrected_phrase": "Yosef is taking the lead on the frontend refactor."
},
    {
        "names": [
                "Joseph Morris"
        ],
        "raw_phrase": "Hey Yosef, can you check the logs?",
        "corrected_phrase": "Hey Joseph, can you check the logs?"
},
    {
        "names": [
                "Yosef Kim"
        ],
        "raw_phrase": "I'm looking at Joseph's latest update.",
        "corrected_phrase": "I'm looking at Yosef's latest update."
},
    {
        "names": [
                "Jon Thomas",
                "Zainab Jackson",
                "Sanjay Moore",
                "Teresa Johnson"
        ],
        "raw_phrase": "Please send the invite to Zaynab.",
        "corrected_phrase": "Please send the invite to Zainab."
},
    {
        "names": [
                "Zainab Schmidt",
                "Sanjay Bailey",
                "Damian Johnson",
                "Caiming Evans"
        ],
        "raw_phrase": "Can Zaynab join the sync tomorrow morning?",
        "corrected_phrase": "Can Zainab join the sync tomorrow morning?"
},
    {
        "names": [
                "Zainab Santos",
                "Antony Edwards",
                "Zainab Torres",
                "Phillip Roberts",
                "Silvio Scott"
        ],
        "raw_phrase": "Zaynab's PR is ready for review.",
        "corrected_phrase": "Zainab's PR is ready for review."
},
    {
        "names": [
                "Vihaan Roberts",
                "Damian Phillips",
                "Yosef Evans",
                "Zainab Turner",
                "Zainab Green"
        ],
        "raw_phrase": "I'll check the calendar to see when Zaynab is free.",
        "corrected_phrase": "I'll check the calendar to see when Zainab is free."
},
    {
        "names": [
                "Nikolas Reed",
                "Zainab Morales",
                "Sanjay Kim",
                "Zainab Moore"
        ],
        "raw_phrase": "Zaynab mentioned the deadline was moved.",
        "corrected_phrase": "Zainab mentioned the deadline was moved."
},
    {
        "names": [
                "Zaynab Thompson"
        ],
        "raw_phrase": "Hey Zainab, can you check the logs?",
        "corrected_phrase": "Hey Zaynab, can you check the logs?"
},
    {
        "names": [
                "Zainab Young"
        ],
        "raw_phrase": "I'm looking at Zaynab's latest update.",
        "corrected_phrase": "I'm looking at Zainab's latest update."
},
]

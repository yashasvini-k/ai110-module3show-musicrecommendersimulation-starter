# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  
VibeFinder 1.0
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This system suggests up to 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and valence. It is intended for classroom exploration of how content-based recommendation algorithms work. It is not intended for real users, production environments, or any platform where recommendation quality directly affects user experience.


---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Each song in the catalog is given a relevance score by comparing its attributes to the user's taste profile. A genre match adds 2 points, a mood match adds 1 point, and two additional scores between 0 and 1 are added based on how close the song's energy and valence are to the user's targets. The closer the match, the higher the score. All songs are then sorted by score and the top 5 are returned with a plain-language explanation of why each one ranked where it did.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The dataset is a small CSV file containing songs with attributes including genre, mood, energy, valence, danceability, acousticness, and tempo. The catalog was expanded from 10 starter songs to include additional entries across a wider range of genres and moods. The dataset is fictional and small, meaning it does not represent the diversity of real-world music and likely over-represents certain genres like pop.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system is fully transparent — every recommendation includes a plain-language explanation of exactly why it ranked where it did. It works immediately for any new song as long as that song has metadata, with no user interaction history needed. The scoring logic is simple enough to reason about and debug by hand, which makes it a good learning tool for understanding how features influence predictions.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system over-prioritizes genre matching because the genre weight (2.0) is double any other feature. This means a pop song with completely mismatched energy and mood will often outscore a lofi song that perfectly matches the user's energy and valence targets. Additionally, if the dataset has more songs in one genre than others, that genre will naturally dominate recommendations across all profiles. The system also assumes every user cares equally about genre vs. mood vs. energy, when in reality different listeners weight these features very differently.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested three distinct user profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock. The High-Energy Pop profile produced the most intuitive results because the dataset likely contains more pop songs. The Chill Lofi profile sometimes surfaced unexpected results when no lofi songs in the catalog matched both mood and energy closely. I also ran a weight experiment by doubling the energy weight, which changed rankings noticeably for profiles where genre and energy were in tension, confirming that the genre weight has an outsized influence on results in the default configuration.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- Add a diversity rule so the same artist or genre cannot appear more than twice in the top 5 results
- Let users adjust their own feature weights through a simple CLI prompt instead of hardcoding them
- Expand the dataset to include at least 50 songs across 8 or more genres so recommendations are less repetitive across different profiles

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this recommender made it clear how much a simple weighting decision shapes what a user sees. The biggest surprise was how strongly the genre weight dominated results — doubling the energy weight visibly shifted rankings, which showed me that small math choices have real consequences for what gets recommended and what gets buried. Using Copilot helped me move faster through boilerplate like the CSV loader and scoring function structure, but I still needed to double-check that the logic matched my intended recipe, especially the closeness formula for energy and valence. What surprised me most was that even a five-line scoring function can produce results that genuinely feel like recommendations — it made me realize that real systems are doing the same thing at much larger scale with many more features. If I extended this project I would add a diversity penalty so the same artist cannot appear more than once in the top 5, and I would experiment with letting users weight features themselves rather than hardcoding the weights.
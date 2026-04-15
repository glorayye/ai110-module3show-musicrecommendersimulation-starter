# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and YouTube combine two strategies: collaborative filtering, which surfaces songs that users with similar taste enjoyed, and content-based filtering, which matches songs based on their audio attributes like energy, mood, and tempo. At scale, these systems layer in contextual signals (time of day, device, recent skips) and use machine learning to continuously re-weight what matters most for each user. This version prioritizes content-based filtering — it scores each song by comparing its attributes to a user's stated preferences, rewards closeness rather than magnitude, and ranks the full catalog to return the best matches. The goal is transparency: every recommendation can be traced back to a specific feature comparison, making it easy to understand why a song was suggested and where the system falls short.

### Song Features

Each `Song` stores: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`.

### User Profile Fields

Each `UserProfile` stores: `favorite_genre`, `favorite_mood`, `target_energy`, `target_valence`, `target_tempo_bpm`, `target_danceability`, `target_acousticness`, `likes_acoustic`.

### Algorithm Recipe

Every song in the catalog is scored against the user profile using these rules:

| Rule | Points |
|---|---|
| Genre exact match | +2.0 |
| Mood exact match | +1.5 |
| Energy closeness: `1 − │song − target│ × 1.0` | 0.0 – 1.00 |
| Valence closeness `× 0.75` | 0.0 – 0.75 |
| Tempo closeness (normalized ÷ 200) `× 0.50` | 0.0 – 0.50 |
| Acousticness closeness `× 0.50` | 0.0 – 0.50 |
| Danceability closeness `× 0.25` | 0.0 – 0.25 |
| **Maximum possible score** | **6.50** |

All songs are then sorted by score (descending) and the top `k` are returned.

### Data Flow

```
songs.csv ──▶ load_songs ──▶ score every song (loop) ──▶ sort descending ──▶ top K results
                               ▲
                          user_prefs dict
```

### Expected Biases

- **Genre dominance:** At +2.0, a genre match outweighs all numeric signals combined in many cases. A song with a perfect energy, valence, and tempo match but a different genre will still lose to a mediocre same-genre song. This could bury cross-genre gems (e.g., a folk track that feels exactly like the user's target energy).
- **Mood as a hard filter:** Mood is binary — no partial credit for adjacent moods like *focused* vs. *chill*. A focused listener will score *chill* songs the same as *aggressive* ones, even though focused and chill are far closer in spirit.
- **Cold start gap:** The profile requires explicit target values for every feature. A real user who just says "I like Mumford & Sons" would need those values inferred — this system has no mechanism for that.
- **Catalog skew:** The dataset of 17 songs has 3 lofi tracks but only 1 classical and 1 latin track. Genre-matched recommendations will be richer for lofi listeners than for latin listeners, purely due to catalog size.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

## 10. Screenshot of recommendations 
![top 3 recs](image.png)
![remaining 2 recs ](image-1.png)
# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch suggests songs from a small catalog based on a user's stated taste preferences — things like their favorite genre, preferred mood, and how energetic or acoustic they like their music. It is built for classroom exploration, not real users. It assumes the user already knows what they like and can describe it numerically — it has no way to learn preferences from listening history or feedback. Every recommendation is fully explainable: you can see exactly which features caused each song to score well or poorly.

---

## 3. How the Model Works

Think of it like a judge scoring contestants. Every song in the catalog gets judged against the user's preferences, and the songs with the highest scores get recommended.

The judge awards points in two ways. First, it checks labels: if a song's genre matches the user's favorite genre, it gets a bonus. Same for mood. These are yes-or-no checks — either it matches or it doesn't. Second, it measures how close each song's audio qualities are to what the user wants. For energy, it asks: how far is this song from the user's target energy level? A song that's very close gets nearly full points; a song that's far away gets fewer. The same closeness check runs for valence (how happy or dark the song sounds), tempo, acousticness, and danceability. All the points are added up, the songs are sorted from highest to lowest score, and the top five are returned.

One additional rule was added during testing: if a user says they prefer acoustic music, any song that is strongly non-acoustic receives a small penalty. This prevents a song from scoring well on labels alone while completely ignoring what the user actually wants to hear.

---

## 4. Data

The catalog contains 17 songs stored in a CSV file. The original starter dataset had 10 songs; 7 were added to improve diversity. Genres represented include pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, metalcore, country, r&b, classical, hip-hop, and latin. Moods include happy, chill, intense, relaxed, focused, moody, emotional, aggressive, nostalgic, soulful, melancholic, and triumphant. Each song has 10 attributes: title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The dataset skews toward Western popular music and has no representation of regional genres like Afrobeats, K-pop, or reggae. Lofi is the most represented genre with three songs, while most other genres have only one — meaning the system naturally gives more variety to lofi listeners than to listeners of underrepresented genres.

---

## 5. Strengths

The system works best when the user's preferences are internally consistent — for example, the intense profile (high energy, fast tempo, low acousticness, rock genre) produced results that felt immediately right, with Storm Runner scoring 6.46 out of 6.50 and every signal aligned. It also handles the absence of categorical matches gracefully: when the ghost profile used genres and moods not in the catalog, the numeric features alone still produced a sensible ranking. The scoring is fully transparent — every point awarded is printed with an explanation, so there are no black-box decisions. This makes it easy to understand why a song was recommended and to diagnose when something feels off.

---

## 6. Limitations and Bias

The most significant weakness discovered through testing is that categorical signals — genre and mood — can override what the audio features clearly say. During the "contradiction" experiment, a user profile with targets that perfectly matched *Clair de Lune* (low energy, slow tempo, near-pure acousticness) still received songs like *Deceivers* near the top simply because the genre label matched, even though the actual sound of that song was the opposite of what the numeric targets described. This happens because genre and mood are awarded fixed bonus points regardless of how well the rest of the song fits, meaning a song that gets a genre match starts with a significant head start over songs that are aurally closer to the user's preference. The system treats genre as a hard signal when in reality it is just a loose category — two songs can share a genre and sound completely different. A fairer design would either reduce the genre bonus further or replace it with a softer similarity measure that accounts for genre overlap, such as grouping rock and metalcore as neighbors rather than treating them as entirely unrelated.

---

## 7. Evaluation

Six user profiles were tested across two categories: three standard profiles (intense, chill, upbeat) and three adversarial profiles (ghost, contradiction, extremes). For each profile, the top 5 recommendations were checked against musical intuition — asking whether a real listener with those preferences would actually enjoy the songs returned. The intense profile performed best, correctly surfacing Storm Runner at 6.46/6.50 with every signal aligned, and consistently separating high-energy tracks from chill or acoustic ones. The ghost profile was the most revealing: with no genre or mood match possible, the ranking fell entirely to numeric closeness, and the results felt reasonable — songs with similar energy and acousticness clustered together even without labels. The contradiction profile exposed the genre dominance bias most clearly: a user whose numeric targets pointed directly at Clair de Lune still received rock and metalcore songs ranked higher because genre matched. The extremes profile uncovered a self-contradiction problem — requesting maximum energy and maximum acousticness simultaneously is physically impossible, and the system had no way to flag or resolve that conflict. The acoustic mismatch penalty was added mid-experiment after observing this, which reduced Pepas' score and surfaced more genuinely acoustic songs, confirming that targeted penalties can correct for weight imbalances without affecting unrelated profiles.

---

## 8. Future Work

The most valuable improvement would be replacing binary genre matching with a similarity table that groups related genres together — so rock and metalcore are treated as closer than rock and classical, rather than equally different. A second improvement would be adding contradiction detection: if a user sets `target_energy` very low but `target_tempo_bpm` very high, the system should warn that those preferences are hard to satisfy simultaneously. Third, the catalog needs to grow significantly — 17 songs is too small to serve listeners in underrepresented genres like classical or latin, where only one song exists. Finally, adding support for negative preferences (e.g., "I never want aggressive songs") would make the system more expressive without requiring the user to specify a positive target for every feature.

---

## 9. Personal Reflection

Building this system made it clear that recommendation is not just a math problem — it is a design problem. Every weight is a choice about what matters, and those choices have consequences for which users the system serves well and which it fails. The most surprising discovery was how much damage a single dominant signal can do: reducing genre from +2.0 to +1.0 immediately changed which songs appeared in the top 5, which showed how sensitive the whole ranking is to a single number. It also changed how I think about apps like Spotify — when Discover Weekly surprises me with something unexpected, it is probably because their system has learned to down-weight genre and lean harder on audio similarity across millions of users. A simple rule-based system like this one will always plateau at the quality of its assumptions, which is exactly why real recommenders use machine learning to let the data decide the weights instead.
One thing I keep wondering is what would happen if every feature was weighted equally — no hierarchy, no bonus points for genre or mood. It might actually surface more surprising or diverse recommendations by not letting any single signal dominate rather provide the user with more audio-accurate songs vs user-preference. The downside might be for a user who only wants rock, equal weights would surface hip-hop and metalcore songs that sound similar but aren't what they asked for. Genre preference is real — the question is just how much it should outweigh everything else, but I haven't tested it.

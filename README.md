<br>

## Overview:

Using a Spotify dataset from Kaggle, I performed **exploratory data analysis** (EDA) and created **visualizations** to uncover **key trends** in song characteristics. I then applied **Principal Component Analysis** (PCA) and trained a **classification model** using **scikit-learn** to categorize songs into one of six distinct **"vibe" clusters**.

Building on this, I developed an interactive **Plotly Dash web application** that allows users to explore music based on both vibe and genre — a feature most music discovery tools lack, offering a more personalized way to find music that fits their taste. The app consists of two main pages:

>**Song Explorer:** Users can filter and browse songs by **mood** and **genre** to discover tracks that match their personal preferences.
>
>**Recommender System:** Users input a song and artist name to receive **customized recommendations** for similar songs based on mood and style.


## Dataset Overview

I got the dataset from kaggle, this is the link.

Below is the first five rows of the dataset. Each row represents a unique song (or track).

|    | genre   | artist_name       | track_name                       | track_id               |   popularity |   acousticness |   danceability |   duration_ms |   energy |   instrumentalness | key   |   liveness |   loudness | mode   |   speechiness |   tempo | time_signature   |   valence |
|---:|:--------|:------------------|:---------------------------------|:-----------------------|-------------:|---------------:|---------------:|--------------:|---------:|-------------------:|:------|-----------:|-----------:|:-------|--------------:|--------:|:-----------------|----------:|
|  0 | Movie   | Henri Salvador    | C'est beau de faire un Show      | 0BRjO6ga9RKCKjfDqeFgWV |            0 |          0.611 |          0.389 |         99373 |    0.91  |              0     | C#    |     0.346  |     -1.828 | Major  |        0.0525 | 166.969 | 4/4              |     0.814 |
|  1 | Movie   | Martin & les fées | Perdu d'avance (par Gad Elmaleh) | 0BjC1NfoEOOusryehmNudP |            1 |          0.246 |          0.59  |        137373 |    0.737 |              0     | F#    |     0.151  |     -5.559 | Minor  |        0.0868 | 174.003 | 4/4              |     0.816 |
|  2 | Movie   | Joseph Williams   | Don't Let Me Be Lonely Tonight   | 0CoSDzoNIKCRs124s9uTVy |            3 |          0.952 |          0.663 |        170267 |    0.131 |              0     | C     |     0.103  |    -13.879 | Minor  |        0.0362 |  99.488 | 5/4              |     0.368 |
|  3 | Movie   | Henri Salvador    | Dis-moi Monsieur Gordon Cooper   | 0Gc6TVm52BwZD07Ki6tIvf |            0 |          0.703 |          0.24  |        152427 |    0.326 |              0     | C#    |     0.0985 |    -12.178 | Major  |        0.0395 | 171.758 | 4/4              |     0.227 |
|  4 | Movie   | Fabien Nataf      | Ouverture                        | 0IuslXpMROHdEPvSl1fTQK |            4 |          0.95  |          0.331 |         82625 |    0.225 |              0.123 | F     |     0.202  |    -21.15  | Major  |        0.0456 | 140.576 | 4/4              |     0.39  |

<br>

The Columns of the Dataset Include:

**`genre`**: what genre the song is 

**`artist_name`**: the artist name

**`track_name`**: the song name

**`track_id`**: the song id (unique to each song)

**`popularity`**: A score from 0 to 100 (higher = more popular), reflecting a track’s recent streaming counts and listener engagement.

**`acousticness`**: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high
confidence the track is acoustic.

**`danceability`**: It describes how suitable a track is for dancing based on a combination of musical
elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least
danceable and 1.0 is most danceable.

**`duration_ms`**: Length of the track in milliseconds. Divide by 1,000 to convert to seconds

**`energy`**: This is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity.
Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a
Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic
range, perceived loudness, timbre, onset rate, and general entropy.

**`instrumentalness`**: Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as
instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the
instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above
0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.

**`key`**: Integer (0–11) representing the musical key of the track using pitch class notation (0 = C, 1 = C♯/D♭, etc.). -1 indicates undetected.

**`liveness`**: Float (0.0–1.0): probability that a track was performed live. Values >0.8 typically indicate live recordings.

**`loudness`**: Overall loudness of the track in decibels (dB). Typical values range from about –60 to 0 dB

**`mode`**: Musical modality: 1 = major, 0 = minor.

**`speechiness`**: It detects the presence of spoken words in a track. The more exclusively speech-like the
recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66
describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe
tracks that may contain both music and speech, either in sections or layered, including such cases as rap
music. Values below 0.33 most likely represent music and other non-speech-like tracks.

**`tempo`**: Estimated tempo in beats per minute (BPM).

**`time_signature`**: Beats per bar (time signature), usually between 3 and 7 (e.g. 4 = 4/4 time)

**`valence`**: Float (0.0–1.0): musical positiveness conveyed by the track (happy vs. negative).



## EDA
First I got rid of any duplicate rows that were in the dataset, and then I checked for NaN values and there were none. meaning my dataset was now fully cleaned and had a row for each unique song id. Next I conducted 

### Bivariate Analysis

Below is a Scatter Plot showing the relationship between the song's Danceability score and Valence Score (How happy the song is)

<iframe
  src="assets/dance_vs_valence.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

<br>
There is a clean relationship between the two suggesting that songs that are considered more danceable are happier.

### Aggregate Statistics

Reggae is considered the happiest music genre followed by children's music. While opera and soundtrack is considered the saddest. 
(soundtrack genre is the collection of music used in a film, television show, video game, or other media)

| genre            |   valence |
|:-----------------|----------:|
| Reggae           |  0.679775 |
| Children's Music |  0.675946 |
| Reggaeton        |  0.65999  |
| Ska              |  0.647291 |
| Blues            |  0.580323 |
| Country          |  0.534908 |

<br>

Ska, electronic, and alternative are notably the highest genre's in energy. Classical and Opera are the lowest (this makes sense)


| genre            |   energy |
|:-----------------|---------:|
| Ska              | 0.836923 |
| Reggaeton        | 0.748457 |
| Electronic       | 0.739263 |
| Alternative      | 0.713933 |
| Children’s Music | 0.712646 |
| Dance            | 0.696151 |

## Classifying Songs Into Moods

Using scikit-learn and PCA, I got the following clusters and labeled them with a fitting vibe/mood that fits

### Cluster 0:
>Valence: 0.47 → neutral
>
>Energy: 0.41 → relaxed
>
>Danceability: 0.59 → somewhat danceable
>
>Acousticness: 0.76 → very acoustic
>
>Tempo: 108 BPM → moderate
>

**Mood/Vibe:**
>"Chill & Acoustic"
>
>Mellow, slightly upbeat acoustic tracks — coffee shop vibes, soft indie.

<br>

### Cluster 1:

>Valence: 0.70 → happy
>
>Energy: 0.77 → very energetic
>
>Danceability: 0.58 → somewhat danceable
>
>Acousticness: 0.16 → mostly electronic/instrumental
>
>Tempo: 157 BPM → very fast

**Mood/Vibe:**
>"Hype / Workout"
>
>High-energy, positive tracks — gym, running, EDM, fast pop.

<br>

### Cluster 2:

>Valence: 0.34 → a bit sad
>
>Energy: 0.71 → energetic
>
>Danceability: 0.57 → moderate
>
>Acousticness: 0.14 → electronic
>
>Tempo: 103 BPM → medium

**Mood/Vibe:**
>"Moody Intensity"
>
>Emotionally heavy but energetic — alt rock, rap, intense vibes.

<br>

### Cluster 3:

>Valence: 0.13 → very sad
>
>Energy: 0.16 → very calm
>
>Danceability: 0.28 → low
>
>Acousticness: 0.88 → very acoustic
>
>Tempo: 100 BPM → slow

**Mood/Vibe:**

>"Sad & Soft"
>
>Depressing or emotional acoustic tracks — breakup music, slow ballads.

<br>

### Cluster 4:

>Valence: 0.28 → sad
>
>Energy: 0.68 → high
>
>Danceability: 0.43 → low-moderate
>
>Acousticness: 0.18 → electronic
>
>Tempo: 154 BPM → fast

**Mood/Vibe:**

>"Angsty / Intense"
>
>Sad but energetic and fast — punk rock, fast rap, maybe rage-type music.

<br>

### Cluster 5:

>Valence: 0.74 → happy
>
>Energy: 0.69 → upbeat
>
>Danceability: 0.73 → very danceable
>
>Acousticness: 0.20 → electronic
>
>Tempo: 106 BPM → moderate

**Mood/Vibe:**

>"Feel-Good / Dance"
>
>Upbeat and fun — feel-good pop, party music, mainstream dance.

<br>

Below is a visualization of the clusters:

<iframe
  src="assets/vibe_clusters.png"
  width="800"
  height="600"
  frameborder="0"
></iframe>


<br>

# **Plotly Dashboard**

## Home Page

## Recommendation Page
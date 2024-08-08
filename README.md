# Spotify Recommendation System
Evaluates song likeness on 16 features through vector-cosine similarity. Utilizes a database of 160000 tracks which describes songs with 16 features. Each playlist analyzed is given a summary based on these features. Searches for a song in the database which is similar to the playlist summary through vector-cosine and recommends those tracks which are mathematically alike. 

A pie chart generator which imports top track listening data, extracts genre information (available only through track-artist info), and weights the genre popularity in the listener's data by how high-ranked that song is on their top tracks list. Imports the top 500 most listened to songs in the past 6 months (defined by "medium-length" stats on Spotify API docs). 

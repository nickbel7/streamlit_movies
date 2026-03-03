import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("movies.csv")

# Extract year from title (e.g. "Toy Story (1995)" → 1995)
df['year'] = df['title'].str.extract(r'\((\d{4})\)').astype(float)

# Clean genre Column and split the genres.  Important step.
df['genres'] = df['genres'].str.split('|')
df_exploded = df.explode('genres') # Create a new row for each genre

# Streamlit app
st.title(" 🎬  Movie Genre Explorer")

# Genre selection
all_genres = sorted(df_exploded['genres'].unique())
selected_genre = st.selectbox("Select a Genre", all_genres)

# Year range slider
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Filter movies by genre and year
genre_movies = df_exploded[
    (df_exploded["genres"] == selected_genre) &
    (df_exploded["year"] >= year_range[0]) &
    (df_exploded["year"] <= year_range[1])
][["title", "year", "genres"]]

# Display movies table
st.subheader(f"Movies in {selected_genre} Genre")
st.dataframe(genre_movies)

# Genre distribution
st.subheader("Genre Distribution")
genre_counts = df_exploded['genres'].value_counts()
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax1, palette="viridis")
ax1.set_xlabel("Number of Movies")
ax1.set_ylabel("")
st.pyplot(fig1)

# Movies released per year
st.subheader("Movies per Year")
movies_per_year = df.groupby('year')['title'].count()
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.fill_between(movies_per_year.index, movies_per_year.values, color="steelblue")
ax2.plot(movies_per_year.index, movies_per_year.values, color="steelblue")
ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Movies")
st.pyplot(fig2)

# Top genres pie chart
st.subheader("Top 5 Genres Share")
top_genres = df_exploded['genres'].value_counts().head(5)
fig3, ax3 = plt.subplots(figsize=(7, 7))
ax3.pie(top_genres.values, labels=top_genres.index, autopct='%1.1f%%')
st.pyplot(fig3)

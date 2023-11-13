import csv
import json
import numpy as np
import re
import requests
import sys

from deep_translator import GoogleTranslator

OMDB_API_KEY = "xxx"


class Movie:
    def __init__(self, title, rating):
        self.title = title
        self.rating = rating

    def __str__(self):
        try:
            description = requests.get(
                f"https://www.omdbapi.com/?apikey={
                    OMDB_API_KEY}&t={self.title}"
            ).json().get("Plot")

            if description == None:
                raise Exception("Empty description")
        except:
            description = "Failed to fetch description from external API"

        return f"{self.title} - {description}"

    def __repr__(self):
        return self.__str__()


GOOD_SCORE_THRESHOLD = 8
NUMBER_OF_PROPOSED_MOVIES = 5

translator = GoogleTranslator(source='auto', target='en')


try:
    with open('cache.json') as jsonfile:
        data = json.load(jsonfile)
except:
    with open('data.csv') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            data.append([])

            i = 0
            for movie_or_rating in row:
                movie_or_rating = re.sub(r'\s+', ' ', movie_or_rating.strip())
                if movie_or_rating == '':
                    break

                if i % 2 == 0:
                    capitalized_words = ' '.join(
                        [word.capitalize()
                         for word in movie_or_rating.split(' ')]
                    )

                    en_movie = translator.translate(capitalized_words)

                    data[-1].append([en_movie])
                else:
                    data[-1][-1].append(float(movie_or_rating))

                i += 1

        with open('cache.json', 'w') as jsonfile:
            json.dump(data, jsonfile)

data = [
    [
        Movie(
            movie_and_rating[0],
            movie_and_rating[1]
        )
        for movie_and_rating in user_movies
    ] for user_movies in data
]


def euclidean_score(movies1: list[Movie], movies2: list[Movie]):
    squared_diffs = []

    rating_per_title = {}

    for movie1 in movies1:
        rating_per_title[movie1.title] = movie1.rating

    for movie2 in movies2:
        title = movie2.title
        if title in rating_per_title:
            squared_diffs.append(
                np.square(movie2.rating - rating_per_title[title])
            )

    if len(squared_diffs) == 0:
        return 0

    return 1.0 / (1.0 + np.sqrt(np.sum(squared_diffs)))


def pearson_score(movies1: list[Movie], movies2: list[Movie]):
    rating_per_title = {}
    rating_count = 0
    user1_sum = 0
    user2_sum = 0

    user1_squared_sum = 0
    user2_squared_sum = 0

    sum_of_products = 0

    for movie1 in movies1:
        rating_per_title[movie1.title] = movie1.rating

    for i, movie2 in enumerate(movies2):
        title = movie2[0]
        if title in rating_per_title:
            rating_count += 1
            user1_movie_rating = rating_per_title[title]
            user2_movie_rating = movies2[i].rating

            user1_sum += user1_movie_rating
            user2_sum += user2_movie_rating

            user1_squared_sum += pow(user1_movie_rating, 2)
            user2_squared_sum += pow(user2_movie_rating, 2)

            sum_of_products += user1_movie_rating * user2_movie_rating

    if rating_count == 0:
        return 0

    sxy = sum_of_products - (user1_sum * user2_sum / rating_count)
    sxx = user1_squared_sum - np.square(user1_sum) / rating_count
    syy = user2_squared_sum - np.square(user2_sum) / rating_count

    if sxx * syy == 0:
        return 0

    return sxy / np.sqrt(sxx * syy)


user_index = int(sys.argv[1].strip())
user_scores = []
user_movies = data[user_index]
score_method_type = sys.argv[2].lower()


for i, other_user_movies in enumerate(data):
    if i == user_index:
        user_scores.append(0)
    else:
        if score_method_type == "pearson":
            user_scores.append(pearson_score(user_movies, other_user_movies))
        else:
            user_scores.append(euclidean_score(user_movies, other_user_movies))

user_indexes_with_movies = []
for index, user_movies_2 in enumerate(data):
    user_indexes_with_movies.append([index, user_movies_2])


def flatten(l):
    return [item for sublist in l for item in sublist]


def generate_movie_proposition(movies: list[Movie], banned_movies: set[str]):
    selected_movies = []

    for movie in movies:
        if movie.title not in banned_movies and movie.rating >= GOOD_SCORE_THRESHOLD:
            selected_movies.append(movie)
        if len(selected_movies) == NUMBER_OF_PROPOSED_MOVIES:
            break

    return selected_movies


banned_movies = set()
for movie in user_movies:
    banned_movies.add(movie.title)


movies_ordered_by_relevance_desc = flatten([
    index_and_movies[1] for index_and_movies in sorted(
        user_indexes_with_movies,
        key=lambda index_and_movies: -user_scores[index_and_movies[0]]
    )
])

recommended_movies = generate_movie_proposition(
    movies_ordered_by_relevance_desc, banned_movies
)

print(f"Recommended movies to watch for user {user_index}:")
for movie in recommended_movies:
    print(movie)
    print()

for already_recommended_movie in recommended_movies:
    banned_movies.add(already_recommended_movie.title)


movies_ordered_by_relevence_asc = flatten([
    index_and_movies[1] for index_and_movies in sorted(
        user_indexes_with_movies,
        key=lambda index_and_movies: user_scores[index_and_movies[0]]
    )
])

print(f"Not recommended movies to watch for user {user_index}:")
for movie in generate_movie_proposition(movies_ordered_by_relevence_asc, banned_movies):
    print(movie)
    print()

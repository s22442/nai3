import csv
import json
import numpy as np
import re
import sys

from deep_translator import GoogleTranslator

USER_INDEX = 11

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


def euclidean_score(movies_with_ratings_1, movies_with_ratings_2):
    squared_diff = []

    rating_per_movie = {}

    for movie_and_rating in movies_with_ratings_1:
        rating_per_movie[movie_and_rating[0]] = movie_and_rating[1]

    for movie_and_rating in movies_with_ratings_2:
        movie = movie_and_rating[0]
        if movie in rating_per_movie:
            squared_diff.append(
                np.square(movie_and_rating[1] - rating_per_movie[movie]))

    if len(squared_diff) == 0:
        return 0
    return 1.0 / (1.0 + np.sqrt(np.sum(squared_diff)))


def pearson_score(movies_with_ratings_1, movies_with_ratings_2):
    rating_per_movie = {}
    num_ratings = 0
    user1_sum = 0
    user2_sum = 0

    user1_squared_sum = 0
    user2_squared_sum = 0

    sum_of_products = 0

    for movie_and_rating in movies_with_ratings_1:
        rating_per_movie[movie_and_rating[0]] = movie_and_rating[1]

    for j, movie_and_rating in enumerate(movies_with_ratings_2):
        movie = movie_and_rating[0]
        if movie in rating_per_movie:
            num_ratings += 1
            user1_movie_rating = rating_per_movie[movie]
            user2_movie_rating = movies_with_ratings_2[j][1]

            user1_sum += user1_movie_rating
            user2_sum += user2_movie_rating

            user1_squared_sum += pow(user1_movie_rating, 2)
            user2_squared_sum += pow(user2_movie_rating, 2)

            sum_of_products += user1_movie_rating * user2_movie_rating

    if num_ratings == 0:
        return 0

    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


def movies_proposition(movies_sorted_by_user_score):
    movies_to_recommend = []
    user_movies_set = set()

    for user_movie_and_rating in user_movies:
        user_movies_set.add(user_movie_and_rating[0])

    for user_index_and_movies in movies_sorted_by_user_score:
        for movie_and_rating in user_index_and_movies[1]:
            if movie_and_rating[0] not in user_movies_set and movie_and_rating[1] >= GOOD_SCORE_THRESHOLD:
                movies_to_recommend.append(movie_and_rating[0])
            if len(movies_to_recommend) == NUMBER_OF_PROPOSED_MOVIES:
                break
        if len(movies_to_recommend) == NUMBER_OF_PROPOSED_MOVIES:
            break

    return movies_to_recommend


user_scores = []
user_movies = data[USER_INDEX]
score_method_type = sys.argv[1].lower()

for i, other_user_movies in enumerate(data):
    if i == USER_INDEX:
        user_scores.append(0)
    else:
        if score_method_type == "pearson":
            user_scores.append(pearson_score(user_movies, other_user_movies))
        else:
            user_scores.append(euclidean_score(user_movies, other_user_movies))

user_indexes_with_movies = []
for index, user_movies_2 in enumerate(data):
    user_indexes_with_movies.append([index, user_movies_2])


user_indexes_with_movies_to_recommend = sorted(
    user_indexes_with_movies, key=lambda index_and_movies: -
    user_scores[index_and_movies[0]]
)
print(
    f"Recommended movies to watch for user {USER_INDEX}:",
    movies_proposition(user_indexes_with_movies_to_recommend)
)

user_indexes_with_movies_to_not_recommend = sorted(
    user_indexes_with_movies, key=lambda index_and_movies: user_scores[index_and_movies[0]]
)

print(
    f"Not recommended movies to watch for user {USER_INDEX}:",
    movies_proposition(user_indexes_with_movies_to_not_recommend)
)

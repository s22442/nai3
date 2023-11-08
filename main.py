import csv
import json

from deep_translator import GoogleTranslator

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
                movie_or_rating = movie_or_rating.strip()
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


print(data)

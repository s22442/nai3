## 💡 About this project

This is a movie recommendation engine that utilizes the Euclidean and Pearson algorithm to recommend 5 movies to watch
and 5 movies not to watch based off of a given list of movies listed and reviewed by a group of people on the scale
from 0.0 to 10.0.

Project created by:
- Kajetan Welc
- Daniel Wirzba

## 🛠️ Project setup
To run this project make sure that you:
- download at least a 3.10 version of Python
- download and install deep_translator with the following command via the terminal:
`pip install deep_translator`,
- generate an api key from: https://www.omdbapi.com/apikey.aspx and use it in OMDB_API_KEY variable,
- launch the project from your favorite IDE with arguments specifying the user index for which the movies are being
    recommended and the algorithm, for example:
    "0 euclidean", "5 pearson".

The list of reviewed movies by users is fetched from data.csv file.

Project created by:
- Kajetan Welc
- Daniel Wirzba


## 🏷️ License
[MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2023-PRESENT Daniel Wirzba Kajetan Welc

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
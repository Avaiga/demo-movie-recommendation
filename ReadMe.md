# Demo Movie Recommendation

## Usage
- [Usage](#usage)
- [Demo Movie Recommendation](#what-is-demo-movie-recommendation)
- [Directory Structure](#directory-structure)
- [License](#license)
- [Installation](#installation)
- [Contributing](#contributing)
- [Code of conduct](#code-of-conduct)

## What is Demo Movie Recommendation

Taipy is a Python library for creating Business Applications. More information on our
[website](https://www.taipy.io).

[Demo Movie Recommendation](https://github.com/Avaiga/demo-movie-recommendation) is a 
full application showing how Taipy Core and Taipy Gui can work together to build a simple 
but powerful application. This demo shows the basics of search a and recommendation 
algorithms. The goal is to be able to search for films and recommend related/similar films. 
These recommendations will use the user profile by tracking their session.

Get data [here](https://files.grouplens.org/datasets/movielens/ml-25m.zip).

### Demo Type
- **Level**: Advanced
- **Topic**: Taipy-GUI, Taipy-Core
- **Components/Controls**: 
  - Taipy GUI: input, selector, chart, expandable, table
  - Taipy Core: datanode, pipeline, scenario

## How to run

This demo works with a Python version superior to 3.8. Install the dependencies of the 
*requirements.txt* and run the *main.py*.

Get data [here](https://files.grouplens.org/datasets/movielens/ml-25m.zip).

## Introduction

A user has a userID generated when the user opens the app. Two pages are created to search and recommend films.

### Search page

- Be able to search for films
- List of films appears after search (selector of movies)
- Clicking on a movie will display a description of said movies, image, ratings, casting, date, ...
    - Possibility to use Imdb api in real time to provide these information
- Recommendation on searched films (not based on syntax but on association with 
  this film/similar films Avengers ~ Batman)
- Recommendation depending on liked films of user

### User page

- Possibility to create Data Nodes for tracking/profiling:
    - Selected films
    - Vewed films
    - Liked films
- Possibility to recommand a list of films based on selected/viewed/liked films (constraints on genres)
    - Example: `np.mean([find_similar_movies(movie_id) for movie_id in liked_movies_id])`
- Deduce user profile (favourite genres, favourite period, ...)
 - when a film is selected, add to the set of the user films (a datanode?)


## Directory Structure


- `src/`: Contains the demo source code.
  - `src/algos`: Contains the functions to be executed as tasks by Taipy.
  - `src/config`: Contains the configuration files.
  - `src/data`: Contains the application data files.
  - `src/pages`: Contains the page definition files.
- `CODE_OF_CONDUCT.md`: Code of conduct for members and contributors of _demo-movie-recommendation_.
- `CONTRIBUTING.md`: Instructions to contribute to _demo-movie-recommendation_.
- `INSTALLATION.md`: Instructions to install _demo-movie-recommendation_.
- `LICENSE`: The Apache 2.0 License.
- `Pipfile`: File used by the Pipenv virtual environment to manage project dependencies.
- `README.md`: Current file.

## License
Copyright 2022 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## Installation

Want to install _Demo Movie Recommendation_? Check out our 
[`INSTALLATION.md`](INSTALLATION.md) file.

## Contributing

Want to help build _Demo Movie Recommendation_? Check out our 
[`CONTRIBUTING.md`](CONTRIBUTING.md) file.

## Code of conduct

Want to be part of the _Demo Movie Recommendation_ community? Check out our 
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) file.
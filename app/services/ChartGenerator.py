import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from app.routes import movies


def filter_movies_by_year(movies, start_year, end_year):
    filtered_movies = [movie for movie in movies if start_year <= movie['year'] <= end_year]
    return filtered_movies


def plot_bar_diagram(filtered_movies):
    years = [str(year) for year in range(2019, 2024)]
    movie_counts = {year: 0 for year in years}
    for movie in movies:
        year = movie['year']
        movie_counts[str(year)] += 1
        plt.bar(movie_counts.keys(), movie_counts.values(), color='blue')
        plt.xlabel('Year')
        plt.ylabel('Number of Movies')
        plt.title('Number of Top-Rated Movies Released Each Year (2019-2023)')
        plt.show()


class ChartGenerator:
    @staticmethod
    def extract_movies_data(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        movie_items = soup.select('.media_results .media .title a')
        movies_data = []

        for movie_item in movie_items:
            title = movie_item.text.strip()
            movie_url = 'https://www.themoviedb.org' + movie_item['href']
            movies_data.append({'title': title, 'movie_url': movie_url})
            return movies_data

    @staticmethod
    def generateChart():
        url = 'https://www.themoviedb.org/movie/top-rated'
        movies_data = ChartGenerator.extract_movies_data(url)
        print(movies_data)

        for movie in movies_data:
            # Extract the release year from the movie URL
            movie['year'] = int(movie['movie_url'].split('/')[-1].split('-')[0])

        start_year = 2019
        end_year = 2023
        filtered_movies = filter_movies_by_year(movies_data, start_year, end_year)

        plot_bar_diagram(filtered_movies)

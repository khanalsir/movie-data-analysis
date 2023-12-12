import requests
from bs4 import BeautifulSoup


class MovieDataExtractor:
    @staticmethod
    def extract_all_movies():
        # Fetch movies from the TMDb website
        movies_list = []
        url = 'https://www.themoviedb.org/movie/top-rated'
        html_page = requests.get(url)
        soup = BeautifulSoup(html_page.content, 'html.parser')

        # Adjust the selector based on the actual HTML structure of the page
        movie_items = soup.select('div.item')  # Example selector; adjust as needed

        for movie_item in movie_items:
            title = movie_item.find('img')['alt']
            print(title + "sssssss")
            img_url = movie_item.find('img')['src']
            rating = movie_item.find('span', class_='average-rating').text.strip()
            movie_url = 'https://www.themoviedb.org' + movie_item.find('a', class_='film-poster')['href']

            movies_list.append({
                'title': title,
                'img_url': img_url,
                'rating': rating,
                'movie_url': movie_url
            })

        return movies_list

    @staticmethod
    def extract_movie_data(imdb_id):
        omdb_api_key = "your_omdb_api_key"
        omdb_url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={omdb_api_key}'

        try:
            response = requests.get(omdb_url)
            response.raise_for_status()
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie data: {e}")
            return None

    @staticmethod
    def extract_movie_info(imdb_id):
        movie_data = MovieDataExtractor.extract_movie_data(imdb_id)

        if movie_data:
            # Extract relevant information from the API response
            title = movie_data.get('Title')
            storyline = movie_data.get('Plot')
            actors = movie_data.get('Actors')
            director = movie_data.get('Director')
            length = int(movie_data.get('Runtime').split(' ')[0]) if movie_data.get('Runtime') else None
            genre = movie_data.get('Genre')
            budget = float(movie_data.get('Budget', '0').replace('$', '').replace(',', ''))
            collection = float(movie_data.get('BoxOffice', '0').replace('$', '').replace(',', ''))
            release_date = movie_data.get('Released')
            image_url = movie_data.get('Poster')

            return {
                'title': title,
                'storyline': storyline,
                'actors': actors,
                'director': director,
                'length': length,
                'genre': genre,
                'budget': budget,
                'collection': collection,
                'release_date': release_date,
                'image_url': image_url
            }
        else:
            return None

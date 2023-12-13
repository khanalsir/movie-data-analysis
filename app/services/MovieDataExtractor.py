import time

import requests
from bs4 import BeautifulSoup


class MovieDataExtractor:
    @staticmethod
    def extract_all_movies():
        data = []
        base_url = 'https://letterboxd.com'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        with requests.Session() as session:
            response = session.get(base_url + '/films/ajax/popular/decade/1980s/?esiAllowFilters=true', headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

            for index, e in enumerate(soup.select('li.listitem')):
                if index == 24:
                    break

                movie_url = base_url + e['data-film-slug']
                index_of_com = movie_url.find("com")
                corrected_url = movie_url[:index_of_com] + "com/film/" + movie_url[index_of_com + 3:]

                # Make a request to the corrected URL
                corrected_page = session.get(corrected_url, headers=headers)
                corrected_soup = BeautifulSoup(corrected_page.text, 'lxml')

                # Extract the image URL from the corrected page
                new_img_url = corrected_soup.select_one('meta[property="og:image"]')['content']

                data.append({
                    'title': e.img['alt'],
                    'img_url': new_img_url,  # e.img['src']
                    'rating': e.get('data-average-rating'),
                    'movie_url': corrected_url
                })

                # Add a delay between requests to avoid rate limiting
                time.sleep(1)

        return data

    @staticmethod
    def extract_movie_data(imdb_id):
        try:
            response = requests.get(imdb_id)
            response.raise_for_status()
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie data: {e}")
            return None

    @staticmethod
    def extract_movie_info(imdb_id):

        # Correct the movie URL
        # imdb id is url for now
        index_of_com = imdb_id.find("com")
        corrected_url = imdb_id[:index_of_com] + "com/film/" + imdb_id[index_of_com + 3:]

        # Make a request to the corrected URL
        corrected_page = requests.get(corrected_url)
        corrected_soup = BeautifulSoup(corrected_page.text, 'html.parser')

        # Extract the image URL from the corrected page
        new_img_url = corrected_soup.select_one('meta[property="og:image"]')['content']

        movie_data = MovieDataExtractor.extract_movie_data(new_img_url)

        if new_img_url:
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

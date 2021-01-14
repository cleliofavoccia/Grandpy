"""Contains all the models of objects use by the application"""
import os
import random
import unicodedata

import requests


class Grandpy:
    """It modelize the bot that treat user request"""

    def __init__(self):
        """Attributes of Grandpy"""
        self.sentences = ["Mais t'ai-je déjà raconté l'histoire de ce lieu "
                          "qui m'a vu en culottes courtes ?", "Je t'ai déjà "
                          "dit qu'ici j'avais rencontré Grandma ?", "Tu sais "
                          "que c'est là qu'est né Django Dad ?"]

    def give_infos(self, user_text):
        """Methods that return a dictionnary with all the informations
        useful to user request"""
        response = {'geolocalisation': None, 'address': None, 'extract': None,
                    'url': None, 'sentence': None}
        user_request = Parser().clean(user_text)

        try:
            response['geolocalisation'] = \
                GooglemapsClient().\
                fetch_location_from_request(user_request)['geolocalisation']
        except requests.exceptions.HTTPError:
            response['address'] = "J'ai pas compris ta demande mon enfant !"
            return response

        response['address'] = GooglemapsClient()\
            .fetch_location_from_request(user_request)['address']

        try:
            page_id = WikipediaClient()\
                .fetch_page_id(response['geolocalisation'])
        except IndexError:
            response['address'] = "J'ai pas compris ta demande mon enfant !"
            return response

        response['extract'] = WikipediaClient()\
            .recover_extract_and_url_from_page(page_id)['extract']
        response['url'] = WikipediaClient()\
            .recover_extract_and_url_from_page(page_id)['url']

        response['sentence'] = self.talk()

        return response

    def talk(self):
        """Return a random sentence from a list of sentences"""
        return random.choice(self.sentences)


class GooglemapsClient:
    def __init__(self):
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json'

    def fetch_location_from_request(self, user_request):
        """Receive request and return a results with address
        and geolocalisation (latitude and longitude) of the request"""
        params = {
            'address': user_request,
            'key': os.getenv("GEOCODING_API_KEY")
        }
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()

            address = response.json()['results'][0]['formatted_address']
            geolocalisation = \
                response.json()['results'][0]['geometry']['location']
            datas = {'address': address, 'geolocalisation': geolocalisation}

            return datas
        except IndexError:
            return "L'API fonctionne pas !"


class WikipediaClient:
    def __init__(self):
        self.url = "https://fr.wikipedia.org/w/api.php"

    def fetch_page_id(self, user_request):
        """Receive latitude and longitude and return page"""
        params = {
            "format": "json",  # response format
            "action": "query",
            "list": "geosearch",  # fetch method
            "gsradius": 10,  # fetch radius around geolocalisation
            "gscoord": f"{user_request['lat']}|{user_request['lng']}",
            # latitude and longitude fetch (geolocalisation)
        }
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        return response.json()['query']['geosearch'][0]['pageid']

    def recover_extract_and_url_from_page(self, page_id):
        """Receive a page id and return his extract"""

        params = {
            "format": "json",  # format
            "action": "query",
            "prop": "extracts|info",  # Properties choosen
            "inprop": "url",
            "exchars": 200,  # Number of characters to return
            "explaintext": True,  # Return raw text
            "pageids": page_id
        }

        response = requests.get(self.url, params=params)

        extract = response.json()['query']['pages'][f'{page_id}']['extract']
        url = response.json()['query']['pages'][f'{page_id}']['canonicalurl']
        datas = {'extract': extract, 'url': url}

        return datas


class Parser:
    def __init__(self):
        self.user_request = None
        self.key_sentences = ['l\'adresse de ', 'ou se trouve ',
                              'ou est ', 'ou se situe ']
        self.stop_words = set()

    def fill_up_stop_words(self):
        file = open("./grandpy/static/stop_words.txt", "r")
        for i in file:
            self.stop_words.add(i)

    def transform_to_lowercase(self, user_request):
        """Convert all the character's string into lowercase"""
        return user_request.lower()

    def remove_all_accent(self, user_request):
        """Remplace all accented characters by normal characters"""
        return unicodedata.normalize('NFD', user_request)\
            .encode('ascii', 'ignore').decode('ascii')

    def extract_location(self, user_request):
        """Extract the part of the string relating to the location sought"""
        for location_sentence in self.key_sentences:
            request = user_request.split(location_sentence)
            if len(request) == 2:
                user_request = request[1]
        return user_request

    def request_formatting(self, user_request):
        """Formate request to pass it in Wikipedia and Google Client"""
        # Remove all ponctuations
        user_request = user_request.replace("\'", " ")
        user_request = user_request.replace("?", " ")
        user_request = user_request.replace(",", " ")
        user_request = user_request.replace(".", " ")

        # Fill up stop_words list
        self.fill_up_stop_words()

        # Remove stop_words
        user_request = [word for word in user_request.split(" ")
                        if word not in self.stop_words]

        user_request = " ".join(user_request)

        # Remove all undesirable spaces
        user_request = user_request.strip()

        return user_request

    def clean(self, user_request):
        """Recieve a sentence and return location
        to pass it in Wikipedia and Google search"""
        user_request = self.transform_to_lowercase(user_request)
        user_request = self.remove_all_accent(user_request)
        user_request = self.extract_location(user_request)
        user_request = self.request_formatting(user_request)
        return user_request

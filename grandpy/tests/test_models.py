"""Contains all the tests of the application"""
import requests
from grandpy.models import GooglemapsClient, Parser, WikipediaClient


class TestParser:
    """Tests of methods from Parser class in models.py"""
    def test_transform_to_lowercase_string_with_uppercase(self):
        """Receive a string with uppercase letters and verify if
        the method transform these in lowercase letters"""
        assert Parser().transform_to_lowercase("Clelio FavOccia") \
               == "clelio favoccia"

    def test_transform_to_lowercase_string_with_lowercase(self):
        """Receive a string with lowercase letters and verify
        if the method modify anything"""
        assert Parser().transform_to_lowercase("clelio favoccia") \
               == "clelio favoccia"

    def test_remove_all_accent_string_with_accent(self):
        """Receive a string with accent letters and verify
        if the method replace these with non accent letters"""
        assert Parser().remove_all_accent("clélio favoccià") \
               == "clelio favoccia"

    def test_remove_all_accent_string_without_accent(self):
        """Receive a string with non accent letters and
        verify if the method do anything on these"""
        assert Parser().remove_all_accent("clelio favoccia") \
               == "clelio favoccia"

    def test_extract_location_from_string(self):
        """Receive a string and verify if the method
        returns the location in it"""
        assert Parser().extract_location("Comment s'est passé "
                                         "ta soirée avec Grandma hier soir? "
                                         "Au fait, pendant que j'y pense,"
                                         " pourrais-tu m'indiquer ou se "
                                         "trouve le musée d'art et "
                                         "d'histoire de Fribourg, s'il te "
                                         "plait?") \
               == "le musée d'art et d'histoire de Fribourg, s'il te plait?"

        assert Parser()\
               .extract_location("Bonsoir Grandpy, j'espère que tu "
                                 "as passé une belle semaine. "
                                 "Est-ce que tu pourrais m'indiquer "
                                 "l'adresse de la tour eiffel? "
                                 "Merci d'avance et salutations à Mamie.") \
               == "la tour eiffel? Merci d'avance et salutations à Mamie."

    def test_request_formatting_removed_stopwords(self, monkeypatch):
        """Receive a string and verify if stop_words are removed from it"""

        assert Parser()\
               .request_formatting("le musee d'art et d'histoire "
                                   "de fribourg, s'il te plait?") \
               == 'musee art histoire fribourg'

        assert Parser().request_formatting("la tour eiffel? "
                                           "merci d'avance et "
                                           "salutations a mamie.") \
               == 'tour eiffel'


class TestGooglemapsClient:
    """Tests of methods from GooglemapsClient class in models.py"""
    def test_fetch_location_from_request(self, monkeypatch):
        """Receive a string and verify if it returns a dictionnary
         with address and geolocalisation"""
        geolocalisation = {'lat': 46.8077191, 'lng': 7.159642}
        address = 'Route de Morat 12, 1700 Fribourg, Switzerland'
        url = ('https://maps.googleapis.com/maps/api/geocode/json',)
        params = {'params': {
            'address': 'musee art histoire Fribourg',
            'key': None}
        }

        class MockRequestResponse:
            """Class to mock a response"""

            status_code = 200

            def raise_for_status(self):
                """Return status in case of error"""
                return requests.HTTPError

            def json(self):
                """Content of mocked response in JSON"""
                return {'results':
                        [{'geometry':
                         {'location':
                          {'lat': 46.8077191,'lng': 7.159642}},
                          'formatted_address':
                          'Route de Morat 12, 1700 Fribourg, Switzerland'}]}

        def mock_google_geolocalisation_api(*args, **kwargs):
            """Method to mock Google Geocode API"""
            mock_google_geolocalisation_api.params \
                = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        monkeypatch.setattr('requests.get',
                            mock_google_geolocalisation_api)

        assert GooglemapsClient()\
               .fetch_location_from_request('musee art histoire Fribourg') \
               == {'address': address, 'geolocalisation': geolocalisation}
        assert mock_google_geolocalisation_api.params["args"] == url
        assert mock_google_geolocalisation_api.params["kwargs"] == params

    def test_fetch_location_from_request_with_error(self, monkeypatch):
        url = ('https://maps.googleapis.com/maps/api/geocode/json',)
        params = {'params': {
            'address': 'musee art histoire Fribourg',
            'key': None}
        }

        class MockRequestResponse:
            """Class to mock a response"""

            status_code = 200

            def raise_for_status(self):
                """Return status in case of error"""
                return requests.HTTPError

            def json(self):
                """Content of mocked response in JSON"""
                return {'results': []}

        def mock_google_geolocalisation_api(*args, **kwargs):
            """Method to mock Google Geocode API"""
            mock_google_geolocalisation_api.params = \
                {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        monkeypatch.setattr('requests.get',
                            mock_google_geolocalisation_api)

        assert GooglemapsClient()\
               .fetch_location_from_request('musee art histoire Fribourg') \
               == "L'API fonctionne pas !"
        assert mock_google_geolocalisation_api.params["args"] == url
        assert mock_google_geolocalisation_api.params["kwargs"] == params


class TestWikipediaClient:
    """Tests of methods from WikipediaClient class in models.py"""
    def test_fetch_page_id_with_geolocalisation(self, monkeypatch):
        """Receive geolocalisation and verify if method return
        a wikipedia page id"""
        geolocalisation = {'lat': 46.8077191, 'lng': 7.159642}
        page_id = 5611974
        url = ("https://fr.wikipedia.org/w/api.php",)
        params = {'params': {
            "format": "json",
            "action": "query",
            "list": "geosearch",
            "gsradius": 10,
            "gscoord": f"{geolocalisation['lat']}|{geolocalisation['lng']}",
        }
        }

        class MockRequestResponse:
            """Class to mock a response"""
            status_code = 200

            def raise_for_status(self):
                """Return status in case of error"""
                return requests.HTTPError

            def json(self):
                """Content of mocked response in JSON"""
                return {'query': {'geosearch': [{'pageid': 5611974}]}}
#
        def mock_wikipedia_page_by_geolocalisation_api(*args,
                                                       **kwargs):
            """Method to mock Wikipedia API"""
            mock_wikipedia_page_by_geolocalisation_api.params = \
                {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        monkeypatch.setattr('requests.get',
                            mock_wikipedia_page_by_geolocalisation_api)

        assert WikipediaClient()\
               .fetch_page_id(geolocalisation)\
               == page_id

        assert mock_wikipedia_page_by_geolocalisation_api\
               .params["args"] == url
        assert mock_wikipedia_page_by_geolocalisation_api\
               .params["kwargs"] == params

    def test_recover_extract_and_url_from_page(self, monkeypatch):
        """Receive a wikipedia page id and verify if the method
        return an extract of this page and his url"""
        page_id = 5611974
        url = ("https://fr.wikipedia.org/w/api.php",)
        params = {'params': {
            "format": "json",
            "action": "query",
            "prop": "extracts|info",
            "inprop": "url",
            "exchars": 200,
            "explaintext": True,
            "pageids": page_id
        }
        }

        class MockRequestResponse:
            """Class to mock a response"""
            status_code = 200

            def raise_for_status(self):
                """Return status in case of error"""
                return requests.HTTPError

            def json(self):
                """Content of mocked response in JSON"""
                return {'query':
                        {'pages':
                         {'5611974':
                          {'extract':
                           "Le musée d'art "
                           "et d'histoire "
                           "de Fribourg "
                           "(abrégé MAHF) est un "
                           "musée fribourgeois "
                           "collectionnant des "
                           "œuvres d’art et "
                           "des objets "
                           "historiques en "
                           "provenance du "
                           "canton du même "
                           "nom.",
                           'canonicalurl':
                           'https://fr.wiki'
                           'pedia.org/wiki/'
                           'Mus%C3%A9e_d%27'
                           'Art_et_d%27Hist'
                           'oire_de_Fribourg'
                          }
                         }
                        }
                       }

        def mock_wikipedia_extract_page_proposition_api(*args, **kwargs):
            """Method to mock Wikipedia API"""
            mock_wikipedia_extract_page_proposition_api.params \
                = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        monkeypatch.setattr('requests.get',
                            mock_wikipedia_extract_page_proposition_api)

        assert WikipediaClient()\
               .recover_extract_and_url_from_page(page_id) == \
               {'extract':
                "Le musée d'art et d'histoire "
                "de Fribourg (abrégé MAHF) est un musée " 
                "fribourgeois collectionnant des œuvres "
                "d’art et des objets historiques " 
                "en provenance du canton du même nom.",
                'url':
                'https://fr.wikipedia.org/wiki/Mus%C3%'
                'A9e_d%27Art_et_d%27Histoire_de_Fribourg'}

        assert mock_wikipedia_extract_page_proposition_api\
               .params["args"] == url
        assert mock_wikipedia_extract_page_proposition_api\
               .params["kwargs"] == params

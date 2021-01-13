import requests

from grandpy.models import Parser
from grandpy.models import GooglemapsClient
from grandpy.models import WikipediaClient


class TestParser:

    def test_transform_to_lowercase_transform_all_uppercase_letters_to_lowercase_letters(self):
        assert Parser().transform_to_lowercase("Clelio FavOccia") == "clelio favoccia"

    def test_transform_to_lowercase_does_not_modify_anything_if_all_letters_are_lowercase(self):
        assert Parser().transform_to_lowercase("clelio favoccia") == "clelio favoccia"

    def test_remove_all_accent_has_removed_all_accent(self):
        assert Parser().remove_all_accent("clélio favoccià") == "clelio favoccia"

    def test_remove_all_accent_does_not_modify_anything_if_all_letters_are_without_accent(self):
        assert Parser().remove_all_accent("clelio favoccia") == "clelio favoccia"

    def test_extract_location_has_extracted_a_clear_location_request_from_a_sentence(self):
        assert Parser().extract_location("Comment s'est passé ta soirée avec Grandma hier soir? "
              "Au fait, pendant que j'y pense, pourrais-tu m'indiquer ou se trouve "
              "le musée d'art et d'histoire de Fribourg, s'il te plait?") == "le musée d'art et d'histoire " \
                                                                             "de Fribourg, s'il te plait?"

        assert Parser().extract_location("Bonsoir Grandpy, j'espère que tu as passé une belle semaine. "
                                         "Est-ce que tu pourrais m'indiquer l'adresse de la tour eiffel? "
                                         "Merci d'avance et salutations à Mamie.") == "la tour eiffel? " \
                                                                                      "Merci d'avance et " \
                                                                                      "salutations à Mamie."

    def test_request_formatting_removed_stopwords(self):
        assert Parser().request_formatting("le musée d'art et d'histoire de Fribourg, s'il te plait?") \
               == 'musée art histoire Fribourg'

        assert Parser().request_formatting("la tour eiffel? Merci d'avance et salutations à Mamie.") == 'tour eiffel'


class TestGooglemapsClient:
    def test_research_geolocalisation_from_user_request_return_latitude_and_longitude(self):
        self.geolocalisation = {'lat': 46.8077191, 'lng': 7.159642}
        self.url = ('https://maps.googleapis.com/maps/api/geocode/json',)
        self.params = {'params' : {
            'address': 'musee art histoire Fribourg',
            'key': None }
        }

        class MockRequestResponse:

            status_code = 200

            def raise_for_status(self):
                return requests.HTTPError

            def json(self):
                return {'results': [{'geometry': {'location': {'lat': 46.8077191, 'lng': 7.159642}}}]}

        def mock_google_geolocalisation_api(*args, **kwargs):
            mock_google_geolocalisation_api.params = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        backup_requests_get = requests.get
        requests.get = mock_google_geolocalisation_api

        assert GooglemapsClient().research_geolocalisation_from_user_request('musee art histoire Fribourg') \
               == self.geolocalisation
        assert mock_google_geolocalisation_api.params["args"] == self.url
        assert mock_google_geolocalisation_api.params["kwargs"] == self.params

        requests.get = backup_requests_get

    def test_research_geolocalisation_from_user_request_return_message_for_IndexError(self):
        self.url = ('https://maps.googleapis.com/maps/api/geocode/json',)
        self.params = {'params': {
            'address': 'musee art histoire Fribourg',
            'key': None}
        }

        class MockRequestResponse:
            status_code = 200

            def raise_for_status(self):
                return requests.HTTPError

            def json(self):
                return {'results': []}

        def mock_google_geolocalisation_api(*args, **kwargs):
            mock_google_geolocalisation_api.params = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        backup_requests_get = requests.get
        requests.get = mock_google_geolocalisation_api

        assert GooglemapsClient().research_geolocalisation_from_user_request('musee art histoire Fribourg') \
               == "L'API fonctionne pas !"
        assert mock_google_geolocalisation_api.params["args"] == self.url
        assert mock_google_geolocalisation_api.params["kwargs"] == self.params

        requests.get = backup_requests_get

    def test_research_address_from_user_request_return_an_address(self):
        self.address = 'Route de Morat 12, 1700 Fribourg, Switzerland'
        self.url = ('https://maps.googleapis.com/maps/api/geocode/json',)
        self.params = {'params': {
            'address': 'musee art histoire Fribourg',
            'key': None}
        }

        class MockRequestResponse:
            status_code = 200

            def raise_for_status(self):
                return requests.HTTPError

            def json(self):
                return {'results': [{'formatted_address': 'Route de Morat 12, 1700 Fribourg, Switzerland'}]}

        def mock_google_address_api(*args, **kwargs):
            mock_google_address_api.params = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        backup_requests_get = requests.get
        requests.get = mock_google_address_api

        assert GooglemapsClient().research_address_from_user_request('musee art histoire Fribourg') \
               == self.address
        assert mock_google_address_api.params["args"] == self.url
        assert mock_google_address_api.params["kwargs"] == self.params

        requests.get = backup_requests_get




class TestWikipediaClient:
    def test_research_page_return_a_proposition_of_page_with_page_id(self):
        self.geolocalisation = {'lat': 46.8077191, 'lng': 7.159642}
        self.page_id = 5611974
        self.url = ("https://fr.wikipedia.org/w/api.php",)
        self.params = {'params' : {
            "format": "json",  # format de la réponse
            "action": "query",  # action à réaliser
            "list": "geosearch",  # méthode de recherche
            "gsradius": 10,  # rayon de recherche autour des coordonnées GPS fournies (max 10'000 m)
            "gscoord": f"{self.geolocalisation['lat']}|{self.geolocalisation['lng']}",  # coordonnées GPS séparées par une barre verticale
        }
        }

        class MockRequestResponse:
            status_code = 200

            def raise_for_status(self):
                return requests.HTTPError

            def json(self):
                return {'query': {'geosearch': [{'pageid': 5611974}]}}
#
        def mock_wikipedia_geolocalisation_page_proposition_api(*args, **kwargs):
            mock_wikipedia_geolocalisation_page_proposition_api.params = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        backup_requests_get = requests.get
        requests.get = mock_wikipedia_geolocalisation_page_proposition_api

        assert WikipediaClient().research_page_id_with_geolocalisation(self.geolocalisation) == self.page_id

        assert mock_wikipedia_geolocalisation_page_proposition_api.params["args"] == self.url
        assert mock_wikipedia_geolocalisation_page_proposition_api.params["kwargs"] == self.params

        requests.get = backup_requests_get

    def test_recover_extract_from_page_return_an_extract(self):
        self.page_id = 5611974
        self.url = ("https://fr.wikipedia.org/w/api.php",)
        self.params = {'params' : {
            "format": "json",  # format de la réponse
            "action": "query",  # action à effectuer
            "prop": "extracts|info",  # Choix des propriétés pour les pages requises
            "inprop": "url",  # Fournit une URL complète, une URL de modification, et l’URL canonique de chaque page.
            "exchars": 200,  # Nombre de caractères à retourner
            "explaintext": True,  # Renvoyer du texte brut (éliminer les balises de markup)
            "pageids": self.page_id
        }
        }

        class MockRequestResponse:
            status_code = 200

            def raise_for_status(self):
                return requests.HTTPError

            def json(self):
                return {'query':
                            {'pages':
                                 {'5611974':
                                      {'pageid': 5611974,
                                                        'extract': "Le musée d'art et d'histoire de Fribourg "
                                                                   "(abrégé MAHF) est un musée fribourgeois "
                                                                   "collectionnant des œuvres d’art et des objets "
                                                                   "historiques en provenance du canton du même nom."}
                                }
                             }
                        }


        def mock_wikipedia_extract_page_proposition_api(*args, **kwargs):
            mock_wikipedia_extract_page_proposition_api.params = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        backup_requests_get = requests.get
        requests.get = mock_wikipedia_extract_page_proposition_api

        assert WikipediaClient().recover_extract_from_page(self.page_id) == \
               "Le musée d'art et d'histoire de Fribourg (abrégé MAHF) est un musée " \
               "fribourgeois collectionnant des œuvres d’art et des objets historiques " \
               "en provenance du canton du même nom."

        assert mock_wikipedia_extract_page_proposition_api.params["args"] == self.url
        assert mock_wikipedia_extract_page_proposition_api.params["kwargs"] == self.params

        requests.get = backup_requests_get

    def test_recover_url_from_page_return_an_url(self):
        self.page_id = 5611974
        self.url = ("https://fr.wikipedia.org/w/api.php",)
        self.params = {'params': {
            "format": "json",  # format de la réponse
            "action": "query",  # action à effectuer
            "prop": "extracts|info",  # Choix des propriétés pour les pages requises
            "inprop": "url",  # Fournit une URL complète, une URL de modification, et l’URL canonique de chaque page.
            "exchars": 200,  # Nombre de caractères à retourner
            "explaintext": True,  # Renvoyer du texte brut (éliminer les balises de markup)
            "pageids": self.page_id
        }
        }

        class MockRequestResponse:
            status_code = 200

            def raise_for_status(self):
                return requests.HTTPError

            def json(self):
                return {'query':
                        {'pages':
                            {'5611974':
                                 {'canonicalurl':
                                        'https://fr.wikipedia.org/wiki/Mus%C3%A9e_d%27Art_et_d%27Histoire_de_Fribourg'}
                             }
                         }
                        }

        def mock_wikipedia_extract_url_proposition_api(*args, **kwargs):
            mock_wikipedia_extract_url_proposition_api.params = {"args": args, "kwargs": kwargs}
            return MockRequestResponse()

        backup_requests_get = requests.get
        requests.get = mock_wikipedia_extract_url_proposition_api

        assert WikipediaClient().recover_url_from_page(
            self.page_id) == 'https://fr.wikipedia.org/wiki/Mus%C3%A9e_d%27Art_et_d%27Histoire_de_Fribourg'

        assert mock_wikipedia_extract_url_proposition_api.params["args"] == self.url
        assert mock_wikipedia_extract_url_proposition_api.params["kwargs"] == self.params

        requests.get = backup_requests_get
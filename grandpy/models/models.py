
class User:
    pass


class Grandpy:

    def do_response_to_request(self, user_request):
        return "Ok, c'est bien reçu !"


class GooglemapsClient:
    def __init__(self):
        self.url = None

    def research_geolocalisation_from_user_request(self, user_request):
        """Receive request and return a results with longitude et latitude of the request (geolocalisation)"""
        pass


class WikipediaClient:
    def __init__(self):
        self.url = "https://fr.wikipedia.org/w/api.php"

    def research_page_with_geolocalisation(self, user_request):
        """Receive latitude and longitude and return correspondant pages"""
        pass

    def recover_extract_from_page(self, page_id):
        """Receive a page id and return his extract"""
        pass

    def recover_url_from_page(self, page_id):
        """Receive a page id and return his url"""
        pass


class Parser:
    def __init__(self):
        self.user_request = None

    def transform_to_lowercase(self, user_request):
        """Convert all the character's string into lowercase"""
        pass

    def remove_all_accent(self, user_request):
        """Remplace all accented characters by normal characters"""
        pass

    def extract_location(self, user_request):
        """Extract the part of the string relating to the location sought"""
        pass

    def request_formatting(self, user_request):
        """Formate request to pass it in Wikipedia and Google Client"""
        pass

    def clean(self, user_request):
        """Recieve a sentence and return location
        to pass it in Wikipedia and Google search"""
        user_request = self.transform_to_lowercase(user_request)
        user_request = self.remove_all_accent(user_request)
        user_request = self.extract_location(user_request)
        user_request = self.request_formatting(user_request)
        return user_request

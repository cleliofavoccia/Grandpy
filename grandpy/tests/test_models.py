from grandpy.models.models import Parser
from grandpy.models.models import GooglemapsClient
from grandpy.models.models import WikipediaClient


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

    def test_request_formatting_removed_stopwords(self):
        assert Parser().request_formatting(['le', 'musée',
                                                    "d'art", 'et', "d'histoire", 'de', 'Fribourg,'
                                                    , "s'il", 'te', 'plait?']) == 'musée art histoire Fribourg'


class TestGooglemapsClient:
    def test_research_geolocalisation_from_user_request_return_lattitude_and_longitude(self):
        assert GooglemapsClient().research_geolocalisation_from_user_request('musée art histoire Fribourg') \
               == {'lat': 46.8077191, 'lng': 7.159642}


class TestWikipediaClient:
    def test_research_page_return_a_proposition_of_page(self):
        assert WikipediaClient().research_page_with_geolocalisation({'lat': 46.8077191, 'lng': 7.159642}) == \
               {'batchcomplete': '', 'query': {'geosearch': [{'pageid': 5611974, 'ns': 0,
                                                              'title': "Musée d'Art et d'Histoire de Fribourg",
                                                              'lat': 46.80774, 'lon': 7.15963, 'dist': 2.5,
                                                              'primary': ''}]}}

    def recover_extract_from_page_return_the_good_extract(self):
        assert WikipediaClient().recover_extract_from_page(5611974) is None

    def recover_url_from_page_return_the_good_url(self):
        assert WikipediaClient().recover_url_from_page(5611974) == \
               'https://fr.wikipedia.org/wiki/Mus%C3%A9e_d%27Art_et_d%27Histoire_de_Fribourg'

import unicodedata
import requests
import os
import random

class User:
    pass


class Grandpy:

    def __init__(self):
        self.sentences = ["Mais t'ai-je déjà raconté l'histoire de ce lieu qui m'a vu en culottes courtes ?",
                     "Je t'ai déjà dit qu'ici j'avais rencontré Grandma ?", "Tu sais que c'est là qu'est "
                                                                            "né Django Dad ?"]

    def give_infos(self, user_text):
        response = {'geolocalisation': None, 'address': None, 'extract': None, 'url': None, 'sentence': None}
        user_request = Parser().clean(user_text)

        try:
            response['geolocalisation'] = GooglemapsClient()\
                .research_geolocalisation_from_user_request(user_request)
        except requests.exceptions.HTTPError:
            response['address'] = "J'ai pas compris ta demande mon enfant !"
            return response

        response['address'] = GooglemapsClient().research_address_from_user_request(user_request)

        try:
            page_id = WikipediaClient().research_page_id_with_geolocalisation(response['geolocalisation'])
        except IndexError:
            response['address'] = "J'ai pas compris ta demande mon enfant !"
            return response

        response['extract'] = WikipediaClient().recover_extract_from_page(page_id)
        response['url'] = WikipediaClient().recover_url_from_page(page_id)

        response['sentence'] = self.talk()

        return response

    def talk(self):
        return random.choice(self.sentences)

class GooglemapsClient:
    def __init__(self):
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json'

    def research_geolocalisation_from_user_request(self, user_request):
        """Receive request and return a results with longitude et latitude of the request (geolocalisation)"""
        params = {
            'address': user_request,
            'key': os.getenv("GEOCODING_API_KEY")
        }
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            return response.json()['results'][0]['geometry']['location']
        except IndexError:
            return "L'API fonctionne pas !"

    def research_address_from_user_request(self, user_request):
        """Receive request and return a postal address"""
        params = {
            'address': user_request,
            'key': os.getenv("GEOCODING_API_KEY")
        }
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            return response.json()['results'][0]['formatted_address']
        except IndexError:
            return "L'API fonctionne pas !"




class WikipediaClient:
    def __init__(self):
        self.url = "https://fr.wikipedia.org/w/api.php"

    def research_page_id_with_geolocalisation(self, user_request):
        """Receive latitude and longitude and return page"""
        params = {
            "format": "json",  # format de la réponse
            "action": "query",  # action à réaliser
            "list": "geosearch",  # méthode de recherche
            "gsradius": 10,  # rayon de recherche autour des coordonnées GPS fournies (max 10'000 m)
            "gscoord": f"{user_request['lat']}|{user_request['lng']}",  # coordonnées GPS séparées par une barre verticale
        }
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        return response.json()['query']['geosearch'][0]['pageid']

    def recover_extract_from_page(self, page_id):
        """Receive a page id and return his extract"""

        params = {
            "format": "json",  # format de la réponse
            "action": "query",  # action à effectuer
            "prop": "extracts|info",  # Choix des propriétés pour les pages requises
            "inprop": "url",  # Fournit une URL complète, une URL de modification, et l’URL canonique de chaque page.
            "exchars": 200,  # Nombre de caractères à retourner
            "explaintext": True,  # Renvoyer du texte brut (éliminer les balises de markup)
            "pageids": page_id
        }

        response = requests.get(self.url, params=params)

        return response.json()['query']['pages'][f'{page_id}']['extract']

    def recover_url_from_page(self, page_id):
        """Receive a page id and return his url"""
        params = {
            "format": "json",  # format de la réponse
            "action": "query",  # action à effectuer
            "prop": "extracts|info",  # Choix des propriétés pour les pages requises
            "inprop": "url",  # Fournit une URL complète, une URL de modification, et l’URL canonique de chaque page.
            "exchars": 200,  # Nombre de caractères à retourner
            "explaintext": True,  # Renvoyer du texte brut (éliminer les balises de markup)
            "pageids": page_id
        }

        response = requests.get(self.url, params=params)

        return response.json()['query']['pages'][f'{page_id}']['canonicalurl']


class Parser:
    def __init__(self):
        self.user_request = None
        self.key_sentences = ['l\'adresse de ', 'ou se trouve ', 'ou est ', 'ou se situe ']
        self.stop_words = {"avance", "Merci", "salutations", "mamie", "Mamie", "chercher", "trouver", "trouve", "plait", "a", "abord","absolument","afin","ah","ai","aie","ailleurs", "ainsi","ait","allaient","allo","allons","allo","alors", "anterieur","anterieure","anterieures","apres","après", "as","assez","attendu","au","aucun","aucune","aujourd", "aujourd'hui","aupres","auquel","aura","auraient","aurait", "auront","aussi","autre","autrefois","autrement","autres", "autrui","aux","auxquelles","auxquels","avaient","avais", "avait","avant","avec","avoir","avons","ayant","b","bah", "bas","basee","bat","beau","beaucoup","bien","bigre","boum", "bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci", "celle-là","celles","celles-ci","celles-là","celui","celui-ci", "celui-là","cent","cependant","certain","certaine","certaines", "certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là", "chacun","chacune","chaque","cher","chers","chez","chiche","chut", "chère","chères","ci","cinq","cinquantaine","cinquante", "cinquantième","cinquième","clac","clic","combien","comme", "comment","comparable","comparables","compris","concernant", "contre","couic","crac","d","da","dans","de","debout","dedans", "dehors","deja","delà","depuis","dernier","derniere","derriere", "derrière","des","desormais","desquelles","desquels","dessous", "dessus","deux","deuxième","deuxièmement","devant","devers","devra","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","douze","douzième","dring","du","duquel","durant","dès","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","est","et","etant","etc","etre","eu","euh","eux","eux-mêmes","exactement","excepté","extenso","exterieur","f","fais","faisaient","faisant","fait","façon","feront","fi","flac","floc","font","g","gens","h","ha","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","minimale","moi","moi-meme","moi-même","moindres","moins","mon","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","plein","plouf","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","seraient","serait","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soit","soixante","son","sont","sous","souvent","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","superpose","sur","surtout","t","ta","tac","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","été","être","ô"}


    def transform_to_lowercase(self, user_request):
        """Convert all the character's string into lowercase"""
        return user_request.lower()

    def remove_all_accent(self, user_request):
        """Remplace all accented characters by normal characters"""
        return unicodedata.normalize('NFD', user_request).encode('ascii', 'ignore').decode('ascii')

    def extract_location(self, user_request):
        """Extract the part of the string relating to the location sought"""
        for location_sentence in self.key_sentences:
            request = user_request.split(location_sentence)
            if len(request) == 2:
                user_request = request[1]
        return user_request

    def request_formatting(self, user_request):
        """Formate request to pass it in Wikipedia and Google Client"""
        user_request = user_request.replace("\'", " ")
        user_request = user_request.replace("?", " ")
        user_request = user_request.replace(",", " ")
        user_request = user_request.replace(".", " ")

        user_request = [word for word in user_request.split(" ") if word not in self.stop_words]

        user_request = " ".join(user_request)

        # On enlève les espaces indésirées en début et fin de la chaîne
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

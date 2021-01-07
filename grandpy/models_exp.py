import requests
from config import GEOCODING_API_KEY

# transform_to_lowercase
string = "Clelio FavOccia"
string2 = "clelio favoccia"
print(string.lower())

# supprime accents
import unicodedata
string3 = "clélio favoccià"
klr = unicodedata.normalize('NFD', string3).encode('ascii', 'ignore').decode('ascii')
print(klr)

# EXTRAIRE LA QUESTION DU LIEU

key_sentences = ['l\'adresse de', 'ou se trouve', 'ou est', 'ou se situe',]

string4 = "Comment s'est passé ta soirée avec Grandma hier soir? " \
          "Au fait, pendant que j'y pense, pourrais-tu m'indiquer ou se trouve " \
          "le musée d'art et d'histoire de Fribourg, s'il te plait?"

for location_sentence in key_sentences:
    request = string4.split(location_sentence)
    if len(request) == 2:
        sentence = request[1]
print(sentence)

# TRAITER LA REQUETE AVEC MOTS CLES
# remplacer apostrophe, virgule et point par espace
string5 = sentence.replace("\'", " ")
string6 = string5.replace("?", " ")
string7 = string6.replace(",", " ")
string8 = string7.replace(".", " ")
print(string8)
# spliter par esapce toute en filtrant avec stop words
stop_words = {"chercher", "trouver", "trouve", "plait", "a", "abord","absolument","afin","ah","ai","aie","ailleurs", "ainsi","ait","allaient","allo","allons","allo","alors", "anterieur","anterieure","anterieures","apres","après", "as","assez","attendu","au","aucun","aucune","aujourd", "aujourd'hui","aupres","auquel","aura","auraient","aurait", "auront","aussi","autre","autrefois","autrement","autres", "autrui","aux","auxquelles","auxquels","avaient","avais", "avait","avant","avec","avoir","avons","ayant","b","bah", "bas","basee","bat","beau","beaucoup","bien","bigre","boum", "bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci", "celle-là","celles","celles-ci","celles-là","celui","celui-ci", "celui-là","cent","cependant","certain","certaine","certaines", "certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là", "chacun","chacune","chaque","cher","chers","chez","chiche","chut", "chère","chères","ci","cinq","cinquantaine","cinquante", "cinquantième","cinquième","clac","clic","combien","comme", "comment","comparable","comparables","compris","concernant", "contre","couic","crac","d","da","dans","de","debout","dedans", "dehors","deja","delà","depuis","dernier","derniere","derriere", "derrière","des","desormais","desquelles","desquels","dessous", "dessus","deux","deuxième","deuxièmement","devant","devers","devra","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","douze","douzième","dring","du","duquel","durant","dès","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","est","et","etant","etc","etre","eu","euh","eux","eux-mêmes","exactement","excepté","extenso","exterieur","f","fais","faisaient","faisant","fait","façon","feront","fi","flac","floc","font","g","gens","h","ha","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","minimale","moi","moi-meme","moi-même","moindres","moins","mon","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","plein","plouf","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","seraient","serait","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soit","soixante","son","sont","sous","souvent","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","superpose","sur","surtout","t","ta","tac","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","été","être","ô"}

string9 = [word for word in string8.split(" ") if word not in stop_words]
print(string9)

# enlever les espaces
for i in string9:
    if i == '':
        string9.remove(i)
print(string9)

# joindre pour requête final en string
string10 = " ".join(string9)
print(string10)
string11 = "+".join(string9)
print(string11)

# CHERCHER DANS GOOGLE
url = f'https://maps.googleapis.com/maps/api/geocode/json?address={string11}&key={GEOCODING_API_KEY}'
response = requests.get(url)
# récupération lattitude et longitude
# print(response.json()['results'][0]['geometry']['location']['lat'])
# print(response.json()['results'][0]['geometry']['location']['lng'])
print(response.json()['results'][0]['geometry']['location'])

# CHERCHER DANS WIKIPEDIA

# On cherche quel page on veut
url = "https://fr.wikipedia.org/w/api.php"

latitude = 46.8077191
longitude = 7.159642

params = {
    "format": "json",  # format de la réponse
    "action": "query",  # action à réaliser
    "list": "geosearch",  # méthode de recherche
    "gsradius": 10,  # rayon de recherche autour des coordonnées GPS fournies (max 10'000 m)
    "gscoord": f"{latitude}|{longitude}",  # coordonnées GPS séparées par une barre verticale
}

response = requests.get(url, params=params)
print(response.json())

# On récupère les informations de la pages qu'on veut

page_id = response.json()['query']['geosearch'][0]['pageid']

params = {
    "format": "json", # format de la réponse
    "action": "query", # action à effectuer
    "prop": "extracts|info", # Choix des propriétés pour les pages requises
    "inprop": "url", # Fournit une URL complète, une URL de modification, et l’URL canonique de chaque page.
    "exchars": 1200, # Nombre de caractères à retourner
    "explaintext": True, # Renvoyer du texte brut (éliminer les balises de markup)
    "pageids": page_id
}

response = requests.get(url, params=params)
# extrait de la page wikipedia
print(response.json()['query']['pages'][f'{page_id}']['extract'])
# url de la page wikipedia
print(response.json()['query']['pages'][f'{page_id}']['canonicalurl'])

import requests , pprint
API_TOKEN = "***REMOVED***"
URL_first = f"https://quotes.rest/quote/random?api_key={API_TOKEN}"
URL = f"https://api.quotable.io/quotes/random"


response = requests.get(URL)
response.raise_for_status()
pprint.pprint(response.json()[0]["content"])
# pprint.pprint(response.json()['contents']["quotes"][0]["quote"])
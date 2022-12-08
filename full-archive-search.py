import requests
import os
import json
import time

# on récupère le "bearer_token" de l'API Twitter
bearer_token = os.environ.get("BEARER_TOKEN")

# on définit le "endpoint" qu'on souhaite interroger
search_url = "https://api.twitter.com/2/tweets/search/all"

# on définit les paramètres de la requête
# on change le compte qu'on moissone et les dates ci-dessous !
# param. optionnels : start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
folder = "2"
account_at = "OGNreports"
query_params = {'query': '(from:' + account_at + ' -is:retweet syria)', 'tweet.fields': 'author_id,created_at',
                'start_time': '2021-01-01T00:00:00Z', 'end_time': '2022-01-01T00:00:00Z',
                'max_results': 500}


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


# on interroge l'API et on retourne le résultat
def connect_to_endpoint(url, params, next_token=None):
    if next_token:
        url = url + "?next_token=" + next_token
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    # on initialise quelques variables
    requests_count = 0
    next_token = None
    start = True

    # on interroge l'API tant qu'on n'atteint pas la dernière page de résultats (next_token)
    while next_token or start:

        # on compte les requêtes pour effectuer les pauses au bon moment (limites Twitter)
        requests_count += 1
        start = False

        # on gère la pagination (next_token)
        json_response = connect_to_endpoint(search_url, query_params, next_token)
        if "next_token" in json_response["meta"]:
            next_token = json_response['meta']['next_token']
            next_token_written = next_token
        else:
            next_token_written = "0"
            next_token = None

        # on écrit les resultats page par page dans un dossier
        file_name = "dumps/" + account_at + "/" + folder + "/tweets_" + next_token_written + ".json"

        with open(file_name, 'w') as outfile:
            json.dump(json_response["data"], outfile, indent=4)

        time.sleep(1)
        if requests_count % 15 == 0:
            time.sleep(900)


if __name__ == "__main__":
    main()

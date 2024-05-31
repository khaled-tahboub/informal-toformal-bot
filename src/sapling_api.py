import requests

def make_request(phrase):
    base_url = "https://api.sapling.ai/api/v1/paraphrase"
    api_key = "TRSOKJTMCWDS229Q5LNHQIYTHB0L70XZ"

    data = {
        "key": api_key,
        "text": phrase
    }
    response = requests.post(base_url, json=data)
    json = response.json()

    results = []
    try:
        results = json["results"]
    except Exception as error:
        print(error.__str__)
        results.append("API ERROR, " + json["msg"])

    return results

def extract_rephrases(results):
    suggestions = []
    for i in range(len(results)):
       object = results[i]
       suggestions.append(object["replacement"])

    return suggestions
            

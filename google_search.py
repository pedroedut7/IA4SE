from itertools import product
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
CSE_ID = os.getenv('CSE_ID')
NUM_RESULTS = 100

population_query = """
    "Class Modeling" OR "UML Modeling" OR "Software Architecture" OR "Software Design" OR "Model-Driven Engineering" OR "Component Design"
    """

intervention_query = """
    "Generative AI" OR "Generative Model" OR "Large Language Model" OR "Retrieval Augmented Generation" OR "NLP"  OR "Machine Learning"
    """

def exclude_website(website):
    return f"-site:{website}"

def include_website(website):
    return f"site:{website}"

def google_search(query, api_key, cse_id, num_results):
    results = []
    for start in range(1, num_results + 1, 10):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query,
            'start': start
        }
        response = requests.get(url, params=params)
        data = response.json()

        if 'items' not in data:
            print("No items found.")
            break

        for item in data['items']:
            results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet'),
                'displayLink': item.get('displayLink')
            })

    return results

def get_google_results():
    websites_to_exclude = [
        'youtube.com',
        'github.com',
        'paperswithcode.com'
    ]

    query = f"({population_query}) AND ({intervention_query}) after:2021"

    for website in websites_to_exclude:
        query += " " + exclude_website(website)

    print("query:", query)

    search_results = google_search(query, API_KEY, CSE_ID, NUM_RESULTS)
    if not search_results:
        print("No results found for this query.")
        return
    pop_df = pd.DataFrame(search_results)
    pop_df.to_csv(f"./google_results/google_results.csv", index=False)
    print(f"Results saved to google_results.csv")

def get_github_results():
    query = f"({population_query}) AND ({intervention_query}) after:2021"

    query += " " + include_website("github.com")

    print("query:", query)

    search_results = google_search(query, API_KEY, CSE_ID, NUM_RESULTS)
    if not search_results:
        print("No results found for this query.")
        return
    pop_df = pd.DataFrame(search_results)
    pop_df.to_csv(f"./github_results/github_results.csv", index=False)
    print(f"Results saved to github_results.csv")

def get_pwc_results():
    query = f"({population_query}) AND ({intervention_query}) after:2021"

    query += " " + include_website("paperswithcode.com")

    print("query:", query)

    search_results = google_search(query, API_KEY, CSE_ID, NUM_RESULTS)
    if not search_results:
        print("No results found for this query.")
        return
    pop_df = pd.DataFrame(search_results)
    pop_df.to_csv(f"./pwc_results/pwc_results.csv", index=False)
    print(f"Results saved to pwc_results.csv")

if __name__ == "__main__":
    os.makedirs('./google_results', exist_ok=True)
    os.makedirs('./github_results', exist_ok=True)
    os.makedirs('./pwc_results', exist_ok=True)

    get_google_results()
    get_github_results()
    get_pwc_results()
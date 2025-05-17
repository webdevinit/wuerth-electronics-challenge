from dotenv import load_dotenv
from serpapi import GoogleSearch
import os
import pandas as pd
from read_bom_results import read_bom_results

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env')
load_dotenv(dotenv_path=env_path, override=True)
serp_api_key = os.getenv("SERP_API_KEY")

def get_search_links(results, max_links=5):
    links = []
    for i in range(min(len(results.get("organic_results", [])), max_links)):
        links.append(results["organic_results"][i]["link"])
    # Pad with empty strings if we have fewer than max_links results
    links.extend([''] * (max_links - len(links)))
    return links

if __name__ == "__main__":
    search_results = []
    params = {
        "engine": "google",
        "api_key": serp_api_key
    }

    bom_results_dir = os.path.join(os.path.dirname(__file__), "sample bom results")
    _, partnumbers = read_bom_results(bom_results_dir)

    for partnumber in partnumbers:
        params["q"] = partnumber
        search = GoogleSearch(params)
        results = search.get_dict()
        links = get_search_links(results)
        
        row = [partnumber] + links
        search_results.append(row)

    # Create DataFrame with appropriate columns
    columns = ['partnumber'] + [f'link{i+1}' for i in range(5)]
    df = pd.DataFrame(search_results, columns=columns)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), "search_results.csv")
    df.to_csv(output_path, index=False)

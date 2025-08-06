import os
import requests
from dotenv import load_dotenv

load_dotenv()

def collaborator_data(username):
    query = """
        query($login: String!) {
            user(login: $login) {
                name
                login
                pronouns
            }
        }
    """
    variables = {"login": username}

    response = requests.post(
        os.getenv('GITHUB_GRAPHQL_URL'),
        json = {"query": query, "variables": variables},
        headers = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN_CLASSIC')}",
            "Content-Type": "application/json"
        }
    )

    response_json = response.json()

    return response_json['data']['user']

def collaborators(owner, repo):
    i = 0
    contributors = []
    github_url = os.getenv('GITHUB_API_URL')
    headers = {
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN_PAT')}",
        "Accept": "application/vnd.github.v3+json"
    }

    while True:
        i += 1

        response = requests.get(
            f"{github_url}repos/{owner}/{repo}/contributors?page={i}&per_page=100", 
                headers = headers
        )

        data = response.json()

        if not data:
            break

        for contributor in data:
            if '[bot]' not in contributor['login']:
                contributors.append(contributor['login'])
    
    return contributors
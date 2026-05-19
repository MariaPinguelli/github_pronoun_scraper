import os
import time
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
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN_PAT')}",
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
            try:
                if (
                        (contributor not in ['status', 'message', 'documentation_url']) and 
                        ('[bot]' not in contributor['login']) and 
                        (contributor['login'] != 'Copilot')
                    ):
                    contributors.append(contributor['login'])
            except Exception as e:
                print(f"\nErro: {e} | Contributor: {contributor}\n")
    
    return contributors

def all_collaborators(owner, repo):
    """
    Busca TODOS os contribuidores usando GraphQL
    Não tem o limite de 500 da REST API
    """
    contributors = []
    github_graphql_url = os.getenv('GITHUB_GRAPHQL_URL')
    headers = {
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN_PAT')}",
        "Content-Type": "application/json"
    }
    
    has_next_page = True
    cursor = None
    
    # Query GraphQL para pegar contribuidores (não colaboradores)
    # Usando repository.defaultBranchRef.target.history para pegar autores de commits
    query = """
    query($owner: String!, $name: String!, $cursor: String) {
      repository(owner: $owner, name: $name) {
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 100, after: $cursor) {
                edges {
                  cursor
                  node {
                    author {
                      user {
                        login
                        name
                      }
                      email
                    }
                  }
                }
                pageInfo {
                  hasNextPage
                  endCursor
                }
                totalCount
              }
            }
          }
        }
      }
    }
    """
    
    while has_next_page:
        variables = {
            "owner": owner,
            "name": repo,
            "cursor": cursor
        }
        
        response = requests.post(
            github_graphql_url,
            json={"query": query, "variables": variables},
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Erro GraphQL: {response.status_code}")
            break
            
        data = response.json()
        
        if "errors" in data:
            print(f"Erros GraphQL: {data['errors']}")
            break
        
        # Navega até os dados dos commits
        try:
            history = data['data']['repository']['defaultBranchRef']['target']['history']
            total_commits = history.get('totalCount', 0)
            print(f"Total de commits no repositório: {total_commits}")
            
            for edge in history.get('edges', []):
                author = edge['node']['author']
                user = author.get('user')
                
                # Se tem usuário associado (não é anônimo)
                if user and user.get('login'):
                    login = user['login']
                    if ('[bot]' not in login and login != 'Copilot'):
                        if login not in contributors:
                            contributors.append(login)
            
            # Informações de paginação
            page_info = history.get('pageInfo', {})
            has_next_page = page_info.get('hasNextPage', False)
            cursor = page_info.get('endCursor')
            
            print(f"Progresso: {len(contributors)} contribuidores únicos até agora")
            
        except (KeyError, TypeError) as e:
            print(f"Erro ao processar dados: {e}")
            break
        
        # Pequena pausa para evitar rate limit
        time.sleep(0.5)
    
    # Remove duplicatas (já estamos fazendo, mas garantia extra)
    contributors = list(set(contributors))
    print(f"\n✅ Total de contribuidores encontrados via GraphQL: {len(contributors)}")
    return contributors
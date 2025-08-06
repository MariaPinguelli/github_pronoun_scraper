import api as api
import files_utils
import utils

print("-----------------START SCRIPT-----------------\n")
repos = files_utils.get_data('repos.json')

for i, repo in enumerate(repos):
    print(f"Repo: {i + 1}/{len(repos)} | Buscando dados do repositório {repo['name']}")
    contributor_list = api.collaborators(repo['owner'], repo['name'])
    contributor_list = sorted(contributor_list, key=str.lower)

    contributor_data = files_utils.get_contributor_data(repo['name'])

    for j, login in enumerate(contributor_list):
        if not any(user['login'] == login for user in contributor_data):
            print(f"Repo: {i + 1}/{len(repos)} | User: {j + 1}/{len(contributor_list)} | Buscando usuário {login}")
            res = api.collaborator_data(login)
            processed_data = utils.process_data(res)
            contributor_data.append(processed_data)
            files_utils.save_data(repo['name'], contributor_data)
    
    print("\n\n")

print("-----------------END SCRIPT-----------------")
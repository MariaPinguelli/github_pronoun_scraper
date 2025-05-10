import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from WikiGendersort.Wiki_Gendersort import wiki_gendersort

print("---------- Iniciando Script ----------")

load_dotenv()

pronoun_dict = {
    'M': 'he/him',
    'F': 'she/her',
    'UNK': 'unknown',
    'INI': 'unknown',
    'UNI': 'unknown',
}

WG = wiki_gendersort()

chrome_options = Options()
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 3)
wait_login = WebDriverWait(driver, 35)

github_url = os.getenv('GITHUB_URL')
github_api_url = os.getenv('GITHUB_API_URL')

headers = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "pronoun_scraping_app"
}

users_file = './users.json'
saved_users = []

if not os.path.exists(users_file):
    print("Arquivo não encontrado. Criando arquivo...")
    with open(users_file, 'w') as f:
        f.write('[]')  # arquivo inicial vazio

with open(users_file, 'r') as f:
    file_content = f.read()
    if file_content.strip():
        saved_users = json.loads(file_content)

contributors = []
i = 0

while True:
    i += 1
    print('Procurando colaboradores do repositório... | ', i)
    response = requests.get(f"{github_api_url}repos/JabRef/jabref/contributors?page={i}&per_page=100", headers=headers)
    data = response.json()
    if not data:
        break

    for contributor in data:
        if not any(user['login'] == contributor['login'] for user in saved_users) and '[bot]' not in contributor['login']:
            contributors.append(contributor)
    
    print("--------------------------------------\n\n")

if contributors:
    saved_users.extend(contributors)
    with open(users_file, 'w') as f:
        json.dump(saved_users, f, indent=2)

    # Login
    print('Fazendo login...')
    driver.get(f"{github_url}login")

    username_input = driver.find_element(By.ID, 'login_field')
    password_input = driver.find_element(By.ID, 'password')

    username_input.send_keys(os.getenv('GITHUB_USERNAME'))
    password_input.send_keys(os.getenv('GITHUB_PASSWORD'))

    login_button = driver.find_element(By.NAME, 'commit')
    login_button.click()

    time.sleep(15)

    for contributor in contributors:
        file_path = f"./users/{contributor['login']}.json"
        user = dict()
        
        if not os.path.exists(file_path): # carregar se já tiver
            print('Criando arquivo: ', file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                pass
        # else:
        print('Lendo arquivo: ', file_path)
        with open(file_path, 'r') as f:
            file_content = f.read()
            try:
                user = json.loads(file_content)
            except:
                pass
              
        if not user or len(file_content) == 0:
            print(f"Buscando usuário {contributor['login']} no github")
            response = requests.get(f"{github_api_url}users/{contributor['login']}", headers=headers)
            user = response.json()

        if 'declared_pronoun' not in user:
            print(f"Buscando declared_pronoun do usuário {user['login']} no github")
            driver.get(f"{github_url}{user['login']}")

            try:
                pronouns = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[itemprop="pronouns"]'))).text
                user['declared_pronoun'] = pronouns
            except Exception as e:
                print(f"\n\nPronome não declarado\n\n")
                user['declared_pronoun'] = 'unknown'

        if 'infered_pronoun' not in user:
            print(f"Inferindo infered_pronoun do usuário {user['login']}")
            if user['name']:
                username = user['name'].split()[0] 
                user['infered_pronoun'] = pronoun_dict[WG.assign(username)]
            else:
                user['infered_pronoun'] = 'unknown'

        if user['declared_pronoun'] != 'unknown':
            user['pronoun'] = user['declared_pronoun']
        elif user['infered_pronoun'] != 'unknown':
            user['pronoun'] = user['infered_pronoun']
        else:
            user['pronoun'] = 'unknown'

        with open(file_path, 'w') as f:
            json.dump(user, f, indent=2)
        
        print("--------------------------------------\n\n")

else:
    print("Não existem novos contribuidores a serem adicionados ao banco de dados.")

print("---------- Fim do Script ----------")

driver.quit()

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

print("---------- Iniciando Script ----------")

load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--headless')
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
    response = requests.get(f"{github_api_url}repos/JabRef/jabref/contributors?page={i}&per_page=100", headers=headers)
    data = response.json()
    if not data:
        break

    for contributor in data:
        if not any(user['login'] == contributor['login'] for user in saved_users) and '[bot]' not in contributor['login']:
            contributors.append(contributor)

if contributors:
    saved_users.extend(contributors)
    with open(users_file, 'w') as f:
        json.dump(saved_users, f, indent=2)

    print("before driver.get")
    # Login
    driver.get(f"{github_url}login")

    username_input = driver.find_element(By.ID, 'login_field')
    password_input = driver.find_element(By.ID, 'password')

    username_input.send_keys(os.getenv('GITHUB_USERNAME'))
    password_input.send_keys(os.getenv('GITHUB_PASSWORD'))
    print('input data')

    login_button = driver.find_element(By.NAME, 'commit')
    login_button.click()
    print('clicked')

    time.sleep(30)

    for contributor in contributors:
        file_path = f"./users/{contributor['login']}.json"
        
        if not os.path.exists(file_path):
            # Criando arquivo vazio
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                pass

            response = requests.get(f"{github_api_url}users/{contributor['login']}", headers=headers)
            user = response.json()

            driver.get(f"{github_url}{contributor['login']}")
            # print("LINHA 94")

            try:
                pronouns = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[itemprop="pronouns"]'))).text
                # print(pronouns)
                user['pronouns'] = pronouns
                print(pronouns)
            except Exception as e:
                print(f"\n\nERRO {e}\n\n")
                user['pronouns'] = 'no_pronouns'

            with open(file_path, 'w') as f:
                json.dump(user, f, indent=2)

else:
    print("Não existem novos contribuidores a serem adicionados ao banco de dados.")

driver.quit()

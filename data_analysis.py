import json
import os

# Lendo a lista de usuários
with open('./users.json', 'r') as f:
    users_list = json.load(f)

stats = {}

# Contando os pronomes
for user in users_list:
    login = user['login']
    # print("login", login)
    user_file = f"./users/{login}.json"
    # print('user_file', user_file)
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            try:
                user_data = json.load(f)
                pronouns = user_data.get('pronouns', 'no_pronouns')
                stats[pronouns] = stats.get(pronouns, 0) + 1
            except Exception as e:
                print(f"\n\nERRO {e}\n\n")
                stats['error'] = stats.get('error', 0) + 1

# Exibindo dados brutos
print("\n---Dados brutos---")
for chave, valor in stats.items():
    print(f"{chave} - {valor}")
print("------------------\n")

# Exibindo dados em porcentagem
print("\n----Dados em %----")
total = len(users_list)
for chave, valor in stats.items():
    porcentagem = (valor / total) * 100
    print(f"{chave} - {porcentagem:.2f}%")
print("------------------\n")

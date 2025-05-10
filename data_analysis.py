import json
import os

# Lendo a lista de usuários
with open('./users.json', 'r') as f:
    users_list = json.load(f)

stats = {
    'pronoun': {},
    'declared_pronoun': {},
    'infered_pronoun': {},
}

no_name = 0
has_name = 0

filtered_user = []

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
                pronouns = user_data.get('pronoun', 'unknown')
                declared_pronoun = user_data.get('declared_pronoun', 'unknown')
                infered_pronoun = user_data.get('infered_pronoun', 'unknown')

                if declared_pronoun != 'unknown':
                    filtered_user.append(user_data)

                # if infered_pronoun == 'unknown':
                #     print(user_data['name'], type(user_data['name']))

                if user_data['name'] == None and infered_pronoun == 'unknown':
                    no_name = no_name + 1
                elif user_data['name'] and infered_pronoun == 'unknown':
                    has_name = has_name + 1
                
                stats['pronoun'][pronouns] = stats.get('pronoun', {}).get(pronouns, 0) + 1
                stats['declared_pronoun'][declared_pronoun] = stats.get('declared_pronoun', {}).get(declared_pronoun, 0) + 1
                stats['infered_pronoun'][infered_pronoun] = stats.get('infered_pronoun', {}).get(infered_pronoun, 0) + 1
            except Exception as e:
                print(f"\n\nERRO {e}\n\n")
                stats['error'] = stats.get('error', 0) + 1

# Exibindo dados brutos
print("\n---Dados brutos---")
for chave, valor in stats.items():
    print(f'------ {chave} -------')
    for chave2, valor2 in valor.items():
        print(f"{chave2} - {valor2}")
    print("------------------\n\n")

# Exibindo dados em porcentagem
print("\n----Dados em %----")
total = len(users_list)
print(f"Total: {total} (total is user_list len)")

for chave, valor in stats.items():
    print(f'------ {chave} -------')
    for chave2, valor2 in valor.items():
        porcentagem = (valor2 / total) * 100
        print(f"{chave2} - {porcentagem:.2f}%")
    print("------------------\n")

filtered_user_total = len(filtered_user)
print('\n-------------------------')
print('Usuários que declararam seus pronomes: ', filtered_user_total)
# print('-------------------------\n\n')
# Exibindo dados diferença entre pronome declarado e inferido
# print("\n----Dados em %---- (total is user_list len)")
declared_pronoun_stats = {
    'diff': 0,
    'equal': 0
}

for user in filtered_user:
    declared_pronoun = user.get('declared_pronoun', 'unknown')
    infered_pronoun = user.get('infered_pronoun', 'unknown')

    if declared_pronoun != infered_pronoun:
        declared_pronoun_stats['diff'] = declared_pronoun_stats['diff'] + 1
    elif declared_pronoun == infered_pronoun:
        declared_pronoun_stats['equal'] = declared_pronoun_stats['equal'] + 1

print('\n')
print('diff n°: ', declared_pronoun_stats['diff'])
print('equal n°: ', declared_pronoun_stats['equal'])
print('--------------')
print(f"diff %: {((declared_pronoun_stats['diff']/filtered_user_total) * 100):.2f}%")
print(f"equal %: {((declared_pronoun_stats['equal']/filtered_user_total) * 100):.2f}%")
print('-------------------------\n')

print('Dados sobre os pronomes inferidos como unknown')
total = no_name + has_name
print(f"Ao total são {total} usuários com pronome inferido como unknown")
print(f"{no_name} - {((no_name/total) * 100):.2f}% sem nome")
print(f"{has_name} - {((has_name/total) * 100):.2f}% com nome")
# print(f"Sendo {no_name} do total de {total} ({((no_name/total) * 100):.2f}%), usuários não tinham um nome declarado")
# print(f"E {has_name} do total de {total} ({((has_name/total) * 100):.2f}%) usuários tinham um nome declarado")

print('-------------------------\n\n')
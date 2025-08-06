import os
import json

def get_contributor_data(repo_name):
    filename = f"db/{repo_name}_list.json"

    verify_file(filename)
    
    return get_data(filename)

def verify_file(filename):
    if not os.path.exists(filename):
        print("Arquivo não encontrado. Criando arquivo...")
        with open(filename, 'w') as f:
            f.write('[]')

def save_data(repo_name, data):
    filename = f"db/{repo_name}_list.json"

    verify_file(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def get_data(filename):
    data = []

    with open(filename, 'r') as f:
        file_content = f.read()
        if file_content.strip():
            data = json.loads(file_content)

    return data
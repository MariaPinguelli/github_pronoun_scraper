from WikiGendersort.Wiki_Gendersort import wiki_gendersort

def process_data(raw_data):
    gendersort = wiki_gendersort()

    pronoun_dict = {
        'M': 'he/him',
        'F': 'she/her',
        'UNK': '',
        'INI': '',
        'UNI': ''
    }
    
    processed_data = {
        'name': None,
        'login': None,
        'declared_pronouns': None,
        'infered_pronouns': None,
    }

    processed_data['name'] = raw_data['name']
    processed_data['login'] = raw_data['login']
    processed_data['declared_pronouns'] = raw_data['pronouns']
    
    if (raw_data['name']):
        processed_data['infered_pronouns'] = pronoun_dict[gendersort.assign(raw_data['name'])]
    
    return processed_data
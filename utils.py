from WikiGendersort.Wiki_Gendersort import wiki_gendersort

def get_pronoun(user):
    invalid_values = [None, '', 'unknown']
    
    declared = user.get('declared_pronouns')
    if declared not in invalid_values:
        return declared
    
    infered = user.get('infered_pronouns')
    if infered not in invalid_values:
        return infered
    
    return 'unknown'

def process_data(raw_data):
    gendersort = wiki_gendersort()

    pronoun_dict = {
        'M': 'he/him',
        'F': 'she/her',
        'UNK': 'unknown',
        'INI': 'unknown',
        'UNI': 'unknown'
    }
    
    raw_pronouns = raw_data.get('pronouns')
    declared_pronouns = 'unknown' if raw_pronouns in [None, ''] else raw_pronouns
    
    processed_data = {
        'name': raw_data.get('name'),
        'login': raw_data.get('login', 'unknown'),
        'declared_pronouns': declared_pronouns,
        'infered_pronouns': 'unknown',
        'pronouns': 'unknown'
    }
    
    if processed_data['name']:
        gender = gendersort.assign(processed_data['name'])
        processed_data['infered_pronouns'] = pronoun_dict.get(gender, 'unknown')
    
    processed_data['pronouns'] = get_pronoun(processed_data)
    
    return processed_data
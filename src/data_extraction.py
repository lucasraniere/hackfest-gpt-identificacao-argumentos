import re

t_regex = r'T[0-9]+\s+[a-zA-Z]+\s+[\d\s\d]+.+'
a_regex = r'A[0-9]+\s+[a-zA-Z]+\s+T[0-9]+\s+.+'
r_regex = r'R[0-9]+\s+[a-z]+\s+Arg[0-9]:T[0-9]+\s+Arg[0-9]:T[0-9]+'

def preproc(response_txt):
    response_txt = re.sub('\t', ' ', response_txt)
    response_txt = re.sub(' END', '', response_txt)
    return response_txt


def data_extraction(response_txt: str):
    response_txt = preproc(response_txt)
    response_data = {
        't': re.findall(t_regex, response_txt) if re.findall(t_regex, response_txt) else [],
        'a': re.findall(a_regex, response_txt) if re.findall(a_regex, response_txt) else [],
        'r': re.findall(r_regex, response_txt) if re.findall(r_regex, response_txt) else []
    }
    return response_data


def data_organizer(response_txt: str):
    data = data_extraction(response_txt)
    final_data = {
        't':{},
        'a':{},
        'r':{}
    }
    for t in data['t']:
        t_number = re.search(r'T[\d]*', t).group() if re.search(r'T[\d]*', t) else 'None'
        t_type = re.search(r'\s+[a-zA-Z]+\s+', t).group().strip() if re.search(r'\s+[a-zA-Z]+\s+', t) else 'None'
        span = tuple(re.search(r'(\d+) (\d+)', t).group().split()) if re.search(r'(\d+) (\d+)', t) else 'None'
        text = re.search(r'[\D]*$', t).group().strip() if re.search(r'[\D]*$', t) else 'None'
        final_data['t'][t_number] = {
            'type': t_type,
            'span': span,
            'text': text
        }
    for a in data['a']:
        a_number = re.search(r'A[\d]*', a).group() if re.search(r'A[\d]*', a) else 'None'
        t = re.search(r'T[\d]*', a).group() if re.search(r'T[\d]*', a) else 'None'
        stance_type = re.search(r'[\D]*$', a).group().strip() if re.search(r'[\D]*$', a) else 'None'
        final_data['a'][a_number] = {
            't': t,
            'stance_type': stance_type
        }
    for r in data['r']:
        r_number = re.search(r'R[\d]*', r).group() if re.search(r'R[\d]*', r) else 'None'
        relation_type = re.search(r'\s+[a-z]+\s+', r).group() if re.search(r'\s+[a-z]+\s+', r) else 'None'
        arg1 = re.findall(r'T[\d]*', r)[0] if re.findall(r'T[\d]*', r)[0] else 'None'
        arg2 = re.findall(r'T[\d]*', r)[1] if re.findall(r'T[\d]*', r)[1] else 'None'
        final_data['r'][r_number] = {
            'relation_type': relation_type,
            'arg1': arg1,
            'arg2': arg2
        }

    return final_data

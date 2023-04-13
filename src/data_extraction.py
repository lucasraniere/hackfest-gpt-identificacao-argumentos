import re

t_regex = r'T[0-9]+\s+[a-zA-Z]+\s+[\d\s\d]+.+'
a_regex = r'A[0-9]+\s+[a-zA-Z]+\s+T[0-9]+\s+.+'
r_regex = r'R[0-9]+\s+[a-z]+\s+Arg[0-9]:T[0-9]+\s+Arg[0-9]:T[0-9]+'

def remove_tab(response_txt):
    return re.sub('\t', ' ', response_txt)


def data_extraction(response_txt: str):
    response_txt = remove_tab(response_txt)
    response_data = {
        't': re.findall(t_regex, response_txt),
        'a': re.findall(a_regex, response_txt),
        'r': re.findall(r_regex, response_txt)
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
        t_number = re.search(r'T[\d]*', t).group()
        t_type = re.search(r'\s+[a-zA-Z]+\s+', t).group().strip()
        span = tuple(re.search(r'(\d+) (\d+)', t).group().split())
        text = re.search(r'[\D]*$', t).group().strip()
        final_data['t'][t_number] = {
            'type': t_type,
            'span': span,
            'text': text
        }
    for a in data['a']:
        a_number = re.search(r'A[\d]*', a).group()
        t = re.search(r'T[\d]*', a).group()
        stance_type = re.search(r'[\D]*$', a).group().strip()
        final_data['a'][a_number] = {
            't': t,
            'stance_type': stance_type
        }
    for r in data['r']:
        r_number = re.search(r'R[\d]*', r).group()
        relation_type = re.search(r'\s+[a-z]+\s+', r).group()
        arg1 = re.findall(r'T[\d]*', r)[0]
        arg2 = re.findall(r'T[\d]*', r)[1]
        final_data['r'][r_number] = {
            'relation_type': relation_type,
            'arg1': arg1,
            'arg2': arg2
        }

    return final_data

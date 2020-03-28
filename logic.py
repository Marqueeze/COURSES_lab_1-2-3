import os

CONST_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя-_'
CONST_eng_letters = 'abcdefghijklmnopqrstuvwxyz-_'
CONST_numbers = '0123456789,.'
CONST_punct = ',.;:!?-"\'»«'


def _tokenize(string, categories):
    token = ''
    tokens = []
    category = None
    flag = 0
    for char in string:
        while True:
            if token:
                if category and flag and char in category:
                    token += char
                    break
                else:
                    tokens.append((token, category))
                    token = ''
            else:
                category = None
                for (cat, cur_flag) in categories:
                    if char in cat:
                        category = cat
                        flag = cur_flag
                        break
                if flag != 2:
                    token += char
                break
    if token:
        tokens.append((token, category))
    return tokens


def _make_ret_path(path, cat):
    add = {CONST_eng_letters: 'foreign',
           CONST_numbers: 'digits'}
    if cat in add:
        add = add[cat]
    else:
        add = cat
    ret = os.path.join(path, add)
    if not os.path.exists(ret):
        os.mkdir(ret)
    return ret


def _find_indicies_of_category(path, cat):
    ret = _make_ret_path(path, cat)
    for file in [_ for _ in os.listdir(path) if os.path.isfile(os.path.join(path, _))]:
        with open(os.path.join(path, file), 'r+') as f:
            ans = [str(i) for i, x in enumerate(_tokenize(f.read(), [(CONST_punct, 0), (' \t\r\n', 2),
                                                                     (CONST_numbers, 1), ('+-=', 0),
                                                                     (CONST_letters + CONST_letters.upper(), 1),
                                                                     (CONST_eng_letters + CONST_eng_letters.upper(), 1)
                                                                     ])) if x[1] == cat]
        with open(os.path.join(ret, file), 'w+') as f:
            f.write(str.join(', ', ans))
    return ret


def tokenize(path):
    ret = _make_ret_path(path, 'tokens')
    for file in [_ for _ in os.listdir(path) if os.path.isfile(os.path.join(path, _))]:
        with open(os.path.join(path, file), 'r+') as f:
            an = str.join(' ', [x[0] for x in _tokenize(f.read(), [(CONST_punct, 0), (' \t\r\n', 2), (CONST_numbers, 1),
                                                                   ('+-=', 0),
                                                                   (CONST_letters + CONST_letters.upper(), 1),
                                                                   (CONST_eng_letters + CONST_eng_letters.upper(), 1)
                                                                   ])])
        with open(os.path.join(ret, file), 'w+') as f:
            f.write(an)
    return ret


def digits_indicies(path):
    ret = _find_indicies_of_category(path, CONST_numbers)
    return ret


def foreign_indicies(path):
    ret = _find_indicies_of_category(path, CONST_eng_letters)
    return ret

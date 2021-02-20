import pandas as pd
import numpy as np
import datetime
import ast


def get_brand(x):
    if 'Visit' in x:
        return x[10:][:-6]
    elif 'Brand' in x:
        return x[7:]
    else:
        return x


def get_date(date):  # string dates

    if type(date) != str:
        return np.nan

    new_date = date[1:-1].replace('.', '')
    different_months = {'July': 'Jul', 'April': 'Apr', 'Sept': 'Sep'}
    date_elements = new_date.split(' ')

    # checking integrity of the date

    if len(date_elements) != 3:
        return np.nan

    if date_elements[1] not in list(different_months.keys()):
        result = datetime.datetime.strptime(new_date, '%d %b %Y')

    else:
        date_elements[1] = different_months[date_elements[1]]
        processed_date = date_elements[0] + ' ' + date_elements[1] + ' ' + date_elements[2]

        result = datetime.datetime.strptime(processed_date, '%d %b %Y')

    return result


def get_categories_and_positions(strings_array):
    strings_array = ast.literal_eval(strings_array)
    result = []
    for category in strings_array:

        chars = []
        for char in ['#', ',']:
            chars = category.replace(char, '')

        if '(' in chars:
            init_ind = chars.index('(')
            chars = chars[:init_ind]

        chars = chars.strip().split(' ')
        position = chars[0]

        name = ''
        for x in range(2, len(chars)):
            name = name + ' ' + chars[x]

        result.append(name.strip()), result.append(position)

    return result


def preprocess_data(data):

    data['brand'] = np.vectorize(get_brand)(data['brand'])
    data['rating'] = data['rating'].apply(lambda x: x[:3] if type(x) == str else x).astype(float)
    data['answers'] = data['answers'].apply(lambda x:
                                            int(x[1:-2].split(' ')[0]) if '\n' in x else x).astype(int)
    data['first_date'] = data['first_date'].apply(lambda x: get_date(x))

    categories_positions = pd.DataFrame(
        data['categories'].apply(lambda x: get_categories_and_positions(x)).tolist()
    ).loc[:, 0:3]
    categories_positions.columns = ['category', 'position_c', 'subcategory', 'position_s']
    data = pd.concat([data, categories_positions], axis=1)

    data.to_csv('../data/interim/amazon_shop_data_interim.csv', index=False)
    return data



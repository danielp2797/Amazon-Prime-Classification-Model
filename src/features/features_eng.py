def add_features(data):

    data['price_band'] = (data['price'] <=70) & (data['price'] >=20)

    notable_brands = data['brand'].value_counts()[data['brand'].value_counts() > 5].index.tolist()
    data['notable_brand'] = data['brand'].isin(notable_brands)

    return data
import json

def games_search(client, title):
    byte_array = client.api_request(
            'games',
            'fields *;search "{}";'.format(title)
          )
        # parse into JSON however you like...

    json_result = json.loads(byte_array.decode('utf-8'))
    if len(json_result) > 0:
        return json_result[0]
    return None

def covers_get_by_id(client, id):
    byte_array = client.api_request(
            'covers',
            'fields *;where id={};'.format(id)
          )
        # parse into JSON however you like...

    json_result = json.loads(byte_array.decode('utf-8'))
    return json_result

def genres_get(client, genre_list):
    formatted_genre_list = ','.join([str(i) for i in genre_list])
    byte_array = client.api_request(
        'genres',
        'fields *;where id=({});'.format(formatted_genre_list)
    )

    json_result = json.loads(byte_array.decode('utf-8'))
    return json_result

def platforms_get(client, platforms_list):
    formatted_platform_list = ','.join([str(i) for i in platforms_list])
    byte_array = client.api_request(
        'platforms',
        'fields *;where id=({});'.format(formatted_platform_list)
    )

    json_result = json.loads(byte_array.decode('utf-8'))
    return json_result  

def release_dates_get(client, release_dates):
    formatted_release_dates = ','.join([str(i) for i in release_dates])
    byte_array = client.api_request(
        'release_dates',
        'fields *;where id=({});'.format(formatted_release_dates)
    )

    json_result = json.loads(byte_array.decode('utf-8'))
    return json_result  
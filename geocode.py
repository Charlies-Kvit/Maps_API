import requests
import pygame
import os


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_request, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError("ERROR")
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]


def get_spn(features):
    lower_corner = features["boundedBy"]["Envelope"]['lowerCorner'].split()
    upper_corner = features["boundedBy"]["Envelope"]['upperCorner'].split()
    delta_1 = abs(float(lower_corner[1]) - float(upper_corner[1])) / 2.0
    delta_2 = abs(float(lower_corner[0]) - float(upper_corner[0])) / 2.0
    return [str(delta_1), str(delta_2)]


def show_map(features, t_long, t_lat):
    map_params = {
        "ll": ",".join([t_long, t_lat]),
        "spn": ",".join(get_spn(features)),
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    with open("map.png", 'wb') as f:
        f.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load("map.png"), (0, 0))
    font = pygame.font.Font(None, 30)
    text = font.render(f"({t_long}, {t_lat})", True, "red")
    screen.blit(text, (300, 230))
    pygame.draw.circle(screen, "red", (300, 225), 5)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove('map.png')

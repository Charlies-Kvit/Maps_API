import requests
import pygame
from time import sleep
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


def show_map():
    spn1 = 0.3
    map_params = {
        "ll": ",".join(["73.355852", "54.972361"]),
        "spn": ",".join(["0.3", "0.3"]),
        "l": "map"
    }
    print('OK')
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    print("OK")
    with open("map.jpg", 'wb') as f:
        f.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load("map.jpg"), (0, 0))
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if spn1 + 1 > 0.2:
                        spn1 += 1
                        map_params['spn'] = ",".join([str(spn1), str(spn1)])
                        response = requests.get(map_api_server, params=map_params)
                        print("OK")
                        with open("map.jpg", 'wb') as f:
                            f.write(response.content)

                        screen.blit(pygame.image.load("map.jpg"), (0, 0))
                        sleep(0.1)
                    
                if event.key == pygame.K_w:
                    if spn1 - 1 > 0.2:
                        spn1 -= 1
                        map_params['spn'] = ",".join([str(spn1), str(spn1)])
                        response = requests.get(map_api_server, params=map_params)
                        print("OK")
                        with open("map.jpg", 'wb') as f:
                            f.write(response.content)
                        screen.blit(pygame.image.load("map.jpg"), (0, 0))
                        sleep(0.1)
                    
        pygame.display.flip()
    pygame.quit()
    os.remove('map.jpg')

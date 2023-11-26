import json
import os
import random
import time

import folium

from geopy.geocoders import Nominatim
import requests


def obter_coordenadas(bairro: str, cidade: str, estado: str) -> tuple:
    print(f'obtendo localização: {bairro}')
    time.sleep(random.randint(1, 4))
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(f'{bairro}, {cidade}, {estado}')
    if location is None:
        print(f'Não localizado {bairro}')
        return 0.0, 0.0
    return location.latitude, location.longitude


def obter_bairros_api(url, token) -> list:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',  # Adjust the content type as needed
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print("API Response:", response.json())
            data = [bairro for bairro in response.json()['result']]
            # print(data)
            return [bairro['name'] for bairro in data]
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")


def plot_map(coord: tuple, cidade: str, estado: str):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(f'{cidade}, {estado}')
    # return location.latitude, location.longitude
    # map_cidade = folium.Map(location=[2.8198, -60.6715], zoom_start=13)
    map_cidade = folium.Map(location=[location.latitude, location.longitude], zoom_start=13)

    for bairro, coordenadas in coord.items():
        print(f'Plotando bairro: {bairro}')
        latitude, longitude = coordenadas
        if latitude == 0.0:
            print('coordenadas invalidas')
            continue
        folium.Marker([latitude, longitude], popup=bairro).add_to(map_cidade)

    map_cidade.save('mapa_bairros.html')
    print('concluído')


# O id da cidade poe ser obtido em: https://brasilaberto.com/docs utilizando a api
# Ex: 3698 = Rio Branco - AC
cityId = 3698
cidade = 'Rio Branco'
estado = 'Acre'
api_url = f'https://brasilaberto.com/api/v1/districts/{cityId}'
# define o token
bearer_token = os.environ.get('my_token', 'não localizado')
# print(bearer_token)
bairros = obter_bairros_api(url=api_url, token=bearer_token)
coord_bairros = {bairro: obter_coordenadas(bairro, 'Rio Branco', 'Acre') for bairro in bairros}
plot_map(coord=coord_bairros, cidade=cidade, estado=estado)

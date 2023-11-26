# geo_bairros

Exemplo de plotagem de bairros de uma cidade em python

Ex:
```python
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
```

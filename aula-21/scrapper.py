from bs4 import BeautifulSoup
import requests


url_imdb = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
url_just_watch = 'https://www.justwatch.com/br/filme/'

html = requests.get(url=url_imdb, headers={'User-Agent': 'Mozilla/5.0'}).content
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())

lista = soup.find('ul', class_='compact-list-view')
titulos = lista.find_all('h3', class_='ipc-title__text')
for titulo in titulos:
    titulo = titulo.text.split('. ')[1]
    print('-----------------------------------------')
    print(titulo)

    titulo_tratado = titulo.lower().replace(' ', '-')
    # print(titulo_tratado)
    
    url_busca = url_just_watch + titulo_tratado
    # print(url_busca)

    html = requests.get(url=url_busca, headers={'User-Agent': 'Mozilla/5.0'}).content
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    opcoes = soup.find('div', class_='buybox-row stream')
    # print(opcoes)

    if not opcoes:
        print('Não foram encontrados links para asistir.')
        continue

    for opcao in opcoes:
        links = opcao.find_all('a', class_='offer')
        for link in links:
            print(link['href'])

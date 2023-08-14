from bs4 import BeautifulSoup
import requests


url_imdb = 'https://www.imdb.com'
url_imdb_top_250 = url_imdb + '/chart/top/?ref_=nv_mv_250'
url_just_watch = 'https://www.justwatch.com/br/filme/'

html = requests.get(url=url_imdb_top_250, headers={'User-Agent': 'Mozilla/5.0'}).content
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())

lista = soup.find('ul', class_='compact-list-view')
titulos = lista.find_all('h3', class_='ipc-title__text')
links = lista.find_all('a', class_='ipc-title-link-wrapper')
for titulo, link in zip(titulos, links):
    titulo = titulo.text.split('. ')[1]
    link = url_imdb + link['href']
    print('-----------------------------------------')
    print('Título: ', titulo)
    print('Link: ', link)

    html = requests.get(url=link, headers={'User-Agent': 'Mozilla/5.0'}).content
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    svg = soup.find('svg', class_='ipc-icon--star')
    parent = svg.parent.parent
    nota = parent.find('span').text
    print('Nota do público: ', nota)

    meta_data = soup.find('ul', class_='ipc-metadata-list')
    itens_meta_data = meta_data.find_all('a', class_='ipc-metadata-list-item__list-content-item--link')
    diretor = itens_meta_data[0].text
    print('Diretor: ', diretor)

    atores = []
    avatares = soup.find_all('div', class_='title-cast-item__avatar')
    for avatar in avatares:
        dados_ator = avatar.find_next_sibling()
        ator = dados_ator.find('a').text
        atores.append(ator)
    print('Atores: ', atores)
        
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

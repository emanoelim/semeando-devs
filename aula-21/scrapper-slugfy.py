import requests
from slugify import slugify
from bs4 import BeautifulSoup


url_imdb = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
url_just_watch = 'https://www.justwatch.com/br/filme/'
resultado = requests.get(url=url_imdb, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(resultado.content, 'html.parser')
# print(soup.prettify())

lista = soup.find('ul', class_='compact-list-view')
titulos = soup.find_all('h3', class_='ipc-title__text')[1:251]
links = soup.find_all('a', class_='ipc-title-link-wrapper')

for titulo, link in zip(titulos, links):
    try:
        print('--------------------------')

        # Tratar titulo para montar a url de busca
        # 1. Um sonho de liberdade = um-sonho-de-liberdade
        titulo_split = titulo.text.split('. ')
        posicao = titulo_split[0]
        titulo_tratado = titulo_split[1]
        titulo_slugfy = slugify(titulo_tratado)
        print('Titulo:', titulo_tratado)
        print('Posição na lista: ', posicao)

        # Acessar filme para extrair detalhes
        link_filme = 'https://www.imdb.com/' + link['href']
        resultado = requests.get(url=link_filme, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resultado.content, 'html.parser')

        # Pegar nota do filme
        icone = soup.find('svg', class_='ipc-icon--star')
        div_pai = icone.parent.parent
        nota = div_pai.find('span').text
        print('Nota: ', nota)

        # Pegar diretor do filme
        diretor = soup.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text
        print(diretor)

        # Pegar elenco do filme
        lista = []
        avatares = soup.find_all('div', class_='ipc-media--avatar')
        for avatar in avatares:
            nome = avatar.find_next_sibling()['aria-label']
            lista.append(nome)
        print(lista)
        
        # Acessar a url
        url = url_just_watch + titulo_slugfy
        resultado = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        if resultado.status_code == 200:        
            # Extrair apenas opções "stream"
            soup = BeautifulSoup(resultado.content, 'html.parser')
            stream = soup.find('div', class_='buybox-row stream')
            if stream:
                links = stream.find_all('a')
                print('Opções para assistir: ')
                for link in links:
                    print(link['href'])
            else:
                print('Não foram encontrados links para assistir')

        else:
            print('Filme não encontrado no JustWatch')
    
    except Exception:
        pass

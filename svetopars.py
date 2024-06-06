import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import csv

# pip install lxml

count = 1
while count <= 61:
    url = f'https://maytoni.su/catalog/svetilniki/?PAGEN_1={count}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    heads = block.find_all('div', class_='inner_wrap TYPE_1')
    print(len(heads))
    for i in heads:
        w = i.find_next('a', href=True)
        print('https://maytoni.su' + w['href'])
        get_url = ('https://maytoni.su' + w['href'])
        tock = requests.get(get_url, headers=headers).text
        loom = BeautifulSoup(tock, 'lxml')
        name = loom.find('div', class_='topic__heading').find('h1')
        print(name.text.strip())
        head = (name.text.strip())
        articul = loom.find('div', class_='article muted font_xs')
        print(' '.join(articul.text.strip().split()))
        codd = (' '.join(articul.text.strip().split()))
        price = loom.find('div', class_='price font-bold font_mxs')
        print(price.text.strip())
        cena = (price.text.strip())
        params = loom.find('div', class_='js-scrolled').find_all('div', class_='properties-group__group')
        print(len(params))
        charact = []
        for param in params:
            cheas = param.find_all_next('div', class_='properties-group__item')
            for clo in cheas:
                print(' '.join(clo.text.strip().split()) + ';')
                all_par = (' '.join(clo.text.strip().split()))
                charact.append(all_par)
        try:
            pixx = loom.find('div', class_='gallery__thumb-wrapper').find_all('div', class_='gallery__item')
            print(len(pixx))
            pixes = []
            for pix in pixx:
                print('https://maytoni.su' + pix.find_next('img', class_='gallery__picture')['data-src'])
                photo = ('https://maytoni.su' + pix.find_next('img', class_='gallery__picture')['data-src'])
                pixes.append(photo)
        except:
            print('None')
            photo = 'None'
            pixes = 'None'

        print('\n')

        storage = {'name': head, 'code': codd, 'price': cena, 'params': '; '.join(charact), 'photoes': '; '.join(pixes),
                   'URL': get_url}
        fields = ['Name', 'Code', 'Price', 'Params', 'Photoes', 'URL']
        with open('svetilniky.csv', 'a+', encoding='utf-16') as file:
            pisar = csv.writer(file, delimiter='$', lineterminator='\r')
            # Проверяем, находится ли файл в начале и пуст ли
            file.seek(0)
            if len(file.read()) == 0:
                pisar.writerow(fields)  # Записываем заголовки, только если файл пуст

            pisar.writerow([storage['name'], storage['code'], storage['price'], storage['params'], storage['photoes'],
                            storage['URL']])
    count += 1
    print(count)

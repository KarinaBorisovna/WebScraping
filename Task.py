from bs4 import BeautifulSoup
import bs4
import requests
from pprint import pprint

HEADERS = {'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
           'Accept-Language': 'ru-RU,ru;q=0.9',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'same-origin',
           'Sec-Fetch-User': '?1',
           'Cache-Control': 'max-age=0',
           'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
           'sec-ch-ua-mobile': '?0'
           }

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}

response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
response.raise_for_status()
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')

articles_dict = {}

for article in articles:
    title = article.find('a', class_='tm-article-snippet__title-link')
    link = title.get('href')
    article_link = f'https://habr.com{link}'
    span_title = title.find('span').text

    date = article.find('time').get('title')
    public_date = date.split(',')


    result = requests.get(f'https://habr.com{link}', headers=HEADERS)
    result.raise_for_status()
    article_content = result.text

    soup = bs4.BeautifulSoup(article_content, features='html.parser')
    article_text = soup.find('div', class_="article-formatted-body")
    all_text = article_text.find_all('p')
    
    for word in KEYWORDS:

        for p in all_text:
            
            if p.text.lower().find(word) == -1:
                articles_dict[span_title] = f'{public_date[0]} - "{span_title}" - {article_link}'
                
for value in articles_dict.values():
    print(value)


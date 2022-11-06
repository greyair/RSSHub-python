from rsshub.utils import DEFAULT_HEADERS, fetch
import requests
from multiprocessing.dummy import Pool as ThreadPool


domain = 'https://i.hacking8.com'

def get_redirect_url(url=''):
    #response = requests.get(url, headers=DEFAULT_HEADERS, allow_redirects=False)
    r = requests.head(url, headers=DEFAULT_HEADERS, stream=True)  
    #print(response.status_code)
    #print(response.url)
    #print(response.text)
    return r.headers['Location']

def parse(post):
    item = {}
    item['description'] = item['title'] = post.css('td:nth-child(3) div div a::text').extract_first()
    re_url = post.css('td:nth-child(3) div div a::attr(href)').extract_first()
    link = get_redirect_url(f"{domain}{re_url}")
    item['link'] = link
    item['pubDate'] = post.css('td:nth-child(1)::text').extract_first().strip()
    item['author'] = post.css('td:nth-child(2) *::text').extract_first().strip()
    #print(str(item))
    return item


def ctx(category='', channel=''):
    r_url = f"{domain}/{category}/{channel}"
    print(r_url)
    tree = fetch(r_url, headers=DEFAULT_HEADERS)
    html = tree.css('tbody')
    posts = tree.css('tbody').css('tr')
    channel_title = html.css('title::text').extract_first()

    pool = ThreadPool(processes=10)
    items = pool.map(parse, posts)
    print('map: 堵塞')
    pool.close()
    pool.join()
    print(items)

    return {
        'title': f'{channel_title} -  Hacking8',
        'link': r_url,
        'description': f'Hacking8 - {channel_title}',
        'author': 'greyair',
        'items': list(items)
    }

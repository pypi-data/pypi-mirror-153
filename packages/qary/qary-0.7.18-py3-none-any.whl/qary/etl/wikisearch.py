import requests
import bs4


def full_text_search(search_text, base_url='https://en.wikipedia.org'):
    """ wikipedia.org full text search that returns list of matching article urls

    >>> len(list(full_text_search('hugo award best novel'))) >= 10
    True
    """
    search_url = '/'.join((base_url, 'w/index.php'))
    page = requests.get(search_url,
                        {'search': search_text},
                        )
    soup = bs4.BeautifulSoup(page.text, features='html5lib')
    soup = (soup.find('div', {'class': 'searchresults'}) or soup).find('ul')
    search_results_set = soup.find_all('li')
    urls = []
    for list_item in search_results_set:
        urls.append(list_item.find('a').get('href'))
    return ['/'.join((base_url, u)) for u in urls if u]

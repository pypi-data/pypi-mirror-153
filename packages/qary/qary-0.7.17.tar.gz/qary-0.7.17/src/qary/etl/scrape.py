import requests

import pandas as pd
import bs4
from tqdm import tqdm


def extract_book_titles(html=''):
    """ Looking for a scifi book title based on fuzzy memory of title

    >>> html = '''
    ...     <tr><td></td><td></td><td>
    ...     <a class="bookTitle" itemprop="url" href="/book/show/4932435-finnikin-of-the-rock">
    ...         <span itemprop="name" role="heading" aria-level="4">Finnikin of the Rock (Lumatere Chronicles, #1)</span>
    ...     </a><br><span class="by">by</span>
    ...     <span itemprop="author" itemscope="" itemtype="http://schema.org/Person">
    ...     <div class="authorName__container">
    ...     <a class="authorName" itemprop="url"
    ...        href="https://www.goodreads.com/author/show/34429.Bruce_Sterling">
    ...        <span itemprop="name">Bruce Sterling</span></a>
    ...     </div>
    ...     </span></td>
    ...     '''

    >>  len(goodreads_titles(html=html))
    1
    """
    soup = bs4.BeautifulSoup(html, features='lxml')
    titles = soup.find_all('a', {'class': 'bookTitle'})
    authors = soup.find_all('a', {'class': 'authorName'})
    print(f'{len(titles)} titles, {len(authors)} authors')
    return [(t.text.strip(), a.text.strip()) for (t, a) in zip(titles, authors)]


def goodreads_titles(
        url='https://www.goodreads.com/list/show/4893.Best_Science_Fiction_of_the_21st_Century',
        verbose=True, num_books=10000):
    """ Scrape book titles and their authors from GoodReads.com

    >>> url = 'https://www.goodreads.com/list/show/114319.Best_Science_Fiction_of_the_20th_Century'

    >>  title_authors = goodreads_titles(url, num_books=10)
    >>  len(title_authors) >= 10
    True
    """
    title_authors = []
    if url.lower().strip().startswith('http'):
        for p in tqdm(range(1, 10)):
            params = {'page': p}
            page = requests.get(url, params=params).text
            title_authors.extend(extract_book_titles(page))
            if len(title_authors) >= num_books:
                break
    return pd.DataFrame(title_authors, columns='title author'.split())


def schmidt_tools(url, verbose=True):
    r""" Scrape the Schmidt Futures forum learning web page for Education project ideas

    >>> import os
    >>> from qary.constants import DATA_DIR
    >>> url = os.path.join(DATA_DIR, 'corpora', 'web_pages', 'Competition Finalists – Futures Forum.html')

    >>  projects = schmidt_tools(url=url, verbose=False)
    >>  len(projects)
    40
    """
    # url = 'https://futuresforumonlearning.org/competition-finalists/'

    if url.lower().strip().startswith('http'):
        page = requests.get(url).text
    else:
        with open(url) as fin:
            page = fin.read()
    soup = bs4.BeautifulSoup(page, features='lxml')
    finalists = soup.find_all('div', {'class': 'accrod-finalists'})
    if not finalists:
        winners_tabs = soup.find_all('div', {'class': 'comptitation-winner'})
        winners = []
        for div in winners_tabs:
            if div:
                winners.extend(list(
                    div.find_all('div', {'class': 'cata-org'}) or
                    div.find_all('div', {'class': 'mdw'})))
                # ipdb.set_trace()

    if verbose:
        print('# Schmidt Futures Tools Competition Finalists')
        print()
        print('1. [Small](#catalyst-prize-finalists)')
        print('2. [Medium](mid-range-prize-finalists)')
        print('3. [Large](large-prize-finalists)')

    projects = []
    for category in finalists:
        group = category.find('div', {'class': 'wpsm_panel-group'})
        tier = category.find('h3')
        if verbose:
            print()
            print()
            print('## ' + tier.text.strip())
            print()
        panels = group.find_all('div', {'class': 'wpsm_panel'})
        for panel in tqdm(panels):
            heading = panel.find('div', {'class': 'wpsm_panel-heading'})
            title = heading.find('h4', {'class': 'wpsm_panel-title'})
            collapsed = panel.find('div', {'class': 'wpsm_panel-collapse'})
            body = collapsed.find('div', {'class': "wpsm_panel-body"})
            team = body.h4.text.strip()
            paragraphs = [p.text.strip() for p in body.find_all('p')]
            if verbose:
                print('### ' + title.text.strip())
                print()
                print('#### ' + team)
                print()
                for p in paragraphs:
                    print('  ' + p)
                    print()
            projects.append({
                'team': team[5:].strip() if team.lower().startswith('team:') else team,
                'summary': paragraphs,
                'title': title.text.strip(),
                'category': tier.text})

    return projects

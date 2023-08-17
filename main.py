import requests as rq
from bs4 import BeautifulSoup as bs
import time
import re
import json

def find_articles(page):
    url = f'https://www.emerald.com/insight/search?q=%22social+entrepreneurship%22&showAll=true&p={page}'
    response = rq.get(url)
    html_text = response.text
    soup = bs(html_text, 'lxml')
    articles = soup.find_all('div', class_='intent_search_result container card-shadow is-animated Search-item__wrapper')
    def splitline(value):
        return ''.join(value.splitlines())
    for article in articles:
        titles = article.find('div', class_='d-lg-flex flex-row no-gutters')
        title = splitline(titles.text.strip())

        authors_html = article.find('p', class_='my-3 medium font-weight-light')
        authors_text = authors_html.text
        authors_list = [author.strip() for author in re.split(r',|and', authors_text)]
        authors_list = list(filter(None, authors_list))
        authors_stringified = json.dumps(authors_list)

        published = article.find('span', class_='intent_publication_date font-weight-normal')
        published_date = published.text.strip()

        doi_html = article.find('span', class_='intent_doi')
        doi = doi_html.text.strip()

        keyword_list = article.find_all('li', class_='list-inline-item mr-0 small')
        keywords = []
        for keyword in keyword_list:
            words = keyword.find('a')
            keywords.append(words.text)
        keywords_stringified = json.dumps(keywords)

        with open('articles/articles.txt', 'a') as f:
            f.write('{\n')
            f.write(f'"title":"{title}",\n')
            f.write(f'"published_date":"{published_date}",\n')
            f.write(f'"authors": {authors_stringified},\n')
            f.write(f'"keywords": {keywords_stringified},\n')
            f.write(f'"doi":"{doi}"\n')
            f.write('},')
    print('File saved!')

page = 1
if __name__ == '__main__':
    while True:
        find_articles(page)
        time.sleep(180)
        page +=1

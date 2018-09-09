import requests
import sys
from xml.etree import ElementTree


class Article(object):
    def __init__(self, title, date, link):
        self.title = title
        self.date = date
        self.link = link

    def to_html(self):
        return '<li>{} - <a href="{}">{}</a></li>'.format(self.date, self.link, self.title)

    def __str__(self):
        return 'Title: {}\nDate: {}\nLink: {}'.format(self.title, self.date, self.link)


def get_articles(rss_url):
    articles = []
    rss = ElementTree.fromstring(requests.get(rss_url).content)

    for item in rss.iter('item'):
        title = item.find('title').text
        date = item.find('pubDate').text
        link = item.find('link').text

        if title is not None:
            articles.append(Article(title=title, date=date, link=link))

    return articles


def get_articles_from_multiple_urls(rss_urls):
    articles = []
    for rss_url in rss_urls:
        articles += get_articles(rss_url)

    return articles


def articles_to_html(articles):
    lis = [article.to_html() for article in articles]

    return """<html>

    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <title>Awesome site of news</title>
    </head>

    <body>
      <h1>Awesome site of news</h1>
      <ol>
        {}
      </ol>
    </body>

</html>""".format('\n            '.join(lis))


def main():
    articles = get_articles_from_multiple_urls([
        'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'http://www.ynet.co.il/Integration/StoryRss1854.xml',
        'http://rss.walla.co.il/feed/22'
    ])

    for article in articles:
        print(article)

    with open('WebScraper\index.html', 'w') as html_file:
        html_file.write(articles_to_html(articles))


if __name__ == '__main__':
    main()

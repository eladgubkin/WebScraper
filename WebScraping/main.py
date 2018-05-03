from bs4 import BeautifulSoup
import requests
import csv
import sys


class Articles(object):

    def __init__(self, url_list, csv_final_file):
        self.url_list = url_list
        self.csv_final_file = csv_final_file

    def write_to_csv(self):

        csv_file = open(self.csv_final_file, 'w')

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['title', 'date', 'link'])

        for url in self.url_list:

            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')

            for item in soup.find_all('item'):

                title = item.title.text
                print title

                date = item.pubdate.text
                print date

                try:
                    link = item.guid.text
                    print link
                # this except is used by Wallla
                except AttributeError:
                    link = item.description.text[46:83]
                    print link

                print ''

                csv_writer.writerow([title, date, link])

        csv_file.close()


class Webpage(object):

    def __init__(self, main_csv):
        self.main_csv = main_csv

    def write_to_page(self, html_output, data):

            with open(self.main_csv, 'r') as data_file:
                csv_data = csv.DictReader(data_file)

                for line in csv_data:
                    if line['date' or 'title' or 'link'] == '':
                        pass
                    else:
                        data.append('{} - <a href="{}">{}</a>'
                                    .format(line['date'], line['link'], line['title']))

            html_output += '<p> <b>{} articles from 3 sites:<br>' \
                           'NewYorkTimes, Ynet, Walla</b></p>'.format(len(data))

            html_output += '\n<ul>'

            for name in data:
                html_output += '\n\t<li>{}</li>'.format(name)

            html_output += '\n</ul>'

            with open('index.html', 'w') as html_file:
                html_file.write('<head><meta charset="UTF-8">'
                                ' <h1>Awesome site of news</h1> </head>')
                html_file.write(html_output)


def main():
    reload(sys)
    sys.setdefaultencoding("UTF-8")

    url_list = ['http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
                'http://www.ynet.co.il/Integration/StoryRss1854.xml',
                'http://rss.walla.co.il/feed/22']

    csv_final_file = 'Scraping&Writing.csv'

    articles = Articles(url_list, csv_final_file)
    articles.write_to_csv()

    html_output = ''
    data = []

    webpage = Webpage('Scraping&Writing.csv')
    webpage.write_to_page(html_output, data)


if __name__ == '__main__':
    main()

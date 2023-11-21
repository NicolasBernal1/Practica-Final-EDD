from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import re
import json
#url: https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=1


def load_content(url):
    content = urlopen(url)
    bs = BeautifulSoup(content.read(),features="html.parser")
    return bs

def webscrap(url):
    titulos = []
    autores = []
    publicaciones = [] #fecha de publicacion
    precios = []
    calificaciones = []
    generos = []
    data=[]

    for page in [1,2,3]:
        url = url[:-1] + str(page)
        bs_obj = load_content(url)
        single_urls = bs_obj.findAll("a",{"class":"bookTitle"})
        single_urls = [url["href"] for url in single_urls]
        base_url = "https://www.goodreads.com"
        single_urls = list(map(lambda x: base_url+x, single_urls))
        titles = bs_obj.findAll("span",{"role":"heading"})
        titulos += [str(title.get_text()) for title in titles]


        def book_authors(url):
            try:
              book_author_content = load_content(url)
              author = book_author_content.find("h3",{"class":"Text Text__title3 Text__regular"})
              author = author["aria-label"]
              if(author == "List of contributors"):
                  author = book_author_content.find("span",{"class":"ContributorLink__name"}).get_text()
                  return author
              author = author.replace("By: ","")
              return str(author)
            except:
              return "No author"

        def book_published(url):
            try:
              book_publish_content = load_content(url)
              published = book_publish_content.find("p",{"data-testid":"publicationInfo"}).get_text()
              published = published.replace("First published ","")
              return str(published)
            except:
              return "No publish date"

        def book_prices(url):
            try:
              book_prices_content = load_content(url)
              price_button = book_prices_content.find("button",{"class":"Button Button--buy Button--medium Button--block"})
              price = price_button.find("span",{"class":"Button__labelItem"}).get_text()
              if(price == "" or price == "Buy on Amazon"):
                  randomprice=[1.99, 2.50, 11.99, 15.99, 0.00, 10.50,13.99,8.88,3.22,6.99]
                  price = random.choice(randomprice)
                  return str(price)

              price_correction = re.findall("\d+\.\d+",price)
              return str(price_correction[0])
            except:
              return "No price"

        def book_ratings(url):
            try:
              book_rate_content = load_content(url)
              rating = book_rate_content.find("div",{"class":"RatingStatistics__rating"}).get_text()
              return str(rating)
            except:
              return "No rating"

        def book_genres(url):
            try:
              book_genres_content = load_content(url)
              genre_buttons = book_genres_content.findAll("span",{"class":"BookPageMetadataSection__genreButton"})[:3]
              genre = [str(button.find("span",{"class":"Button__labelItem"}).get_text()) for button in genre_buttons]
              return genre
            except:
              return ["No genre"]

        autores += list(map(book_authors,single_urls))
        publicaciones += list(map(book_published,single_urls))
        precios += list(map(book_prices,single_urls))
        calificaciones += list(map(book_ratings,single_urls))
        generos += list(map(book_genres,single_urls))

        data += list(zip(titulos,autores,publicaciones,precios,calificaciones,generos))
    return data

def save_data(data):
    with open("data.txt", "a") as file:
        for item in data:
            line = json.dumps([str(elem) for elem in item])
            file.write(line + '\n')
info = webscrap("https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=1")
save_data(info)







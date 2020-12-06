import os
import shutil
import urllib.request as request
import urllib.parse as parse
from bs4 import BeautifulSoup
from PIL import Image
import getImg
from selenium import webdriver

def get_urllist():
    # Get PDFs of all articles in 'https://www.wxwenku.com'
    core_url = 'https://www.wxwenku.com'
    main_url = 'https://www.wxwenku.com/a/9506?p='
    article_urllist = list()
    idx = 0
    # Get the links of each articles
    while(True):
        idx_url = main_url + str(idx)
        idx_page = request.urlopen(idx_url)
        idx_html = idx_page.read().decode('utf-8')
        idx_soup = BeautifulSoup(idx_html, "html.parser")
        link_list = idx_soup.find_all('h4')
        if len(link_list) <= 1: break
        article_idx_urllist = [link_idx.parent['href'] for link_idx in link_list[1:]]
        article_idx_urllist = [core_url + link_idx for link_idx in article_idx_urllist]
        article_urllist.extend(article_idx_urllist)
        idx += 1
    return article_urllist

if __name__ == '__main__':
    browser = webdriver.Firefox()
    article_urllist = get_urllist()
    if not os.path.exists('tmp'): os.mkdir('tmp')
    if not os.path.exists('pdfs'): os.mkdir('pdfs')
    for i, url in enumerate(article_urllist):
        getImg.Webshot(url, 110, 0, browser, 'tmp')
        img = Image.open(os.path.join('tmp', "shot.png"))
        img.save(os.path.join('pdfs', 'article' + str(i) + '.pdf'))
    shutil.rmtree('tmp')



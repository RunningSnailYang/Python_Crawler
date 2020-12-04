import os
import re
import urllib.request as request
import urllib.parse as parse
from bs4 import BeautifulSoup

def getlist_url_stre(conference):
    '''
    Get CVF paper list by urllib, string methods and regular expressions
    conference: type: string, such as "ICCV2019", "CVPR2020"
    '''
    main_url = 'https://openaccess.thecvf.com'
    # Get responses of the main url
    # type(main_page): http.client.HTTPResponse
    # We can also create request object firstly and then get responses, such as:
    # main_request = request.Request(url = os.path.join(main_url, 'menu'),
    # headers = {'UserAgent':'Mozilla'})
    # main_page = request.urlopen(main_request)
    # main_request will include more information and have the better disguise
    main_page = request.urlopen(os.path.join(main_url, 'menu'))
    # After read(), get object of type 'bytes'. After decode, get string of html
    main_html = main_page.read().decode('utf-8')
    # Get all raw strings of the accessible conferences, such as 'CVPR2020.py'
    # \D: non number, \d: number, {4}: match 4 times
    conference_list = re.findall('\D{4}\d{4}.py', main_html)
    # Post process the the string, such as 'CVPR2020.py' to 'CVPR2020'
    conference_list = [conf[:-3] for conf in conference_list]
    # The inputted conference should be in the conference list
    if conference not in conference_list: raise Exception('The conference is not found')
    # Get responses of the conference url
    conf_page = request.urlopen(os.path.join(main_url, conference))
    conf_html = conf_page.read().decode('utf-8') # Conference html
    paper_raw_list_all, paper_title_list, paper_author_list = list(), list(), list()
    # If the papers of the conference are categorized by date.
    if not 'ptitle' in conf_html:
        # Get the link of the papers in each day
        day_raw_list = re.findall('href=".*?day.*?">', conf_html)
        day_list = [day_raw[6:-2] for day_raw in day_raw_list]
        for day in day_list:
            # Get the information of papers in each day
            day_page = request.urlopen(os.path.join(main_url, day))
            day_html = day_page.read().decode('utf-8')
            paper_raw_list_all.extend(re.findall('<dt class="ptitle">[\s\S]*?</dt>\n<dd>'
                                                 '[\s\S]*?</dd>\n<dd>[\s\S]*?</dd>', day_html))
    else:
        paper_raw_list_all.extend(re.findall('<dt class="ptitle">[\s\S]*?</dt>\n<dd>[\s\S]'
                                             '*?</dd>\n<dd>[\s\S]*?</dd>', conf_html))
    for paper_raw in paper_raw_list_all:
        # Get each paper title
        paper_title = re.search('<dt class="ptitle"><br>.*?.html">(.*?)</a></dt>\n', paper_raw).group(1)
        # Get authors of the paper
        authors = re.findall('submit\(\);">(.*)</a>', paper_raw)
        authors = [author.strip() for author in authors]
        paper_title_list.append(paper_title)
        paper_author_list.append(authors)
    # Title list, authors list
    return paper_title_list, paper_author_list

def getlist_url_strebs(conference):
    '''
    Get CVF paper list by urllib, string methods,  regular expressions and BeautifulSoup
    conference: type: string, such as "ICCV2019", "CVPR2020"
    '''
    main_url = 'https://openaccess.thecvf.com'
    # Get responses of the main url
    # type(main_page): http.client.HTTPResponse
    main_page = request.urlopen(os.path.join(main_url, 'menu'))
    # After read(), get object of type 'bytes'. After decode, get string of html
    main_html = main_page.read().decode('utf-8')
    # Parse main_html into main_soup. type(main_soup): 'bs4.BeautifulSoup'
    main_soup = BeautifulSoup(main_html, "html.parser")
    # Get all raw data of the accessible conferences
    # conference_list: [<dd> CVPR 2020...</dd>, <dd>..., ...]
    # type(conference_list): bs4.element.ResultSet
    # type(conference_list[0]): bs4.element.Tag
    conference_list = main_soup.find_all('dd')
    # Get all accessible conferences
    # conference.get_text().strip(): example: 'CVPR 2020, Virtual [Main Conference]  [Workshops]'
    conference_list = [''.join(re.split('[ ,]', conference.get_text().strip())[:2])
                       for conference in conference_list]
    # The inputted conference should be in the conference list
    if conference not in conference_list: raise Exception('The conference is not found')
    # Get responses of the conference url
    conf_page = request.urlopen(os.path.join(main_url, conference))
    conf_html = conf_page.read().decode('utf-8')  # Conference html
    conf_soup = BeautifulSoup(conf_html, "html.parser")
    paper_title_list, paper_author_list = list(), list()

    # If the papers of the conference are categorized by date.
    if not 'ptitle' in conf_html:
        # Get the link of the papers in each day
        day_raw_list = conf_soup.find_all('dd')
        day_list = [day_raw.find('a')['href'] for day_raw in day_raw_list]
        for day in day_list:
            # Get the information of papers in each day
            day_page = request.urlopen(os.path.join(main_url, day))
            day_html = day_page.read().decode('utf-8')
            day_soup = BeautifulSoup(day_html, "html.parser")
            # Find all elements of the title
            paper_title_day = day_soup.find_all('dt')
            paper_title_day = [paper_title.find('a').get_text() for paper_title in paper_title_day]
            paper_title_list.extend(paper_title_day)
            # Find all elements of the authors
            paper_author_day = day_soup.find_all('dd')
            paper_author_day = [[author.find('input')['value'].strip() for author in paper_author.find_all('form')]
                                for paper_author in paper_author_day
                                if len(paper_author.find_all('form'))]
            paper_author_list.extend(paper_author_day)
    else:
        paper_title_list = conf_soup.find_all('dt')
        paper_title_list = [paper_title.find('a').get_text() for paper_title in paper_title_list]
        paper_author_list = conf_soup.find_all('dd')
        paper_author_list = [[author.find('input')['value'].strip() for author in paper_author.find_all('form')]
                             for paper_author in paper_author_list
                             if len(paper_author.find_all('form'))]
    return paper_title_list, paper_author_list





    
    
    

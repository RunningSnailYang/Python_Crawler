import os
import re
import urllib.request as request
import urllib.parse as parse
from bs4 import BeautifulSoup
import mechanicalsoup

def getlist_from_baidu(conference):
    # Get paper list of the conference by searching on Baidu
    search_engine = 'http://www.baidu.com'
    browser = mechanicalsoup.Browser()
    search_page = browser.get(search_engine) # type(search_page): <Reponse [200]>
    search_soup = search_page.soup # type(search_soup): bs4.BeautifulSoup
    form = search_soup.select('form')[0]
    inputs = form.select('input')
    inputs[-2]['value'] = 'CVF' # Fill the form
    # Submit the filled form and get the new page
    result_page = browser.submit(form, search_page.url)
    result_soup = result_page.soup
    # Get the target search result
    candidate_elements = result_soup.find_all('div')
    target_element = [element for element in candidate_elements
                      if element.has_attr('id') and element['id'] == '1'][0]
    target_url = target_element.find('a')['href']
    main_page = request.urlopen(target_url)
    main_url = main_page.url[:-5]
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






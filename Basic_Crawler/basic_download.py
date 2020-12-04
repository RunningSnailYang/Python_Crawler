import os
import re
import shutil
import urllib.request as request
import urllib.parse as parse
from bs4 import BeautifulSoup

def getpdf_title_url(conference):
    '''
    Get the titles and pdf urls of papers in the conference
    conference: type: string, such as "ICCV2019", "CVPR2020"
    '''
    main_url = 'https://openaccess.thecvf.com'
    # This form is used to disguise the request and provide more information
    main_request = request.Request(url = os.path.join(main_url, 'menu'),
                                   headers = {'UserAgent':'Mozilla'})
    main_page = request.urlopen(main_request)
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
    paper_title_list, paper_pdf_list = list(), list()

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
            # Find all elements of the pdf link
            paper_pdf_day = day_soup.find_all('dd')
            paper_pdf_day = [os.path.join(main_url, paper_pdf.find('a')['href'])
                             for paper_pdf in paper_pdf_day if paper_pdf.find('a').get_text() == 'pdf']

            paper_pdf_list.extend(paper_pdf_day)
    else:
        paper_title_list = conf_soup.find_all('dt')
        paper_title_list = [paper_title.find('a').get_text() for paper_title in paper_title_list]
        paper_pdf_list = conf_soup.find_all('dd')
        paper_pdf_list = [os.path.join(main_url, paper_pdf.find('a')['href'])
                         for paper_pdf in paper_pdf_list if paper_pdf.find('a').get_text() == 'pdf']

    return paper_title_list, paper_pdf_list

def getpdf_url_retrieve(conference):
    '''
    Download all PDFs of papers in this conference with urllib, urllib.request.urlretrive
    conference: type: string, such as "ICCV2019", "CVPR2020"
    '''
    if not os.path.exists(conference): os.mkdir(conference)
    paper_title_list, paper_pdf_list = getpdf_title_url(conference)
    for paper_title, paper_pdf in zip(paper_title_list, paper_pdf_list):
        if '/' in paper_title: paper_title = ' '.join(paper_title.split('/'))
        # paper_pdf: link of the pdf. os.path.join(...): file path and name
        request.urlretrieve(paper_pdf, os.path.join(conference, paper_title + '.pdf'))

def getpdf_url_filewrite(conference):
    '''
    Download all PDFs of papers in this conference with urllib and file writing.
    conference: type: string, such as "ICCV2019", "CVPR2020"
    '''
    if not os.path.exists(conference): os.mkdir(conference)
    paper_title_list, paper_pdf_list = getpdf_title_url(conference)
    for paper_title, paper_pdf in zip(paper_title_list, paper_pdf_list):
        if '/' in paper_title: paper_title = ' '.join(paper_title.split('/'))
        # paper_pdf: link of the pdf. os.path.join(...): file path and name
        file_name = os.path.join(conference, paper_title + '.pdf')
        with open(file_name, 'wb') as out_file, request.urlopen(paper_pdf) as response:
            data = response.read()  # a `bytes` object
            out_file.write(data)

def getpdf_url_shutil(conference):
    '''
    Download all PDFs of papers in this conference with urllib and shutil.
    conference: type: string, such as "ICCV2019", "CVPR2020"
    '''
    if not os.path.exists(conference): os.mkdir(conference)
    paper_title_list, paper_pdf_list = getpdf_title_url(conference)
    for paper_title, paper_pdf in zip(paper_title_list, paper_pdf_list):
        if '/' in paper_title: paper_title = ' '.join(paper_title.split('/'))
        # paper_pdf: link of the pdf. os.path.join(...): file path and name
        file_name = os.path.join(conference, paper_title + '.pdf')
        with open(file_name, 'wb') as out_file, request.urlopen(paper_pdf) as response:
            shutil.copyfileobj(response, out_file)
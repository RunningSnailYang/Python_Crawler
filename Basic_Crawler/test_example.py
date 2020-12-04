import os
from basic_read import *
from basic_download import *
from basic_interect import *

# Test functions in basic_read
def test_basic_read(conference):
    if not os.path.exists('paper_list.txt'): os.mknod('paper_list.txt')
    paper_title_list, paper_author_list = getlist_url_stre(conference)
    # paper_title_list, paper_author_list = getlist_url_strebs(conference)

    with open('paper_list.txt', 'w') as paper_list_file:
        for title, author in zip(paper_title_list, paper_author_list):
            paper_list_file.write(title + '\n')
            paper_list_file.write(', '.join(author) + '\n\n')

# Test functions in basic_download
def test_basic_download(conference):
    getpdf_url_retrieve(conference)
    # getpdf_url_filewrite(conference)
    # getpdf_url_shutil(conference)

# Test functions in basic_interect
def test_basic_interect(conference):
    if not os.path.exists('paper_list.txt'): os.mknod('paper_list.txt')
    paper_title_list, paper_author_list = getlist_from_baidu(conference)

    with open('paper_list.txt', 'w') as paper_list_file:
        for title, author in zip(paper_title_list, paper_author_list):
            paper_list_file.write(title + '\n')
            paper_list_file.write(', '.join(author) + '\n\n')

if __name__ == '__main__':
    conference = 'CVPR2020'
    test_basic_read(conference)
    # test_basic_download(conference)
    # test_basic_interect(conference)


# -*- coding: utf-8 -*-

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from io import StringIO

# from io import StringIO
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfinterp import process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# import re

import pdfplumber
import pandas as pd


def performance(content):
    return


def read_from_pdfplumber(file_path, is_cover=False, is_catalog=False, is_content=False, page_min=None, page_max=None):
    """
    读取pdf文件
    """
    with pdfplumber.open(file_path) as file:
        total_pages = len(file.pages)
        content = ''
        if is_cover:
            content += file.pages[0].extract_text()
            return content
        if is_catalog:
            first_catalog = file.pages[1].extract_text()
            catalog_page_min = int(first_catalog.split('\n')[2].split(' ')[-1])
            catalog_page_max = int(first_catalog.split('\n')[3].split(' ')[-1])
            for i in range(catalog_page_min - 1, catalog_page_max - 1):
                content += file.pages[i].extract_text()
        if is_content:
            for i in range(page_min - 1, page_max):
                content += file.pages[i].extract_text()
        return content

def pdf_analysis(data_path, file_name):
    cover = read_from_pdfplumber('{0}{1}'.format(data_path, file_name), is_cover=True)
    catalog = read_from_pdfplumber('{0}{1}'.format(data_path, file_name), is_catalog=True)
    sector_page = pd.DataFrame(catalog.split('\n')).iloc[3:-3].drop_duplicates()
    sector_page = sector_page[sector_page[0].apply(lambda x: True if len(x.split(' ')) == 2 else False)]
    sector_page['SECTOR_NAME'] = sector_page[0].apply(lambda x: x.split(' ')[0])
    sector_page['PAGE_MIN'] = sector_page[0].apply(lambda x: x.split(' ')[1])
    sector_page = sector_page.set_index('SECTOR_NAME')[['PAGE_MIN']]
    sector_page['PAGE_MAX'] = sector_page['PAGE_MIN'].shift(-1)
    sector_page = sector_page.dropna()
    for sector_name in list(sector_page.index):
        page_min = int(sector_page.loc[sector_name]['PAGE_MIN'])
        page_max = int(sector_page.loc[sector_name]['PAGE_MAX'])
        content = read_from_pdfplumber('{0}{1}'.format(data_path, file_name), is_content=True, page_min=page_min, page_max=page_max)
    return

def test_PyPDF2(data_path, file_name):
    from PyPDF2 import PdfFileReader
    with open('{0}{1}'.format(data_path, file_name), 'rb') as f:
        file = PdfFileReader(f)
        info = file.getDocumentInfo()
        pages = file.getNumPages()
        content = ''
        for page in range(pages):
            content += file.getPage(page).extractText()
    return

def test_pdfrw(data_path, file_name):
    from pdfrw import PdfReader
    file = PdfReader('{0}{1}'.format(data_path, file_name))
    keys = file.keys()
    info = file.Info
    root_keys = file.Root.keys()
    pages = len(file.pages)
    content = ''
    for page in range(pages):
        content += file.pages[page].Contents.stream
    return

def test_pikepdf(data_path, file_name):
    import pikepdf
    with pikepdf.open('{0}{1}'.format(data_path, file_name)) as file:
        info = file.docinfo
        pages = len(file.pages)
        content = ''
        for page in range(pages):
            content += file.pages[page]
    return

def test_pdfminer3k(data_path, file_name):
    output = StringIO()
    with open('{0}{1}'.format(data_path, file_name), 'rb') as f:
        praser = PDFParser(f)
        doc = PDFDocument(praser)
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        pdfrm = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(pdfrm, laparams=laparams)
        interpreter = PDFPageInterpreter(pdfrm, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if hasattr(x, "get_text"):
                    content = x.get_text()
                    output.write(content)
    content = output.getvalue()
    output.close()
    return

def test_pdfplumber(data_path, file_name):
    import pdfplumber
    with pdfplumber.open('{0}{1}'.format(data_path, file_name)) as file:
        pages = len(file.pages)
        content = ''
        for page in range(pages):
            content += file.pages[page].extract_text()
    return

def test_PyMuPDF(data_path, file_name):
    import fitz
    file = fitz.open('{0}{1}'.format(data_path, file_name))
    pages = file.page_count
    metadata = file.metadata
    toc = file.get_toc()
    content = ''
    for page in range(pages):
        page_content = file.load_page(page)
        content += page_content.get_text('text')
    return

if __name__ == '__main__':
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/pdf/'
    file_name = '上海衍复投资管理有限公司_自定义报告_衍复臻选中证1000指数增强一号私募证券投资基金（20220201-20220228）.pdf'
    pdf_analysis(data_path, file_name)

    # test_PyPDF2(data_path, file_name)
    # test_pdfrw(data_path, file_name)
    # test_pikepdf(data_path, file_name)
    # test_pdfminer3k(data_path, file_name)
    test_pdfplumber(data_path, file_name)  # pd.DataFrame(file.pages[4].extract_tables()).T
    # test_PyMuPDF(data_path, file_name)

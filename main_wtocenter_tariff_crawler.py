# -*- coding: utf-8 -*-
import logging

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import config as config
from list_data import Country, HS2code, HS4code
from utils.tools import try_except_log, time_log, args_time_log, logger

logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

data_path = config.DATA_PATH


@args_time_log
def get_data(import_cy, export_cy, hs2code, hs4code):
    Select(browser.find_element_by_name("ctl00$ContentPlaceHolder1$selectImport")).select_by_value(import_cy)
    Select(browser.find_element_by_name("ctl00$ContentPlaceHolder1$selectExport")).select_by_value(export_cy)
    Select(browser.find_element_by_name("ctl00$ContentPlaceHolder1$selectHS2Code")).select_by_value(hs2code)
    Select(browser.find_element_by_name("ctl00$ContentPlaceHolder1$selectHS4Code")).select_by_value(hs4code)

    search = browser.find_element_by_name('ctl00$ContentPlaceHolder1$btn_serarch')
    search.click()

    year, text_ver, hscode, description, ad_valorem_tax, unit_tax, import_cy, export_cy = [], [], [], [], [], [], [], []

    td = browser.find_elements_by_css_selector('td:nth-child(4')
    for i in range(0, len(td)):
        content = browser.find_elements_by_css_selector('td:nth-child(1)')
        year.append(content[i].text)

        content = browser.find_elements_by_css_selector('td:nth-child(2)')
        text_ver.append(content[i].text)

        content = browser.find_elements_by_css_selector('td:nth-child(3)')
        hscode.append(content[i].text)

        content = browser.find_elements_by_css_selector('td:nth-child(4)')
        description.append(content[i].text)

        content = browser.find_elements_by_css_selector('td:nth-child(5)')
        ad_valorem_tax.append(content[i].text)

        content = browser.find_elements_by_css_selector('td:nth-child(6)')
        unit_tax.append(content[i].text)

    df = pd.DataFrame({'year': year, 'text_ver': text_ver, 'HS_code': hscode, 'description': description,
                       'ad_valorem_tax': ad_valorem_tax, 'unit_tax': unit_tax})
    df.insert(loc=0, column='Export', value=import_cy)
    df.insert(loc=1, column='Import', value=export_cy)
    return df


@try_except_log
@time_log
def download_wtocenter_tariff():
    country = Country  # [:2]
    hs2 = HS2code  # [:3]
    hs4 = HS4code  # [:3]

    for in_cy in country:
        df = pd.DataFrame()
        ex_cy = country.copy()
        ex_cy.remove(in_cy)
        for ex in ex_cy:
            for i, j in zip(hs2, hs4):
                temp_df = get_data(in_cy, ex, i, j)
                df = pd.concat([df, temp_df], axis=0)
                # sleep(1)
            df.to_csv('./{output}/{in_cy}_{ex_cy}.csv'.format(output=data_path, in_cy=in_cy, ex_cy=ex),
                      index=False)


if __name__ == '__main__':
    # selenium
    # browser = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = '/opt/google/chrome/google-chrome'
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")

    browser.get("http://db2.wtocenter.org.tw/tariff/Search_byHSCode.aspx/")
    download_wtocenter_tariff()
    browser.close()
    logger.info('*' * 80)

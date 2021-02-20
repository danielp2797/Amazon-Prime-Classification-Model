from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
import numpy as np
import pandas as pd
import random
from tqdm import tqdm # console progress bar

main_url = 'https://www.amazon.co.uk/s?k='
product_name = 'boxing+fighting+gloves'
PATH = 'C:/Program Files (x86)/chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get(main_url + product_name)

found_products = driver.find_elements_by_css_selector('div[data-component-type="s-search-result"]')

pages = driver.find_element_by_css_selector('ul[class="a-pagination"]')
max_page = int(pages.find_element_by_css_selector('li[class="a-disabled"][aria-disabled="true"]').text)

page = 1

print('Scrapping', product_name, 'pages:', max_page, 'estimated number of products:', 60*max_page)
results = []

while (page <= max_page):

    driver.get(main_url + product_name + '&page={}'.format(page))

    for x in tqdm(range(len(found_products))):

        found_products_iter = driver.find_elements_by_css_selector('div[data-component-type="s-search-result"]')

        try:
            WebDriverWait(driver, 10).until(  # it accepts the cookies every time which goes back and forward
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[id="sp-cc-accept"]'))
            ).click()
        except:  # if the cookies button does not exists just pass
            pass

        #----------------- market info -------------------------------------------------------------------

        # sponsored option
        sponsored_option = False
        try:
            found_products_iter[x].find_element_by_css_selector(
                'a[aria-label="View Sponsored information or leave ad feedback"]')
            sponsored_option = True
        except (NoSuchElementException, StaleElementReferenceException):  # if the cookies button does not exists just pass
            pass
        # print(sponsored_option)

        # prime option
        prime_option = False
        try:  # it raises if prime icon is not found

            found_products_iter[x].find_element_by_css_selector(
                'i[class="a-icon a-icon-prime a-icon-medium"][role="img"][aria-label="Amazon Prime"]')
            prime_option = True
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        # print(prime_option)

        try:
            price_rounded = found_products_iter[x].find_element_by_css_selector('span[class="a-price-whole"]').text
        except (NoSuchElementException, StaleElementReferenceException):
            price_rounded = np.nan

        try:
            product_ratings = found_products_iter[x].find_element_by_css_selector('span[class="a-icon-alt"]').get_attribute('innerHTML')
        except (NoSuchElementException, StaleElementReferenceException):
            product_ratings = np.nan

        # product click in order to get detailed info
        found_products_iter[x].find_element_by_css_selector('img[class="s-image"]').click()
        sleep(2)

        # get brand name
        try:  # it raises if the seller brand has not a shop in Amazon
            brand_amazon_shop = driver.find_element_by_css_selector('a[id=bylineInfo]').get_attribute('innerHTML')
        except NoSuchElementException:
            brand_amazon_shop = np.nan

        # get product title, rating and number of ratings
        product_title, product_ratings_number = np.nan, np.nan
        try:
            product_title = driver.find_element_by_css_selector('span[id=productTitle]').get_attribute('innerHTML').strip()
        except:
            pass
        try:
            product_ratings_number = driver.find_element_by_css_selector('span[id=acrCustomerReviewText]').get_attribute(
                'innerHTML')
        except:
            pass

        # number of answered questions
        try:  # it raises if no questions are answered
            answered_questions = driver.find_element_by_css_selector('a[id="askATFLink"][href="#Ask"]')
            answered_questions = answered_questions.find_element_by_tag_name('span').get_attribute('innerHTML')
        except NoSuchElementException:
            answered_questions = 0

        # first data available
        try:  # it raises if no first date available had been provided
            first_date = driver.find_element_by_css_selector('table[id="productDetails_detailBullets_sections1"]')
            first_date = first_date.find_element_by_tag_name('td').get_attribute('innerHTML')
        except NoSuchElementException:
            first_date = np.nan

        # position in ranks
        categories = []

        try: # raises if seller info is not in a table
            category_names = driver.find_element_by_xpath("//*[contains(text(), 'Best Sellers Rank')]").find_element_by_xpath('..').find_elements_by_tag_name('a')
            for elem in category_names:
                categories.append(elem.find_element_by_xpath('..').text)
        except (NoSuchElementException, StaleElementReferenceException): # then information is splitted by the \n char
            try:
                categories = driver.find_element_by_css_selector('li[id="SalesRank"]').text.split('\n')
            except(NoSuchElementException, StaleElementReferenceException): # no info about rank
                categories = []

        results.append((product_title, brand_amazon_shop, product_ratings,
                        product_ratings_number, price_rounded,
                        prime_option, answered_questions, first_date,
                        sponsored_option, categories, x, page))
        driver.back()
        sleep(random.randint(0,3))

    products_data = pd.DataFrame(results,
                                 columns=['title', 'brand', 'rating',
                                          'ratings_number', 'price',
                                          'prime_option', 'answers',
                                          'first_date', 'sponsored_option', 'categories',
                                          'position', 'page'])
    products_data.to_csv('../data/raw/amazon_shop_data_{}.csv'.format(product_name.replace('+', '_')),
                         index=False)

    page += 1  # next page

print('\n', 'Scrapping finished')
driver.close()



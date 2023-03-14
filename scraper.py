import requests
import time
import collections
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

# selenium for interacting with the webpage, being a dynamic one

# handle exceptions
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)


# function to search products on each page
def showProducts():
    pages = 2
    # iteration through pages
    while pages:
        # we search items by their class, card item, which contains all the data we need
        time.sleep(1)
        products = driver.find_elements(By.CLASS_NAME,
                                        "card-item")

        # iterate through all the products present on a page
        for i in products:
            # handle exception if product not found with special label
            try:
                # if element with special label found append it to our list of dictionaries
                if WebDriverWait(driver, 5).until(
                        EC.visibility_of(i.find_element(By.XPATH, ".//span[@class='card-v2-badge-cmp badge commercial-badge']"))).text != "":
                    product_object = {'categorie': i.find_element(By().XPATH,
                                                                  ".//span[@class='card-v2-badge-cmp badge commercial-badge']").text, 'produs': i.get_attribute("data-name"), 'link': i.find_element(By().XPATH,
                                                                                                                                                                                                     ".//a[@class='card-v2-title semibold mrg-btm-xxs js-product-url']").get_attribute("href")}
                    list_of_products.append(product_object)
            except:
                pass
        try:
            # try to get to the second page, if button not found we get out of the function
            productsChangePage = WebDriverWait(driver, 5).until(
                EC.visibility_of(driver.find_element(By.CLASS_NAME, "js-change-page")))
            productsChangePage.click()
            pages = pages-1
        except:
            return
    # if we are on the second page we return to the first one
    driver.back()

# checks if the class exists (for checking if a page is a shop page or it has only a list of products), we are searching for the latter


def check_exists_by_class(classname):
    # handle exceptions
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.CLASS_NAME, "js-products-container")))
    except StaleElementReferenceException:
        return False
    except NoSuchElementException:
        return False
    except TimeoutException:
        return False
    return True


url = "https://www.emag.ro/"

# replace the path of the chrome driver with the path of your chrome driver, or add chrome driver to the path
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(
    'C:ChromeDriver\chromedriver.exe', options=chr_options)

driver.get(url)

driver.maximize_window()

# get a list of all the categories
categories = driver.find_elements(By.CLASS_NAME,
                                  "megamenu-list-department__department-name")

nrCategories = len(categories)

# initialize the list of dicitonaries
list_of_products = []

# we close the accept cookies pop-up and the connect to your account pop-up because it stays in the way of selecting the next page later
try:
    cookie = WebDriverWait(driver, 100).until(
        EC.visibility_of(driver.find_element(By.XPATH, "//button[@class='btn btn-primary js-accept gtm_h76e8zjgoo btn-block']")))
    time.sleep(5)
    cookie.click()
    time.sleep(5)
    # closing the second pop-up might take a bit to close because i wanted to make sure that it appears on the screen
    closeButton = WebDriverWait(driver, 100).until(
        EC.visibility_of(driver.find_element(By.XPATH, "//button[@class='js-dismiss-login-notice-btn dismiss-btn btn btn-link pad-sep-none pad-hrz-none']")))
    time.sleep(5)
    closeButton.click()
except:
    pass


try:
    # itterate through all the categories
    for z in range(1, nrCategories):
        # change the current category after every iteration
        category = WebDriverWait(driver, 5).until(
            EC.visibility_of(categories[z]))

        # hover over the categories so we see the subcategories
        hov = ActionChains(driver).move_to_element(categories[z])
        hov.perform()

        # for every category we only care about the ones that have the special label (ex:'Super Pret' etc.)
        try:
            labels = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//span[@class='label label-danger'] | //span[@class='label label-success']"
                                                     )))
        except TimeoutException:
            categories = driver.find_elements(By.CLASS_NAME,
                                              "megamenu-list-department__department-name")
            labels.clear()
            continue

        n = len(labels)

        # iterate through every labeled subcategory of each category
        for i in range(n):
            flag = 0
            flag2 = 0
            if i != 0:
                ActionChains(driver).move_to_element(
                    categories[z]).perform()
                # time.sleep(5)
                labels = driver.find_elements(By.XPATH,
                                              "//span[@class='label label-danger'] | //span[@class='label label-success']"
                                              )
            # The labeled subcategory "Alege produsul potrivit:Info" is not a link so with the following conditions we avoid it
            if i < n-2:
                k = WebDriverWait(driver, 5).until(
                    EC.visibility_of(labels[i+1]))
                if k.find_element(By.XPATH, '..').text == "Alege produsul potrivit:Info":
                    flag = 1
            elif i == n-2:
                k = WebDriverWait(driver, 5).until(
                    EC.visibility_of(labels[i+1]))
                if k.find_element(By.XPATH, '..').text == "Alege produsul potrivit:Info":
                    flag2 = 1

            # we wait for the label to load and move to it
            j = WebDriverWait(driver, 5).until(
                EC.visibility_of(labels[i]))
            hov = ActionChains(driver).move_to_element(j)

            # if it is a link we click on it
            if j.find_element(By.XPATH, '..').text != "Alege produsul potrivit:Info":
                j.click()
                # check if the page is a list of products
                if check_exists_by_class("js-products-container card-collection list-view-updated show-me-a-grid"):
                    # if it is we search for all the products on the first 2 pages and go back
                    showProducts()
                    driver.back()
                else:
                    driver.back()
                time.sleep(5)

                # if we come back to the page from another one we need to search again for the categories
                categories = driver.find_elements(By.CLASS_NAME,
                                                  "megamenu-list-department__department-name")
            else:
                # we search again for the categories just in case
                categories = driver.find_elements(By.CLASS_NAME,
                                                  "megamenu-list-department__department-name")

            # here we decide what to do if the next element is not a link
            if flag == 1:
                i = i+1
            if flag2 == 1:
                break

        # we find again all the actual categrories and search the previous labeled subcategories (labels)
        categories = driver.find_elements(By.CLASS_NAME,
                                          "megamenu-list-department__department-name")
        labels.clear()
except StaleElementReferenceException:
    pass
except NoSuchElementException:
    pass

# close the webdriver after we are finished itterating
driver.close()


result = collections.defaultdict(list)

# split the initial list with all elements in n lists based on 'categorie'
for d in list_of_products:
    result[d['categorie']].append(d)

result_list = list(result.values())

# print each list of dictionaries based on categorie
for category_list in result_list:
    print(category_list)
    print('\n')

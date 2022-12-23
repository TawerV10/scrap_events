from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import csv

def save_cookie(driver, path):
    with open(path, 'w') as filehandler:
        json.dump(driver.get_cookies(), filehandler)

def load_cookie(path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)

    return cookies

def main():
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        driver.get('https://live.websummit.com')

        time.sleep(1)
        for cookie in load_cookie('cookies.json'):
            driver.add_cookie(cookie)
        time.sleep(1)

        data = []
        count = 1
        while True:
            time.sleep(2)

            try:
                links = driver.find_elements(By.XPATH, "//div[@class='attendee-item directory-item card -link']/a")

                for link in links:
                    url = link.get_attribute('href')
                    if url not in data:
                        driver.execute_script("window.open('');")

                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(url)
                        time.sleep(2)

                        html = driver.page_source
                        soup = BeautifulSoup(html, 'lxml')

                        try:
                            name = soup.find(class_='profile-head__name').text.strip()
                        except:
                            name = ''
                        try:
                            role = soup.find(class_='profile-head__role').text.strip()
                        except:
                            role = ''
                        try:
                            info = soup.find(class_='profile-head__info').text.strip()
                        except:
                            info = ''
                        try:
                            description = soup.find(class_='profile-head__description').text.strip()
                        except:
                            description = ''
                        try:
                            location = soup.find_all(class_='profile-head__summary-item')[0].text.strip()
                        except:
                            location = ''
                        try:
                            industry = soup.find_all(class_='profile-head__summary-item')[1].text.strip()
                        except:
                            industry = ''

                        with open('data.csv', 'a', encoding='utf-8', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([
                                name, role, info, description, location, industry
                            ])

                        print(count, url)
                        count += 1
                        data.append(url)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    else:
                        break
            except:
                continue

            try:
                button = driver.find_elements(By.XPATH, "//button[@class='pagination__button']")[1]
                button.click()
            except:
                break

        # save_cookie(driver, 'cookies.json')

    except Exception as ex:
        print(ex)
    finally:
        driver.stop_client()
        driver.close()
        driver.quit()

if __name__ == '__main__':
    main()
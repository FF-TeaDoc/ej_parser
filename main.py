import bs4
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chromedriver = 'chromedriver'

def create_dict_ej(soup):
    items = soup.find_all('div', {"class", "dnevnik-day"})
    schedule = {}
    for item in items:
        title = item.find('div', {'class', 'dnevnik-day__title'}).text.replace(" ", "").replace("\n", "")
        date = title.split(sep=",")
        dayOfTheWeek = date[0]
        date = date[1]
        lessons = item.find_all('div', {"class", "dnevnik-lesson"})
        schedule[dayOfTheWeek] = {}
        for lesson in lessons:
            try:
                number = int(lesson.find('div', {"class", "dnevnik-lesson__number dnevnik-lesson__number--time"}).text.replace(" ", "").replace("\n", "").replace(".", ''))
                lessonTime = lesson.find('div', {"class", "dnevnik-lesson__time"}).text.split(sep='–')
                lessonStart = lessonTime[0]
                lessonEnd = lessonTime[1]
                subject = lesson.find('span', {"class", "js-rt_licey-dnevnik-subject"}).text
                mark = lesson.find('div', {"class", "dnevnik-lesson__marks js-rt_licey-dnevnik-marks"}).text.replace(" ", "").replace("\n",'')
                homeWork = lesson.find('div', {"class", "dnevnik-lesson__task"})
                if homeWork is not None:
                    homeWork = homeWork.text.replace('\n', '').replace("                                               ", "")
                lessonTheme = lesson.find('span', {"class", "js-rt_licey-dnevnik-topic"})
                if lessonTheme is not None:
                    lessonTheme = lessonTheme.text
                if not mark:
                    mark = None
                schedule[dayOfTheWeek].update(
                    {
                        subject:
                        {
                            'number': number,
                            'lessonStartTime': lessonStart,
                            'lessonEndTime': lessonEnd,
                            'mark': mark,
                            'homeWork': homeWork,
                            'topic': lessonTheme
                            }
                    })
            except Exception as e:
                print(e)
    return schedule

def ej_auth(driver, login, password):
    driver.get("https://school.nso.ru/authorize?return_uri=/journal-app/")
    driver.find_element_by_xpath("//input[@type='text']").send_keys(login)
    driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "dnevnik-day__lessons")))
    html = driver.page_source
    driver.quit()
    soup = bs4.BeautifulSoup(html, features='html.parser')
    dict = create_dict_ej(soup)
    return dict

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chromedriver, options=options)
    now = dt.now()
    dict = ej_auth(driver, 'Логин?', 'Пароль?')
    print(dt.now() - now)
    print(dict)

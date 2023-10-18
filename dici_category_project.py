from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경


category = ['idolmaster_new1','depression_new1','comic_new3','m_entertainer_new1','drama_new3','maplestory_new','bts','lostark','bitcoins_new1','iamsolo']
pages = [1000, 1000, 1000, 1000, 1000, 2000,2000,1000,1000,1000]
df_titles = pd.DataFrame()

#for l in range(0, 6):
for l in range(5,7):
    section_url = 'https://gall.dcinside.com/board/lists/?id={}'.format(category[l])
    titles = []
    # for k in range(1, pages[l] + 1):
    for k in range(1, pages[l]+1):
        url = section_url + '&page={}'.format(k)
        driver.get(url)
        time.sleep(0.5)
        for i in range(4, 51):                                               ######################################################
            try:
                title = driver.find_element('xpath', '//*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[{}]/td[2]/a'.format(i)).text
                title = re.compile('[^가-힣]').sub(' ', title)
                titles.append(title)
            except:
                print('error{} {} {}'.format(l,k,i))

        if k % 10 == 0:
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[l]
            df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
            df_titles.to_csv('D:\work\python\intel_first_team_project\crawling_data\crawling_data_{}_{}.csv'.format(l,k), index=False)
            titles = []

    df_section_title = pd.DataFrame(titles, columns=['titles'])
    df_section_title['category'] = category[l]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
    df_titles.to_csv('D:\work\python\intel_first_team_project\crawling_data\maplestory_bts_crawling_data.csv', index=False)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

driver.close()



# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[4]/td[2]/a
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[5]/td[2]/a
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[6]/td[2]/a
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[7]/td[2]/a[1]
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[8]/td[2]/a
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[9]/td[2]/a[1]
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[10]/td[2]/a[1]
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[11]/td[2]/a[1]
# //*[@id="container"]/section[1]/article[2]/div[2]/table/tbody/tr[51]/td[2]/a[1]
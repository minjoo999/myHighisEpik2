import time
from matplotlib.pyplot import axis #서버와 통신할 때 시간을 지연
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from typing import *

driver = webdriver.Chrome('chromedriver.exe')

# 로그인
driver.get('https://www.genie.co.kr/member/popLogin?page_rfr=https%3A//www.genie.co.kr/')
user_id = driver.find_element(By.ID, "gnb_uxd")
user_id.send_keys("")

user_pw = driver.find_element(By.ID, "gnb_uxx")
user_pw.send_keys("")

login_btn = """//*[@id="f_login_layer"]/input[2]"""
driver.find_element(By.XPATH, login_btn).click()
time.sleep(1)
# print("로그인 완료")

# 인기곡에서 곡정보 & 가사 뽑고 리스트에 각각 넣어서 분류하기 -> pandas로 CSV 파일 만들어 저장하기
# 이후 저장된 CSV로 분석할 예정

# 절차: 인기곡 -> 제목, 앨범명, 참여진 정보 (피쳐링, 작사, 작곡, 편곡) 저장 -> 가사 페이지 넘어가서 저장하기 -> 다 끝나면 다음 페이지 넘겨서 반복
# 1곡당 작업을 함수로 만든 뒤 반복 돌리기


# __annotations__

# 리스트
# 앨범명 추가 필요
title: List = []
featuring: List = []
lyricist: List = []
composer: List = []
producer: List = []
lyrics: List = []
runningtime: List = []
album: List = []

# 에픽하이 인기곡 페이지 접속
driver.get("https://www.genie.co.kr/detail/artistSong?xxnm=14943161")

# 곡정보 리스트별로 저장하기
# 모든 정보를 상세정보에서 뽑기.


def epik_info(n):

    # 상세정보 들어가기
    details = f"""//*[@id="songlist-box"]/div[2]/table/tbody/tr[{n}]/td[4]/a"""
    print("click")
    driver.find_element(By.XPATH, details).click()

    # 제목
    tit = driver.find_element(By.XPATH, """//*[@id="body-content"]/div[2]/div[2]/h2""")
    # print(tit)
    print(tit.text)
    title.append(tit.text)

    # 토글버튼 (있으면 누르기)
    try:
        toggle = """//*[@id="body-content"]/div[2]/div[2]/ul/li[1]/a"""
        print("click")
        driver.find_element(By.XPATH, toggle).click()
        time.sleep(1)
        
    except:
        pass

    # 피쳐링
    # 2부터 시작해서 전원 수집해야 하는데 가능한가...?
    # 끝이 미정인 반복문: while?
    # li[i]가 있으면 append 하고, 없으면 다음으로 넘어가게

    # 여기서 오류는 'len = 0'이 아니라 NoSuchElementException 이었음
    i = 2
    feats = []
    while True:
        try:
            feat = driver.find_element(By.XPATH, f"""//*[@id="artist_etc_layer"]/ul/li[{i}]/a""")
            feats.append(feat.text)
            print(feat.text)
            i = i + 1
        except:
            break

    print(feats)
    featuring.append(feats)
    # 이후 중첩리스트를 flatten으로 풀어주기

    # 재생시간
    runn = driver.find_element(By.XPATH, """//*[@id="body-content"]/div[2]/div[2]/ul/li[4]/span[2]""")
    runningtime.append(runn.text)
    print(runn.text)

    # 앨범명
    alb = driver.find_element(By.XPATH, """//*[@id="body-content"]/div[2]/div[2]/ul/li[2]/span[2]/a""")
    album.append(alb.text)
    print(alb.text)

    # 작사가, 작곡가, 편곡가: 공동작곡은 a[1], a[2] 식이지만 단독작곡은 a로 끝남
    # 없을수도 있음. 셋중 하나만 있거나, 혹은 셋다 없거나.
    # img의 alt 텍스트가 '작곡가', '작사가', '편곡자' 중 무엇인지에 따라 입력하도록 하는게 맞을듯.


    # li[5]부터 시작, li[5]가 작사가, 작곡가, 편곡자? -> 해당사항 따라 넣기
    # 없으면 끝내고 넘어가기

    # 해당 과정을 전부 함수화 하기. 넣는 리스트만 달라지게 하고.

    lyrs = []
    comps = []
    prod = []

    def input_txt(aim, num):
        l = 1
        try:
            while True:
                try:
                    # 공동작업
                    cnt = driver.find_element(By.XPATH, f"""//*[@id="body-content"]/div[2]/div[2]/ul/li[{num}]/span[2]/a[{l}]""")
                    aim.append(cnt.text)
                    print(cnt.text)
                    l = l + 1
                except:
                    num = num + 1
                    # print(num)
                    return num
                    # break
        except:
            # 단독작업
            cnt = driver.find_element(By.XPATH, f"""//*[@id="body-content"]/div[2]/div[2]/ul/li[{num}]/span[2]/a""")
            aim.append(cnt.text)
            print(cnt.text)
            num = num + 1
            print(num)
            return num


    j = 5
    # txt에 해당하는 태그 숫자는 왜 안 바뀌니!! j는 바뀌었는데!!
    while True:
        try:
            txt = driver.find_element(By.XPATH, f"""//*[@id="body-content"]/div[2]/div[2]/ul/li[{j}]/span[1]/img""").get_attribute('alt')
            print(txt)   
            if txt == "작사가":
                input_txt(lyrs, j)
                j = j + 1

            elif txt == "작곡가":
                input_txt(comps, j)
                j = j + 1
            
            elif txt == "편곡자":
                input_txt(prod, j)
                j = j + 1
            
            else:
                print("input 완료")
                break

        except:
            print("input")
            break
    
    lyricist.append(lyrs)
    composer.append(comps)
    producer.append(prod)
    
    # 가사
    # //*[@id="pLyrics"]/p
    lyric = driver.find_element(By.XPATH, """//*[@id="pLyrics"]/p""")
    print(lyric.text)
    lyrics.append(lyric.text)

    # 뒤로가기
    driver.back()

# 2페이지 //*[@id="divListContainer"]/div[2]/a[4]
# 3페이지 //*[@id="divListContainer"]/div[2]/a[5]
# 4페이지 //*[@id="divListContainer"]/div[2]/a[6]
# 1페이지 //*[@id="divListContainer"]/div[2]/a[3]



def one_page(i):
    n = 1
    while True:
        if n < 31:
            if i == 0:
                epik_info(n)
                n = n + 1
            else:
                try:
                    epik_info(n)
                    mybtn = driver.find_element(By.XPATH, f"""//*[@id="divListContainer"]/div[2]/a[{i+3}]""")
                    mybtn.click()
                    time.sleep(0.5)
                    n = n + 1
                except:
                    break
        else:
            nextbtn = driver.find_element(By.XPATH, """//*[@id="divListContainer"]/div[2]/a[13]""")
            nextbtn.click()
            time.sleep(1)
            break


for k in range(10):
    one_page(k)

 
# DataFrame + CSV 가공
dic = {'제목': title, '앨범': album, '피쳐링': featuring, '작사가': lyricist, '작곡가': composer, '편곡자': producer,
        '재생시간': runningtime, '가사': lyrics}
df = pd.DataFrame(dic)
print(df)

df.to_csv('crawling_final.csv', sep=',', index=False)
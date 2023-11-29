import requests
import re
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from pprint import pprint


class Crawl:
    @staticmethod
    def select(day):
        # a = input("차트를 선택하세요. 1.일간(day) 2.주간(week) 3.월간(month)")
        inputs = ''
        try:
            if day == '일간':
                inputs += "day"
            elif day == '주간':
                inputs += "week"
            elif day == '월간':
                inputs += "month"
            else:
                inputs += "잘못된 입력값입니다."
        except Exception as E:
            print(E)
        return inputs

    @staticmethod
    def crawling(day):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        url = f'https://www.melon.com/chart/{Crawl.select(day)}/index.htm'
        req = requests.get(url, headers = header)
        html = req.text
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        parse = BeautifulSoup(html, 'html.parser')
        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        singers = parse.find_all("div", {"class": "ellipsis rank02"})
        albums = parse.find_all("div", {"class": "ellipsis rank03"})
        mvs = parse.select("#tb_list tr div.wrap_song_info a[href*='playSong']")
        likes_first = driver.find_elements_by_xpath('//*[@id="lst50"]/td[8]/div/button/span[2]')
        likes_second = driver.find_elements_by_xpath('//*[@id="lst100"]/td[8]/div/button/span[2]')

        # 좋아요
        like_first = [ele.text for ele in likes_first]
        like_second = [ele.text for ele in likes_second]
        like = like_first + like_second

        # 사진 url 뽑기
        pic = []
        for cnt in range(1, 3):
            if cnt == 1:
                container = parse.select('tr#lst50')
            else:
                container = parse.select('tr#lst100')
            for c in container:
                img = c.select_one('div.wrap > a > img')
                imgSrc = img.attrs["src"]
                pic.append(imgSrc)

        # 뮤직비디오url
        musicvideo = []
        for m in mvs:
            link = m['href']
            matched = re.search(r"(\d+)\)", link)
            song_id = matched.group(1)
            song_url = 'https://www.melon.com/video/detail2.htm?songId={}&menuId=19041201'.format(song_id)
            musicvideo.append(song_url)

        # 랭킹
        lst = []
        for i,j,k,l,m,n in zip(titles, singers, albums, like , musicvideo, pic):
            lst.append((i.find("a").get_text().replace('\'',''), j.find("a").get_text().replace('\'',''), k.find("a").get_text().replace('\'',''), l, m, n))
        pprint(lst)
        return lst

if __name__ == '__main__':
    Crawl().crawling()
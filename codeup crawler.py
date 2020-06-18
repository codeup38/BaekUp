# Codeup OJ Status Crawler
#
#
# Copyright 2020 Github codeup38 All rights reserved.
# https://codeup.kr/userinfo.php?user=kimgihong38
#
#
# 콘텐츠를 허가 없이 크롤링하여 사용하는 것은 불법입니다.
#
# 해당 Crawler Source Code를 활용하여 특정 사이트 크롤링을 하기 전에
# 특정 사이트 운영자에게 허락을 구하고 크롤링 진행을 하기 바랍니다.
#
#

import requests
from bs4 import BeautifulSoup
from modify import modifyData
from tqdm import tqdm
from datetime import datetime as time
from datetime import timedelta

user_agent = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

def DateToEndNum(end):

    inputTime = time(int(end[0:4]),
                     int(end[5:7]),
                     int(end[8:10]))
    
    req = requests.get('https://codeup.kr/status.php', headers = user_agent)
    html = req.text
    result = BeautifulSoup(html, "html.parser")

    submit = result.select (
        'tr > td > a[data-placement="top"]'
        )

    for i in range(len(submit)):
        data = str(submit[i])
        timeString = data[53:72]

        submitNum = result.select (
                'tr > td'
                    )
        
        compareTime = time(int(timeString[0:4]),
                           int(timeString[5:7]),
                           int(timeString[8:10]))
        
        if (inputTime-compareTime).days  == 0:
            return eval(submitNum[i*9])
        
    url = str(eval(submitNum[90].text)-1)

    while True:

        req = requests.get('https://codeup.kr/status.php?&top='+url, headers = user_agent)
        html = req.text
        result = BeautifulSoup(html, "html.parser")
        
        intUrl = eval(url)
    
        submit = result.select (
        'tr > td > a[data-placement="top"]'
            )
        submitNum = result.select (
                    'tr > td'
            )
        
        for i in range(len(submit)):
            data = str(submit[i])
            timeString = data[53:72]
        
            compareTime = time(int(timeString[0:4]),
                               int(timeString[5:7]),
                               int(timeString[8:10]))

            
            #if (inputTime-compareTime).days  >= -1:
            #print(inputTime, compareTime)
            print(submitNum[i*9].text)
                
            if (inputTime-compareTime).days  == 0:
                return eval(submitNum[i*9].text)

        intUrl-=20
        url = str(intUrl)
    
def main():

    

    start = input('시작 날짜 xxxx-xx-xx 형식으로 입력')
    end = input('종료 날짜 xxxx-xx-xx 형식으로 입력')

    endNum = DateToEndNum(end)

    print(endNum)
    return
    startNum = DateToStartNum()


if __name__ == '__main__':
    main()

import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

def latestSubmit() :

    user_agent = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    req = requests.get('https://www.acmicpc.net/status', headers = user_agent)
    html = req.text
    result = BeautifulSoup(html, "html.parser")

    submit_number = result.select(
        'tr > td'
    )
    submit_date = result.select(
        'tr > td > a[data-placement="top"]'
    )

    return submit_number[0].text, str(submit_date[0])[130:154]

def findEndSubmitNumber(latestSubmitNumber, endYear, endMonth, endDay) :

    user_agent = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    url = int(latestSubmitNumber)
    while True :
        req = requests.get('https://www.acmicpc.net/status?top=%d' %(url), headers = user_agent)
        html = req.text
        result = BeautifulSoup(html, "html.parser")

        submit_date = result.select(
            'tr > td > a[data-placement="top"]'
        )

        lastCurDate = str(submit_date[19])[130:154].split()
        lastCurYear = lastCurDate[0].split('년')
        lastCurMonth = lastCurDate[1].split('월')
        lastCurDay = lastCurDate[2].split('일')

        if(lastCurYear[0] == endYear and lastCurMonth[0] == endMonth and lastCurDay[0] == endDay) :
            for i in range(0,20,1) : 
                curDate = str(submit_date[i])[130:154].split()
                curYear = curDate[0].split('년')
                curMonth = curDate[1].split('월')
                curDay = curDate[2].split('일')
                if(curYear[0] == endYear and curMonth[0] == endMonth and curDay[0] == endDay) :
                    submit_number = result.select(
                        'tr > td'
                    )
                    endSubmitNumber = submit_number[i*9].text
                    return endSubmitNumber, str(submit_date[i])[130:154]
        else :
            url -= 20
            continue

def pageCrawling(file, result) :

    dataByCrawling = result.select(
        'tr > td'
    )

    for i in range(0,180,1) :
        if(i%9 == 0 and i != 0) :
            file.write('\n')
        
        if(dataByCrawling[i].text == '') :
            file.write('공백')
        else :
            noSpace = re.sub('&nbsp;', '', dataByCrawling[i].text)
            file.write(noSpace)
        file.write(' ')

def indexCrawling(index, file, result) :

    dataByCrawling = result.select(
        'tr > td'
    )

    for i in range(0,index*9,1) :
        if(i%9 == 0 and i != 0) :
            file.write('\n')
        
        if(dataByCrawling[i].text == '') :
            file.write('공백')
        else :
            noSpace = re.sub('&nbsp;', '', dataByCrawling[i].text)
            file.write(noSpace)
        file.write(' ')


def main() :

    user_agent = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    latestSubmitCheck = input(' 가장 최근에 제출된 제출 번호와 날짜를 알고 싶다면 \
1을 입력하세요.\n 원하지 않으면 0을 입력해주세요.\n: ')

    if latestSubmitCheck == '1' :
        latestSubmitNumber, latestSubmitDate = latestSubmit()
        print('문제 번호 : %s, 날짜 : %s' %(latestSubmitNumber, latestSubmitDate))

    stYear, stMonth, stDay = input(' 크롤링 할 시작 날짜(연도, 월, 일)을 \'-\' 로 분리하여 입력하시오 \n: ').split('-')
    endYear, endMonth, endDay = input(' 크롤링 할 마지막 날짜(연도, 월, 일)을 \'-\' 로 분리하여 입력하시오 \n: ').split('-')

    print('\n\n 크롤링을 시작합니다.\n\n 개수에 따라 시간이 다소 걸릴수 \
있습니다.')

    # 마지막 날짜를 통해, 마지막 제출번호 구하기
    endSubmitNumber, endDate = findEndSubmitNumber(latestSubmitNumber, endYear, endMonth, endDay)
    print('\n\n 마지막 제출 번호 : %s 시간 : %s 부터 시작 날짜까지 크롤링을 시작합니다.....' %(endSubmitNumber, endDate))

    # 마지막 제출번호부터 시작 날짜까지 크롤링하기
    file = open("data_origin_BaekJoon.txt",'w+', -1, "utf-8")

    url = int(endSubmitNumber)
    crawlingFinish = False

    while True :
        req = requests.get('https://www.acmicpc.net/status?top=%d' %(url), headers = user_agent)
        html = req.text
        result = BeautifulSoup(html, "html.parser")

        submit_date = result.select(
            'tr > td > a[data-placement="top"]'
        )

        lastCurDate = str(submit_date[19])[130:154].split()
        lastCurYear = lastCurDate[0].split('년')
        lastCurMonth = lastCurDate[1].split('월')
        lastCurDay = lastCurDate[2].split('일')
 
        if(int(lastCurYear[0]) > int(stYear)) :
            # 페이지 크롤링
            pageCrawling(file, result)

        elif(int(lastCurYear[0]) == int(stYear)) :
            if(int(lastCurMonth[0]) > int(stMonth)) :
                # 페이지 크롤링
                pageCrawling(file, result)

            elif(int(lastCurMonth[0]) == int(stMonth)) :
                if(int(lastCurDay[0]) >= int(stDay)) :
                    # 페이지 크롤링
                    pageCrawling(file, result)

                else :
                    # 해당 페이지 크롤링 후 break
                    for i in range(0,20,1) :
                        curDate = str(submit_date[i])[130:154].split()
                        curDay = curDate[2].split('일')

                        if(int(curDay[0]) < int(stDay)) :
                            indexCrawling(i, file, result)
                            crawlingFinish = True
                            break
            else :
                # 해당 페이지 크롤링 후 break
                for i in range(0,20,1) :
                    curDate = str(submit_date[i])[130:154].split()
                    curMonth = curDate[1].split('월')

                    if(int(curMonth[0]) < int(stMonth)) :
                        indexCrawling(i, file, result)
                        crawlingFinish = True
                        break
        else :
            # 해당 페이지 크롤링 후 break
            for i in range(0,20,1) :
                curDate = str(submit_date[i])[130:154].split()
                curYear = curDate[0].split('년')

                if(int(curYear[0]) < int(stYear)) :
                    indexCrawling(i, file, result)
                    crawlingFinish = True
                    break
        
        if(crawlingFinish) :
            break
        
        file.write('\n')
        url -= 20
    
    file.close()

    print('\n\n==========Done!==========')
    input('Press Any Key ')
    return 0

if __name__ == '__main__' :
    main()

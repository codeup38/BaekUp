import requests
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

        # firstCurDate = str(submit_date[0])[130:154].split()
        # firstCurYear = firstCurDate[0].split('년')
        # firstCurMonth = firstCurDate[1].split('월')
        # firstCurDay = firstCurDate[2].split('일')
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
                    return endSubmitNumber, url
        else :
            url -= 20
            continue

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

    # 시작, 마지막 날짜를 통해 시작, 마지막 제출번호 값 저장
    endSubmitNumber, endUrl = findEndSubmitNumber(latestSubmitNumber, endYear, endMonth, endDay)
    print(endSubmitNumber, endUrl)


if __name__ == '__main__' :
    main()
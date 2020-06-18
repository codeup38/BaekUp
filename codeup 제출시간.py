import requests
from bs4 import BeautifulSoup

user_agent = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

req = requests.get('https://codeup.kr/status.php', headers = user_agent)
html = req.text
result = BeautifulSoup(html, "html.parser")

submit = result.select (
    'tr > td > a[data-placement="top"]'
    )

for i in range(len(submit)):
    data = str(submit[i])
    timeString = data[53:72]
    year = timeString[0:4]
    month = timeString[5:7]
    date = timeString[8:10]
    print("년도 : " + year + " 월 : " + month + " 일 : "  + date)

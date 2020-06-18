import requests
from bs4 import BeautifulSoup

user_agent = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

req = requests.get('https://codeup.kr/status.php', headers = user_agent)
html = req.text
result = BeautifulSoup(html, "html.parser")

submit = result.select (
    'a'
    )

for i in range(len(submit)):
    print(submit[i], '\n')

    print('hi')

from bs4 import BeautifulSoup
import json
import requests
from fake_headers import Headers

#html = open('index.html', encoding='utf-8').read()
HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
headers = Headers(browser="firefox", os="win").generate()
html = requests.get(HOST, headers=headers).text
soup = BeautifulSoup(html, 'lxml')
job_list = soup.find_all('div', {'class': 'serp-item'})
job_list_full = []
def new_vacancies_SPB_Moscow():
    for i in job_list:
        link = i.find('a')['href']
        city = i.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
        salary = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        company = i.find('a', {'data-qa': "vacancy-serp__vacancy-employer"})
        description = i.find('div', {'class': 'g-user-content'})
        if salary is None:
            pass
        else:
            salary = salary.text
        job_list_full.append({
            'link': link,
            'salary': salary,
            'company': company.text,
            'city': city.text,
            'description': description.text
        })
    return job_list_full
print(new_vacancies_SPB_Moscow())


def django_flask_vacancies():
    filtered_list = []
    for item in job_list_full:
        if ('Django' in list(item.values())[4]) or ('Flask' in list(item.values())[4]):
            filtered_list.append(item)
    x = json.dumps(filtered_list)
    return x
print(django_flask_vacancies())

with open("data.json", 'w') as file:
    json.dump(django_flask_vacancies(), file, ensure_ascii=False, indent=4)

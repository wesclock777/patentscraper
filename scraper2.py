import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

patentnums = []
datesfiled = []
descs = []
assignees = []

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

for num in range(1,38):
    page= requests.get('http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r='+str(num)+'&f=G&l=50&d=PTXT&p=1&S1=(%22rofin-sinar%22.ASNM.)&OS=AN/%22rofin-sinar%22&RS=AN/%22rofin-sinar%22', headers=headers,verify=False)
    if page.status_code==200:
        soup = BeautifulSoup(page.content, 'html.parser')
        desc = soup.find('font', size="+1")
        if(desc.get_text()!=None):
            descs.append(desc.get_text())
            print(num,":",desc.get_text())
        else:
            descs.append("No title found")
            print("ERROR NO TITLE FOUND")
        title = soup.find('title')
        number = title.get_text().split()[3]
        patentnums.append(number)

        tables = soup.find_all('tr')
        for row in tables:
            if(row.find('th',text=re.compile('^File'))!=None):
                datefiled = row.find('td').find('b')
                datefiled = datefiled.get_text()
                datesfiled.append(datefiled)
                break

        tables = soup.find_all('tr')
        for row in tables:
            if(row.find('th',text=re.compile('^Assignee'))!=None):
                datefiled = row.find('td').find('b')
                assignee = datefiled.get_text()
                assignees.append(assignee)
                break

patents2 = pd.DataFrame({
    "patent number": patentnums,
    "date filed" : datesfiled,
    "patent title" : descs,
    "assignees" : assignees

})

patents2.to_csv('patents-rofin-sinar.csv')

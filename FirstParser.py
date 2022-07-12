# -*- coding: utf-8 -*-
"""
Sextant mods parser: result -> xlsx (id_sextant, mod, (int)weight)
Created on Fri Aug  7 22:43:43 2020
Parser #1: poedb.tw
@author: Ryze
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_table(table):#Функция разбора таблицы с вопросом
    res = pd.DataFrame()
    id_sextant = 0
    mod_description = ''
    mod_weight = ''
    if len(table.find_all('td')) != 0: # пропуск th - table head
        if table.find_all('td')[0].get_text() == "Simple Sextant":
            id_sextant = 1
        elif table.find_all('td')[0].get_text() == "Prime Sextant" :
            id_sextant = 2
        else:
            id_sextant = 3        
        ModDescriptionContent = table.find_all('td')[2].contents       
        #print(ModDescriptionContent)
        for i in range(3, len(ModDescriptionContent)):
            if ModDescriptionContent[i].name == 'br':
                mod_description += '\n'
            else:
                mod_description += ModDescriptionContent[i].string
        # t_html = table.find('td').prettify()           # str
        # t_length = len(table.find_all('td'))             # 4
        # t_3_html = table.find_all('td')[3].prettify()    # str
        # t_3_array = table.find_all('td')[3].contents
        # t_3_array_0_html = table.find_all('td')[3].contents[0].prettify()
        # t_3_array_0_tag = table.find_all('td')[3].contents[0].name
        # t_3_array_0_text = table.find_all('td')[3].contents[0].string
        for child in table.find_all('td')[3].contents[0].children:
            if child.find(' 0') == -1:
                mod_weight = int(child.replace('default ', ''))
            
        ### print parsed content
        # print(id_sextant)
        # print(mod_description)
        # print(mod_weight)
        
        # question_tr=table.find('tr',{'class': 'question'})
        # #Получаем сам вопрос
        # question=question_tr.find_all('td')[1].find('div').text.replace('<br />','\n').strip()
        
        # widget_info=question_tr.find_all('div', {'class':'widget__info'})
        # #Получаем ссылку на сам вопрос
        # link_question='https://www.banki.ru'+widget_info[0].find('a').get('href').strip()
        # #Получаем уникальным номер вопроса
        # id_question=link_question.split('=')[1]
    
        # #Получаем того кто задал вопрос
        # who_asked=widget_info[1].find('a').text.strip()
        # #Получаем ссылку на профиль
        # who_asked_link='https://www.banki.ru'+widget_info[1].find('a').get('href').strip()
        # #Получаем уникальный номер профиля
        # who_asked_id=widget_info[1].find('a').get('href').strip().split('=')[1]
    
        # #Получаем из какого города вопрос
        # who_asked_city=widget_info[1].text.split('(')[1].split(')')[0].strip()
        
        # #Получаем дату вопроса
        # date_question=widget_info[1].text.split('(')[1].split(')')[1].strip()
        
        # #Получаем ответ если он есть сохраняем
        # answer_tr=table.find('tr',{'class': 'answer'})
        # if(answer_tr!=None):
        #     answer=answer_tr.find_all('td')[1].find('div').text.replace('<br />','\n').strip() 
        
        #Пишем в таблицу и возвращаем
        res=res.append(pd.DataFrame([[id_sextant, mod_description, mod_weight]], columns = ['Sextant ID','Mod','Weight']), ignore_index=True)
        #print(res)
    return(res) 
#   print(soup.find_all('td')[0])
#   <td>
#       <a class="item_currency" data-hover="?t=item&amp;
#       n=Simple+Sextant" href="/us/Simple_Sextant">
#            <img height="16" src="https://web.poecdn.com/image/Art/2DItems
#            /Currency/AtlasRadiusTier1.png?scale=1&amp;w=1&amp;h=1"/>
#            Simple Sextant
#        </a>
#   </td>
#   print(soup.find_all('td')[0].strings)   #generator object
#   print(soup.find_all('td')[0].string)    #None
#   print(soup.find_all('td')[0].child)     #None
#   print(soup.find_all('td')[0].get_text())#'Simple sextant'
#   print(soup.find_all('td')[0].contents)  #<a...>Simple sextants</a>
#   print(soup.find_all('td')[0].descendants)#generator object
   
url = 'https://poedb.tw/us/mod.php?type=Sextant'
r = requests.get(url)
with open('pars.html', 'w', encoding='utf-8') as output_file:
    output_file.write(r.text)
result = pd.DataFrame()
soup = BeautifulSoup(r.text, features="lxml") #Отправляем полученную страницу в библиотеку для парсинга
tables=soup.find_all('tr') #Получаем все таблицы с вопросами


for item in tables:
    res=parse_table(item)
    result=result.append(res, ignore_index=True)

result.to_excel('result.xlsx')
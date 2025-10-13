import requests
import webbrowser
import json
from requests.exceptions import RequestException


def request_(user_request: str):
    try:
        url = f'https://ru.wikipedia.org/w/api.php?action=query&list=search&utf8=&format=json&srsearch="{user_request}"'

        headers = {
            'User-Agent': "MyApp/1.0 (https://example.com/; anem650@gmail.com)"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.json()
        return result
    
    except requests.RequestException as e:
        print(f'Ошибка при выполнении запроса: {e}')
        return None

    except json.JSONDecodeError as e:
        print(f'Ошибка при разборе JSON: {e}')
        return None
    

def article_process(articles: list[dict]):
    print('\nНайденные статьи:\n Для выхода, введите 0')
    index: int = 1
    for article in articles:
        for article_title in article:
            print(f'{index} - {article_title}')
            index += 1

    chosen_article_index: str = input('Введите номер: ')
    if chosen_article_index == '0':
        return main()
    
    if not chosen_article_index.isdigit() or not (1 <= int(chosen_article_index) <= 10):
        print('Некорректный ввод')  
        return article_process(articles) 
    else:
        for title in articles[int(chosen_article_index) - 1].keys():
            pageid = articles[int(chosen_article_index) - 1][title]
        webbrowser.open(f'https://ru.wikipedia.org/w/index.php?curid={pageid}')
        return article_process(articles)

def process(result: list[dict]):
    articles: list[dict] = []

    if len(result) == 0:
        return 'Ваш запрос не дал результатов'
    else:
        for article in result:
            articles.append({article['title']: article['pageid']})
        
    print(article_process(articles))


def main():
    user_request = input("\nВведите ваш запрос (для выхода введите 0) : ")

    while user_request != '0': 

        result = request_(user_request)
        if not (result == None):
            result = result['query']['search']
            print(process(result))
            user_request = input("\nВведите ваш запрос (для выхода введите 0) : ")

    return 'До свидания'

print(main())
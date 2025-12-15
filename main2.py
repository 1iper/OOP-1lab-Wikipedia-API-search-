import requests
import webbrowser
import json
from requests.exceptions import RequestException
from typing import List, Dict, Optional


class WikipediaSearcher:
    
    BASE_URL = "https://ru.wikipedia.org/w/api.php"
    
    def __init__(self, user_agent: str = "MyApp/1.0"):

        self.user_agent = user_agent
        self.headers = {'User-Agent': user_agent}
        
    def search_articles(self, query: str) -> Optional[Dict]:
       
        try:
            params = {
                'action': 'query',
                'list': 'search',
                'utf8': '',
                'format': 'json',
                'srsearch': f'"{query}"'
            }
            
            response = requests.get(
                self.BASE_URL, 
                headers=self.headers, 
                params=params
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f'Ошибка при выполнении запроса: {e}')
            return None
            
        except json.JSONDecodeError as e:
            print(f'Ошибка при разборе JSON: {e}')
            return None


class ArticleProcessor:
    
    def __init__(self, max_articles: int = 10):
        self.max_articles = max_articles
        
    def process_search_results(self, search_results: Dict) -> List[Dict[str, int]]:

        if not search_results:
            return []
            
        articles = search_results.get('query', {}).get('search', [])        
        if not articles:
            return []
            
        processed_articles = []
        for article in articles[:self.max_articles]:
            processed_articles.append({
                article['title']: article['pageid']
            })
            
        return processed_articles
    
    def display_articles(self, articles: List[Dict[str, int]]) -> Optional[str]:

        if not articles:
            print("Ваш запрос не дал результатов")
            return None
            
        print('\nНайденные статьи:\n(Для выхода введите 0)')
        
        for index, article in enumerate(articles, 1):
            title = list(article.keys())[0]
            print(f'{index} - {title}')
        
        return self._get_user_choice(articles)
    
    def _get_user_choice(self, articles: List[Dict[str, int]]) -> Optional[str]:

        while True:
            choice = input('\nВведите номер статьи: ').strip()
            
            if choice == '0':
                return None
                
            if not choice.isdigit():
                print('Пожалуйста, введите число')
                continue
                
            choice_num = int(choice)
            
            if not (1 <= choice_num <= len(articles)):
                print(f'Пожалуйста, введите число от 1 до {len(articles)}')
                continue
                
            selected_article = articles[choice_num - 1]
            article_title = list(selected_article.keys())[0]
            page_id = selected_article[article_title]
            
            return article_title, page_id


class WikipediaBrowser:
    
    def __init__(self):
        self.searcher = WikipediaSearcher()
        self.processor = ArticleProcessor()
        self.running = False
        
    def open_article(self, article_info: tuple) -> None:

        if not article_info:
            return
            
        title, page_id = article_info
        url = f'https://ru.wikipedia.org/w/index.php?curid={page_id}'
        print(f'\nОткрываю статью: "{title}"')
        webbrowser.open(url)
    
    def run_search_cycle(self) -> None:

        while True:
            user_request = input("\nВведите ваш запрос (для выхода введите 0): ").strip()
            
            if user_request == '0':
                print("До свидания!")
                break
                
            if not user_request:
                print("Запрос не может быть пустым")
                continue
                
            # Поиск статей
            search_results = self.searcher.search_articles(user_request)
            
            if search_results is None:
                print("Произошла ошибка при поиске")
                continue
            
            # Обработка результатов
            articles = self.processor.process_search_results(search_results)
            
            # Отображение и выбор статьи
            article_info = self.processor.display_articles(articles)
            
            # Открытие выбранной статьи
            if article_info:
                self.open_article(article_info)
    
    def start(self) -> None:
        print("=== Wikipedia Browser ===")
        self.running = True
        self.run_search_cycle()


def main():
    app = WikipediaBrowser()
    app.start()


if __name__ == "__main__":
    main()
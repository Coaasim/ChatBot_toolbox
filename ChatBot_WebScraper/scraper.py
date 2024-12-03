import requests
from bs4 import BeautifulSoup

def get_latest_news(topic):
    # Example: Scraping BBC News for simplicity
    url = f"https://www.bbc.com/search?q={topic}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Sorry, I couldn't fetch the news at the moment."

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='css-8tq3w8-Stack e1y4nx260')

    news_list = []
    for article in articles[:5]:  # Get top 5 articles
        title = article.find('h1').get_text() if article.find('h1') else "No Title"
        link = article.find('a')['href'] if article.find('a') else "#"
        news_list.append({'title': title, 'link': link})

    if not news_list:
        return "No news found for your query."

    return news_list

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_github_trends():
    url = "https://github.com/trending"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    trends = []
    for repo in soup.select('article.Box-row'):
        repo_data = {
            'name': repo.select_one('h2 a').text.strip(),
            'url': f"https://github.com{repo.select_one('h2 a')['href']}",
            'description': repo.select_one('p').text.strip() if repo.select_one('p') else '',
            'stars': repo.select('a.Link--muted')[0].text.strip(),
            'forks': repo.select('a.Link--muted')[1].text.strip(),
            'language': repo.select_one('span[itemprop="programmingLanguage"]').text.strip() 
                        if repo.select_one('span[itemprop="programmingLanguage"]') else 'N/A',
            'scraped_at': datetime.now().isoformat()
        }
        trends.append(repo_data)
    
    with open('trending_repos.json', 'w') as f:
        json.dump(trends, f, indent=2)
    
    print(f"✅ Scraped {len(trends)} trending repos")

if __name__ == "__main__":
    scrape_github_trends()

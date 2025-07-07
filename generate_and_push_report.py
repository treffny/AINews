import os
import subprocess
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_web_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_news_from_sciencedaily(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    news_items = []
    articles = soup.find_all("div", class_="latest-news-item") + \
               soup.find_all("div", class_="card") + \
               soup.find_all("li", class_="list-group-item")
    for article in articles:
        title_tag = article.find("a", class_="latest-head") or \
                    article.find("a", class_="card-title") or \
                    article.find("a") # General search for any link within the article
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            if link and not link.startswith("http"):
                link = "https://www.sciencedaily.com" + link
            if title and link:
                news_items.append({"title": title, "link": link})
    return news_items

def extract_news_from_techcrunch(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    news_items = []
    articles = soup.find_all('div', class_='post-block')
    for article in articles:
        title_tag = article.find('h2', class_='post-block__title').find('a')
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
            news_items.append({'title': title, 'link': link})
    return news_items

def extract_news_from_defense_gov(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    news_items = []
    articles = soup.find_all('div', class_='listing-item')
    for article in articles:
        title_tag = article.find('h3', class_='listing-item__title').find('a')
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = 'https://www.defense.gov' + title_tag['href']
            news_items.append({'title': title, 'link': link})
    return news_items

def extract_news_from_ibm(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    news_items = []
    articles = soup.find_all('div', class_='article-card__content')
    for article in articles:
        title_tag = article.find('h3', class_='article-card__title').find('a')
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = 'https://www.ibm.com' + title_tag['href']
            news_items.append({'title': title, 'link': link})
    return news_items

def generate_report_content():
    today_date = datetime.now().strftime("%B %d, %Y")
    report_points = []
    references = []
    ref_count = 1

    # --- General AI News ---
    general_news_sources = [
        ("https://www.sciencedaily.com/news/computers_math/artificial_intelligence/", extract_news_from_sciencedaily),
        ("https://techcrunch.com/category/artificial-intelligence/", extract_news_from_techcrunch),
    ]

    for url, extractor in general_news_sources:
        html = get_web_content(url)
        if html:
            news = extractor(html)
            for item in news[:3]: # Get top 3 from each general source
                report_points.append(f"*   **{item['title']}**: (Source: {url.split('/')[2]}) [Ref{ref_count}]")
                references.append(f"[Ref{ref_count}] {item['link']}")
                ref_count += 1

    # --- AI in Defense and Security ---
    defense_security_sources = [
        ("https://www.defense.gov/Spotlights/Artificial-Intelligence/", extract_news_from_defense_gov),
        ("https://www.ibm.com/think/topics/ai-security", extract_news_from_ibm),
    ]

    for url, extractor in defense_security_sources:
        html = get_web_content(url)
        if html:
            news = extractor(html)
            for item in news[:3]: # Get top 3 from each defense/security source
                report_points.append(f"*   **{item['title']}**: (Source: {url.split('/')[2]}) [Ref{ref_count}]")
                references.append(f"[Ref{ref_count}] {item['link']}")
                ref_count += 1

    # --- Construct the report ---
    report_text = f"""## Date: {today_date}\n\n### General AI News\n\n"""
    if not report_points:
        report_text += "*   No new AI news found today. Please check back later.\n"
    else:
        general_news = [p for p in report_points if "defense.gov" not in p and "ibm.com" not in p]
        defense_security_news = [p for p in report_points if "defense.gov" in p or "ibm.com" in p]

        # Add general news (up to 5 points)
        if general_news:
            for point in general_news[:5]:
                report_text += f"{point}\n"
        else:
            report_text += "*   No general AI news found today.\n"

        report_text += f"\n### AI in Defense and Security\n\n"
        # Add defense/security news (up to 5 points)
        if defense_security_news:
            for point in defense_security_news[:5]:
                report_text += f"{point}\n"
        else:
            report_text += "*   No AI in Defense and Security news found today.\n"

    report_text += f"\n### Important Tools and Innovations\n\n*   **No specific new tools or innovations identified today.** (This section can be expanded with more targeted searches if needed.)\n\n## References\n\n"""
    for ref in references:
        report_text += f"{ref}\n"

    return report_text

def update_github_repo(repo_path, file_name, commit_message):
    os.chdir(repo_path)

    # Add the updated file
    subprocess.run(["git", "add", file_name], check=True)

    # Commit the changes
    subprocess.run(["git", "commit", "-m", commit_message], check=True)

    # Push to GitHub (requires prior authentication setup, e.g., PAT)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your local Git repository
    # This script assumes it's run from the root of your cloned GitHub repository.
    github_repo_path = os.getcwd() # Assumes the script is run from the repo root

    report_file_name = "daily_ai_news_report.md"
    commit_msg = "Daily AI News Report Update"

    # Generate the new report content
    new_report_content = generate_report_content()

    # Write the new content to the Markdown file
    with open(report_file_name, "w") as f:
        f.write(new_report_content)

    print(f"'{report_file_name}' updated with new content.")

    try:
        # Update and push to GitHub
        update_github_repo(github_repo_path, report_file_name, commit_msg)
        print("Report successfully committed and pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating GitHub repository: {e}")
        print("Please ensure Git is configured and you have push access to the repository.")
        print("You might need to set up a Personal Access Token (PAT) for authentication.")




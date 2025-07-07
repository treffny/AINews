import requests

try:
    response = requests.get("https://www.sciencedaily.com/news/computers_math/artificial_intelligence/", timeout=10)
    response.raise_for_status()
    with open("sciencedaily_content.html", "w") as f:
        f.write(response.text)
    print("ScienceDaily content fetched successfully.")
except requests.exceptions.RequestException as e:
    print(f"Error fetching ScienceDaily content: {e}")



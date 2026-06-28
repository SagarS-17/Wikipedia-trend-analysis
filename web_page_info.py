import csv
import pandas
from datetime import datetime
from urllib.parse import quote
import time
import requests

# Target date for fetching the top articles leaderboard (Format: YYYY-MM-DD)

target_date = input("Enter target date(yyyy/mm/dd): ")

# Date range to collect page info from

start_date = input("Enter start date(Format: YYYYMMDD) : ") + "00"
end_date = input("Enter end date(Format: YYYYMMDD) :") + "00"

# Header as per Wikimedia API Policy

user_agent = "MyWikipediaTopArticlesBot/1.0 (contact: sagar42wc@gmail.com)"

def title_collection():
    print("Starting data collection.")
    
    url1 = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{target_date}"
    
    headers = {"User-Agent": user_agent}

    response = requests.get(url1, headers=headers, timeout=10)
    print(response.status_code)

    data = response.json()
    articles_list = data.get("items", [{}])[0].get("articles", [])

    print("\nArticles Found:")

    all_rows = []
    for title in articles_list:
        all_rows.append(title["article"])
        print(title["article"])
        if len(all_rows) == 11:
            break

    return all_rows

def fetch_pageviews(article: str, start_date: str, end_date: str) -> list:

# Handle spaces, special characters like parenthesis and underscore

    url2 = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article}/daily/{start_date}/{end_date}"

    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(url2, headers=headers, timeout=10)

# Handling server issues

        if response.status_code != 200:
            print(f"Failed to fetch data for '{article}'. Status code: {response.status_code}")
            return []

        data = response.json()
        results = []

        for item in data.get("items", []):

# Convert date to DD-MM-YYYY
            raw_timestamp = item["timestamp"]
            formatted_date = datetime.strptime(raw_timestamp, "%Y%m%d00").strftime(
                "%d-%m-%y"
            )

            results.append(
                {
                    "Page Title": article,
                    "Date": formatted_date,
                    "Number of Visits": item["views"],
                }
            )

        return results

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching data for '{article}': {e}")
        return []


def main():

    all_data = []

    articles = title_collection()

    for article in articles:
        print(f"Fetching info for: '{article}'")
        article_data = fetch_pageviews(article, start_date, end_date)
        all_data.extend(article_data)

# Adding delay to reduce request frequency

        time.sleep(0.1)

    if not all_data:
        print("No data was retrieved. File will not be created.")
        return

# Write data to CSV

    try:
        fieldnames = ["Page Title", "Date", "Number of Visits"]
        with open("wikipedia_pageviews.csv", mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)

        print(f"Data successfully saved to wikipedia_pageviews.csv:.")

    except IOError as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    main() 
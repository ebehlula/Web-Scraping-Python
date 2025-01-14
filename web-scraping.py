import re
import requests
from urllib.parse import urlparse


def validate_url(url):

    # Validate if the given string is a properly formatted URL
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def check_domain_reachability(url):

   # Check if the domain is reachable by making a HEAD request

    try:
        # Send a HEAD request to check domain reachability
        response = requests.head(url, timeout=10)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            print(f"Edge case trying to find if there is any usual info.")
            return True
        else:
            print(
                f"Domain is reachable but returned status code {response.status_code}.")
            return False
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the domain. Please check the URL.")
        return False
    except requests.exceptions.Timeout:
        print("Request timed out. The domain took too long to respond.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking domain reachability: {e}")
        return False


def get_pattern_from_selector(selector_type, selector_value):

   # Generates regex pattern based on user's selector choice with integrated quote handling

    patterns = {
        # class
        '1': f'<div class="{selector_value}".*?>((?:<blockquote.*?>.*?</blockquote>)?.*?)</div>',
        # id
        '2': f'<div id="{selector_value}".*?>((?:<blockquote.*?>.*?</blockquote>)?.*?)</div>',
        # tag
        '3': f'<{selector_value}.*?>((?:<blockquote.*?>.*?</blockquote>)?.*?)</{selector_value}>'
    }
    return patterns.get(selector_type, '')


def clean_text(html_content):

   # Clean HTML content by removing tags while preserving quote structure

    # Handle blockquotes first
    quote_pattern = r'<blockquote.*?><div.*?><cite.*?>(.*?) wrote:</cite>(.*?)</div></blockquote>'

    def quote_replacement(match):
        author = match.group(1)
        quote_content = re.sub(r'<[^>]*>', '', match.group(2)).strip()
        return f"{author}: {quote_content}"

    # Replace blockquotes while preserving structure
    content = re.sub(quote_pattern, quote_replacement, html_content)

    # Remove remaining HTML tags
    content = re.sub(r'<[^>]*>', '', content)

    # Clean up whitespace while preserving structure
    content = re.sub(r'\s+', ' ', content).strip()

    return content


def scrape_content(url, selector_type, selector_value):

   # Scrapes content from specified elements on the webpage

    try:
        # Headers to mimic Chrome browser
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        # Send request
        response = requests.get(url, headers=headers, timeout=30)

        # Get the content even if it's a 404
        html_content = response.text

        # Log the response status
        if response.status_code != 200:
            print(
                f"Warning: Server returned status code {response.status_code}")
            print("Attempting to process content anyway...\n")

        pattern = get_pattern_from_selector(selector_type, selector_value)

        if not pattern:
            print("Invalid selector type chosen.")
            return

        matches = re.findall(pattern, html_content, re.DOTALL)

        if not matches:
            print(f"No elements found matching the selector: {selector_value}")
            return

        output = []

        for match in matches:
            cleaned_text = clean_text(match)
            if cleaned_text:  # Only append non-empty matches
                output.append(cleaned_text)

        # Display the formatted results
        for i, content in enumerate(output, start=1):
            print(f"{i}. [{content}]")

    except requests.exceptions.ConnectionError as e:
        if "Name or service not known" in str(e) or "Failed to resolve" in str(e):
            print("The website doesn't exist or the domain name could not be resolved.")
        else:
            print(
                "Failed to connect to the website. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Request timed out. The website took too long to respond.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_selector_info():

   # Gets selector type and value from user input

    print("\nSelect the type of element you want to scrape:")
    print("1. Class name (e.g., 'content', 'post-text')")
    print("2. ID (e.g., 'main-content', 'post-123')")
    print("3. HTML tag (e.g., 'p', 'article')")

    while True:
        selector_type = input("Enter your choice (1-3): ").strip()
        if selector_type in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    selector_value = input("Enter the selector value: ").strip()
    return selector_type, selector_value


def main():
    while True:
        url = input("\nEnter the URL to scrape (or 'quit' to exit): ").strip()

        if url.lower() in ['quit', 'exit', 'q']:
            print("Exiting program...")
            break

        if not validate_url(url):
            print(
                "Invalid URL format. Please enter a valid URL including 'http://' or 'https://'")
            continue

        if not check_domain_reachability(url):
            continue

        selector_type, selector_value = get_selector_info()
        scrape_content(url, selector_type, selector_value)


if __name__ == "__main__":
    main()

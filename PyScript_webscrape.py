import requests
from bs4 import BeautifulSoup

def extract_news(url):
    """
    Extracts chapter names and their associated verses with meanings from the given webpage.

    Args:
        url: The URL of the webpage to scrape.

    Returns:
        A string containing chapter names and their associated verses with meanings.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, 'html.parser')

    cnt = "Index:\n"
    chapter_divs = soup.find_all('div', class_='r bb r-lang-en r-chapter')
    for i, chapter_div in enumerate(chapter_divs):
        anchor = chapter_div.find('a', href=True)
        if anchor:
            chapter_name = anchor.text.strip()
            chapter_url = anchor['href']
            cnt += f"{i+1}. {chapter_name}\n"

            # Get the chapter page content
            url = 'https://vedabase.io/'
            final_url = url + chapter_url.strip('/')
            chapter_response = requests.get(final_url)
            chapter_response.raise_for_status()
            chapter_soup = BeautifulSoup(chapter_response.content, 'html.parser')

            # Find the verse section on the chapter page
            for verse_section in chapter_soup.find_all('dl', class_='r r-verse'):
                if verse_section:
                    for dt in verse_section.find_all('dt'):
                        textnum_link = dt.find('a', href=True)
                        if textnum_link:
                            textnum = textnum_link.text.strip()
                            meaning_dd = dt.find_next_sibling('dd')
                            if meaning_dd:
                                meaning = meaning_dd.text.strip()
                                cnt += f"  - {textnum}: {meaning}\n"

    return cnt

if __name__ == "__main__":
    url = 'https://vedabase.io/en/library/bg/'  # Replace with the actual URL
    content = extract_news(url)

    # Print the extracted content
    #print(content)

    # Save the content to a file
    with open('chapters_with_verses.txt', 'w', encoding="utf-8") as f:
        f.write(content)

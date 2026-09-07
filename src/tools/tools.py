from langchain.tools import tool
import os
import requests
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()
from rich import print

from bs4 import BeautifulSoup
from readability import Document 
import trafilatura
import re


tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def  web_search(query: str) -> str:
    """search the web for a given query and return the results"""
    result= tavily.search(query=query,max_results=5)
    out =[]
    for i in result['results']:
        out.append(f"Title: {i['title']}\nURL: {i['url']}\nSnippet: {i['content'][:300]}\n")
    return "\n-------\n".join(out)
    #print(result)




@tool
def scrape_url(url: str) -> str:
    """
    Scrape a webpage URL and return the main readable text.
    """

    try:
        # Send request to webpage
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        response.raise_for_status()

        html = response.text

        # -----------------------------------------
        # Method 1: Trafilatura
        # -----------------------------------------

        text = trafilatura.extract(html)

        if text:
            # Clean text
            text = re.sub(r"\n+", "\n", text)
            text = re.sub(r"[ \t]+", " ", text)

            return text.strip()

        # -----------------------------------------
        # Method 2: Readability
        # -----------------------------------------

        document = Document(html)

        readable_html = document.summary()

        soup = BeautifulSoup(
            readable_html,
            "html.parser"
        )

        text = soup.get_text(
            separator="\n",
            strip=True
        )

        if text:
            text = re.sub(r"\n+", "\n", text)
            text = re.sub(r"[ \t]+", " ", text)

            return text.strip()

        # -----------------------------------------
        # Method 3: BeautifulSoup fallback
        # -----------------------------------------

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # Remove unnecessary elements
        for tag in soup.find_all(
            ["script", "style", "nav", "footer", "header"]
        ):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True
        )

        text = re.sub(r"\n+", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()

    except requests.exceptions.Timeout:
        return "Error: Request timed out."

    except requests.exceptions.RequestException as e:
        return f"Error accessing URL: {e}"

    except Exception as e:
        return f"Error scraping URL: {e}"




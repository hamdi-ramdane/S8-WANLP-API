from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

scraper_bp = Blueprint("scraper", __name__)

SUPPORTED_DOMAINS = {
    "aljazeera.net": {
        "title_tag": {"name": "h1"},
        "content_tag": {"name": "p", "attrs": {"class": "x_MsoNormal"}},
        "date_tag": {"name": "span", "attrs": {"class": "article-dates__published"}}
    },
    "echoroukonline.com": {
        "title_tag": {"name": "h1", "attrs": {"class": "ech-sgmn__title ech-sgmn__sdpd"}},
        "content_tag": {"name": "p"},
        "date_tag": {"name": "time", "attrs": {"class": "ech-card__mtil"}}
    },
    "alarabiya.net": {
        "title_tag": {"name": "h1", "attrs": {"class": "headingInfo_title"}},
        "content_tag": {"name": "p", "attrs":{"class": "body-1 paragraph"}},
        "date_tag": {"name": "time"}
    },
    "bbc.com/arabic": {
        "title_tag": {"name": "span", "attrs": {"class": "css-s2yxgf"}},
        "content_tag": {"name": "p", "attrs": {"class": "css-1bamlcy"}},
    },
    "elkhabar.com": {
        "title_tag": {"name": "h1", "attrs": {"class": ""}},
        "content_tag": {"name": "p", "attrs": {"class": ""}},
    },
}

def scrape_article(url):
    domain = urlparse(url).netloc.replace("www.", "")
    
    if domain not in SUPPORTED_DOMAINS:
        return None, f"Unsupported domain: {domain}"
    
    rules = SUPPORTED_DOMAINS[domain]

    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title_element = soup.find(**rules["title_tag"])
        content_element = soup.find(**rules["content_tag"])
        date_element = soup.find(**rules["date_tag"])

        title = title_element.get_text(strip=True) if title_element else "Title not found"
        content = content_element.get_text(strip=True) if content_element else "Content not found"
        pub_date = date_element.get_text(strip=True) if date_element else "Publication date not found"

        return {"title": title, "content": content ,"publication_date": pub_date}, None

    except Exception as e:
        return None, f"Scraping error: {str(e)}"

@scraper_bp.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    result, error = scrape_article(url)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 200


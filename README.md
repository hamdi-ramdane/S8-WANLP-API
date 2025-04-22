## Supported Domains

- aljazeera.net
- echoroukonline.com
- alarabiya.net
- bbc.com/arabic/
- elkhabar.com

## Installation

```
git clone https://github.com/hamdi-ramdane/S8-WANLP-API.git
cd S8-WANLP-PROJECT-SCRAPPER
pip install -r requirements.txt
```

## Usage

```
python app.py
```

```
curl -X POST http://localhost:5000/scrape
    -H "Content-Type: application/json"
    -d '{"url": "https://www.aljazeera.net/news/liveblog/..."}'
{
  "publication_date": "...",
  "title": "...",
  "content": "..."
}
```

```
curl -X POST http://localhost:5000/check_news
    -H "Content-Type: application/json"
    -d '{"text": "..."}'
{
  "similarity_score": 0.5882358434954242,
  "status": "real",
  "title": "...",
  "url": "..."
}
```

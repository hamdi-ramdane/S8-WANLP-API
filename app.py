
from flask import Flask
from endpoints.check_news import check_news_bp
from endpoints.scrape import scraper_bp

app = Flask(__name__)

app.register_blueprint(check_news_bp)
app.register_blueprint(scraper_bp)

if __name__ == "__main__":
    app.run(debug=True)

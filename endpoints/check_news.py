from flask import Blueprint, request, jsonify
import pandas as pd
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

check_news_bp = Blueprint('check_news', __name__)

# --- Normalize Arabic text ---
def normalize_arabic(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ؤ', 'ء', text)
    text = re.sub(r'ئ', 'ء', text)
    text = re.sub(r'ة', 'ه', text)
    return text

# --- Load news from JSON ---
def load_news_data():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data/news_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['text'] = df['title'].fillna('') + ' ' + df['content'].fillna('')
    return df

# --- Search for similar news ---
def search_news(user_text, news_df, threshold=0.4):
    corpus = news_df['text'].tolist()
    corpus.append(user_text)

    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    top_match_idx = similarity.argmax()
    top_score = similarity[0, top_match_idx]

    if top_score >= threshold:
        matched_row = news_df.iloc[top_match_idx]
        return {
            'matched': True,
            'title': matched_row['title'],
            'url': matched_row['url'],
            'similarity_score': float(top_score)
        }
    else:
        return {'matched': False}

@check_news_bp.route('/check_news', methods=['POST'])
def check_news():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field'}), 400

    user_text = normalize_arabic(data['text'])
    news_df = load_news_data()
    result = search_news(user_text, news_df)

    if result['matched']:
        return jsonify({
            'status': 'real',
            'title': result['title'],
            'url': result['url'],
            'similarity_score': result['similarity_score']
        })
    else:
        return jsonify({'status': 'possibly_fake'})

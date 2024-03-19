# # #!/usr/bin/env python3


from flask import Flask, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.clear()
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # page_views is 0 if it doesn't exist in session
    page_views = session.get('page_views', 0)
    
    # Add page_views by 1
    session['page_views'] = page_views + 1
    
    # Check if the user has viewed more than 3 pages
    if page_views >= 3:
        return {'message': 'Maximum pageview limit reached'}, 401
    
    # Get article by ID
    article = Article.query.get(id)
    
    # If article doesn't exist, return 404
    if not article:
        return {'message': 'Article not found'}, 404
    
    # If it does, return the article data
    return jsonify(article.serialize()), 200

if __name__ == '__main__':
    app.run(port=5555)

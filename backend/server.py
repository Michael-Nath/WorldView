from typing import Dict
from flask import Flask, request
from typing import Dict
from flask_restful import Resource, Api
from extraction.core_extraction import CORE_EXECUTION
from flask_cors import CORS
app = Flask(__name__)
api = Api(app)
cors = CORS(app)


class Article(Resource):
    def get(self):
        args = request.args
        url = args.get("url")
        attributes: Dict = CORE_EXECUTION(url)
        payload = {
            "status": 200,
            "error": False,
            "headline": attributes["headline"],
            "headline_sentiment": attributes["headline_sentiment"],
            "content_sentiment": attributes["content_sentiment"],
            "top_words": attributes["top_words"],
            "content_summary": attributes["content_summary"]
        }
        return payload
        # here the scraping function should be called with the url as input

class Perspectives(Resource):
    def get(self):
        args = request.args
        url = args.get("url")
        # articles = get_articles(url)
        # clusters = cluster(articles)
        articles = [
                {
                "id": '1', 
                "type": 'article', 
                "data": {
                "url": "http://google.com",
                "headline": "Headline 1",
                "summary": ["hello there", "this is great"],
                "keywords": ["Top", "Low"],
                "cluster_id": "2",
                "sentiment": {
                "pos": 1.1,
                "neg": 0.2,
                "neu": 0.1
                    },
                },
            "position": { "x": 200, "y": 200 }
            },
        ]
        
        clusters = [
            {
            "id": '2', 
            "type": 'cluster', 
            "data": {
                "sentiment": {
                    "pos": 0.7,
                    "neg": 0.2,
                    "neu": 0.1
                },
                "numNodes": 5,
                "degree": 3,
                "keywords": ["Test", "hey", "lol"]
            },
            "position": { "x": 250, "y": 200 }
            },
        ]
        return {"articles": articles, "clusters": clusters}

class Hello(Resource):
    def get(self):
        return "Hello"

api.add_resource(Article, "/get-article-data")
api.add_resource(Perspectives, "/get-perspectives")
api.add_resource(Hello, "/")

if __name__ == '__main__':
    host = "0.0.0.0"
    # host = None
    app.run(debug=True, host=host)

from typing import Dict
from flask import Flask, request
from typing import Dict
from flask_restful import Resource, Api
from extraction import core_extraction
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


api.add_resource(Article, "/get-article-data")
if __name__ == '__main__':
    # host = "0.0.0.0"
    host = None
    app.run(debug=True, host=host)

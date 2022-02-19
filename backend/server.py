from typing import Dict
from flask import Flask, request
from typing import Dict
from flask_restful import Resource, Api
from the_glue import CORE_EXECUTION
app = Flask(__name__)
api = Api(app)


class Article(Resource):
    def get(self):
        args = request.args
        url = args.get("url")
        attributes: Dict = CORE_EXECUTION(url)
        print(attributes.keys())
        print(attributes["top_words"])
        print(attributes["top_phrases"])
        payload = {
            "status": 200,
            "error": False,
            "headline": attributes["headline"],
            "headline_sentiment": attributes["headline_sentiment"],
            "content_sentiment": attributes["content_sentiment"],
            "top_words": attributes["top_words"],
            # "top_phrases": attributes["top_phrases"]
        }
        return payload
        # here the scraping function should be called with the url as input


api.add_resource(Article, "/get-article-data")
if __name__ == '__main__':
    app.run(debug=True)

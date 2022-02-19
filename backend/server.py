from flask import Flask, request
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)


class Article(Resource):
    def get(self):
        args = request.args
        url = args.get("url")
        return url
        # here the scraping function should be called with the url as input


api.add_resource(Article, "/article")
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

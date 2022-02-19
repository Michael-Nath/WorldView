import boto3
from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with
app = Flask(__name__)
api = Api(app)


class Article(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("url", type=str, help="must be string")
        args = parser.parse_args()
        url = args["url"]
        # here the scraping function should be called with the url as input
        
api.add_resource(Article, "/article")
if __name__ == '__main__':
    app.run(debug=True)
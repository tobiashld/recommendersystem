import os
from src.service.recommenderservice import recommend_for_movie as movieservice
from flask_restful import Api, Resource
from flask import Flask,jsonify,request,abort
from flask_cors import CORS,cross_origin
import requests

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods = ['GET'])
@cross_origin()
def mainRoute():
    startpath = '.'
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
    return  jsonify(info="hello this is an educationally used api. For more Details go to https://frontend-recommendersystem.herokuapp.com/")


@app.route('/get/<id>')
def index(id):
    id = int(id)
    return movieservice(id)

@app.route('/dropdownsearch', methods = ['GET'])
@cross_origin()
def dropdownSearchRoute():
    searchtitle = str(request.args.get("searchtitle")).lower()
    endsuchstring = ""
    for word in searchtitle.split(" "):
        endsuchstring += "*"+word+"*"
    api_url =  "http://solrrecommendersystem.cf:8984/solr/filme/select?q=searchtitle%3A"+endsuchstring+"&q.op=OR&rows=3"
    response = requests.get(api_url)
    if response.status_code == 200 and hasattr(response,"text"): #and response.text > 0:
        return jsonify(response.text)       
    else:
        abort(404)


if __name__=='__main__':
    cfg_port = os.getenv('PORT', "80")
    app.run(host="0.0.0.0", port=cfg_port)#, debug=True)
    #Test
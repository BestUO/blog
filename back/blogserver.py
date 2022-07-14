import sys
isDebug = True if sys.gettrace() else False

from flask import Flask
from src.routefun import CustomRoute
import src.myglobal as Global
from gevent import pywsgi
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,   
    default_limits=["20000 per day"]
)

@limiter.limit("3 per minute")
def test():
    return CustomRoute.hello_world()

if __name__ == "__main__":
    app.add_url_rule('/hello',view_func=test,methods=['POST',"GET"])
    app.add_url_rule('/api/getArticleList',view_func=CustomRoute.GetArticleList,methods=['POST', "GET"])
    app.add_url_rule('/api/getArticleDetail',view_func=CustomRoute.getArticleDetail,methods=['POST',"GET", "OPTIONS"])
    app.add_url_rule('/api/getTagList',view_func=CustomRoute.GetTagList,methods=['POST',"GET"])
    app.add_url_rule('/api/styletransfer',view_func=CustomRoute.StyleTransfer,methods=['POST',"GET"])

    app.add_url_rule('/api/uploadfile',view_func=CustomRoute.upload,methods=['POST',"GET"])
    app.add_url_rule('/img/<string:filename>',view_func=CustomRoute.GetPicture,methods=["GET"])
    app.add_url_rule('/img/<string:date>/<string:filename>',view_func=CustomRoute.GetDatePicture,methods=["GET"])

    if(not isDebug):
        from gevent import monkey
        monkey.patch_all()
        server = pywsgi.WSGIServer((Global.config["http_server"]["ip"],Global.config["http_server"]["port"]), app)
        server.serve_forever()
    else:
        app.run(Global.config["http_server"]["ip"],Global.config["http_server"]["port"])
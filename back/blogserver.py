from flask import Flask

from src.routefun import CustomRoute
import src.myglobal as Global

app = Flask(__name__)

if __name__ == "__main__":
    app.add_url_rule('/hello/',view_func=CustomRoute.hello_world,methods=['POST',"GET"])
    app.add_url_rule('/api/getArticleList',view_func=CustomRoute.GetArticleList,methods=['POST', "GET"])
    app.add_url_rule('/api/getArticleDetail',view_func=CustomRoute.getArticleDetail,methods=['POST',"GET", "OPTIONS"])
    app.add_url_rule('/api/getTagList',view_func=CustomRoute.GetTagList,methods=['POST',"GET"])

 
    # tmp = Global.dbmanager.execute_query("select * from test",True)

    app.run(Global.config["http_server"]["ip"],Global.config["http_server"]["port"])
from flask import Flask,request,make_response
from flask_cors import CORS, cross_origin
from functools import wraps
import src.myglobal as Global
import json

def wrapTheFunction(fun):
    method = request.method
    headers = request.headers
    url = request.url
    if(method == "GET"):
        param = request.args
    elif(method == "POST"):
        if(headers.environ["CONTENT_TYPE"]=="application/x-www-form-urlencoded"):
            param = request.form
        elif(headers.environ["CONTENT_TYPE"]=="application/json"):
            param = request.get_json()
        else:
            param = request.get_data()

    ResponseData = fun(param)
    res = make_response(ResponseData) # 设置响应体
    res.status = '200' # 设置状态码
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-Type'] = 'application/json'
    return res

def ParseRequestDecorator(fun):
    @wraps(fun)
    def GetFun():
        return wrapTheFunction(fun)
    return GetFun

def ParseRequestOptionsDecorator(fun):
    @wraps(fun)
    @cross_origin()
    def GetFun():
        return wrapTheFunction(fun)
    return GetFun

class CustomRoute:

    @staticmethod
    @ParseRequestDecorator
    def hello_world(param, *args, **kwargs):
        return "hello world" 

    @staticmethod
    @ParseRequestDecorator
    def GetArticleList(param, *args, **kwargs):
        ArticlesData = {"count":0,"list":[]}
        tag_id = param["tag_id"]
        pageNum = int(param["pageNum"])-1
        pageSize = int(param["pageSize"])

        if tag_id=="":
            sql = "select id,title,`desc`,tag,create_time from article limit " + str(pageNum*pageSize) + "," + str(pageSize)
        else:
            sql = "select id,title,`desc`,tag,create_time from article where FIND_IN_SET(\"" + str(tag_id) + "\",tag) limit " + str(pageNum*pageSize) + "," + str(pageSize)

        articles = Global.dbmanager.execute_query(sql,True)
        ArticlesData["count"] = len(articles)
        for article in articles:
            ArticlesData["list"] += [CustomRoute.GetArticleInfo(article)]

        ResponseData  = {"code":0,"data":ArticlesData,"message":"OK"}

        return ResponseData

    @staticmethod
    @ParseRequestDecorator
    def GetTagList(param, *args, **kwargs):
        TagsData = {"count":0,"list":[]}
        keyword = param["keyword"]
        pageNum = int(param["pageNum"])-1
        pageSize = int(param["pageSize"])

        if keyword=="":
            sql = "select * from taglist limit " + str(pageNum*pageSize) + "," + str(pageSize)
        else:
            sql = "select * from taglist where name = "+ keyword +" limit " + str(pageNum*pageSize) + "," + str(pageSize)

        tags = Global.dbmanager.execute_query(sql,True)
        TagsData["count"] = len(tags)
        for tag in tags:
            TagsData["list"] += [{"name":tag["name"],"_id":tag["id"]}]

        ResponseData  = {"code":0,"data":TagsData,"message":"OK"}

        return ResponseData

    @staticmethod
    @ParseRequestOptionsDecorator
    @cross_origin()
    def getArticleDetail(param, *args, **kwargs):
        TagsData = {"toc":"","_id":"","author":"Boray","category":[],
                "comments":[],"create_time":"","desc":"","content":"",
                "id":0,"img_url":"","numbers":0,"keyword":[],"like_users":[],"meta":{"views":0,"likes":0,"comments":0},
                "origin":0,"state":1,"tags":[],"title":"title","update_time":""}


        sql = "select title,create_time,file_name from article where id=" + param["id"]
        results = Global.dbmanager.execute_query(sql,True)
        TagsData["title"] = str(results[0]["title"])
        TagsData["create_time"] = str(results[0]["create_time"])
        with open(Global.config["blog_dir"] + results[0]["file_name"],'r', encoding='utf-8') as f:
            html = f.read()
            TagsData["content"] = html

        ResponseData  = {"code":0,"data":TagsData,"message":"OK"}

        return ResponseData

    @staticmethod
    def GetArticleInfo(article):
        articleinfo = {"category":"",
                        "create_time":str(article["create_time"]),
                        "desc":article["desc"],
                        "img_url":"",
                        "meta":"",
                        "tags":article["tag"].split(","),
                        "title":article["title"],
                        "_id":article["id"]}
        return articleinfo

from flask import Flask,request,make_response
from flask_cors import CORS, cross_origin
from functools import wraps
import src.myglobal as Global
import json
import os
import redis
import hashlib
import time

def wrapTheFunction(fun):
    method = request.method
    headers = request.headers
    url = request.url
    if(method == "GET"):
        param = request.args
    elif(method == "POST"):
        if(headers.environ["CONTENT_TYPE"]=="application/x-www-form-urlencoded" or headers.environ["CONTENT_TYPE"].__contains__("multipart/form-data")):
            param = dict(list(request.files.items()) + list(request.form.items()))
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
            sql = "select id,title,`desc`,tag,create_time from article order by id desc limit " + str(pageNum*pageSize) + "," + str(pageSize)
        else:
            sql = "select id,title,`desc`,tag,create_time from article where FIND_IN_SET(\"" + str(tag_id) + "\",tag) order by id desc limit " + str(pageNum*pageSize) + "," + str(pageSize)

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


        sql = "select title,`desc`,create_time,file_name,keywords from article where id=" + param["id"]
        results = Global.dbmanager.execute_query(sql,True)
        TagsData["title"] = str(results[0]["title"])
        TagsData["desc"] = str(results[0]["desc"])
        TagsData["keyword"] = results[0]["keywords"].split(",")
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

    @staticmethod
    def GetFileRes(file_path,suffix):
        if request.method == 'GET':
            if not os.path.isfile(file_path):
                image_data = "No FileName"
            else:
                with open(file_path, "rb") as f:
                    image_data = f.read()
        else:
            image_data = "Need GET Request"
        res = make_response(image_data) # 设置响应体
        res.status = '200' # 设置状态码
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Content-Type'] = 'image/' + suffix
        return res

    @staticmethod
    def GetPicture(filename):
        file_path = Global.config["img_dir"] + filename
        suffix = filename.split('.')[-1]
        return CustomRoute.GetFileRes(file_path, suffix)

    @staticmethod
    def GetDatePicture(date, filename):
        file_path = Global.config["img_dir"] + date + "/" + filename
        suffix = filename.split('.')[-1]
        return CustomRoute.GetFileRes(file_path, suffix)

    @staticmethod
    def MkdirByDay():
        datedir = time.strftime("%Y%m%d",time.localtime()) + "/"
        filedir = Global.config["img_dir"] + datedir
        os.makedirs(filedir,exist_ok=True)
        return datedir

    @staticmethod
    @ParseRequestOptionsDecorator
    @cross_origin()
    def upload(param, *args, **kwargs):
        img = param['file']
        file_bytes = img.read()
        imgName = CustomRoute.MkdirByDay()
        if(param.get("filename")):
            imgName += param.get("filename")
        else:
            imgName += hashlib.md5(file_bytes).hexdigest()+"."+ img.filename.split(".")[-1]

        file_path = Global.config["img_dir"] + imgName
        if(not os.path.exists(file_path)):
            file_path_tmp = file_path +".tmp"
            with open(file_path_tmp,"wb") as file:
                file.write(file_bytes)
            os.rename(file_path_tmp,file_path)
    
        #url是图片的路径
        url = "http://{ip}:{port}/img/{filename}".format(ip=Global.config["http_server"]["ext-ip"], port=Global.config["http_server"]["port"],
        filename=imgName)

        ResponseData  = {"code":0,"data":url,"message":"OK"}

        return ResponseData

    @staticmethod
    def StyleTransfer_WCT_AdaIN(param):
        functionname = param["functionname"]
        alpha = str(param["alpha"])
        sourceimgname = param["sourceimgurl"].split("/")[-1]
        styleimgname = param["styleimgurl"].split("/")[-1]
        uuid = hashlib.md5((functionname+alpha+sourceimgname+styleimgname).encode('utf-8')).hexdigest()
        resultimgname = CustomRoute.MkdirByDay() + uuid +"_result.jpg"
        if(not os.path.exists(Global.config["img_dir"] + resultimgname)):
            element = "{uuid}-{functionname}-{sourceimgurl}#{styleimgurl}#{alpha}".format(
                uuid=uuid,functionname=functionname,sourceimgurl=param["sourceimgurl"],styleimgurl=param["styleimgurl"],alpha=alpha)
            rclient = redis.Redis(host=Global.config["redis"]["host"], port=Global.config["redis"]["port"], password=Global.config["redis"]["passwd"], db=0)
            rclient.rpush(functionname,element)
        return resultimgname

    @staticmethod
    def StyleTransfer_Fast(param):
        functionname = param["functionname"]
        sourceimgname = param["sourceimgurl"].split("/")[-1]
        faststyle = param["faststyle"]
        uuid = hashlib.md5((functionname+sourceimgname+faststyle).encode('utf-8')).hexdigest()
        resultimgname = CustomRoute.MkdirByDay() + uuid +"_result.jpg"
        if(not os.path.exists(Global.config["img_dir"] + resultimgname)):
            element = "{uuid}-{functionname}-{sourceimgurl}#{faststyle}".format(
                uuid=uuid,functionname=functionname,sourceimgurl=param["sourceimgurl"],faststyle=faststyle)
            rclient = redis.Redis(host=Global.config["redis"]["host"], port=Global.config["redis"]["port"], password=Global.config["redis"]["passwd"], db=0)
            rclient.rpush(functionname,element)
        return resultimgname

    @staticmethod
    @ParseRequestOptionsDecorator
    @cross_origin()
    def StyleTransfer(param, *args, **kwargs):
        functionname = param["functionname"]
        if(functionname == "StyleTransfer_WCT" or functionname == "StyleTransfer_AdaIN"):
            resultimgname = CustomRoute.StyleTransfer_WCT_AdaIN(param)
        elif(functionname == "StyleTransfer_Fast"):
            resultimgname = CustomRoute.StyleTransfer_Fast(param)
        else:
            return {"code":0,"data":"no functionname","message":"OK"}

        timewait=60
        while(timewait>0):
            if(os.path.exists(Global.config["img_dir"] + resultimgname)):
                break
            time.sleep(2)
            timewait -=2

        url = "http://{ip}:{port}/img/{filename}".format(ip=Global.config["http_server"]["ext-ip"], port=Global.config["http_server"]["port"],
        filename=resultimgname)
        ResponseData  = {"code":0,"data":url,"message":"OK"}
        return ResponseData
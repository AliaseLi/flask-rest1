import os
import uuid

from flask import request, jsonify, session
from flask_restful import Api, Resource, marshal_with, fields, marshal, reqparse
from werkzeug.datastructures import FileStorage

import settings
from dao import *
from models import *

api = Api()


def init_api(app):
    api.init_app(app)


class UserApi(Resource):  # 声明User资源
    def get(self):
        # 单独查找
        key = request.args.get('key')
        if key:
            user = query(User).filter(db.or_(User.id == key,
                                             User.phone == key,
                                             User.name == key)).first()
            if user != None:
                return {'state': 'ok',
                        'msg': '查询成功',
                        'data': user.json, }
            return {'state': 'fail',
                    'msg': '暂无数据'}

        # 从数据库中查询所有的数据
        return {'state': 'ok',
                'data': [user for user in queryAll(User)]}

    def post(self):
        user = User()
        # 从上传的form对象中取出name和phone
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        save(user)  # 添加到数据库
        return {'state': 'ok', 'msg': '添加用户{}成功'.format(user.name)}

    def put(self):
        # 从上传的form对象中取出id,name和phone
        id = request.form.get('uid')
        user = queryById(User, id)
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        save(user)
        return {'state': 'ok', 'msg': '用户{}修改成功'.format(user.name)}

    def delete(self):
        id = request.form.get('id')
        flag = deleteById(User, id)
        # delete(queryById(User,id))
        return {'state': 'ok', 'msg': '删除用户{}成功'.format(id)}


class ImageApi(Resource):
    img_fields = {"id":fields.Integer,
                  "name":fields.String,
                  "url":fields.String,
                  "size":fields.Integer(default=1)}
    get_out_fields = {
        "state": fields.String(default='ok'),
        "data": fields.Nested(img_fields),
        "size": fields.Integer(default=1)
    }

    # 输入定制
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,  # 参数类型
                        required=False,  # 是否必要
                        help='请提供id参数') # 必要参数的提示

    # @marshal_with(get_out_fields)
    def get(self):
        # self.parser.parse_args() # 解析参数，如果参数不满足，则会直接返回
        print('-----------', request.args)
        id = request.args.get('id')

        if id:
            images = query(Image).filter(Image.id==id).all()
            # return marshal(image, self.get_out_fields)
        else:
            images = queryAll(Image)
        data = {'state':'ok',
            'data': images,
            'size':len(images)}

        # 向session中存入用户名
        session['login_name'] = 'aliase'
        return marshal(data, self.get_out_fields)

    def delete(self):
        self.parser.parse_args()
        id = request.form.get('id')
        if id:
            image = query(Image).get(id)
            delete(image)
            return {'state':'ok',
                    'msg':'{}删除成功'.format(image.name)}
        else:
            return {'state': 'fail',
                    'msg': '暂无数据'}

class UploadApi(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('img', type=FileStorage,
    #                     location='files',
    #                     required=True,
    #                     help='必须提供一个名为img的File表单参数')

    def post(self):

        # print(request.files)
        upFile:FileStorage = request.files.get('photo')
        # print('#########',request.form)
        # 获取文件名的扩展名
        extName = "." + upFile.filename.split('.')[-1]
        fileName = str(uuid.uuid4()).replace('-','')+extName
        # print(extName, fileName)
        saveFilePath = os.path.join(settings.STATIC_DIR, 'images/'+fileName)
        # print('########',saveFilePath)
        # 图片链接地址存入数据库
        img = Image()
        img.name = request.form.get('name')
        img.url = '/static/images/'+fileName
        save(img)

        upFile.save(saveFilePath,1024)
        upFile.close()
        return jsonify({"msg":"上传文件成功",
                        "path":'/static/'+fileName})

class MusicApi(Resource):
    # c创建request参数的解析器
    parser = reqparse.RequestParser()

    # 向参数解析器中添加参数说明
    parser.add_argument('key',dest='name', type=str, required=True,
                        help='必须要提供的参数')
    parser.add_argument('id', type=int,help='请确定id是否为数值型')
    parser.add_argument('tag',action='append',required=True,
                        help='至少提供一个tag标签')
    parser.add_argument('session',location='cookies',help='无法连接服务器')

    # 定制输出
    music_fields = {
        'id':fields.Integer,
        'name':fields.String,
        'singer':fields.String,
        'url':fields.String(attribute='mp3_url')
    }
    out_fields = {
        'state':fields.String(default='ok'),
        'msg':fields.String(default='查询成功'),
        'data':fields.Nested(music_fields)
    }
    @marshal_with(out_fields)
    def get(self):
        # 按name搜索
        # 通过request参数解析器，开始解析请求参数
        # 如果请求参数不能满足条件，则直接返回参数相关的help说明
        args = self.parser.parse_args()

        # 从 args中读取name请求参数的值
        name = args.get('name')
        tags = args.get('tag')

        #从args中读取session
        session = args.get('session')
        print('session>>>',session)

        musics = query(Music).filter(Music.name.like('%{}%'.format(name)))
        if musics.count():
            return {'data':musics.all()}


        return {'msg':'{} 暂未发行,标签：{}'.format(name,tags)}
# -----------------------------------------
# 将资源添加到api对象中，并声明uri
api.add_resource(UserApi, '/user/')
api.add_resource(ImageApi, '/image/')
api.add_resource(UploadApi, '/upload/')
api.add_resource(MusicApi, '/music/')
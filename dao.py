from flask_sqlalchemy import SQLAlchemy, BaseQuery

db = SQLAlchemy()
def init_db(app):
    db.init_app(app)


def query(cls) -> BaseQuery:  # 通过 -> 声明函数返回的类型
    return db.session.query(cls)

def queryAll(cls):
    return query(cls).all()

def queryById(cls,id):  # 根据id查找数据
    return query(cls).get(int(id))

def save(obj):  # 添加和更新
    db.session.add(obj)
    db.session.commit()

def delete(obj): # 删除
    db.session.delete(obj)
    db.session.commit()

def deleteById(cls, id):
    try:
        obj = queryById(cls, id)
        delete(obj)
        return True
    except:
        return False

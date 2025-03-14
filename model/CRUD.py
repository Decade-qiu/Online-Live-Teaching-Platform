# -*- coding: utf-8 -*-
import datetime
import json  # 导入日期时间模块
from model.models import CC, Comment, Course, Post, User, Video, Msg, Stream
from tools.orm import ORM
from werkzeug.security import generate_password_hash  # 生成哈希密码
import math
from flask import request, session



# 定义生成日期时间的函数
def dt():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 专门用于增删改查
class CRUD:
    # 验证用户唯一性，昵称1、邮箱2、手机3
    @staticmethod
    def user_unique(data, method=1):
        # 创建会话
        connect = ORM.db()
        user = None
        # 事务处理的逻辑
        try:
            model = connect.query(User)
            if method == 1:
                # 昵称
                user = model.filter_by(name=data).first()
            if method == 2:
                # 邮箱
                user = model.filter_by(email=data).first()
            if method == 3:
                # 手机
                user = model.filter_by(phone=data).first()
        except Exception as e:
            connect.rollback()  # 如果发生异常直接回滚
        else:
            connect.commit()  # 没有发生异常直接提交
        finally:
            connect.close()  # 无论是否发生异常最后一定关闭会话
        if user:
            return True
        else:
            return False

    @staticmethod
    # 保存注册用户
    def save_regist_user(form):
        # 创建会话
        connect = ORM.db()
        try:
            user = User(
                name=form.data['name'],
                pwd=generate_password_hash(form.data['pwd']),
                email=form.data['email'],
                phone=form.data['phone'],
                sex=None,
                xingzuo=None,
                face=None,
                info=None,
                createdAt=dt(),
                updatedAt=dt()
            )
            # 添加记录
            connect.add(user)
        except Exception as e:
            connect.rollback()
            return False
        else:
            connect.commit()
            return True
        finally:
            connect.close()

    # 登录验证
    @staticmethod
    def check_login(name, pwd):
        connect = ORM.db()
        result = False
        try:
            user = connect.query(User).filter_by(name=name).first()
            if user:
                if user.check_pwd(pwd):
                    result = True
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return result

    # 保存用户信息
    @staticmethod
    def save_user(form):
        connect = ORM.db()
        try:
            user = connect.query(User).filter_by(id=int(form.data['id'])).first()
            user.name = form.data['name']
            user.email = form.data['email']
            user.phone = form.data['phone']
            user.sex = int(form.data['sex'])
            user.xingzuo = int(form.data['xingzuo'])
            user.face = form.data['face']
            user.info = form.data['info']
            user.updatedAt = dt()
            user.role = form.data['role']
            connect.add(user)
            print(form.data['role'])
            print(user.role)
            print("!!!!!!!!!")
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return True

    # 获取用户
    @staticmethod
    def user(name):
        connect = ORM.db()
        user = None
        try:
            user = connect.query(User).filter_by(name=name).first()
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return user

    # 获取视频
    @staticmethod
    def video(id):
        connect = ORM.db()
        video = None
        try:
            video = connect.query(Video).filter_by(id=int(id)).first()
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return video

    # 保存消息
    @staticmethod
    def save_msg(content, streamid):
        connect = ORM.db()
        try:
            msg = Msg(
                content=content,
                createdAt=dt(),
                updatedAt=dt(),
                streamId=streamid
            )
            connect.add(msg)
        except Exception as e:
            print(e)
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()

    # 保存消息
    @staticmethod
    def save_con(content, streamid):
        connect = ORM.db()
        try:
            con = Comment(
                content=content,
                createdAt=dt(),
                updatedAt=dt(),
                courseId=streamid
            )
            connect.add(con)
        except Exception as e:
            print(e)
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()

    @staticmethod
    def save_cc(content, streamid):
        connect = ORM.db()
        try:
            cc = CC(
                content=content,
                createdAt=dt(),
                updatedAt=dt(),
                courseId=streamid
            )
            connect.add(cc)
        except Exception as e:
            print(e)
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
    
    # 查询消息
    @staticmethod
    def new_msg(sid):
        connect = ORM.db()
        data = None
        try:
            data = connect.query(Msg).filter_by(streamId=sid).order_by(Msg.createdAt.asc()).limit(200).all()
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return data

    # 保存直播信息
    @staticmethod
    def save_stream(form):
        connect = ORM.db()
        try:
            stream = Stream(
                title=form.data['title'],
                url=form.data['url'],
                createdAt=dt(),
                userid=form.data['userid']
            )
            connect.add(stream)
        except Exception as e:
            connect.rollback()
            return False
        else:
            connect.commit()
            return True
        finally:
            connect.close()

    # 显示直播信息
    @staticmethod
    def show_stream(name, page):
        connect = ORM.db()
        model = None
        try:
            if name == 'all_1mqnabzvxc':
                model = connect.query(Stream).order_by(Stream.createdAt.desc())
            else:
                model = connect.query(Stream).filter_by(userid=name).order_by(Stream.createdAt.desc())
        except Exception as e:
            connect.rollback()
            print(e)
        else:
            connect.commit()
        finally:
            connect.close()
        return model.paginate(page=page, per_page=6)

    # 显示直播信息
    @staticmethod
    def show_my_stream(name):
        connect = ORM.db()
        model = None
        try:
            if name == 'all_1mqnabzvxc':
                model = connect.query(Stream).order_by(Stream.createdAt.desc())
            else:
                model = connect.query(Stream).filter_by(userid=name).order_by(Stream.createdAt.desc())
        except Exception as e:
            connect.rollback()
            print(e)
        else:
            connect.commit()
        finally:
            connect.close()
        return CRUD.page(model)

    # 根据id获取直播信息
    def find_stream(id):
        connect = ORM.db()
        stream = None
        try:
            stream = connect.query(Stream).filter_by(id=int(id)).first()
        except Exception as e:
            connect.rollback()
        else:
            connect.commit()
        finally:
            connect.close()
        return stream

    @staticmethod
    def page(model):
        # 获取页码
        page = request.args.get("page", 1)
        page = int(page)
        # 统计数据表中有多少条记录
        total = model.count()
        if total:
            # 每页显示多少条
            shownum = 12
            # 确定总共显示多少页
            pagenum = int(math.ceil(total / shownum))
            # 判断小于第一页
            if page < 1:
                page = 1
            # 判断大于最后一页
            if page > pagenum:
                page = pagenum

            # sql限制查询，每次查询限制多少条，偏移量是多少
            offset = (page - 1) * shownum
            # 分页查询
            data = model.limit(shownum).offset(offset)
            # 上一页
            prev_page = page - 1
            next_page = page + 1
            if prev_page < 1:
                prev_page = 1
            if next_page > pagenum:
                next_page = pagenum
            arr = dict(
                pagenum=pagenum,
                page=page,
                prev_page=prev_page,
                next_page=next_page,
                data=data
            )
        else:
            arr = dict(
                data=[]
            )
        return arr

    @staticmethod
    def show_video(q):
        session = ORM.db()
        res = None
        try:
            model = None
            if q:
                model = session.query(Video).filter(
                    Video.name.like('%{}%'.format(q))
                ).order_by(Video.createdAt.desc())
            else:
                model = session.query(Video).order_by(Video.createdAt.desc())
            res = CRUD.page(model)
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return res

    @staticmethod
    def save_post(data):
        session = ORM.db()
        try:
            post = Post(
                content=data,
                createdAt=dt()
            )
            session.add(post)
        except Exception as e:
            session.rollback()
            return False
        else:
            session.commit()
            return True
        finally:
            session.close()

    @staticmethod
    def get_posts():
        session = ORM.db()
        res = None
        try:
            res = session.query(Post).order_by(Post.createdAt.desc())
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return res

    @staticmethod
    def get_post(id):
        session = ORM.db()
        res = None
        try:
            res = session.query(Post).filter_by(id=id).first()
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return res

    # 保存直播信息
    @staticmethod
    def save_course(form):
        connect = ORM.db()
        try:
            data = {'info': form.data['content'], 'name': session.get('name', '')}
            print(data, form.data['userid'])
            course = Course(
                title=form.data['title'],
                createdAt=dt(),
                content=json.dumps(data),
                face=form.data['face'],
                own=form.data['userid']
            )
            connect.add(course)
        except Exception as e:
            connect.rollback()
            print(e)
            return False
        else:
            connect.commit()
            return True
        finally:
            connect.close()

    # 显示直播信息
    @staticmethod
    def show_course(name, page):
        connect = ORM.db()
        model = None
        try:
            if name == 'all_1mqnabzvxc':
                model = connect.query(Course).order_by(Course.createdAt.desc())
            else:
                model = connect.query(Course).filter(Course.content.like(f"%{name}%")).order_by(Course.createdAt.desc())
        except Exception as e:
            connect.rollback()
            print(e)
        else:
            connect.commit()
        finally:
            connect.close()
        return model.paginate(page=page, per_page=6)
    
    @staticmethod
    def find_course(name):
        connect = ORM.db()
        model = None
        try:
            model = connect.query(Course).filter_by(id=name).order_by(Course.createdAt.desc()).first()
        except Exception as e:
            connect.rollback()
            print(e)
        else:
            connect.commit()
        finally:
            connect.close()
        return model
    
    @staticmethod
    def add_course(title, stu):
        connect = ORM.db()
        try:
            course = connect.query(Course).filter_by(title=title).first()
            content = json.loads(course.content)
            names = content['names']
            names += " "+stu
            content['names'] = names
        except Exception as e:
            connect.rollback()
            print(e)
            return False
        else:
            connect.commit()
            return True
        finally:
            connect.close()
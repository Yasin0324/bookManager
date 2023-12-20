from flask import Flask, request
from flask.views import MethodView
from extension import db,cors
from models import *
from sqlalchemy import or_
from flask import  jsonify
import random
import smtplib
from email.mime.text import MIMEText
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1224@localhost:3306/bookmanager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hzy_gyx'#token签名
db.init_app(app)
cors.init_app(app)
app.config['ENV'] = 'development'

# 生成 token
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 设置 token 的过期时间
    }
    secret_key = app.config['SECRET_KEY']  # 设置密钥，用于签名 token
    token = jwt.encode(payload, secret_key, algorithm='HS256')  # 生成 token
    return token

@app.route('/')
def hello_world():
    return 'Hello World!'

# 一、图书查询接口
@app.route('/getBooks/',methods=['GET'])
def get_books():
    
    title = request.args.get('book_title', None)
    author = request.args.get('book_author', None)

    query = db.session.query(Book)
    print(query)

    tip = 0
    if title:
        print(query)
        tip = 1
        query = query.filter(Book.book_title.like(f'%{title}%'))
        print(query)
    if author:
        tip = 1
        query = query.filter(Book.book_author.like(f'%{author}%'))

    books = query.all()
    if not books:
        return {
            'code': '404',
            'message': '没有找到书籍'
        }

    results = [
        {
            "book_id" : book.book_id,
            "book_title" : book.book_title,
            "book_type" : book.book_type,
            "book_price" : book.book_price,
            "book_author" : book.book_author,
            "book_publisher" : book.book_publisher,
            "admin_id" : book.admin_id,
            "book_number" : book.book_number,
        } for book in books
    ]

    return {
        'code': 200,
        'tip':tip,
        'results': results,
        'message': '查询成功'
    }

#二、登录接口
@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    user_type = data.get('user_type')
    email = data.get('student_email')
    password = data.get('password')
    admin_ = data.get('admin_name')

    if user_type == 1:
        student = db.session.query(Student).filter_by(student_email=email).first()
        if student and student.student_password == password:
            #用学生邮箱生成token
            token=generate_token(email)
            results = {
                "student_id": student.student_id,
                "student_name": student.student_name,
                "student_email": student.student_email,
                'student_password':student.student_password,
                "user_type": 1
            }
            return {
                'code': 200,
                'result': results,
                'message': '登录成功',
                'token':token
            }
        else:
            return {
            'code': 500,
            'message': '用户名或密码错误'
            }
    elif user_type == 0:
        admin = db.session.query(Admin).filter_by(admin_name=admin_).first()
        if admin and admin.admin_password == password:
            #用管理员名字生成token
            token=generate_token(admin_)
            results = {
            "admin_id": admin.admin_id,
            "admin_name": admin.admin_name,
            "admin_password": admin.admin_password,
            "user_type": 0
            }
            return {
            'code': 200,
            'result': results,
            'message': '登录成功',
            'token':token
            }
        else:
            return {
            'code': 500,
            'message': '用户名或密码错误'
            }
    else:
        return {
        'code': 500,
        'message': '用户类型错误'
    }

    
#三、借还图书接口
@app.route('/read_back/', methods=['POST'])
def read_back():
    # 检查请求中是否包含token
    token = request.headers.get('token')
    if not token:
        return {
                'code':500,
                'message':'您没有权限'
                }
    # 验证token是否有效
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {
            'code':500,
            'message':'token验证失败'
        }
    except jwt.InvalidTokenError:
        return {
            'code':500,
            'message':'token验证失败'
        }
    data = request.json
    book_ = data.get('book_id')
    action = data.get('action')
    student_id = data.get('student_id')
    read_id = data.get('read_id')

    book = db.session.query(Book).filter_by(book_id = book_).first()

    if book:
        if action == 0:
            if book.book_number > 0:
                book.book_number -= 1
                db.session.add(book)
                new_read = Read(student_id=student_id,book_id=book_,read_time=datetime.datetime.now().strftime('%y-%m-%d'))
                db.session.add(new_read)
                db.session.commit()
                return {
                    'code':200,
                    'message':'借阅成功'
                }
            else:
                return {
                    'code':500,
                    'message':'操作失败'
                    }
        elif action == 1:
            book.book_number += 1
            db.session.add(book)
            read = db.session.query(Read).filter_by(student_id=student_id, read_id=read_id).first()
            if read:
                read.back_time = datetime.datetime.now().strftime('%y-%m-%d')
                db.session.add(read)
            db.session.commit()
            return {
                    'code':200,
                    'message':'归还成功'
                }
        else:
            return {
                'code':500,
                'message':'数据错误'
            }
    else:
        return {
                'code':500,
                'message':'未找到数据'
            }


# 四、图书信息上传/修改/删除接口
@app.route('/addBook/',methods=['POST'])
def add_book():
    # 检查请求中是否包含token
    token = request.headers.get('token')
    if not token:
        return {
                'code':500,
                'message':'您没有权限'
                }
    # 验证token是否有效
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {
            'code':500,
            'message':'token验证失败'
        }
    except jwt.InvalidTokenError:
        return {
            'code':500,
            'message':'token验证失败'
        }
    form = request.json
    action = form.get('action')
    
    if action == 0:#添加数据
        book = Book()
        book.book_title = form.get('book_title')
        book.book_type = form.get('book_type')
        book.book_price = form.get('book_price')
        book.book_author = form.get('book_author')
        book.book_publisher = form.get('book_publisher')
        book.book_number = form.get('book_number')
        book.admin_id = form.get('admin_id')
        db.session.add(book)
        db.session.commit()
        return {
        'code':200 ,  
        'message': '添加成功',
        }
    elif action==1:#修改数据
        book_id = form.get('book_id')
        book = Book.query.get(book_id)
    
        if book is None:
            # 如果没有找到对应的book_id，报错
            return {
                'code':500,
                'message':"未找到图书"
            }
        else:
            
        # 更新或设置book的信息
            book.book_title = form.get('book_title')
            book.book_type = form.get('book_type')
            book.book_price = form.get('book_price')
            book.book_author = form.get('book_author')
            book.book_publisher = form.get('book_publisher')
            book.book_number = form.get('book_number')
            book.admin_id = form.get('admin_id')
    
            db.session.add(book)
            db.session.commit()

            return {
                'status': 'success',
                'message': '修改成功',
            }
    
    else:   #删除数据
        book_id = form.get('book_id')
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()

        return {
            'status': 'success',
            'message': '删除成功',
        }

#使用接口5以及接口6注意事项：接口6首先从前端获取到email，随后发送验证码，将验证码返回给前端，前端收到后，将所有学生输入的数据以及前端从后端得到的验证码发回给后端接口5进行验证
#五、学生注册接口
@app.route('/signUp/', methods=['POST'])
def sign_up():
    form = request.json
    print(form)
    student_id = form.get('student_id')
    student_email = form.get('student_email')
    student_password = form.get('student_password')
    student_name = form.get('student_name')
    verify = form.get('verify')#这是用户输入验证码
    verification_code = form.get('verify_code')#这是前端从后端得到的验证码

    if verify == verification_code:
        new_student = Student()
        new_student.student_email = student_email
        new_student.student_id = student_id
        new_student.student_name = student_name
        new_student.student_password =student_password
        db.session.add(new_student)
        db.session.commit()
        return {
            'code':200,
            'message':'注册成功'
        }
    else:
        return {
            'code':500,
            'message':'注册失败'
        }
        
#六、发送验证码接口
@app.route('/verify/', methods=['POST'])
def send_verification_code():
    form = request.json
    email = form.get('student_email')
    #生成验证码
    code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    smtp_server = 'smtp.qq.com'
    smtp_port = 587
    smtp_username = '485484849@qq.com'
    smtp_password = 'ddvgvjucfrxkbjdj'

    message = MIMEText(f'Your verification code is: {code}')
    message['Subject'] = 'Verification Code'
    message['From'] = '485484849@qq.com'
    message['To'] = email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(message)
    server.quit()
    return {
        'code':200,
        'message':'发送验证码成功',
        'verify':code
    }


#七、学生信息接口
@app.route('/studentInformation/',methods=['GET'])
def get():
    student_name = request.args.get('student_name',None)
    # 检查请求中是否包含token
    token = request.headers.get('token')
    if not token:
        return {
            'code':500,
            'message':'您没有权限'
            }
    # 验证token是否有效
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {
        'code':500,
        'message':'token验证失败'
        }
    except jwt.InvalidTokenError:
        return {
        'code':500,
        'message':'token验证失败'
        }
    
    if not student_name:
        query = db.session.query(Student)
        students = query.all()
        if students is None:
            return {
            'code': '404',
            'message': '未找到数据'
        }
        else:
            results = [
                {
                    'student_id': student.student_id,
                    'student_name':student.student_name,
                    'student_password':student.student_password,
                    'student_email':student.student_email
                } for student in students
            ]
        
            return {
                'code': 200,
                'tip':0,
                'results': results,
                'message': '查询成功'
            } 
    print(student_name)
    students = db.session.query(Student).filter((Student.student_name.like(f'%{student_name}%')))
    print(students)
    if students is None:
            return {
            'code': '404',
            'message': '未找到数据'
        }
    else:
        results = [
                {
                    'student_id': student.student_id,
                    'student_name':student.student_name,
                    'student_password':student.student_password,
                    'student_email':student.student_email
                } for student in students
            ]
        
        return {
                'code': 200,
                'results': results,
                'message': '查询成功'
            }


#八、查询借阅记录接口
class AdminGetInformationApi(MethodView):
    def get(self,student_id):
        # 检查请求中是否包含token
        token = request.headers.get('token')
        if not token:
            return {
                'code':500,
                'message':'您没有权限'
                }
        # 验证token是否有效
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {
            'code':500,
            'message':'token验证失败'
            }
        except jwt.InvalidTokenError:
            return {
            'code':500,
            'message':'token验证失败'
            }
            
        if not student_id:
            query = db.session.query(StudentRead)
            books = query.all()
            if books is None:
                return {
                    'code': '404',
                    'message': '没有找到记录'
                }
            else:
                results = [
                {
                    "book_id" : book.book_id,
                    "book_title" : book.book_title,
                    "book_type" : book.book_type,
                    "book_price" : book.book_price,
                    "book_author" : book.book_author,
                    "book_publisher" : book.book_publisher,
                    "admin_id" : book.admin_id,
                    "book_number" : book.book_number,
                    "read_time" : book.read_time,
                    "back_time" : book.back_time,
                    "student_id" : book.student_id,
                    "read_id":book.read_id
                } for book in books
                ]
            
                return {
                    'code': 200,
                    'tip':0,
                    'results': results,
                    'message': '查询成功'
                }
        else:
            books = db.session.query(StudentRead).filter_by(student_id=student_id).all()
            if books is None:
                return {
                    'code': '404',
                    'message': '没有找到记录'
                }
            else:
                results = [
                {
                    "book_id" : book.book_id,
                    "book_title" : book.book_title,
                    "book_type" : book.book_type,
                    "book_price" : book.book_price,
                    "book_author" : book.book_author,
                    "book_publisher" : book.book_publisher,
                    "admin_id" : book.admin_id,
                    "book_number" : book.book_number,
                    "read_time" : book.read_time,
                    "back_time" : book.back_time,
                    "student_id" : book.student_id,
                    "read_id":book.read_id
                } for book in books
                ]
            
                return {
                    'code': 200,
                    'tip':0,
                    'results': results,
                    'message': '查询成功'
                }
admingetinformation_view = AdminGetInformationApi.as_view('admingetinformation_api')
app.add_url_rule('/readInformation/', defaults={'student_id': None}, view_func=admingetinformation_view, methods=['GET'])
app.add_url_rule('/readInformation/<int:student_id>', view_func=admingetinformation_view, methods=['GET'])

# 根据学生id获取学生全部属性 
@app.route('/getStudent/', methods=['GET'])
def get_student():
    # 获取请求参数中的学生 id
    student_id = request.args.get('student_id', None)

    # 如果没有提供学生 id，则返回错误信息
    if not student_id:
        return {
            'code': 400,
            'message': '缺少学生 id'
        }

    # 查询学生信息
    student = Student.query.get(student_id)

    # 如果没有找到学生，则返回错误信息
    if not student:
        return {
            'code': 404,
            'message': '没有找到学生'
        }

    # 创建结果对象
    result = {
        "student_id": student.student_id,
        "student_name": student.student_name,
        "student_email": student.student_email,
        "student_password": student.student_password
    }

    # 返回成功信息和学生信息
    return {
        'code': 200,
        'result': result,
        'message': '查询成功'
    }


if __name__ == '__main__':
    app.run(debug=True)
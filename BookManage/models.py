from extension import db
from sqlalchemy import Table, MetaData

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    book_title = db.Column(db.String(255),nullable=False)
    book_type = db.Column(db.String(255),nullable=False)
    book_price = db.Column(db.Float,nullable=False)
    book_author = db.Column(db.String(255))
    book_publisher = db.Column(db.String(255))
    admin_id = db.Column(db.Integer)
    book_number = db.Column(db.Integer,nullable = False)

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.String(255),primary_key=True)
    student_name = db.Column(db.String(255),nullable=False)
    student_email = db.Column(db.String(255),nullable = False)
    student_password = db.Column(db.String(255),nullable=  False)
    
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer,primary_key=True)
    admin_name = db.Column(db.String(255),nullable=False)
    admin_password = db.Column(db.String(255),nullable = False)

class Read(db.Model):
    __tablename__ = 'read'
    student_id = db.Column(db.String(255),primary_key=True)
    book_id = db.Column(db.Integer,primary_key=True)
    read_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    read_time = db.Column(db.DateTime,nullable = False)
    back_time = db.Column(db.Date,nullable=False)
    

class StudentRead(db.Model):
    __tablename__ = 'student_read'
    read_id = db.Column(db.Integer,primary_key = True)
    book_id = db.Column(db.Integer,primary_key=True)
    book_title = db.Column(db.String(255),nullable=False)
    book_type = db.Column(db.String(255),nullable=False)
    book_price = db.Column(db.Float,nullable=False)
    book_author = db.Column(db.String(255))
    book_publisher = db.Column(db.String(255))
    admin_id = db.Column(db.Integer)
    book_number = db.Column(db.Integer,nullable = False)
    read_time = db.Column(db.DateTime,nullable = False)
    back_time = db.Column(db.Date,nullable=False)
    student_id = db.Column(db.String(255))
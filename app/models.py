from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    application = db.relationship('Application', backref='student', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False) 
    mobile_number = db.Column(db.String(10), nullable=False)
    academic_background = db.Column(db.Text, nullable=False)
    id_proof_path = db.Column(db.String(200), nullable=True) 
    degree_certificate_path = db.Column(db.String(200), nullable=True)  
    status = db.Column(db.String(20), default='pending', nullable=False)

# class Application(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'), unique=True, nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     dob = db.Column(db.Date, nullable=False)  # New Field
#     academic_background = db.Column(db.String(200), nullable=False)
#     id_proof_path = db.Column(db.String(200), nullable=True)  # New Field
#     degree_certificate_path = db.Column(db.String(200), nullable=True)  # New Field
#     status = db.Column(db.String(20), default='pending')

#     student = db.relationship('Student', back_populates='application')

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    # First, try loading as Admin
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin

    # Otherwise, try loading as Student
    return Student.query.get(int(user_id))

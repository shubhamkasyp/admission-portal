from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo,Regexp
from flask_wtf.file import FileField, FileAllowed

class ApplicationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number',validators=[DataRequired(),Regexp(r'^\d{10}$', message="Enter a valid 10-digit mobile number")])
    academic_background = TextAreaField('Academic Background', validators=[DataRequired()])
    id_proof = FileField('Upload ID Proof (PDF)', validators=[DataRequired(), FileAllowed(['pdf'], 'PDF files only!')])
    degree_certificate = FileField('Upload Degree Certificate (PDF)', validators=[DataRequired(), FileAllowed(['pdf'], 'PDF files only!')])
    submit = SubmitField('Submit Application')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

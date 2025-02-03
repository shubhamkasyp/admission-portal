from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, send_file,current_app
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import Student, Application, Admin
from app.forms import ApplicationForm, LoginForm
from app.utils import generate_admission_letter, admin_required
import os

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def home():
    form = ApplicationForm()    
    if form.validate_on_submit():
        # Check if student already exists
        existing_student = Student.query.filter_by(email=form.email.data).first()
        
        if existing_student:
            flash("Student already exists! Please use a different email.", "warning")
            return redirect(url_for('main.home'))

        # If student does not exist, create a new record
        student = Student(email=form.email.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.flush()  # Assigns an ID to the student before committing

        application = Application(
            student=student,
            name=form.name.data.upper(),
            dob=form.dob.data,
            mobile_number=form.mobile_number.data,
            academic_background=form.academic_background.data
        )
        
        # Handle ID Proof Upload
        if form.id_proof.data:
            id_filename = f"id_proof_{student.id}.pdf"
            form.id_proof.data.save(os.path.join('static', 'uploads', id_filename))
            application.id_proof_path = id_filename
        db.session.add(application)
        
        # Handle Degree Certificate Upload
        if form.degree_certificate.data:
            degree_filename = f"degree_{student.id}.pdf"
            form.degree_certificate.data.save(os.path.join('static', 'uploads', degree_filename))
            application.degree_certificate_path = degree_filename

        db.session.add(application)
        try:
            db.session.commit()
            flash("Your application has been submitted successfully!", "success")
            return redirect(url_for('main.student_login'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while submitting your application. Please try again.", "danger")

    return render_template('home.html', form=form)



@bp.route('/login', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        # Print the user class for debugging
        print(f"Current user: {current_user.__class__.__name__}") 
        # if isinstance(current_user, Admin):
        #     return redirect(url_for('main.admin_dashboard'))  # Admin login
        return redirect(url_for('main.student_dashboard'))  # Student login

    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()  
        if user and user.check_password(form.password.data):
            login_user(user)
            # Redirect based on user type
            if isinstance(user, Admin):
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.student_dashboard'))
        
        flash('Invalid email or password', 'danger')
    
    return render_template('student_login.html', form=form)


@bp.route('/student/dashboard')
@login_required
def student_dashboard():
    if isinstance(current_user, Student):  # Ensure the current user is a Student
        if current_user.application:  # Check if the student has an application
            return render_template('student_dashboard.html', application=current_user.application)
        else:
            flash("You don't have an application yet.", "warning")
            return redirect(url_for('main.home'))  # Redirect to the home page if no application exists
    else:
        flash("Student doesn't Exist. Please fill the details","warning")
        return redirect(url_for('main.home'))
    # else:
    #     flash("Admins cannot access the student dashboard.", "warning")
    #     return redirect(url_for('main.admin_dashboard'))  # Redirect Admin to the home page

from flask import send_file, flash, redirect, url_for
import os

@bp.route('/view_document/<int:application_id>/<document_type>')
@admin_required
def view_document(application_id, document_type):
    application = Application.query.get_or_404(application_id)

    # Check which document type to serve
    if document_type == 'id_proof':
        document_path = application.id_proof_path
    elif document_type == 'degree_certificate':
        document_path = application.degree_certificate_path
    else:
        flash("Invalid document type.", "danger")
        return redirect(url_for('main.admin_dashboard'))

    # Check if the document path is available
    if not document_path:
        flash("No document found for this application.", "warning")
        return redirect(url_for('main.admin_dashboard'))

    # Construct the absolute file path
    document_file_path = os.path.join(os.getcwd(), 'static', 'uploads', document_path)

    # Debugging: Print and check if file exists
    print("Document path being accessed:", document_file_path)

    # Check if the file exists
    if not os.path.exists(document_file_path):
        flash("File not found! It may have been deleted or moved.", "danger")
        return redirect(url_for('main.admin_dashboard'))

    # Serve the document for download
    return send_file(document_file_path, as_attachment=False)

@bp.route('/download_admission_letter')
@login_required
def download_admission_letter():
    if isinstance(current_user, Student) and current_user.application.status == 'approved':
        # Generate or get the admission letter path
        pdf_path = generate_admission_letter(current_user.application)

        # Check if the file exists before sending
        if not os.path.exists(pdf_path):
            flash("Admission letter could not be generated. Please try again later.", "danger")
            return redirect(url_for('main.student_dashboard'))

        # Return the PDF as a downloadable file
        return send_file(pdf_path, as_attachment=True)

    flash("Only students with approved applications can download the admission letter.", "danger")
    return redirect(url_for('main.student_dashboard'))


@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))  # Redirect to admin dashboard if already logged in
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.email.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('main.admin_dashboard'))  # Redirect admin to their dashboard
        flash('Invalid username or password', 'danger')
    return render_template('admin_login.html', form=form)

@bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    applications = Application.query.all()
    return render_template('admin_dashboard.html', applications=applications)

@bp.route('/admin/review/<int:application_id>', methods=['GET', 'POST'])
@admin_required
def review_application(application_id):
    application = Application.query.get_or_404(application_id)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'approve':
            application.status = 'approved'
        elif action == 'reject':
            application.status = 'rejected'
        db.session.commit()
        flash(f'Application {action}d successfully', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('review_application.html', application=application)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

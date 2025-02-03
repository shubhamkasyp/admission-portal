from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from fpdf import FPDF
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.student_login'  # Make sure this is pointing to the student login


    # Lazy import to avoid circular import issues
    with app.app_context():
        from app import routes
        app.register_blueprint(routes.bp)

    return app



def create_admin():
    from app.models import Admin  # Import inside function to avoid circular import issues
    admin_email = 'admin@example.com'
    admin_password = 'admin123'   

    with app.app_context():
        admin = Admin.query.filter_by(username=admin_email).first()
        if admin is None:
            admin = Admin(username=admin_email)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user {admin_email} created.")
        else:
            print("Admin user already exists.")


# For generating Admission letter 
def generate_admission_letter(application):
    # Define a proper file path
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Get absolute directory of current script
    folder_path = os.path.join(base_dir, "static", "admission_letters")  # Ensure proper directory structure
    os.makedirs(folder_path, exist_ok=True)  # Create directory if it doesn't exist

    file_path = os.path.join(folder_path, f"admission_letter_{application.id}.pdf")  # Full path to the PDF

    # Create a PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Admission Letter", ln=True, align="C")
    pdf.ln(10)  # Line break

    # Body
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Dear {application.name},\n\n"
                          f"We are pleased to inform you that your application has been approved.\n\n"
                          f"Academic Background: {application.academic_background}\n\n"
                          f"Please keep this letter for your records.\n\n"
                          f"Best regards,\n"
                          f"NPTEL Office")

    # Save the PDF
    pdf.output(file_path)

    return file_path  # Return the correct path

# Create the app
app = create_app()

# Create the admin user within the app context
with app.app_context():
    db.create_all()  # Ensure all tables are created
    create_admin()
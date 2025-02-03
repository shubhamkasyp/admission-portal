from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import Admin
import os
from fpdf import FPDF

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Ensure that the user is authenticated and is an instance of Admin
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            abort(403)  # Forbidden error if not an admin
        return f(*args, **kwargs)
    return decorated_function



def generate_admission_letter(application):
    # Define a proper file path
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Get absolute directory of the script
    folder_path = os.path.join(base_dir, "static", "admission_letters")  # Correct folder path
    os.makedirs(folder_path, exist_ok=True)  # Ensure the directory exists

    file_path = os.path.join(folder_path, f"admission_letter_{application.id}.pdf")  # Define the file path correctly

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

    return file_path  # Return the correct absolute file path

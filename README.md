# Student Admission System

A web application built using Flask for managing student admission processes. This system allows students to submit applications, view application statuses, and download admission letters once approved. Admins can review applications, approve or reject them, and access uploaded documents.

---

## 📦 Project Setup

### Step 1️⃣: Download the Project
1. **Download** the ZIP file of this project to your local machine.
2. **Extract** the contents into a folder on your local machine.

### Step 2️⃣: Install Dependencies
1. Open **Visual Studio Code (VS Code)**.
2. Open the terminal in VS Code by navigating to **Terminal > New Terminal**.
3. Install all the required dependencies by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

### Step 3️⃣: Start the Flask Server
1. In the terminal, navigate to the **root directory** of the project where `main.py` is located.
2. Run the following command to start the Flask server:

    ```bash
    python main.py
    ```

3. Once the server starts, you should see an HTTP link in the terminal. Click on it, and the application will open in your browser.

---

## 🔑 Login Credentials

### Admin Login:
- **Email:** `admin@example.com`
- **Password:** `admin123`

Once logged in as an **Admin**, you can:
- View all submitted applications.
- View uploaded documents for each application.
- Review applications and **approve** or **reject** them.

---

### Student Login:
- **Student 1 Credentials:**
  - **Email:** `shubham@gmail.com`
  - **Password:** `shubham123`
  
- **Student 2 Credentials:**
  - **Email:** `amit@gmail.com`
  - **Password:** `amit123`

After logging in as a **Student**, you can:
- View your **profile details**.
- Check your **application status**.
- Download the **admission letter** once approved by the admin.

---

## 🚀 Features

### For Students:
- **Submit applications** with personal details and documents.
- View the **status** of submitted applications.
- **Download admission letters** after admin approval.

### For Admins:
- **Review all student applications**.
- View **documents uploaded by students** (e.g., ID Proof, Degree Certificate).
- Approve or reject applications based on the review.
- Manage student profiles and their application statuses.

---

## 🛠️ Technologies Used

- **Python**: The primary programming language for the application.
- **Flask**: Web framework used to build the application.
- **SQLite**: Database to store student and application data.
- **Jinja2**: Templating engine used in Flask for dynamic HTML rendering.

---

## 🤝 Contributing

If you'd like to contribute to this project, feel free to fork it and submit a pull request. Please ensure that your changes are well-documented and that the project runs without errors after your modifications.

---

## 🖥️ Acknowledgements

- **Flask Documentation**: For guiding the development of the application.
- **SQLite Documentation**: For providing useful database management tips.
- **VS Code**: For being a great IDE for Python development.

---

## 📬 Contact

For any questions or issues, feel free to contact me at [shubhamkasyapreal@gmail.com]

---

Happy coding and enjoy using the Student Admission System! 🎉

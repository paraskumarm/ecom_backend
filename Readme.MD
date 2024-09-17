# E-Commerce Project Setup

## Backend Setup

1. **Create a Virtual Environment**:
   - On Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

2. **Install Dependencies**:
   - Run the following command to install all required dependencies:
     ```bash
     pip3 install -r requirements.txt
     ```
   - If this doesn't work, install dependencies manually one by one from `requirements.txt` using:
     ```bash
     pip3 install <package_name>
     ```

3. **Run the Backend Server**:
   - Start the Django server:
     ```bash
     python3 manage.py runserver
     ```

---

## Frontend Setup

1. **Install Dependencies**:
   - Navigate to the frontend project directory and run:
     ```bash
     npm install
     ```

2. **Start the Frontend**:
   - To start the frontend, run:
     ```bash
     npm start
     ```

---

## Notes
- Ensure both backend and frontend servers are running for full functionality.
- For any issues related to dependencies, refer to `requirements.txt` for the backend and `package.json` for the frontend.

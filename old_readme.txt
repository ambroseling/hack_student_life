# Hack Student Life

A web application for managing student events at UofT, built with Flask and React.

## Running the Application

### Backend Setup (Flask)

1. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   export FLASK_APP=backend/app.py
   cd backend
   flask run
   ```
   Server will run on http://localhost:8080

### Frontend Setup (React)

1. Install dependencies:
   ```bash
   cd frontend/hack_student_life_gui
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```
   Frontend will run on http://localhost:3000

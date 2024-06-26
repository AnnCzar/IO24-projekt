# IO24 Project - Face Motion Monitor
An application for monitoring changes in facial expressions in Parkinson's disease.

## Features
The application supports tracking of neurological disorder progression in Parkinson's disease by monitoring facial muscle mobility.
- Patient and doctor management.
- Report generation with results and examination history.

## Technology Stack
- React.js, 
- Django, 
- MySQL,
- Material-UI.

## Running Instructions

### Prerequisites
Ensure you have the following installed on your machine:
- min Python 3.8
- Node.js
- npm (Node Package Manager)
- MySQL

## Backend Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/AgnBrd/IO24-projekt.git
   cd <repository-directory>
   ```
2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   ```
3. **Activate the Virtual Environment**
   
   - On Windows:
   ```sh
   venv\Scripts\activate
   ```
   - On macOS and Linux:
   ```sh
   source venv/bin/activate
   ```
4. **Install Backend Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
5. **Set Up the Database**
   - Ensure MySQL server is running.
   - Create a database for the project. 
   - Update the database configuration in settings.py.
6. **Apply Migrations**
   ```sh
   python manage.py migrate
   ```
7. **Run the Backend Server**
   ```sh
   python manage.py runserver
   ```
## Frontend Setup
1. **Navigate to the Frontend Directory
   ```sh 
   cd frontend
   ```
2. **Install Frontend Dependencies**
   ```sh 
   npm install
   npm run build
   ```
3. **Run the Frontend Server**
   ```sh 
   npm start
   ```
## Viewing API Documentation
The application uses Swagger to generate API documentation. To view the API documentation:
1. Ensure the backend server is running.
2. Open a web browser and navigate to http://localhost:8000/swagger/.


## Authors

- Agnieszka - [GitHub](https://github.com/AgnBrd)
- Anna - [GitHub](https://github.com/AnnCzar)
- Julia - [GitHub](https://github.com/slovik02)
- Marta - [GitHub](https://github.com/mpruc)
- Laura - [GitHub](https://github.com/268312)
- Paulina - [GitHub](https://github.com/268310)

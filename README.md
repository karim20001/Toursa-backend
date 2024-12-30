# Tour Ticket Booking System

## Overview
This project is a backend system for buying tour tickets, featuring payment integration with the Zarinpal gateway. It provides APIs to manage available and unavailable tours, as well as to handle user tour purchases.

## Features
- **Browse Tours**: API to fetch all available and unavailable tours.
- **Purchase Tours**: API to securely buy tickets for tours.
- **Payment Gateway Integration**: Integration with Zarinpal for secure payments.
- **User Dashboard**: API to display tours purchased by the user.

## Prerequisites
- [Python](https://www.python.org/) (version 3.8 or higher)
- [Docker](https://www.docker.com/) (for containerized deployment)
- [Zarinpal Developer Account](https://www.zarinpal.com/) (for payment gateway integration)
- A database system (e.g., PostgreSQL, MySQL, or SQLite)

## Installation
### Using Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tour-ticket-backend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd tour-ticket-backend
   ```
3. Build the Docker image:
   ```bash
   docker build -t tour-ticket-backend .
   ```
4. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env --name tour-ticket tour-ticket-backend
   ```
5. The API will be available at:
   ```
   http://localhost:8000
   ```

### Without Docker
1. Create a virtual environment:
   ```bash
   python -m venv env
   ```
2. Activate the virtual environment:
   - **On Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source env/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. The API will be available at:
   ```
   http://localhost:8000
   ```

## Configuration
1. Create a `.env` file in the project root directory.
2. Add the following environment variables:
   ```env
   ZARINPAL_MERCHANT_ID=your_zarinpal_merchant_id
   DATABASE_URL=your_database_connection_string
   SECRET_KEY=your_secret_key
   ```
## Tech Stack
- **Language**: Python
- **Framework**: Django/Flask (depending on your choice)
- **Database**: PostgreSQL/MySQL/SQLite (choose based on your preference)
- **Payment Gateway**: Zarinpal API
- **Containerization**: Docker

## Roadmap
- Add user authentication and authorization.
- Implement API versioning.
- Introduce search and filtering for tours.
- Add rate limiting to APIs.

## Contributing
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add your feature description'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

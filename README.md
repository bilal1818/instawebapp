# Video Sharing Platform

A scalable, cloud-native web application for sharing videos and photos, built with Django and designed for Microsoft Azure deployment.

## Features

- Role-based authentication (creators and consumers)
- Upload and view videos/photos with metadata
- Comment and rate content
- Browse and search functionality
- RESTful API with token authentication

## Setup Instructions (Windows)

### Prerequisites

- Python 3.8+ installed
- Git installed
- MySQL client installed

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd video_sharing_platform
   ```

2. Activate the existing virtual environment:
   ```
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Database Setup

The application now uses MySQL with Azure Database for MySQL:

1. Make sure MySQL client libraries are installed on your system
   - Windows: Download and install from MySQL website or use package manager

2. Run the setup script:
   ```
   # PowerShell
   .\setup_mysql.ps1
   
   # Bash (if using WSL or Git Bash)
   ./setup_mysql.sh
   ```

3. Run the development server:
   ```
   python manage.py runserver
   ```

4. Access the application at http://127.0.0.1:8000/

## Project Structure

- `core/`: Main application with models, views, and API logic
- `users/`: User authentication and management
- `templates/`: HTML templates with base.html
- `static/`: Static files (CSS, JavaScript)
- `media/`: User-uploaded content

## Development Notes

- MySQL is used for both development and production
- Azure MySQL is configured for production deployment
- For full cloud setup, Azure Blob Storage and Cache for Redis are recommended

## License

MIT 
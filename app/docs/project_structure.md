# Smart AI Gym Trainer

A web application for real-time exercise tracking and nutrition assistance using computer vision and AI.

## Project Structure

The project follows a modular structure for better organization and maintainability:

```
Smart-AI-Gym-Trainer/
│
├── app/                          # Main application directory
│   ├── __init__.py               # Makes app a Python package
│   ├── app.py                    # Main Flask application factory
│   │
│   ├── backend/                  # Backend code
│   │   ├── __init__.py
│   │   ├── api/                  # API routes and endpoints
│   │   │   ├── __init__.py
│   │   │   └── routes.py         # Flask routes
│   │   │
│   │   ├── config/               # Configuration
│   │   │   ├── __init__.py
│   │   │   └── config.py         # App configuration
│   │   │
│   │   ├── exercise_modules/     # Exercise tracking modules
│   │   │   ├── __init__.py
│   │   │   ├── exercise_tracker.py  # Exercise tracking logic
│   │   │   └── pose_detector.py     # Pose detection with MediaPipe
│   │   │
│   │   ├── models/               # Data models
│   │   │   └── __init__.py
│   │   │
│   │   └── utils/                # Utility functions
│   │       └── __init__.py
│   │
│   ├── database/                 # Database connection and queries
│   │   └── db_connect.py         # Database connector
│   │
│   ├── docs/                     # Documentation
│   │
│   └── frontend/                 # Frontend code
│       ├── static/               # Static files
│       │   ├── css/              # Stylesheets
│       │   ├── images/           # Images
│       │   ├── js/               # JavaScript files
│       │   └── gifs/             # Exercise demonstration GIFs
│       │
│       └── templates/            # HTML templates
│
├── run.py                        # Application entry point
└── requirements.txt              # Project dependencies
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Preethamn15/Smart-AI-Gym-Trainer.git
cd Smart-AI-Gym-Trainer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python run.py
```

4. Open your browser and navigate to http://127.0.0.1:5000

## Features

- Real-time exercise tracking using computer vision
- Form correction and exercise suggestions
- Exercise rep counting
- Personalized fitness plans
- Meal planning assistance
- Progress tracking

## Technologies Used

- Python 3.9+
- Flask for web server
- OpenCV and MediaPipe for computer vision
- HTML, CSS, JavaScript for frontend
- MySQL for database

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Preetham N
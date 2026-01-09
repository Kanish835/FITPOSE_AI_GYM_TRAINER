<h1 align="center">🤖 AI Gym Trainer</h1>
<h3 align="center">Your Smart Workout & Nutrition Assistant</h3>

<p align="center">
  <img src="app/frontend/static/images/demo.gif" width="600"/><br>
  <b>Real-Time Exercise Tracking · Posture Feedback · AI Nutrition Planner</b>
</p>

---

## Overview

AI Gym Trainer is an all-in-one smart fitness platform designed to revolutionize home and personal workouts using the power of Artificial Intelligence and Computer Vision. This intelligent system offers real-time monitoring of exercises, automated posture correction feedback, and advanced dietary analysis—making it a comprehensive virtual gym assistant.

Whether you're a beginner looking for guidance, a student working on a final year project, or a fitness enthusiast aiming to optimize your training, this platform is built to help you achieve your goals with minimal equipment and maximum efficiency.

---

## Project Structure

The project now follows a modular, organized structure for better maintainability:

```
Smart-AI-Gym-Trainer/
│
├── app/                          # Main application directory
│   ├── backend/                  # Backend code
│   │   ├── api/                  # API routes and endpoints
│   │   ├── config/               # Configuration
│   │   ├── exercise_modules/     # Exercise tracking modules
│   │   ├── models/               # Data models
│   │   └── utils/                # Utility functions
│   │
│   ├── database/                 # Database connection and queries
│   ├── docs/                     # Documentation
│   │
│   └── frontend/                 # Frontend code
│       ├── static/               # Static files (CSS, JS, images)
│       └── templates/            # HTML templates
│
├── run.py                        # Application entry point
└── requirements.txt              # Project dependencies
```

For more detailed information about the structure, see [Project Structure Documentation](app/docs/project_structure.md).

---

## Features

-  **Live Exercise Tracking** – Detects 7 exercises using computer vision (e.g., squats, push-ups, dumbbell curls, alternative dumbbell curls).
-  **Posture Feedback** – Real-time form evaluation: `Good Posture ` or `Fix Your Form `.
-  **Food Recognition** – YOLOv5 model estimates nutrition from camera-captured food images.
-  **Health Metrics** – Calculates BMI, BMR, and stores data in a MySQL database.
-  **Personalized Fitness Plan** – Tailored routines based on your body profile and goals.
-  **Meal Planner** – Smart meal suggestions for weight loss, muscle gain, or maintenance.
-  **AI Integration** – Uses deep learning & pose estimation for accurate analysis.
-  **MySQL Integration** – Logs workouts, meals, and progress for every user.

---

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Preethamn15/Smart-AI-Gym-Trainer-With-RealTime-Exercise-Tracking-and-Nutrition-Assistant.git
cd Smart-AI-Gym-Trainer-With-RealTime-Exercise-Tracking-and-Nutrition-Assistant
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

Alternatively, you can use the provided batch file:
```bash
start_app.bat
```

---

##  Tech Stack

| Area          | Technologies |
|---------------|--------------|
| Computer Vision | OpenCV, MediaPipe, YOLOv5 |
| AI/ML          | Custom Pose Estimation, Torch Models |
| Frontend/UI    | HTML, CSS, PHP (Web), Tkinter |
| Backend        | Python (Flask) |
| Database       | MySQL |
| IDE            | VS Code |

---

##  Use Cases

- Home workouts with real-time feedback
- Smart diet tracking using food detection
- Fitness planning for students, professionals & beginners
- Great Final Year Project with AI + ML integration

---
## Sample Screens & Demo
## 🎥 Demo Video – Full Walkthrough

[![Watch Demo](Videos%20and%20photos/thumbnail.jpg)](https://github.com/Preethamn15/Smart-AI-Gym-Trainer-With-RealTime-Exercise-Tracking-and-Nutrition-Assistant/raw/main/Videos%20and%20photos/be333e32-4dfb-4134-9203-f8fa997b441e.mov)

> 🔗 Click the image above download the `.mov` demo video you will get the full view of website.


###  AI Personalized Plan
<img src="Videos and photos/AI Personalized Plan.png" width="600"/>

###  Badges and Achievements
<img src="Videos and photos/Badges and Achivements.png" width="600"/>

###  Body Metrics Calculator
<img src="Videos and photos/Body Metrics Calculator.png" width="600"/>

### 🍽Macronutrient Calculator
<img src="Videos and photos/Macro nutrient calculator.png" width="600"/>

---


This is our final year project, and it includes all the trending technologies like AI and Deep Learning.
For 1st, 2nd, and 3rd-year students, this can be a great reference model to showcase in your college and score full marks.

## 📄 Research Paper

We have also published a research paper based on an earlier version of this project — feel free to check it out for reference.  
Since then, we've made significant improvements to the model.

 **[View Research Paper (PDF)](Paper/Paper%20published%20for%20reference.pdf)**


## Migration from Old Structure

If you're updating from the previous project structure, you can use the migration script to help organize your files:

```bash
python migrate_files.py
```

This script will copy files from the old structure to the new one while preserving the original files.

---

⚠️ Note: I won't be uploading the main folder and SQL file required to run the full model here.
📩 If you're interested in running the complete project, feel free to contact me — I'll provide all the necessary files and step-by-step guidance.


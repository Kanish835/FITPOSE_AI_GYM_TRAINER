"""
API Routes for the Smart AI Gym Trainer
--------------------------------------
This module defines all the routes for the application.
"""

from flask import render_template, Response, jsonify, request, redirect
import threading
import time
import cv2
import numpy as np
import os
from app.backend.exercise_modules.exercise_tracker import ExerciseTracker
from app.backend.exercise_modules.pose_detector import PoseDetector

# Global variables
camera = None
detector = None
exercise_type = None
rep_count = 0
is_running = False
lock = threading.Lock()
exercise_tracker = None

# Initial detected object for food recognition
detected_object = "None"

def generate_frames():
    """Generate video frames for streaming"""
    global camera, detector, exercise_type, rep_count, is_running
    last_processing_time = time.time()
    frame_interval = 1/30  # Target 30 FPS
    
    while True:
        current_time = time.time()
        
        # Skip processing if it's been less than the frame interval (prevents overloading CPU)
        if current_time - last_processing_time < frame_interval:
            time.sleep(0.001)  # Small sleep to prevent CPU hogging
            continue
            
        last_processing_time = current_time
        
        if not is_running:
            # If we're not tracking, just yield a blank frame
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Smaller blank frame
            cv2.putText(blank_frame, "Exercise tracking not active", (150, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            _, buffer = cv2.imencode('.jpg', blank_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.03)  # Slower refresh when inactive
            continue
        
        # Try to read frame with error handling
        try:    
            success, img = camera.read()
            if not success:
                time.sleep(0.01)
                continue  # Skip this iteration and try again
            
            # Lower resolution for better performance (640x480 instead of 1280x720)
            img = cv2.resize(img, (640, 480))
            
            # Detect pose
            img = detector.findPose(img, draw=True)
            lmList = detector.findPosition(img, draw=False)
            
            with lock:
                if exercise_tracker:
                    img = exercise_tracker.process_frame(img, lmList, detector)
                    rep_count = exercise_tracker.count
            
            # Encode with lower quality for faster streaming
            _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
        except Exception as e:
            print(f"Frame generation error: {e}")
            time.sleep(0.01)  # Small delay before retrying

def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/')
    def index():
        # Redirect root to home page
        return render_template('home_static.html')

    @app.route('/home')
    def home():
        # Serve the home page
        return render_template('home_static.html')

    @app.route('/Exercise.html')
    def exercise():
        return render_template('Exercise.html')

    @app.route('/exercise')
    def exercise_route():
        return render_template('Exercise.html')

    @app.route('/index.html')
    def original_index():
        # Keep access to original index.html if needed
        return render_template('index.html')

    @app.route('/guide.html')
    def guide():
        return render_template('guide.html')

    @app.route('/BMI.html')
    def bmi():
        # Serve the BMI calculator page
        return render_template('bmi_static.html')

    @app.route('/help.html')
    def help_page():
        # Serve the help page
        return render_template('help_static.html')
        
    @app.route('/meal-planner')
    def meal_planner():
        # Serve the meal planner page
        return render_template('meal_planner_static.html')
        
    @app.route('/personalized_plan.php')
    def personalized_plan():
        # Serve the personalized plan page
        return render_template('personalized_plan_static.html')
        
    @app.route('/workout_logs.php')
    def workout_logs():
        # Serve the workout logs page
        return render_template('workout_logs_static.html')
        
    @app.route('/dashboard.php')
    def dashboard():
        # Serve the dashboard page
        return render_template('dashboard_static.html')
        
    @app.route('/fitness_plan.php')
    def fitness_plan():
        # Serve the fitness plan page
        return render_template('fitness_plan_static.html')
        
    @app.route('/achievements.php')
    def achievements():
        # Serve the achievements page
        return render_template('achievements_static.html')
        
    @app.route('/about.php')
    def about():
        # Serve the about page
        return render_template('about_static.html')
        
    @app.route('/contact.php')
    def contact():
        # Serve the contact page
        return render_template('contact_static.html')
        
    @app.route('/profile.php')
    def profile():
        # Serve the profile page
        return render_template('profile_static.html')
        
    @app.route('/logout.php')
    def logout():
        # Redirect to home page for now
        return redirect('/')

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/start-exercise/<exercise>')
    def start_exercise(exercise):
        global camera, detector, exercise_type, is_running, exercise_tracker
        
        # Check if exercise type is valid
        valid_exercises = ["lateral-rise", "alt-dumbbell-curls", "barbell-row", 
                          "push-up", "squats", "shoulder-press", "tricep-dips"]
        
        if exercise not in valid_exercises:
            return jsonify(success=False, error=f"Unknown exercise: {exercise}")
        
        # Release any existing camera
        if camera is not None:
            camera.release()
            time.sleep(0.5)  # Allow time for camera to fully release
        
        # Initialize camera with specific settings for better performance
        camera = cv2.VideoCapture(0)
        
        # Set lower resolution for better performance
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 30)  # Target 30 FPS
        
        # Verify camera is working
        success, _ = camera.read()
        if not success:
            return jsonify(success=False, error="Could not access webcam. Please check your camera connection.")
        
        detector = PoseDetector()
        exercise_type = exercise
        
        with lock:
            exercise_tracker = ExerciseTracker(exercise)
            is_running = True
        
        return jsonify(success=True, message=f"Started {exercise} tracking")

    @app.route('/stop-exercise')
    def stop_exercise():
        global camera, is_running, rep_count
        
        with lock:
            is_running = False
            final_count = rep_count
            rep_count = 0
        
        if camera is not None:
            camera.release()
            camera = None
        
        return jsonify(success=True, message="Exercise tracking stopped", final_count=final_count)


    # API to get rep count and suggestion
    @app.route('/get-reps')
    def get_reps():
        with lock:
            count = rep_count
            suggestion = exercise_tracker.get_suggestion() if exercise_tracker else ""
            # Add form quality information
            form_quality = exercise_tracker.form_quality if exercise_tracker else "Neutral"
            is_wrong_exercise = form_quality == "Wrong Exercise"
        return jsonify(count=count, suggestion=suggestion, form_quality=form_quality, wrong_exercise=is_wrong_exercise)

    @app.route('/update', methods=['POST'])
    def update():
        global detected_object
        detected_object = request.json.get('object_name', 'None')
        return jsonify(success=True)

    @app.route('/get_object')
    def get_object():
        return jsonify(object_name=detected_object)
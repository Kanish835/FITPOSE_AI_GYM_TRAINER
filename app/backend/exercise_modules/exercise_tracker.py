"""
Exercise Tracker Class for tracking and analyzing different exercises.
"""

import cv2
import numpy as np

class ExerciseTracker:
    """
    A class for tracking and analyzing different exercises.
    
    This class provides functionality to:
    - Track repetitions for different exercises
    - Analyze form quality
    - Provide suggestions for improvement
    - Validate exercise movement patterns
    
    Attributes:
        exercise_type: The type of exercise being tracked
        count: The number of repetitions completed
        dir: Direction indicator for rep counting
        angle: Current angle at the key joint
        low: Lower threshold angle for rep counting
        high: Upper threshold angle for rep counting
        suggestion: Current form suggestion/feedback
        form_quality: Quality assessment of current form
    """
    
    def __init__(self, exercise_type):
        """
        Initialize the ExerciseTracker for a specific exercise.
        
        Args:
            exercise_type: The type of exercise to track
        """
        self.exercise_type = exercise_type
        self.count = 0
        self.dir = 0  # 0: not started, 1: going up/down
        self.angle = 0
        # Default range values - will be overridden based on exercise
        self.low = 70
        self.high = 160
        self.suggestion = ""
        self.form_quality = "Neutral"  # Can be "Good Form", "Bad Form", or "Neutral"
        self.rep_detected = False
        self.last_angle = 0
        self.confidence_threshold = 0.0  # For motion validation
        self.motion_history = []  # To track the pattern of movement
        
        # Set exercise-specific parameters
        self._configure_exercise_params()
        
    def _configure_exercise_params(self):
        """Set exercise-specific parameters like angles and thresholds"""
        if self.exercise_type == "push-up":
            self.low = 70
            self.high = 160
            self.confidence_threshold = 0.6
            # Points for push-ups: Left Shoulder (11), Left Elbow (13), Left Wrist (15)
            self.points = [11, 13, 15]
            
        elif self.exercise_type == "squats":
            self.low = 70
            self.high = 160
            self.confidence_threshold = 0.6
            # Points for squats: Left Hip (23), Left Knee (25), Left Ankle (27)
            self.points = [23, 25, 27]
            
        elif self.exercise_type == "shoulder-press":
            self.low = 60
            self.high = 170
            self.confidence_threshold = 0.7
            # Shoulder press points: Left Shoulder (11), Left Elbow (13), Left Wrist (15)
            self.points = [11, 13, 15]
            # Direction matters for shoulder press (vertical movement)
            self.vertical_movement = True
            
        elif self.exercise_type == "lateral-rise":
            self.low = 80
            self.high = 140
            self.confidence_threshold = 0.7
            # Points for lateral raise: Left Shoulder (11), Left Elbow (13), Left Wrist (15)
            self.points = [11, 13, 15]
            # Lateral raise requires specific sideways movement
            self.horizontal_movement = True
            
        elif self.exercise_type == "barbell-row":
            self.low = 70
            self.high = 150
            self.confidence_threshold = 0.6
            # Points for barbell row: Left Shoulder (11), Left Elbow (13), Left Wrist (15)
            self.points = [11, 13, 15]
            
        elif self.exercise_type == "tricep-dips":
            self.low = 70
            self.high = 160
            self.confidence_threshold = 0.6
            # Points for tricep dips: Left Shoulder (11), Left Elbow (13), Left Wrist (15)
            self.points = [11, 13, 15]
            
        elif self.exercise_type == "alt-dumbbell-curls":
            self.low = 50
            self.high = 160
            self.confidence_threshold = 0.7
            # Points for bicep curls: Left Shoulder (11), Left Elbow (13), Left Wrist (15)
            self.points = [11, 13, 15]
        else:
            # Default
            self.points = [11, 13, 15]
    
    def _validate_movement(self, lmList):
        """
        Validate that the movement matches the expected pattern for the exercise.
        
        Args:
            lmList: List of landmarks from pose detection
            
        Returns:
            bool: True if movement pattern is valid for the exercise, False otherwise
        """
        is_valid = True
        
        if self.exercise_type == "shoulder-press":
            # For shoulder press, check that wrists move significantly upward
            # Check if wrist is moving vertically above elbow
            if len(lmList) > 15:  # Ensure we have wrist and shoulder points
                wrist = lmList[15][1:3]  # Wrist position
                elbow = lmList[13][1:3]  # Elbow position
                shoulder = lmList[11][1:3]  # Shoulder position
                
                # Store motion history for shoulder press validation
                if not hasattr(self, 'wrist_y_history'):
                    self.wrist_y_history = []
                
                # Add current wrist Y position to history
                self.wrist_y_history.append(wrist[1])
                if len(self.wrist_y_history) > 10:
                    self.wrist_y_history.pop(0)
                
                # For shoulder press:
                # 1. Wrists must go above shoulders at the top
                # 2. Wrists must move vertically (not primarily horizontally like in bicep curls)
                # 3. Arms must extend fully overhead at the top position
                
                # Detect if movement pattern matches bicep curl
                # In bicep curls, wrist stays below shoulder height and moves toward shoulder
                if len(self.wrist_y_history) > 5:
                    # Check if wrist stays below shoulder level (typical for bicep curl)
                    if all(y > shoulder[1] for y in self.wrist_y_history):
                        is_valid = False
                        self.suggestion = "This looks like a bicep curl, not a shoulder press"
                
                # When at top position, wrist should be above shoulder for shoulder press
                if self.angle < 80:  # At the top position
                    if not (wrist[1] < shoulder[1]):
                        is_valid = False
                        self.suggestion = "Extend arms upward for shoulder press"
                
        elif self.exercise_type == "alt-dumbbell-curls":
            # For bicep curls, elbow should remain relatively fixed
            if len(lmList) > 15:
                shoulder = lmList[11][1:3]  # Shoulder position
                elbow = lmList[13][1:3]  # Elbow position
                wrist = lmList[15][1:3]  # Wrist position
                
                # Store elbow position history if not already done
                if not hasattr(self, 'elbow_position_history'):
                    self.elbow_position_history = []
                    
                # Add current elbow position to history
                self.elbow_position_history.append(elbow)
                if len(self.elbow_position_history) > 10:
                    self.elbow_position_history.pop(0)
                    
                # Calculate change in elbow position
                elbow_x_change = abs(elbow[0] - self.last_elbow_x) if hasattr(self, 'last_elbow_x') else 0
                
                # For curls, wrist should move toward shoulder while elbow stays fixed
                if elbow_x_change > 30:  # Elbow moving too much horizontally
                    is_valid = False
                    self.suggestion = "Keep elbow fixed for bicep curls"
                
                # Check if wrist goes above elbow (not typical in curls)
                if wrist[1] < elbow[1] - 50:  # Wrist significantly above elbow
                    is_valid = False
                    self.suggestion = "Keep wrist movement in front of body for curls"
                
                # Store current position for next comparison
                self.last_elbow_x = elbow[0]
                
        return is_valid

    def process_frame(self, img, lmList, detector):
        """
        Process a video frame to track exercise form and reps.
        
        Args:
            img: Input video frame
            lmList: List of landmarks from pose detection
            detector: PoseDetector instance
            
        Returns:
            img: Processed image with visualization
        """
        self.suggestion = ""  # Reset suggestion each frame
        self.form_quality = "Neutral"
        
        if not lmList or len(lmList) < 33:
            self.suggestion = "Make sure your body is visible to the camera."
            return img
            
        # Get the specific angle for this exercise using the configured points
        if len(self.points) == 3:
            self.angle = detector.findAngle(img, self.points[0], self.points[1], self.points[2])
        
        # Validate the movement pattern is correct for this exercise
        is_valid_movement = self._validate_movement(lmList)
        if not is_valid_movement:
            self.form_quality = "Wrong Exercise"
            if not self.suggestion:
                self.suggestion = f"This doesn't look like a {self.exercise_type.replace('-', ' ')}"
            return img  # Skip rep counting if wrong movement

        # Process specific exercise feedback
        if self.exercise_type == "push-up":
            if self.angle < 80:
                self.suggestion = "Bend your arms more to go lower!"
                self.form_quality = "Bad Form"
            elif self.angle > 150:
                self.suggestion = "Straighten your elbows at the top!"
                self.form_quality = "Good Form"
            elif self.angle > 90 and self.angle < 120:
                self.suggestion = "Keep your back straight, not too high or low"
                self.form_quality = "Good Form"
            else:
                self.suggestion = "Maintain controlled movement"
                self.form_quality = "Neutral"
                
        elif self.exercise_type == "squats":
            if self.angle < 80:
                self.suggestion = "Go deeper, bend your knees more"
                self.form_quality = "Good Form" 
            elif self.angle > 150:
                self.suggestion = "Stand tall, keep core engaged"
                self.form_quality = "Good Form"
            else:
                self.suggestion = "Keep knees aligned with toes"
                self.form_quality = "Neutral"
                
        elif self.exercise_type == "shoulder-press":
            if self.angle < 70:
                self.suggestion = "Lower the weights more, full range of motion"
                self.form_quality = "Good Form"
            elif self.angle > 160:
                self.suggestion = "Extend arms fully overhead"
                self.form_quality = "Good Form"
            else:
                self.suggestion = "Press weights directly overhead"
                self.form_quality = "Neutral"
                
        elif self.exercise_type == "lateral-rise":
            if self.angle < 90:
                self.suggestion = "Raise arms to shoulder height"
                self.form_quality = "Bad Form"
            elif self.angle > 110:
                self.suggestion = "Don't raise arms too high"
                self.form_quality = "Bad Form"
            else:
                self.suggestion = "Perfect height, maintain control"
                self.form_quality = "Good Form"
                
        elif self.exercise_type == "barbell-row":
            if self.angle < 80:
                self.suggestion = "Pull barbell closer to your body"
                self.form_quality = "Good Form"
            elif self.angle > 130:
                self.suggestion = "Lower the weight with control"
                self.form_quality = "Neutral"
            else:
                self.suggestion = "Keep your back straight"
                self.form_quality = "Good Form"
                
        elif self.exercise_type == "tricep-dips":
            if self.angle < 70:
                self.suggestion = "Go deeper for full tricep engagement"
                self.form_quality = "Good Form"
            elif self.angle > 150:
                self.suggestion = "Straighten arms completely at top"
                self.form_quality = "Good Form"
            else:
                self.suggestion = "Keep elbows close to body"
                self.form_quality = "Neutral"
                
        elif self.exercise_type == "alt-dumbbell-curls":
            if self.angle < 60:
                self.suggestion = "Curl the weight fully to shoulder"
                self.form_quality = "Good Form"
            elif self.angle > 160:
                self.suggestion = "Extend arm fully between reps"
                self.form_quality = "Good Form"
            else:
                self.suggestion = "Keep elbow fixed by your side"
                self.form_quality = "Neutral"
        else:
            # Generic fallback for any other exercise
            self.suggestion = "Maintain proper form throughout"
            self.form_quality = "Neutral"

        per = np.interp(self.angle, (self.low, self.high), (0, 100))
        bar = np.interp(self.angle, (self.low, self.high), (650, 100))

        # Only count reps if we've verified this is the correct exercise movement
        if self.form_quality != "Wrong Exercise":
            if per == 100:
                if self.dir == 1:
                    self.count += 1
                    self.dir = 0
            elif per == 0:
                if self.dir == 0:
                    self.dir = 1

        # Adjust UI for smaller 640x480 resolution
        
        # Draw simpler progress bar on the right side
        bar_height = np.interp(self.angle, (self.low, self.high), (350, 100))
        cv2.rectangle(img, (580, 100), (620, 350), (0, 255, 0), 2)
        cv2.rectangle(img, (580, int(bar_height)), (620, 350), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (560, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        # Display rep count in top-left
        cv2.putText(img, f'Reps: {int(self.count)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        # Display form quality with color coding
        form_color = (255, 255, 255)  # Default white for neutral
        if self.form_quality == "Good Form":
            form_color = (0, 255, 0)  # Green for good form
        elif self.form_quality == "Bad Form":
            form_color = (0, 0, 255)  # Red for bad form
        elif self.form_quality == "Wrong Exercise":
            form_color = (0, 0, 255)  # Red for wrong exercise
            
        # Display text based on form quality
        display_text = self.form_quality
        
        # Simplified form quality display - just text with colored background
        text_size = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_width = text_size[0] + 20  # Add padding
        
        # Draw background rectangle for text
        bg_color = (0, 0, 0)  # Default black background
        if self.form_quality == "Wrong Exercise":
            bg_color = (0, 0, 128)  # Darker red background for wrong exercise
        
        cv2.rectangle(img, 
                     (320 - text_width//2, 30), 
                     (320 + text_width//2, 70), 
                     bg_color, 
                     -1)  # Filled rectangle
                     
        # Draw the form quality text
        cv2.putText(img, 
                   display_text, 
                   (320 - text_size[0]//2, 58),  # Center text
                   cv2.FONT_HERSHEY_SIMPLEX, 
                   0.8, 
                   form_color, 
                   2)
                   
        # If wrong exercise is detected, also show a more prominent warning
        if self.form_quality == "Wrong Exercise":
            # Add a warning message at the bottom
            warning_text = f"Detected: Not {self.exercise_type.replace('-', ' ')}"
            warning_size = cv2.getTextSize(warning_text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
            
            # Warning at the bottom with transparent background
            cv2.rectangle(img, 
                         (320 - warning_size[0]//2 - 10, 420), 
                         (320 + warning_size[0]//2 + 10, 460), 
                         (0, 0, 80), 
                         -1)  # Filled rectangle
                         
            cv2.putText(img, 
                       warning_text, 
                       (320 - warning_size[0]//2, 450),  # Center text
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.9, 
                       (255, 255, 255), 
                       2)
        
        return img

    def get_suggestion(self):
        """
        Get the current form suggestion.
        
        Returns:
            str: Current suggestion for improving form
        """
        return self.suggestion
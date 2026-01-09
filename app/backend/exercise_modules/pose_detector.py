"""
PoseDetector Class for detecting and analyzing human poses using MediaPipe.
"""

import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    """
    A class for detecting and analyzing human poses using the MediaPipe library.
    
    This class provides methods to:
    - Detect pose landmarks in images
    - Find positions of specific landmarks
    - Calculate angles between landmarks
    
    Attributes:
        mp_pose: MediaPipe pose solution
        pose: Pose estimation model
        mp_draw: MediaPipe drawing utilities
    """
    
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True, 
                 enable_segmentation=False, smooth_segmentation=True):
        """
        Initialize the PoseDetector with MediaPipe pose detection.
        
        Args:
            mode: Whether to treat the input images as a batch or not.
            complexity: Model complexity (0=Lite, 1=Full, 2=Heavy)
            smooth_landmarks: Whether to filter landmarks across frames
            enable_segmentation: Whether to generate segmentation mask
            smooth_segmentation: Whether to filter segmentation mask across frames
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(mode, complexity, smooth_landmarks, 
                                      enable_segmentation, smooth_segmentation)
        self.mp_draw = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        """
        Detect pose in the input image.
        
        Args:
            img: Input image (BGR format)
            draw: Whether to draw landmarks on the image
            
        Returns:
            Image with pose landmarks drawn if draw=True
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, 
                                        self.mp_pose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        """
        Find the positions of all landmarks in the image.
        
        Args:
            img: Input image
            draw: Whether to draw circles at landmark positions
            
        Returns:
            List of landmarks with their positions [id, x, y]
        """
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        """
        Calculate the angle between three points (landmarks).
        
        Args:
            img: Input image
            p1: First point ID
            p2: Second point ID (middle/joint)
            p3: Third point ID
            draw: Whether to draw the angle on the image
            
        Returns:
            Angle in degrees
        """
        lmList = self.findPosition(img, draw=False)
        if lmList:
            # Get coordinates of the three points
            x1, y1 = lmList[p1][1], lmList[p1][2]
            x2, y2 = lmList[p2][1], lmList[p2][2]
            x3, y3 = lmList[p3][1], lmList[p3][2]

            # Calculate the angle
            angle = np.degrees(np.arctan2(y3 - y2, x3 - x2) - 
                              np.arctan2(y1 - y2, x1 - x2))
            angle = angle + 360 if angle < 0 else angle
            angle = angle if angle <= 180 else 360 - angle

            if draw:
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            return angle
        return 0
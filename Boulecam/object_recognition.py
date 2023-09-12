import cv2
import numpy as np
from typing import List, Dict, Tuple
from collections import namedtuple

# Define a BocciaBall as a namedtuple for easy access to properties
BocciaBall = namedtuple("BocciaBall", ["x", "y", "radius"])

class ObjectRecognition:
    def __init__(self):
        self.small_ball_color_range = ((0, 0, 0), (0, 0, 0))  # Set color range for small boccia ball
        self.large_ball_color_range = ((0, 0, 0), (0, 0, 0))  # Set color range for large boccia ball

    def detect_boccia_balls(self, image: np.ndarray) -> Tuple[BocciaBall, List[BocciaBall]]:
        """Detect boccia balls in the given image and return the small boccia ball and a list of large boccia balls"""
        small_ball = self._detect_ball(image, self.small_ball_color_range)
        large_balls = self._detect_balls(image, self.large_ball_color_range)
        return small_ball, large_balls

    def _detect_ball(self, image: np.ndarray, color_range: Tuple[Tuple[int, int, int], Tuple[int, int, int]]) -> BocciaBall:
        """Detect a single ball in the given image within the specified color range and return it as a BocciaBall"""
        # Convert the image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask for the specified color range
        mask = cv2.inRange(hsv, color_range[0], color_range[1])

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour and assume it is the ball
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate the center and radius of the ball
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)

        return BocciaBall(x, y, radius)

    def _detect_balls(self, image: np.ndarray, color_range: Tuple[Tuple[int, int, int], Tuple[int, int, int]]) -> List[BocciaBall]:
        """Detect multiple balls in the given image within the specified color range and return them as a list of BocciaBalls"""
        # Convert the image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask for the specified color range
        mask = cv2.inRange(hsv, color_range[0], color_range[1])

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the center and radius of each ball and add them to the list
        balls = [BocciaBall(*cv2.minEnclosingCircle(contour)) for contour in contours]

        return balls

    def measure_distances(self, small_ball: BocciaBall, large_balls: List[BocciaBall]) -> Dict[BocciaBall, float]:
        """Measure the distances between the small boccia ball and each of the large boccia balls and return them as a dictionary"""
        distances = {large_ball: self._distance(small_ball, large_ball) for large_ball in large_balls}
        return distances

    def _distance(self, ball1: BocciaBall, ball2: BocciaBall) -> float:
        """Calculate the distance between two balls"""
        return ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) ** 0.5

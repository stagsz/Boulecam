import cv2
import numpy as np
from typing import Tuple

class Calibration:
    def __init__(self):
        self.calibration_matrix = np.eye(3)
        self.distortion_coefficients = np.zeros(5)

    def calibrate(self, calibration_images: list[np.ndarray], board_size: Tuple[int, int], square_size: float):
        """Calibrate the camera using multiple images of a chessboard pattern"""
        # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        object_points = np.zeros((board_size[0] * board_size[1], 3), np.float32)
        object_points[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2) * square_size

        # Arrays to store object points and image points from all the images
        all_object_points = []
        all_image_points = []

        for image in calibration_images:
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, board_size, None)

            # If found, add object points, image points
            if ret:
                all_object_points.append(object_points)
                all_image_points.append(corners)

        # Calibrate the camera
        ret, self.calibration_matrix, self.distortion_coefficients, _, _ = cv2.calibrateCamera(all_object_points, all_image_points, gray.shape[::-1], None, None)

        return ret

    def undistort(self, image: np.ndarray) -> np.ndarray:
        """Undistort the given image using the calibration matrix and distortion coefficients"""
        return cv2.undistort(image, self.calibration_matrix, self.distortion_coefficients, None, self.calibration_matrix)

import cv2
import numpy as np
from typing import List, Dict
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

class ARVisualization(App):
    def __init__(self, object_recognition):
        super().__init__()
        self.object_recognition = object_recognition

    def build(self):
        self.layout = FloatLayout()
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)
        return self.layout

    def on_start(self):
        self.camera = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.camera.read()
        if ret:
            small_ball, large_balls = self.object_recognition.detect_boccia_balls(frame)
            distances = self.object_recognition.measure_distances(small_ball, large_balls)
            self.display_ar(frame, small_ball, large_balls, distances)

    def display_ar(self, frame: np.ndarray, small_ball, large_balls: List, distances: Dict):
        """Display the AR visualization with boccia balls and distances overlaid on the camera feed"""
        # Draw the small boccia ball
        cv2.circle(frame, (int(small_ball.x), int(small_ball.y)), int(small_ball.radius), (0, 255, 0), 2)

        # Draw the large boccia balls and the distances
        for large_ball in large_balls:
            cv2.circle(frame, (int(large_ball.x), int(large_ball.y)), int(large_ball.radius), (0, 0, 255), 2)
            cv2.putText(frame, f"{distances[large_ball]:.2f}", (int(large_ball.x), int(large_ball.y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Convert the frame to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # Display the texture on the image widget
        self.image_widget.texture = texture

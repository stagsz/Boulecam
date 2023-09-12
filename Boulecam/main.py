from kivy.app import App
from object_recognition import ObjectRecognition
from ar_visualization import ARVisualization
from interface import Interface
from calibration import Calibration
from language_support import LanguageSupport

class BocciaARApp(App):
    def build(self):
        self.object_recognition = ObjectRecognition()
        self.ar_visualization = ARVisualization(self.object_recognition)
        self.interface = Interface()
        self.calibration = Calibration()
        self.language_support = LanguageSupport({'en': 'English'})

        return self.interface

    def on_start(self):
        self.ar_visualization.start()

    def on_stop(self):
        self.ar_visualization.stop()

if __name__ == '__main__':
    BocciaARApp().run()

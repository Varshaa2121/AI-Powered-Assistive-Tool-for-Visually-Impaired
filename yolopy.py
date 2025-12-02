from ultralytics import YOLO as __Net
import cv2 as __cv

class Detector:
    def __init__(self, path):
        self.__core = __Net(path)

    def scan(self, frame):
        output = self.__core(frame)
        results = []

        for r in output:
            for b in r.boxes:
                label = self.__core.names[int(b.cls[0])]
                confidence = float(b.conf[0])
                results.append((label, confidence))

        return results

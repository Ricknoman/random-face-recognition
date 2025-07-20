import cv2
import numpy as np
from ultralytics import YOLO
import random

class properties:
    def screenshot(self):
        cap = cv2.VideoCapture(0)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Try to take another shot")
                break
            cv2.imshow("Press 's' to take screenshot", frame)
            key = cv2.waitKey(1)
            if key == ord("s"):
                frame_count += 1
                file = f"filename{frame_count}.png"
                cv2.imwrite(file, frame)
            if key == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()

    def image(self, image_path):
        return cv2.imread(image_path)  # Keep it in color for YOLO

class main(properties):
    def function(self, filename):
        self.img = super().image(filename)
        model = YOLO("assets/yolov8s-face-lindevs.pt") 
        
        results = model(self.img)
        self.result = results[0]
        self.boxes = self.result.boxes

        for box in self.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            color = np.random.randint(0, 255, size=3).tolist()
            label = f"Face: {conf:.2f}"
            cv2.rectangle(self.img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(self.img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        while True:
            cv2.imshow("YOLO Face Detection", self.img)
            key = cv2.waitKey(0)
            if key == ord('q'):
                break
            elif key == ord('s'):
                if len(self.boxes) > 0:
                    selected = random.randint(0, len(self.boxes) - 1)
                    box = self.boxes[selected]
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cropped = self.img[y1:y2, x1:x2]
                    cv2.imshow(f"Face {selected}", cropped)
                else:
                    print("No face detected.")
            elif key==ord('x'):
              cv2.destroyAllWindows()  
        cv2.destroyAllWindows()

v = main()
p = "assets\WhatsApp Image 2025-07-17 at 21.19.18_fb2ee2d2.jpg"
v.function(p)

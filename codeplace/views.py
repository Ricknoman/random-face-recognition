from django.shortcuts import render
import cv2, numpy as np, random, os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import imageform,uploadedimage
from ultralytics import YOLO
import random
# Load YOLO model once (global)
model = YOLO("assets/yolov8s-face-lindevs.pt")
# Create your views here.

def home(request):
    return render(request,'home.html')

def upload(request):
    if request.method == 'POST':
        form = imageform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('result', pk=form.instance.pk)
    else:
        form = imageform()
    return render(request, 'home.html', {'form': form})
        

def capture(request):
    cap=cv2.VideoCapture(0)
    ret,frame=cap.read()
    cap.release()

    filename="captured_frame.jpg"
    filepath=os.path.join(settings.MEDIA_ROOT,"images",filename)
    cv2.imwrite(filepath,frame)
    uploaded = uploadedimage.objects.create(image="images/" + filename)
    return redirect("result", pk=uploaded.pk)

def result(request, pk):
    uploaded = uploadedimage.objects.get(pk=pk)
    image_path = os.path.join(settings.MEDIA_ROOT, str(uploaded.image))
    img = cv2.imread(image_path)          # read image
    results = model(img)                  # run YOLO model
    boxes = results[0].boxes     
    faces_path = []

    # ensure directories exist
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "faces"), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "results"), exist_ok=True)

    for i, box in enumerate(boxes):        # get face boxes
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cropped_face = img[y1:y2, x1:x2]
        face_file = f"face_{pk}_{i}.jpg"
        face_path = os.path.join(settings.MEDIA_ROOT, "faces", face_file)
        cv2.imwrite(face_path, cropped_face)
        # use MEDIA_URL so the URL is absolute (starts with '/media/')
        faces_path.append(settings.MEDIA_URL + f"faces/{face_file}")

    result_face = f"result_{pk}.jpg"
    result_path = os.path.join(settings.MEDIA_ROOT, "results", result_face)
    cv2.imwrite(result_path, img)
    result_url = settings.MEDIA_URL + f"results/{result_face}"

    random_face = random.choice(faces_path) if faces_path else None
    size_kb = round(os.path.getsize(image_path) / 1024, 2)
    return render(request, "result.html", {
         "result": result_url,
        "faces": faces_path,
        "size": size_kb,
        "random_face": random_face
    })


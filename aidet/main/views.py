import os
import io
import runpy
import contextlib
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from ultralytics import YOLO
from django.core.files.storage import FileSystemStorage
from .test import run_inference

# Load YOLO model
MODEL_PATH = os.path.join(settings.BASE_DIR, "main", "model", "xdet-v1-model.pt")
yolo_model = YOLO(MODEL_PATH)


# Home page
def index(request):
    return render(request, 'main/index.html')


# Detection page (maybe with upload form)
def detection(request):
    return render(request, 'main/detection.html')


# Run a separate Python script (rule.py)
def run_my_code(request):
    buf = io.StringIO()
    path = os.path.join(settings.BASE_DIR, "main", "rule.py")
    with contextlib.redirect_stdout(buf):
        runpy.run_path(path, run_name="__main__")
    output = buf.getvalue().strip()
    formatted_output = output.replace("\n", "<br>")
    return HttpResponse(formatted_output or "OK")


def detect_view(request):
    if yolo_model is None:
        return HttpResponse(
            "<h2 style='color:red;'>⚠️ Model file is missing!</h2>"
            "<p>Please place <b>xdet-v1-model.pt</b> inside <code>main/model/</code> folder.</p>"
        )

    context = {}

    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]

        # Save uploaded file inside MEDIA/uploads/
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "uploads"))
        filename = fs.save(image.name, image)
        file_path = fs.path(filename)

        # Run YOLO prediction
        results = yolo_model.predict(file_path)
        r = results[0]
        probs = r.probs
        pred_index = probs.top1
        pred_name = r.names[pred_index]
        confidence = probs.top1conf.item()

        # Add prediction to context
        context["prediction"] = pred_name.upper()
        context["confidence"] = f"{confidence:.2%}"

    return render(request, "main/run.html", context)
    # return render(request, "main/run.html")

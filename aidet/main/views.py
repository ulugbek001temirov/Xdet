from django.shortcuts import render

# Create your views here.
def index(request):
    data ={
        "title": "AI Imaging Solutions",
    }
    return render(request, 'main/index.html',data)
def detection(request):
    return render(request, 'main/detection.html')
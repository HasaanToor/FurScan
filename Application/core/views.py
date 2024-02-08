import os
import cv2
import numpy as np
from keras.models import load_model

from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render 
class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def cat_conjunct(request):
    message = ""
    prediction = ""
    result_text = ""
    accuracy = 0.0  # Initialize accuracy to zero
    fss = CustomFileSystemStorage()
    
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        image_url = fss.url(_image)

        # Set the image dimensions
        img_width, img_height = 100, 100

        new_images = []
        img = cv2.imread(path)
        img = cv2.resize(img, (img_width, img_height))
        new_images.append(img)

        # Load the trained model
        model = load_model('models/model_with_augmentation_combined.h5')

        new_images = np.array(new_images)
        new_images = new_images.astype('float32') / 255.0
        predictions = model.predict(new_images)

        # Set the threshold probability
        threshold = 0.5  

        for i, prediction in enumerate(predictions):
            probability = prediction[0]
            if probability >= threshold:
                print(f"Image {i + 1}: The eye is infected with a probability of {probability:.2f}.")
            else:
                print(f"Image {i + 1}: The eye is not infected with a probability of {1 - probability:.2f}.")

        accuracy = predictions[0][0]
        result_text = "The eye is infected." if accuracy >= threshold else "The eye is not infected."

        return TemplateResponse(
            request,
            "CatConjuct.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": result_text,
                "accuracy": f"{accuracy:.2%}",
            },
        )
    except MultiValueDictKeyError:
        return TemplateResponse(
            request,
            "CatConjuct.html",
            {"message": "No image selected"},
        )
def animals(request):
    return render(request, 'animals.html')

def index(request):
    return render(request, 'index.html')
def CatConjunctForm(request):
    return render(request, 'CatConjunctForm.html')
def Cats(request):
    return render(request, 'Cats.html')

def Dogs(request):
    return render(request, 'Dogs.html')
def Kennel(request):
    return render(request, 'Kennel.html')
def disclaimer(request):
    return render(request, 'disclaimer.html')
def learnmore(request):
    return render(request, 'learnmore.html')
def cateyes(request):
    return render(request, 'CatEyes.html')
def bloating(request):
    return render(request, 'Bloating.html')
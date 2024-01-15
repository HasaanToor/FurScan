import os
import cv2
import numpy as np
from keras.models import load_model

from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length = None):
        self.delete(name)
        return name
    
def index(request):
    message = ""
    prediction = ""
    result_text =""
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
                print(f"Image {i+1}: The eye is infected with a probability of {probability:.2f}.")
            else:
                print(f"Image {i+1}: The eye is not infected with a probability of {1 - probability:.2f}.")
        
        if predictions[0][0] >= threshold:
            result_text = "The eye is infected."
        else:
            result_text = "The eye is not infected."
        return TemplateResponse(
            request, 
            "index.html",
            {
                "message": message, 
                "image": image, 
                "image_url": image_url,
                "prediction": result_text,
            },
        )
    except MultiValueDictKeyError:
        return TemplateResponse(
            request, 
            "index.html",
            {"message": "No image selected"},
        )
from django.shortcuts import render
from .forms import UploadImageForm
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

def predict_eye_infection(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Load the trained model
            model = load_model('models/model.h5')

            # Set the image dimensions
            img_width, img_height = 100, 100

            new_images = []
            uploaded_image = request.FILES['image']
            image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)
            image = cv2.resize(image, (img_width, img_height))
            new_images.append(image)

            new_images = np.array(new_images)
            new_images = new_images.astype('float32') / 255.0
            predictions = model.predict(new_images)

            # Set the threshold probability
            threshold = 0.5  

            result_messages = []

            for i, prediction in enumerate(predictions):
                probability = prediction[0]
                if probability >= threshold:
                    result_messages.append(f"Image {i+1}: The eye is infected with a probability of {probability:.2f}.")
                else:
                    result_messages.append(f"Image {i+1}: The eye is not infected with a probability of {1 - probability:.2f}.")

            # You can pass the result_messages to your template or render it in the response
            context = {'form': form, 'result_messages': result_messages}
            return render(request, 'index.html', context)
    else:
        form = UploadImageForm()

    return render(request, 'index.html', {'form': form})

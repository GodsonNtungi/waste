from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
from tensorflow import keras
from PIL import Image
import numpy as np
import os
import time

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR,'Interpretation','Model1.h5')

waste = {0:'HDPE',1:'LDPE',2:'OTHER',3:'PET',4:'PP',5:'PS',6:'PVC'}

def home(request):
    return render(request,"upload.html")

@csrf_exempt
def image_upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        print(type(image_file))
        model = keras.models.load_model(file_path)
        image = Image.open(image_file)
        image = image.rotate(-90, Image.NEAREST, expand=1)
        image = image.resize((256, 256))
        image.save("test.jpg")
        image = np.array(image)
        prediction = model.predict([image[None, :, :, :]])
        print(str(prediction))
        results = [[i, r] for i, r in enumerate(prediction[0]) if r > 0]
        results.sort(key=lambda x: x[1], reverse=True)

        value=[]
        data = {"Type of plastic:":waste[results[0][0]]}
        value.append(data)

        if not value:
            data = {"disease": "Unidentified", "percentage": '100%'}
            value.append(data)
        # do something with the image file, such as save it to disk or process it

        return JsonResponse({'message':value})
    else:
        return JsonResponse({'message':"Failed,no image received"})

# Create your views here.

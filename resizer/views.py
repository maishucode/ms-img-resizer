from django.http import JsonResponse
from django.shortcuts import render
from PIL import Image
from .resize_function import convert_and_save_to_s3

def home(request):
    if request.method == 'POST':
        # Handle file upload
        file = request.FILES['file']
        aspect_ratio = request.POST.get('aspect_ratio')
        file_name = file.name

        # Open the image using PIL
        img = Image.open(file)
        resized_img_url = convert_and_save_to_s3(img, file_name, aspect_ratio)
        print(resized_img_url)

        # Return the image URL as JSON
        return JsonResponse({'url': resized_img_url})

    return render(request, 'resizer/home.html')

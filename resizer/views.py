from django.http import JsonResponse
from django.shortcuts import render
from PIL import Image
import base64
from io import BytesIO
from .resize_function import convert_to_aspect_ratio

def home(request):
    if request.method == 'POST':
        # Handle file upload
        file = request.FILES['file']
        aspect_ratio = request.POST.get('aspect_ratio')

        # Open the image using PIL
        img = Image.open(file)

        # Resize the image
        resized_img = convert_to_aspect_ratio(img, aspect_ratio)

        # Convert the image to base64
        buffer = BytesIO()
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == 'png':
            resized_img.save(buffer, format='PNG')
        elif file_extension in ['jpg', 'jpeg']:
            resized_img.save(buffer, format='JPEG')
        elif file_extension == 'gif':
            resized_img.save(buffer, format='GIF')
        else:
            return JsonResponse({'error': 'Unsupported file format'}, status=400)

        # Encode image as base64
        img_str = base64.b64encode(buffer.getvalue()).decode()

        # Return the base64 string to the frontend
        return JsonResponse({'image_base64': img_str, 'format': file_extension})

    return render(request, 'resizer/home.html')
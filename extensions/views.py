from PIL import Image
import mimetypes
import pyheif
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.contrib.auth.decorators import login_required

def get_max_file_size(user):
    if user.is_authenticated:
        if user.subscription_level == 'premium':
            return settings.MAX_FILE_SIZE_PREMIUM
        else:
            return settings.MAX_FILE_SIZE_STANDARD
    else:
        return settings.MAX_FILE_SIZE_DEFAULT

"""
To jpg
"""
@login_required()
def convert_file_to_jpg(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        
        if not file:
            return render(request, 'converter/error.html', {'message': 'No file selected.'})
        max_file_size = get_max_file_size(request.user)
        if file.size > max_file_size:
            return render(request, 'converter/error.html', {'message': 'File size exceeds the maximum limit.'})
        
        fs = FileSystemStorage()
        uploaded_file_path = fs.save(file.name, file)
        absolute_file_path = os.path.join(fs.location, uploaded_file_path)

        if file.name.endswith('.HEIC'):
            converted_file_path = convert_heic_to_jpg(absolute_file_path)
        elif file.name.endswith('.png'):
            converted_file_path = convert_png_to_jpg(absolute_file_path)
        elif file.name.endswith('.gif'):
            converted_file_path = convert_gif_to_jpg(absolute_file_path)
        else:
            return render(request, 'converter/error.html', {'message': 'Unsupported file format.'})

        return redirect('extension:success', file_path=converted_file_path)

    return render(request, 'converter/convert_jpg.html')

@login_required
def download_file(request, file_path):
    file_name = os.path.basename(file_path)
    content_type, _ = mimetypes.guess_type(file_path)
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


def convert_heic_to_jpg(file_path):
    # Conversion logic from HEIC to JPG
    heif_file = pyheif.read(file_path)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    converted_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
    image.save(converted_file_path, 'JPEG')
    return converted_file_path

def convert_png_to_jpg(file_path):
    image = Image.open(file_path)
    converted_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
    image.convert('RGB').save(converted_file_path, 'JPEG')
    return converted_file_path

def convert_gif_to_jpg(file_path):
    image = Image.open(file_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    converted_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
    image.save(converted_file_path, 'JPEG')
    return converted_file_path


"""
To png
"""
@login_required
def convert_file_to_png(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        
        if not file:
            return render(request, 'converter/error.html', {'message': 'No file selected.'})
        max_file_size = get_max_file_size(request.user)
        if file.size > max_file_size:
            return render(request, 'converter/error.html', {'message': 'File size exceeds the maximum limit.'})
        
        fs = FileSystemStorage()
        uploaded_file_path = fs.save(file.name, file)
        absolute_file_path = os.path.join(fs.location, uploaded_file_path)

        if file.name.endswith('.HEIC'):
            converted_file_path = convert_heic_to_png(absolute_file_path)
        elif file.name.endswith('.jpg'):
            converted_file_path = convert_jpg_to_png(absolute_file_path)
        elif file.name.endswith('.gif'):
            converted_file_path = convert_gif_to_png(absolute_file_path)
        else:
            return render(request, 'converter/error.html', {'message': 'Unsupported file format.'})

        return redirect('extension:success', file_path=converted_file_path)

    return render(request, 'converter/convert_png.html')

def convert_heic_to_png(file_path):
    heif_file = pyheif.read(file_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    converted_file_path = file_path.rsplit('.', 1)[0] + '.png'
    image.save(converted_file_path, 'PNG')
    return converted_file_path

def convert_jpg_to_png(file_path):
    image = Image.open(file_path)
    converted_file_path = file_path.rsplit('.', 1)[0] + '.png'
    image.save(converted_file_path, 'PNG')
    return converted_file_path

def convert_gif_to_png(file_path):
    image = Image.open(file_path)
    if image.mode != 'P':
        image = image.convert('P')
    converted_file_path = file_path.rsplit('.', 1)[0] + '.png'
    image.save(converted_file_path, 'PNG')
    return converted_file_path

"""
    To gif
"""
@login_required
def convert_file_to_gif(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        
        if not file:
            return render(request, 'converter/error.html', {'message': 'No file selected.'})
        max_file_size = get_max_file_size(request.user)
        if file.size > max_file_size:
            return render(request, 'converter/error.html', {'message': 'File size exceeds the maximum limit.'})
        
        fs = FileSystemStorage()
        uploaded_file_path = fs.save(file.name, file)
        absolute_file_path = os.path.join(fs.location, uploaded_file_path)

        if file.name.endswith('.HEIC'):
            converted_file_path = convert_heic_to_gif(absolute_file_path)
        elif file.name.endswith('.jpg'):
            converted_file_path = convert_jpg_to_gif(absolute_file_path)
        elif file.name.endswith('.png'):
            converted_file_path = convert_png_to_gif(absolute_file_path)
        else:
            return render(request, 'converter/error.html', {'message': 'Unsupported file format.'})

        return redirect('extension:success', file_path=converted_file_path)

    return render(request, 'converter/convert_gif.html')

def convert_heic_to_gif(file_path):
    # Conversion logic from HEIC to GIF
    heif_file = pyheif.read(file_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    converted_file_path = file_path.rsplit('.', 1)[0] + '.gif'
    image.save(converted_file_path, 'GIF')
    return converted_file_path

def convert_png_to_gif(file_path):
    image = Image.open(file_path)
    converted_file_path = file_path.rsplit('.', 1)[0] + '.gif'
    image.save(converted_file_path, 'GIF')
    return converted_file_path

def convert_jpg_to_gif(file_path):
    image = Image.open(file_path)
    converted_file_path = file_path.rsplit('.', 1)[0] + '.gif'
    image.save(converted_file_path, 'GIF')
    return converted_file_path

@login_required
def success_view(request, file_path):
    return render(request, 'converter/success.html', {'file_path': file_path})


def error_view(request):
    return render(request, 'converter/error.html')


"""
mov to mp4
"""
from django.shortcuts import render
from django.http import HttpResponse
from moviepy.editor import VideoFileClip

@login_required
def convert_mov_to_mp4(request):
    if request.method == 'POST' and request.FILES.get('mov_file'):
        mov_file = request.FILES['mov_file']

        # Save the uploaded MOV file to a temporary location
        with open('input.mov', 'wb+') as destination:
            for chunk in mov_file.chunks():
                destination.write(chunk)

        # Perform the conversion using moviepy
        clip = VideoFileClip("input.mov")
        clip.write_videofile("output.mp4")

        # Provide the converted MP4 file for download
        with open("output.mp4", 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename=output.mp4'
            return response

    return render(request, 'converter/convert_to_mp4.html')


# import cairosvg
# from PIL import Image

# def convert_svg_to_jpg(svg_file_path, output_jpg_path, width=800, height=600):
#     # Convert SVG to PNG using cairosvg
#     png_output = cairosvg.svg2png(url=svg_file_path, write_to=None)

#     # Create PIL Image from the PNG data
#     image = Image.open(io.BytesIO(png_output))

#     # Resize the image to the desired dimensions
#     image = image.resize((width, height))

#     # Convert PIL Image to JPG format and save
#     image.convert('RGB').save(output_jpg_path, 'JPEG')

# # Usage example
# svg_file_path = 'path/to/input.svg'
# output_jpg_path = 'path/to/output.jpg'
# convert_svg_to_jpg(svg_file_path, output_jpg_path)
# #To work out the cost per 100mls if there is an offer such as 3 for £5.50. It also works out cost per bottle
# def calc_100mls():
#     num_bottles = int(input("Enter the number of bottles: "))
#     mls_per_bottle = int(input("Enter milliliters per bottle: "))
#     total_mls = num_bottles * mls_per_bottle
#     get_cost = float(input("How much do they cost: "))
#     cost_per_100mls = (get_cost / total_mls) * 100
#     cost_per_bottle = (get_cost / num_bottles)
#     return f"The cost per 100mls is {cost_per_100mls:.2f}, The cost per bottle is {cost_per_bottle:.2f}"
# #To work out the cost per 100gs if there is an offer such as 3 for £5.50. It also works out cost per item
# def calc_100gs():
#     num_items = int(input("Enter the number of items: "))
#     grams_per_item = int(input("Enter grams per items: "))
#     total_grams = num_items * grams_per_item
#     get_cost = float(input("How much do they cost: "))
#     cost_per_100grams = (get_cost / total_grams) * 100
#     cost_per_item = (get_cost / num_items)
#     return f"The cost per 100grams is {cost_per_100grams:.2f}, The cost per item is {cost_per_item:.2f}"

# #find out how much you are saving
# def calculate_savings():
#     percentage_off = float(input("Enter the percent off?: "))
#     initial_cost = float(input("Enter tne cost of the item?: "))
#     savings = (percentage_off / 100) * initial_cost
#     return f"You saved £{savings:.2f}"
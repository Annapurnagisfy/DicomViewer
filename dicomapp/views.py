# from django.shortcuts import render
# import zipfile
# import os
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# import pydicom

# def upload_zip(request):
#     if request.method == 'POST' and request.FILES['zip_file']:
#         zip_file = request.FILES['zip_file']
        
#         # Store uploaded file temporarily
#         fs = FileSystemStorage()
#         filename = fs.save(zip_file.name, zip_file)
#         file_path = fs.url(filename)
        
#         print(f"Uploaded file path: {file_path}")  # Print the uploaded file path

#         # Unzip the file
#         zip_folder = os.path.join(settings.MEDIA_ROOT, 'unzipped')
#         os.makedirs(zip_folder, exist_ok=True)
        
#         with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filename), 'r') as zip_ref:
#             print("Files inside the ZIP:", zip_ref.namelist())  # Print all files in the zip before extracting
#             zip_ref.extractall(zip_folder)

#         # Get all files and check if they are DICOM or image files
#         dicom_files = []
#         image_files = []
#         for root, dirs, files in os.walk(zip_folder):  # Walk through all directories and subdirectories
#             print(f"Scanning directory: {root}")  # Print the current directory being scanned
#             for file in files:
#                 print(f"Checking file: {file}")  # Print the file being checked
#                 dicom_path = os.path.join(root, file)  # Full path of the file
#                 try:
#                     # Try to load it as a DICOM file (whether it has an extension or not)
#                     dcm = pydicom.dcmread(dicom_path, stop_before_pixels=True)
#                     relative_dicom_path = os.path.relpath(dicom_path, settings.MEDIA_ROOT)  # Get relative path
#                     dicom_files.append(os.path.join('media', relative_dicom_path).replace("\\", "/"))
#                     print(f"DICOM file found: {relative_dicom_path}")  # Print the relative DICOM path
#                 except Exception as e:
#                     # If it's not a DICOM file, check for image files
#                     if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif')):
#                         image_path = os.path.join('media', 'unzipped', root, file).replace("\\", "/")
#                         image_files.append(image_path)
#                         print(f"Image file found: {image_path}")  # Print the image path

#         # Print the final list of image and DICOM files
#         print("All extracted image paths:")
#         for image in image_files:
#             print(image)
        
#         print("All extracted DICOM paths:")
#         for dicom in dicom_files:
#             print(dicom)

#         # Render the image display template with the image and DICOM paths
#         return render(request, 'dicomapp/image_display.html', {'images': image_files, 'dicoms': dicom_files})
    
#     return render(request, 'dicomapp/upload_zip.html')


# from django.shortcuts import render
# import zipfile
# import os
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# import shutil

# def upload_zip(request):
#     if request.method == 'POST' and request.FILES['zip_file']:
#         zip_file = request.FILES['zip_file']
        
#         # Store uploaded file temporarily
#         fs = FileSystemStorage()
#         filename = fs.save(zip_file.name, zip_file)
#         file_path = fs.url(filename)
        
#         print(f"Uploaded file path: {file_path}")  # Print the uploaded file path

#         # Unzip the file - clear previous files first
#         zip_folder = os.path.join(settings.MEDIA_ROOT, 'unzipped')
        
#         # Remove previous unzipped files
#         if os.path.exists(zip_folder):
#             shutil.rmtree(zip_folder)  # Delete the unzipped folder and all its contents
#         os.makedirs(zip_folder, exist_ok=True)  # Re-create the folder

#         with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filename), 'r') as zip_ref:
#             print("Files inside the ZIP:", zip_ref.namelist())  # Print all files in the zip before extracting
#             zip_ref.extractall(zip_folder)

#         # Get all files and check if they are DICOM or image files
#         image_files = []
#         for root, dirs, files in os.walk(zip_folder):  # Walk through all directories and subdirectories
#             print(f"Scanning directory: {root}")  # Print the current directory being scanned
#             for file in files:
#                 print(f"Checking file: {file}")  # Print the file being checked
#                 file_path = os.path.join(root, file)  # Full path of the file

#                 # Check for image file extensions (including DICOM files)
#                 if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif', 'dcm')):
#                     relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)  # Get relative path
#                     image_path = relative_path.replace("\\", "/")
#                     image_files.append(image_path)  # Add image file to the list
#                     print(f"Image/DICOM file found: {image_path}")  # Print the image path

#         # Print the final list of image and DICOM files
#         print("All extracted image/DICOM paths:")
#         for image in image_files:
#             print(image)

#         # Render the image display template with the image paths (including DICOM files)
#         return render(request, 'dicomapp/image_display.html', {'images': image_files})
    
#     return render(request, 'dicomapp/upload_zip.html')

from PIL import Image
import pydicom
import os
import shutil
import zipfile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render
import logging

def upload_zip(request):
    if request.method == 'POST' and request.FILES['zip_file']:
        zip_file = request.FILES['zip_file']
        
        # Store uploaded file temporarily
        fs = FileSystemStorage()
        filename = fs.save(zip_file.name, zip_file)
        file_path = fs.url(filename)
        
        print(f"Uploaded file path: {file_path}")  # Print the uploaded file path

        # Unzip the file - clear previous files first
        zip_folder = os.path.join(settings.MEDIA_ROOT, 'unzipped')
        
        # Remove previous unzipped files
        if os.path.exists(zip_folder):
            shutil.rmtree(zip_folder)  # Delete the unzipped folder and all its contents
        os.makedirs(zip_folder, exist_ok=True)  # Re-create the folder

        with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filename), 'r') as zip_ref:
            print("Files inside the ZIP:", zip_ref.namelist())  # Print all files in the zip before extracting
            zip_ref.extractall(zip_folder)

        # Get all files and check if they are DICOM or image files
        image_files = []
        for root, dirs, files in os.walk(zip_folder):  # Walk through all directories and subdirectories
            print(f"Scanning directory: {root}")  # Print the current directory being scanned
            for file in files:
                print(f"Checking file: {file}")  # Print the file being checked
                file_path = os.path.join(root, file)  # Full path of the file

                # Check for image file extensions (including DICOM files)
                relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)  # Get relative path
                image_path = relative_path.replace("\\", "/")

                # Print file extension
                file_extension = os.path.splitext(file)[1].lower()
                print(f"File: {file} has extension: {file_extension}")

                # If the file has an image extension (jpg, jpeg, png)
                if file_extension in ('.jpg', '.jpeg', '.png'):
                    image_files.append(image_path)  # Add image file to the list
                    print(f"Image/DICOM file found: {image_path}")  # Print the image path

                # If the file has no extension or is a DICOM file (.dcm)
                elif file_extension == '' or file_extension == '.dcm':
                    print(f"Attempting to convert DICOM file {file} to JPEG...")
                    try:
                        # For DICOM files, use pydicom to read and convert
                        dicom_data = pydicom.dcmread(file_path)
                        
                        # Check if the DICOM file contains pixel data
                        if 'PixelData' in dicom_data:
                            # Convert pixel data to a Pillow image
                            image = Image.fromarray(dicom_data.pixel_array)
                            new_file_path = os.path.splitext(file_path)[0] + ".jpeg"
                            image = image.convert("RGB")  # Convert to RGB before saving as JPEG
                            image.save(new_file_path, "JPEG")
                            os.remove(file_path)  # Delete the original DICOM file
                            relative_new_path = os.path.relpath(new_file_path, settings.MEDIA_ROOT)
                            image_files.append(relative_new_path.replace("\\", "/"))
                            print(f"Converted and added: {relative_new_path}")  # Print the converted image path
                        else:
                            print(f"No pixel data in DICOM file {file}. Skipping conversion.")
                    except Exception as e:
                        print(f"Error converting DICOM file {file_path}: {e}")
                        continue
                else:
                    # For other unsupported extensions, skip or handle accordingly
                    print(f"Skipping unsupported file type: {file}")
                    continue

        # Print the final list of image and DICOM files
        print("All extracted image/DICOM paths:")
        for image in image_files:
            print(image)

        # Render the image display template with the image paths (including converted DICOM files)
        return render(request, 'dicomapp/image_display.html', {'images': image_files})
    
    return render(request, 'dicomapp/upload_zip.html')

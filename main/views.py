from django.views.decorators.csrf import csrf_protect
# main/views.py
import os
import cv2
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as djangoLogin, logout as djangoLogout, authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import UserProfileForm, FileUploadForm
from .models import UploadedFile, UserProfile
from django.conf import settings
from django.http import HttpResponse

def home(request):
    return render(request, 'main/index.html', {'user': request.user})

def base_view(request):
    return render(request, 'main/base.html')

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
    else:
        profile_form = UserProfileForm(instance=user_profile)

    files_count = UploadedFile.objects.filter(user=request.user).count()
    total_size = UploadedFile.objects.filter(user=request.user).aggregate(Sum('file_size'))['file_size__sum'] or 0

    return render(request, 'main/profile.html', {
        'profile_form': profile_form,
        'files_count': files_count,
        'total_size': total_size,
    })

@login_required
def drive_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            return redirect('drive')
    else:
        form = FileUploadForm()

    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'main/drive.html', {'form': form, 'files': files})

@login_required
def another_page_view(request):
    # Your logic for another page view here
    return render(request, 'main/another_page.html')

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file.delete()
    return redirect('drive')

def view_file(request, fid):
    uploaded_file = get_object_or_404(UploadedFile, pk=fid)
    file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=uploaded_file.file_type)
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Capture face using OpenCV
        camera = cv2.VideoCapture(0)
        return_code, image = camera.read()
        camera.release()

        # Save the captured image to the media directory
        media_root = settings.MEDIA_ROOT
        image_filename = f'{username}.jpg'
        image_path = os.path.join(media_root, 'profile_pics', image_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Save the image
        cv2.imwrite(image_path, image)

        # Create a new user using the standard User model
        user = User.objects.create_user(username=username, password=password)

        # Create a UserProfile instance for the user
        profile_picture = f'profile_pics/{image_filename}'
        UserProfile.objects.create(user=user, profile_picture=profile_picture)

        # Log in the user
        djangoLogin(request, user)
        return redirect('/drive')  # Redirect to drive after registration

    return render(request, 'main/register.html')

import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as djangoLogin
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.conf import settings

import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as djangoLogin
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.conf import settings

import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as djangoLogin
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.conf import settings
from django.contrib import messages  # Import messages framework for displaying notifications

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Capture face using OpenCV for authentication
            camera = cv2.VideoCapture(0)
            _, face = camera.read()
            camera.release()

            try:
                # Get the UserProfile associated with the user
                user_profile = UserProfile.objects.get(user__username=username)

                # Get the path to the saved face image
                saved_face_path = user_profile.profile_picture.path

                # Load the saved face image using OpenCV
                saved_face = cv2.imread(saved_face_path)

                # Define threshold value for face matching
                threshold_value = 100.0  # Adjust this threshold as needed

                # Perform face recognition
                if are_faces_matching(saved_face, face, threshold_value):
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        djangoLogin(request, user)
                        return redirect('/drive')
                    else:
                        messages.error(request, 'Invalid username or password.')
                        return redirect('/login')
                else:
                    messages.error(request, 'Face does not match. Please try again.')
                    return redirect('/login')

            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found.')
                return redirect('/login')

        else:
            # Form is invalid
            messages.error(request, 'Invalid username or password.')
            return redirect('/login')

    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})

def are_faces_matching(face1, face2, threshold_value):
    # Implement face recognition logic to compare face1 and face2
    # Example: Use OpenCV or a face recognition library to compare faces
    mse = np.sum((face1.astype("float") - face2.astype("float")) ** 2)
    mse /= float(face1.shape[0] * face1.shape[1])

    # Return True if MSE is below the threshold value (faces match)
    return mse < threshold_value


from django.contrib.auth import logout  # Add this import

def logout_view(request):
    logout(request)
    return redirect('index')

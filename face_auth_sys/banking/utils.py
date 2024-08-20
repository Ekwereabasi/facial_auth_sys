import os
from django.core.exceptions import ValidationError
from google.cloud import vision_v1
from django.conf import settings
from .models import CustomUser

def authenticate_user_with_facial_recognition(uploaded_image):
    client = vision_v1.ImageAnnotatorClient()

    # Save the uploaded image temporarily
    temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
    with open(temp_image_path, 'wb') as temp_image_file:
        for chunk in uploaded_image.chunks():
            temp_image_file.write(chunk)
    
    with open(temp_image_path, 'rb') as image_file:
        content = image_file.read()

    # Create a Google Vision API Image object
    uploaded_image = vision_v1.Image(content=content)
    response_uploaded = client.face_detection(image=uploaded_image)
    
    # Check if a face was detected in the uploaded image
    if not response_uploaded.face_annotations:
        os.remove(temp_image_path)
        raise ValidationError("No face detected in the uploaded image.")

    # Iterate through users and compare their profile pictures
    for user in CustomUser.objects.all():
        profile_picture_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)
        
        # Check if the profile picture path is a file
        if not os.path.isfile(profile_picture_path):
            continue  # Skip if the path is not a valid file
        
        with open(profile_picture_path, 'rb') as profile_image_file:
            profile_content = profile_image_file.read()

        # Create a Google Vision API Image object for the profile picture
        profile_image = vision_v1.Image(content=profile_content)
        response_profile = client.face_detection(image=profile_image)
        
        # Check if a face was detected in the profile picture
        if not response_profile.face_annotations:
            continue
        
        # Compare facial landmarks between the uploaded image and profile picture
        uploaded_face = response_uploaded.face_annotations[0]
        profile_face = response_profile.face_annotations[0]

        def compare_faces(uploaded_face, profile_face):
            # Note: Google Vision API does not provide direct landmarks comparison; this is a placeholder
            # Actual comparison should involve more complex logic or another service for reliable results

            # For the sake of example, let's use a simple comparison based on bounding box
            uploaded_bounds = uploaded_face.bounding_poly
            profile_bounds = profile_face.bounding_poly

            # Simple comparison: check if bounding boxes overlap significantly
            def bbox_overlap(bounds1, bounds2):
                # Example logic: check if the bounding boxes overlap
                # Implement a more sophisticated overlap or similarity check as needed
                return True  # Placeholder for actual overlap check

            if bbox_overlap(uploaded_bounds, profile_bounds):
                return True

            return False

        if compare_faces(uploaded_face, profile_face):
            os.remove(temp_image_path)
            return user

    # Clean up the temporary image
    os.remove(temp_image_path)
    raise ValidationError("Facial recognition failed. The uploaded image does not match any profile picture.")


import cv2
import dlib
import numpy as np

# Load pre-trained models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('path_to_shape_predictor_68_face_landmarks.dat')

# Load source and target images
source_img = cv2.imread('maleModel.jpeg')
target_img = cv2.imread('shivesh.jpg')

# Detect faces and landmarks
source_faces = detector(source_img)
target_faces = detector(target_img)

if len(source_faces) == 1 and len(target_faces) == 1:
    source_landmarks = predictor(source_img, source_faces[0])
    target_landmarks = predictor(target_img, target_faces[0])

    # Calculate affine transformation
    transformation_matrix = cv2.getAffineTransform(
        np.array(source_landmarks.parts()[:3]),
        np.array(target_landmarks.parts()[:3])
    )

    # Apply warp affine
    warped_source = cv2.warpAffine(source_img, transformation_matrix, (target_img.shape[1], target_img.shape[0]))

    # Optional: Blend the images
    alpha = 0.5
    swapped_face = cv2.addWeighted(target_img, 1 - alpha, warped_source, alpha, 0)

    # Display or save the result
    cv2.imshow('Swapped Face', swapped_face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Unable to detect faces in one or both images.")

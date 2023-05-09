import cv2
import os


def images_to_video(image_folder, video_name, fps):
    # Get the file path of the first image in the folder
    first_image = os.path.join(image_folder, os.listdir(image_folder)[0])
    # Read the dimensions of the first image
    img = cv2.imread(first_image)
    height, width, _ = img.shape

    # Initialize the VideoWriter object
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    # Iterate over the images in the folder and write them to the video
    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)
        img = cv2.imread(image_path)
        video.write(img)

    # Release the video object to save the video file
    video.release()


images_to_video(r'D:\Diploma_data\ultralytics\examples\YOLOv8-OpenCV-ONNX-Python\sequence','video.mp4',24)
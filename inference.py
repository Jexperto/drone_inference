import cv2.dnn
import numpy as np
from ultralytics.yolo.utils import yaml_load
from ultralytics.yolo.utils.checks import check_yaml

CLASSES = yaml_load(check_yaml('visdrone.yaml'))['names']
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def predict(model, input_image):
    original_image = input_image
    [height, width, _] = original_image.shape
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image
    scale = length / 640

    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
    model.setInput(blob)
    outputs = model.forward()

    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []

    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= 0.25:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2], outputs[0][i][3]]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)

    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

    detections = []
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        detection = {
            'class_id': class_ids[index],
            'class_name': CLASSES[class_ids[index]],
            'confidence': scores[index],
            'box': box,
            'scale': scale}
        detections.append(detection)
        draw_bounding_box(original_image, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                          round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

    return original_image


consumer_types = ["file", "picamera"]
producer_types = ["file", "spi"]


def infer(onnx_model, consumer_type='file', producer_type='file', **kwargs):
    if consumer_type in consumer_types and producer_type in producer_types:
        if consumer_type == 'file':
            from detectionio.consumer.fileconsumer import FileVideoConsumer
            filepath = kwargs['inputpath']
            input_stream = FileVideoConsumer(filepath=filepath)

        elif consumer_type == 'picamera':
            # configure video params if needed
            from detectionio.consumer.picameraconsumer import PiVideoConsumer
            input_stream = PiVideoConsumer(resolution=kwargs["picamera_resolution"], framerate=kwargs["fps"],
                                           use_video_port=kwargs["picamera_use_video_port"],
                                           format=kwargs["picamera_format"])

        if producer_type == 'file':
            from detectionio.producer.fileproducer import FileVideoProducer
            filepath = kwargs['outputpath']
            resolution = input_stream.shape[0], input_stream.shape[1]  # noqa
            out_stream = FileVideoProducer(filepath, resolution=resolution)

        elif producer_type == 'spi':
            from detectionio.producer.spiproducer import SPIVideoProducer

            out_stream = SPIVideoProducer(bus_num=kwargs["spi_bus_num"], device_num=kwargs["spi_device_num"],
                                          spi_mode=kwargs["spi_mode"],
                                          spi_max_speed_hz=kwargs["spi_hz"])
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnx_model)
    # input_stream = videofeed_consumer.FileVideoConsumer('in/test.mp4')

    for image in input_stream.start():
        res = predict(model, image)
        out_stream.push_image(res)
    out_stream.close()

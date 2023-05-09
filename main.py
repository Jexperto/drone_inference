import argparse

from inference import infer, consumer_types, producer_types
import logging
import sys
from detectionio.utils.spiconfig import SPIModeConfig, SPIHzConfig

logging.basicConfig(filename='inference.log', encoding='utf-8', level=logging.DEBUG)

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def main(onnx_model, consumer_type, producer_type, inputpath, outputpath, spi_hz, spi_mode, spi_bus_num,
         spi_device_num, fps, picamera_use_video_port, picamera_format,
         picamera_resolution):
    picamera_resolution = picamera_resolution.split("x")
    infer(onnx_model, consumer_type=consumer_type, producer_type=producer_type,
          inputpath=inputpath,
          outputpath=outputpath, spi_mode=spi_mode,
          spi_bus_num=spi_bus_num, spi_device_num=spi_device_num, spi_hz=spi_hz, fps=fps,
          picamera_use_video_port=picamera_use_video_port, picamera_format=picamera_format,
          picamera_resolution=picamera_resolution)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',
                        default=r'D:\Diploma_data\ultralytics\examples\YOLOv8-OpenCV-ONNX-Python\model\best.onnx',
                        help='Input your onnx model.')
    parser.add_argument('--consumertype', default='picamera',
                        help=f'Type of video consumer to use. One of: {consumer_types}')
    parser.add_argument('--producertype', default='spi',
                        help=f'Type of video producer to use. One of: {producer_types}')
    parser.add_argument('--inputpath', nargs='?', help='Path to .mp4 input file')
    parser.add_argument('--outputpath', nargs='?', help='Path to .mp4 output file')
    parser.add_argument('--spi_hz', nargs='?', default=SPIModeConfig.LOW_CLOCK_LEADING,
                        help=f'One of {SPIHzConfig.__dict__["_member_names_"]}')
    parser.add_argument('--spi_mode', nargs='?', default=SPIHzConfig.Hz7629,
                        help=f'One of {SPIModeConfig.__dict__["_member_names_"]}')
    parser.add_argument('--spi_bus_num', nargs='?', default=0)
    parser.add_argument('--spi_device_num', nargs='?', default=0)
    parser.add_argument('--fps', nargs='?', default=15)
    parser.add_argument('--picamera_use_video_port', nargs='?', default=True)
    parser.add_argument('--picamera_format', nargs='?', default='jpeg')
    parser.add_argument('--picamera_resolution', nargs='?', default='640x480',
                        help="Camera resolution. Example: 640x480")
    args = parser.parse_args()
    main(args.model, args.consumertype, args.producertype, args.inputpath, args.outputpath, args.spi_hz, args.spi_mode,
         args.spi_bus_num, args.spi_device_num, args.fps, args.picamera_use_video_port, args.picamera_format,
         args.picamera_resolution)

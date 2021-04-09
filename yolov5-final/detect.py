import time
import cv2
import torch
import numpy as np
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, set_logging
from utils.torch_utils import select_device


def detect(source, weights, imgsz, device='gpu'):
    # Initialize
    set_logging()
    device = select_device(device)
    half = device.type != 'cpu'  # half precision only supported on CUDA
    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16
    # Padded resize
    img = letterbox(source, imgsz, stride=32)[0]
    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    tensor_img = torch.from_numpy(img).to(device)
    tensor_img = tensor_img.half() if half else tensor_img.float()  # uint8 to fp16/32
    tensor_img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if tensor_img.ndimension() == 3:
        tensor_img = tensor_img.unsqueeze(0)
    # Inference
    pred = model(tensor_img, augment=False)[0]
    # Apply NMS
    pred = non_max_suppression(pred, 0.25, 0.45, classes=0, agnostic=False)

    if len(pred[0].cpu().numpy()) != 0:
        """
            (x1, y1) = (int(pred[0].cpu().numpy()[0][0]), int(pred[0].cpu().numpy()[0][1]))
            (x2, y2) = (int(pred[0].cpu().numpy()[0][2]), int(pred[0].cpu().numpy()[0][3]))
        """
        print("==================================================================================")
        print(pred[0].cpu().numpy())
        show_img = img.transpose((1, 2, 0)).copy().astype(np.uint8)
        cv2.rectangle(show_img, (int(pred[0].cpu().numpy()[0][0]), int(pred[0].cpu().numpy()[0][1])),
                      (int(pred[0].cpu().numpy()[0][2]), int(pred[0].cpu().numpy()[0][3])), (0, 255, 0), 3)
        cv2.imshow('detect', show_img)
        cv2.moveWindow('detect', 1300, 500)
        cv2.waitKey(1)
    else:
        pass
    print(f'Done. ({time.time() - t0:.3f}s)')


if __name__ == '__main__':
    print(torch.cuda.is_available())
    with torch.no_grad():
        detect('./ROV', 'weights/best2.pt', 640)

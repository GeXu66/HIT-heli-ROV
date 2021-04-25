import time
import cv2
import torch
import numpy as np
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, set_logging
from utils.torch_utils import select_device


def detect(source, weights, imgsz, device='gpu', DEBUG=False):
    # Initialize
    label = ['circle', 'square']
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
    pred = model(tensor_img, augment=True)[0]
    # Apply NMS
    pred = non_max_suppression(pred, 0.25, 0.45, classes=(0, 1), agnostic=False)
    if len(pred[0].cpu().numpy()) != 0:
        """
            (x1, y1) = (int(pred[0].cpu().numpy()[0][0]), int(pred[0].cpu().numpy()[0][1]))
            (x2, y2) = (int(pred[0].cpu().numpy()[0][2]), int(pred[0].cpu().numpy()[0][3]))
        """
        print("==================================================================================")
        print(pred[0].cpu().numpy())
        if DEBUG:
            show_img = img.transpose((1, 2, 0)).copy().astype(np.uint8)
            show_img = cv2.cvtColor(show_img, cv2.COLOR_RGB2BGR)
            cv2.rectangle(show_img, (int(pred[0].cpu().numpy()[0][0]), int(pred[0].cpu().numpy()[0][1])),
                          (int(pred[0].cpu().numpy()[0][2]), int(pred[0].cpu().numpy()[0][3])), (0, 255, 0), 3)
            show_img = cv2.putText(show_img, label[int(pred[0].cpu().numpy()[0][5])],
                                   (int(show_img.shape[1] * 0.03), int(show_img.shape[0] * 0.2)),
                                   cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('detect', show_img)
            cv2.moveWindow('detect', 1300, 500)
            cv2.waitKey(1)
            return pred[0].cpu().numpy()[0]
        else:
            return pred[0].cpu().numpy()[0]
    else:
        pass
    print(f'Done. ({time.time() - t0:.3f}s)')

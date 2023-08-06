from seg_mask_modifs import mask_generator
import cv2
import numpy as np

cap = cv2.VideoCapture('mouth.mp4')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)
size = (frame_width, frame_height)
out = cv2.VideoWriter('mouth_out.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
obj = mask_generator.mask_generator()
while True:
    ret, img = cap.read()
    if ret:
        mask = obj.generate(img, ['upper_lip', 'lower_lip'])
        mask[mask > 200] = 127
        eye = cv2.merge([np.zeros((img.shape[:2]), dtype=np.uint8), np.zeros((img.shape[:2]), dtype=np.uint8), mask])
        mask = obj.generate(img, ['mouth'])
        mask[mask > 200] = 127
        nose = cv2.merge([np.zeros((img.shape[:2]), dtype=np.uint8), mask, np.zeros((img.shape[:2]), dtype=np.uint8)])
        res = cv2.add(img, eye)
        res = cv2.add(res, nose)
        out.write(res)
    else:
        break

cap.release()
out.release()

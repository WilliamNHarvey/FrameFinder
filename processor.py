import cv2
import numpy as np

def process_frame(img_rgb, template, count): 
  img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

  w, h = template.shape[::-1]

  res = cv2.matchTemplate(img_gray,template,cv2.TM_CCORR_NORMED)
  threshold = 0.95
  loc = np.where( res >= threshold)
  n_locations = len(list(zip(*loc[::-1])))
  if n_locations > 0:
    for pt in zip(*loc[::-1]):
      cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite('frames/res{0}.png'.format(count),img_rgb)
    return [1, count]
  return [0, count]

def imread(template_file):
  return cv2.imread(template_file,0)
---
title: udp视频传输
tags:
  - python
  - opencv
cover: /img/微信截图_20230720023925.png
categories:
- 折腾记录
date: 2023-07-02 00:30:26
description:
---
# 直接使用udp传输整个图片
这两个程序在本地局域网运行良好，但是一旦使用frp通过公网传输就会导致数据包丢失后一部分，或者说只有每张图片的前一部分数据能够传输成功

> server.py

```
import cv2
import socket
import numpy as np
import time

capture = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('127.0.0.1', 8088)

while True:
    t = time.time()
    ret, img = capture.read()
    params = [cv2.IMWRITE_JPEG_QUALITY, 0]
    data = cv2.imencode(".jpg", img, params)[1]
    data = np.array(data).tobytes()
    print(data)
    sock.sendto(data, addr)
    print(time.time() - t)
```

> client.py

```
import cv2
import socket
import numpy as np
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8088))

while True:
    data, addr = sock.recvfrom(65535)
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow('img', img)
    cv2.waitKey(1)
    print(len(img))
```

# 将图片分片传输

# MIT Marine Robotics Summer School

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository relates to the design of an ocean lander using a Raspberry Pi 0.

Our goal in this project is to capture the highest number of different marine species on camera.

## Contributors

- Thomas @wooohoooo
- Nick @nhpf
- David @dalmeida97
- Yosef @yosefguevara012
- Tell me your GitHub usernames :)

To avoid the computational overhead of video encoding, we will store a JPG sequence of 720p resolution. The FPS rate will be 2fps to avoid unnecessary redundancy and considering storage constraints.

To ensure proper setup during deployment, a live preview can be seen on a monitoring device.

After the JPG sequence is stored on the SD card, the lander will be retrieved and the images will be post-processed to automatically count the different species.

This post-processing comprises:

1. Color correction for underwater vision

   Choose one of the approaches:
   - Use GAN: [Underwater-Color-Correction](https://github.com/cameronfabbri/Underwater-Color-Correction)
   - Simpler algorithm: [Dive Color Corrector](https://github.com/bornfree/dive-color-corrector/tree/main)

2. Object detection and classification

   As suggested by @wooohoooo, an unsupervised approach is beneficial since we don't know how many types of fish there are, and we only care about differentiating them.

   @wooohoooo's suggestion was using DINOv2: [How to Classify Images with DINOv2](https://blog.roboflow.com/how-to-classify-images-with-dinov2/)

   Additional references:
   - [YOLO-Fish](https://www.sciencedirect.com/science/article/abs/pii/S1574954122002977)
   - [Automatic fish detection in underwater videos by a deep neural network-based hybrid motion learning system](https://academic.oup.com/icesjms/article/77/4/1295/5366225)

## Project Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
``

## License

This repository is licensed under the [MIT License](https://github.com/nhpf/mit-marine-robotics/blob/master/LICENSE)

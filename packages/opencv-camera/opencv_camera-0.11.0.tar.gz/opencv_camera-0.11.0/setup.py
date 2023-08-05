# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opencv_camera',
 'opencv_camera.apriltag',
 'opencv_camera.bin',
 'opencv_camera.display',
 'opencv_camera.mono',
 'opencv_camera.parameters',
 'opencv_camera.save',
 'opencv_camera.stereo',
 'opencv_camera.targets']

package_data = \
{'': ['*']}

install_requires = \
['attr', 'colorama', 'matplotlib', 'numpy', 'opencv-python']

entry_points = \
{'console_scripts': ['opencv_calibrate = '
                     'opencv_camera.bin.camera_calibrate:main',
                     'opencv_capture = opencv_camera.bin.video_capture:main',
                     'opencv_mjpeg = opencv_camera.bin.mjpeg_server:main',
                     'udp_client = opencv_camera.bin.udp_client:main',
                     'udp_server = opencv_camera.bin.udp_server:main']}

setup_kwargs = {
    'name': 'opencv-camera',
    'version': '0.11.0',
    'description': 'An OpenCV camera library',
    'long_description': '# OpenCV Camera\n\n![CheckPackage](https://github.com/MomsFriendlyRobotCompany/opencv_camera/workflows/CheckPackage/badge.svg)\n![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/opencv_camera)\n[![Latest Version](https://img.shields.io/pypi/v/opencv_camera.svg)](https://pypi.python.org/pypi/opencv_camera/)\n[![image](https://img.shields.io/pypi/pyversions/opencv_camera.svg)](https://pypi.python.org/pypi/opencv_camera)\n[![image](https://img.shields.io/pypi/format/opencv_camera.svg)](https://pypi.python.org/pypi/opencv_camera)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/opencv_camera?color=aqua)\n\nSimple threaded camera and calibration code using OpenCV. This tries to simplify some things\n\n## Install\n\nThe preferred way to install is using `pip`:\n\n```\npip install opencv_camera\n```\n\n## Usage\n\nSee the jupyter notebooks under the `docs` in the repository for some examples.\n\n### Colorspace\n\nChange between common colorspaces with:\n\n- `bgr2gray(image)`\n- `gray2bgr(image)`\n- `bgr2rgb(image)`\n- `rgb2bgr(image)`\n- `bgr2hsv(image)`\n- `hsv2bgr(image)`\n\n### Calibration\n\nCreate a mosaic of input calibration images with `mosaic(images, width)`\n\n![](https://github.com/MomsFriendlyRobotCompany/opencv_camera/blob/master/pics/mosaic.png?raw=true)\n\nCalibrate a camera with:\n\n```python\ncalibrator = CameraCalibration()\nboard = ChessboardFinder((9,6), 1)\ncam, cal = calibrator.calibrate(images, board)\n```\n\nDisplay all of the found image points with `coverage((width, height), imagePoints)`\n\n![](https://github.com/MomsFriendlyRobotCompany/opencv_camera/blob/master/pics/target-points.png?raw=true)\n\n### Distortion\n\nUse the found calibration parameters to undistort an image:\n\n```python\nun = UnDistort(cameraMatrix, distortionCoeff, w, h)\ncorr_img = un.undistort(image)\n```\n\nVisualize the lens distortion with:\n\n```python\nvisualizeDistortion(cameraMatrix, distortCoeff, height, width)\n```\n\n![](https://github.com/MomsFriendlyRobotCompany/opencv_camera/blob/master/pics/py-dist.png?raw=true)\n\n### Stereo\n\nCalibrate a stereo camera with:\n\n```python\nstereoCal = StereoCalibration()\nboard = ChessboardFinder((9,6), 1)\nok, cm, sc = stereoCal.calibrate(imgL, imgR, board)\n```\n\nDraw epipolar lines in stereo images with `drawEpipolarLines(imgpointsL,imgpointsR,imgL,imgR)`\n\n![](https://github.com/MomsFriendlyRobotCompany/opencv_camera/blob/master/pics/epipolar.png?raw=true)\n\n## Apps\n\nUse `program --help` to display switches for each of the following:\n\n- `opencv_calibrate`: calibrate a camera\n- `opencv_capture`: simple tool to capture and save images\n- `opencv_mjpeg`: sets up a simple jmpeg server so you can view images in a web browser\n- `udp_server x.x.x.x`: sends camera images via UDP\n- `udp_client x.x.x.x`: displays UDP camera images from server\n\n# ToDo\n\n- [ ] Add in `apriltag` calibration\n- [ ] Add pointcloud from stereo\n- [x] Add parameters for known cameras\n- [ ] Add Jupyter notebook documentation and examples\n- [x] Simplify stereo camera\n- [x] Add `computeReprojectionErrors` and `visualizeReprojErrors`\n- [x] Add `visualizeDistortion`\n- [ ] Add `visualizeExtrinsics`\n\n# Change Log\n\n| Data       | Version | Notes                                     |\n|------------|---------|-------------------------------------------|\n| 2020-12-27 | 0.10.10 | added distortion and reprojection display |\n| 2020-09-15 | 0.10.8 | added known camera params and general cleanup |\n| 2020-08-24 | 0.10.6 | added UDP image server and client |\n| 2020-07-03 | 0.10.2 | renamed and focused on camera |\n| 2018-07-19 |  0.9.4 | simple clean-up and updating some things |\n| 2017-10-29 |  0.9.3 | bug fixes |\n| 2017-04-09 |  0.9.0 | initial python 3 support |\n| 2017-03-31 |  0.7.0 | refactored and got rid of things I don\'t need |\n| 2017-01-29 |  0.6.0 | added video capture (video and images) program |\n| 2016-12-30 |  0.5.3 | typo fix |\n| 2016-12-30 |  0.5.1 | refactored |\n| 2016-12-11 |  0.5.0 | published to PyPi |\n| 2014-3-11  |  0.2.0 | started |\n\n# MIT License\n\n**Copyright (c) 2014 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/opencv_camera/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

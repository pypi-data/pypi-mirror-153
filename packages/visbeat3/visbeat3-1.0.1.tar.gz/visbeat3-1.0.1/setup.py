import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name="visbeat3",
  version="1.0.1",
  author="Haofan Wang",
  author_email="haofanwang.ai@gmail.com",
  description="Python3 Implementation for 'Visual Rhythm and Beat' SIGGRAPH 2018",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/haofanwang/visbeat3",
  packages=setuptools.find_packages(),
  install_requires=[
        'numpy',
        'scipy',
        'bs4',
        'librosa==0.9.1',
        'imageio==2.9.0',
        'imageio-ffmpeg==0.4.5',
        'requests',
        'moviepy==1.0.3',
        'termcolor',
        'youtube-dl',
        'matplotlib',
        'opencv-python'
    ],
  scripts=['bin/dancefer'],
  include_package_data=True,
  package_data={'data': ['visbeat3/assets/*']},
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: Apache Software License",
  "Operating System :: OS Independent",
  ],
)

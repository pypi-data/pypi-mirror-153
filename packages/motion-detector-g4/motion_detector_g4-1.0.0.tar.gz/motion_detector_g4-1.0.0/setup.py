from setuptools import setup
from os import path


top_level_directory = path.abspath(path.dirname(__file__))
with open(path.join(top_level_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
   name='motion_detector_g4',
   version='1.0.0',
   description='Motion Detector',
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Genzo',
   author_email='genzo@bk.ru',
   url='https://github.com/Genzo4/motion_detector',
   project_urls={
           'Bug Tracker': 'https://github.com/Genzo4/motion_detector/issues',
       },
   classifiers=[
      'Development Status :: 4 - Beta',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Intended Audience :: Developers',
      'Intended Audience :: Education',
      'Intended Audience :: Information Technology',
      'Natural Language :: English',
      'Natural Language :: Russian',
      'Topic :: Scientific/Engineering',
      'Topic :: Scientific/Engineering :: Image Recognition',
      'Topic :: Software Development',
      'Topic :: Software Development :: Libraries :: Python Modules'
   ],
   keywords=['motiondetector', 'motion_detector', 'motion-detector', 'opencv', 'opencv-contrib-python', 'g4'],
   license='MIT',
   packages=['motion_detector_g4'],
   install_requires=['opencv-contrib-python', 'numpy'],
   python_requires='>=3.6'
)
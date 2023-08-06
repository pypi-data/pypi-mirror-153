from setuptools import setup, find_packages
setup(name='MaskOff',
      version='0.4',
      url='https://github.com/ALEX-MGN/Maskoff.git',
      license='MIT',
      author='crazyShurik',
      author_email='pereverzev0701@mail.ru',
      packages = ['MaskOff'],
      install_requiers=['cmake','dlib','face_recognition','imutils']
      )
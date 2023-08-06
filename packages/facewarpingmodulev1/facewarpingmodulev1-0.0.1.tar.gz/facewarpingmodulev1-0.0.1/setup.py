from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='facewarpingmodulev1',
    version='0.0.1',
    description='Face Warping module',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Faiq Rauf',
    author_email='faiqrauf64@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='deepfakes',
    packages=find_packages(),
    install_requires=['pyYAML==3.12','yamlloader==1.1.0','easydict==1.7','matplotlib==1.5.3','dlib==19.16.0','opencv==3.4.0', 'tensorflow==2.7.0', 'tf-slim==1.1.0','easydict==1.9','dlib==19.16.0','opencv-python==3.4.17.63','opencv-contrib-python==4.5.5.64',' opencv-python-headless==4.5.2.52']
)
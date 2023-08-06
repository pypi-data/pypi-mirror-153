from setuptools import find_packages, setup

setup(
  name = 'cv_image_suit',
  packages = find_packages(),
  include_package_data=True,
  version = '0.6',
  license='GNU',
  description = 'Its an auto image classification and experimentation library',
  long_description='cv_image_suit is a deep learning image classification library written in Python, running on top of the machine learning platform TensorFlow.Keras. It was developed with a focus on enabling fast experimentation of images classification. You can classify any image with any classification model in Keras appliaction without writing any lines of code.',
  long_description_content_type="text/markdown",
  url="https://github.com/uday446/cv_image_suit",
  author = 'Udayrajsinh Jadeja',
  author_email = 'ujadeja96@gmail.com',
  keywords = ['cv_image_suit'],
  install_requires=[
        'tensorflow==2.4.1',
        'scipy',
        'numpy',
        'pandas',
        'Pillow==8.3.2',
        'fastapi',
        'typing_extensions==4.2.0'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  entry_points={
        "console_scripts": [
            "cv_image_suit = cv_image_suit.main:start_app",
        ]},
)

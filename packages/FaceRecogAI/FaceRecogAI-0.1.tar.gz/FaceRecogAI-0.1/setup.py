from setuptools import setup, find_packages


setup(
    name='FaceRecogAI',
    version='0.1',
    license='MIT',
    author="Sai Pranav Kishan (Eliza Kishan)",
    author_email='saipranavkishan@outlook.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='Face Recognition',
    install_requires=[
          'opencv-python',
      ],

)
from setuptools import setup, find_packages

setup(
    name='simctg',
    version='0.1',
    license='MIT',
    author="Yixuan Su",
    author_email='ys484@outlook.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/yxuansu/SimCTG',
    keywords='SimCTG Library',
    install_requires=[
          'absl-py',
          'pytest',
          'sacrebleu==1.4.10',
          'six',
          'wheel',
          'progressbar', 
          'sklearn', 
          'torch==1.6.0', 
          'torchvision==0.7.0',
          'transformers==4.7.0',
          'pyyaml',
          'nltk',
          'sentencepiece',
          'spacy',
          'gdown',
          'seaborn',
          'matplotlib',
          'pandas',
      ],

)
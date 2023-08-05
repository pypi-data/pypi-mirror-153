from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='HoloNet',
    version='0.0.4',
    packages=['HoloNet', 'HoloNet.tools', 'HoloNet.plotting', 'HoloNet.predicting', 'HoloNet.preprocessing'],
    url='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    author='lihaochen',
    author_email='1421127652@qq.com',
    description='Decoding functional cell–cell communication events by multi-view graph learning on spatial transcriptomics',
    install_requires=[
        'pynvml',
        'numpy',
        'torch',
        'pandas',
        'anndata',
        'tqdm',
        'scipy',
        'scikit-learn',
        'scanpy',
        'networkx',
        'matplotlib',
        'seaborn'
        ],
)

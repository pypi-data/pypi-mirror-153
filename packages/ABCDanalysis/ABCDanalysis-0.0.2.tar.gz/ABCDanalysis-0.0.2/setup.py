from gettext import install
from setuptools import setup, find_packages

setup(
    name = 'ABCDanalysis',
    version = '0.0.2',
    description= 'analysis the ABCD dataset to predict mental health issue',
    py_modules=['BinaryNeuralNet','BestData', 'BestExplainer', 'EnsembleClassifier', 'Utils', 'Dashbaord'],
    

    install_requires = ["Pandas"],

    #packages=find_packages("src"),  # include all packages under src
    package_dir={'':'src'},
)

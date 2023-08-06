from setuptools import setup

setup(
    name='PhonemeSER',

    version='1.0.1',

    description='Predict speech emotions from wav files.',

    py_modules=['PhonemeSER', 'predict', 'Train_test', 'FormantsLib/FormantsExtract', 'FormantsLib/FormatsHDFread']
)
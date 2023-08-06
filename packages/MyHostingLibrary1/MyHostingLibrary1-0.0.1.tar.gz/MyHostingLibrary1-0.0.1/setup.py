from setuptools import find_packages, setup 

setup(
    name='MyHostingLibrary1',
    packages=find_packages(),
    version='0.0.1',
    description='My first Python library',
    author='Ingenieria Biomedica Cohorte 2020',
    author_email= 'monitortemperaturaiuhi@gmail.com',
    license='MIT',
    install_requires=['tkinter', 'pyrebase', 'random', 'time', 'datetime', 'email.message', 'Adafruit_DHT', 'RPi.GPIO', 'os'],
    keywords= 'bioterio',
)
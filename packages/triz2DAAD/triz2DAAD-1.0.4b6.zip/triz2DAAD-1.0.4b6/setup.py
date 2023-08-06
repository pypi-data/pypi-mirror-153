from setuptools import setup

with open('README.txt', encoding='UTF-8') as f:
	a=f.read()

setup(
	name='triz2DAAD',
	author="Pedro Fernández",
	author_email="rockersuke@gmail.com",
	version='1.0.4b6',
	license="MIT",	
	url="http://www.zonafi.es/triz2DAAD/",
	description="Convierte mapas de aventuras de texto generados por Trizbort en código fuente para el DAAD.",
	long_description=a,
	python_requires=">=3.6",
	scripts=['triz2DAAD.py']
)
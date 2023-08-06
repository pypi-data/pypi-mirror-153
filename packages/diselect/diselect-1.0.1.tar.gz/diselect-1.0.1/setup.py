from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name='diselect',
	version='1.0.1',
	license='MIT',
	description='smart and convenient dict flatten library for complex container nested with dict and list',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author = 'HS Moon',
	author_email = 'pbr112@naver.com',
	py_modules = ['diselect'],
	install_requires=[],
	keywords='crawlite',
	url='https://github.com/zwolf21/diselect',
	packages=find_packages(exclude=['contrib', 'docs', 'tests']),
	classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
	python_requires=">=3.8"
)

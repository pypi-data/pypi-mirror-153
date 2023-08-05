from setuptools import setup, find_packages



setup(
	name='diselect',
	version='0.0.1',
	license='MIT',
	description='smart and convenient value selector in complex container nested with dict and list(from json data)',
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
)

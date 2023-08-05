from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10 ',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='caged',
    version='0.0.1',
    description='Dados do NOVO CAGED',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Guilherme Nogueira',
    author_email='guilherme.info.nog@aluno.ufsj.edu.br',
    license='MIT',
    classifiers=classifiers,
    keywords='novo caged',
    packages=find_packages(),
    install_requires=['']
)
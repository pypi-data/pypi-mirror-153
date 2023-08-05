from setuptools import setup, find_packages

classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: Microsoft :: Windows :: Windows 10 ',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]

setup(
    name='ngcaged',
    version='1.0.0',
    author='Guilherme Nogueira',
    author_email='guilherme.info.nog@aluno.ufsj.edu.br',
    packages=['ngcaged'],
    description='Dados do NOVO CAGED',
    long_description=open('README.md').read() + '\n',
    url='',
    license='MIT',
    classifiers=classifiers,
    keywords='novo caged',
    install_requires=['']
)
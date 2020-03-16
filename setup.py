from distutils.core import setup

requiremets = open('requirements.txt').read().split("\n")
setup(
    name='crismis_gsoc',
    packages=['crismis_gsoc'],
    version='1.0',
    license='MIT',
    description='GSoC 2020 CRISMIS project task',
    author='Ankur Kumar',
    author_email='ank@leoank.me',
    entry_points='''
        [console_scripts]
        crismis_gsoc=bin.crismis_gsoc:cli
    ''' ,
    url='https://github.com/leoank/crismis_gsoc',
    keywords=['GSoC', 'CRISMIS'],
    install_requires=requiremets,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

from distutils.core import setup
setup(
    name='OMSTD-lefito',
    version='dev',
    packages=['omstd_lefito', 'omstd_lefito.lib'],
    url='',
    license='MIT',
    entry_points={
        'console_scripts': [
            'omstd-lefito = omstd_lefito.lefito:main',
            ],
    },
    author='pertxas',
    author_email='partxas<-at->gmail.com',
    description='OMSTD Exercise: LFI scanner.',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        ],
)

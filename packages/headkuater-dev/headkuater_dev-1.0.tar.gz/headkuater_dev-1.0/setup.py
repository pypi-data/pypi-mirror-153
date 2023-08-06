from setuptools import setup, find_packages
import app




setup(
    name='headkuater_dev',
    version=1.0,
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'headkuter =app:headkurter'  #ponting to executeable function
        ]
    },
    install__requires=[
        'click==8.1.3',
        'colorama==0.4.4',
    ],
        zip_safe = False
    )
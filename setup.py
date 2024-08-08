from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'youtube_dl',
    'pathlib',
    'pandas'
]

setup(
    name='DataCreep',
    version='1.0',
    description='An application that analyzes a Spotify user\'s listening data',
    author='Siddha Basu',
    author_email='basu.siddha@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
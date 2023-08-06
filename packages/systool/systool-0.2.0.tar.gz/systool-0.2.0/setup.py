from setuptools import setup


setup(
    name='systool',
    version='0.02.00',
    license='MIT',
    author="Bruna Calazans (bruna-calazans) & Pedro Chiachio (MoleDownTheHole)",
    author_email='pcardoso@systra.com',
    package_dir={'': 'main'},
    include_package_data=True,
    package_data={'utils': ['charts.py', 'maps.py', 'readWrite.py']},
    url='https://github.com/MoleDownTheHole/SysTool',
    keywords='systool',
    install_requires=['pytest', 'pandas', 'numpy', 'matplotlib', 'matplotlib_scalebar', 'geopandas'],
)

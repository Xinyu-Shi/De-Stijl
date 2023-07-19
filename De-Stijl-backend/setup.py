from setuptools import setup, find_packages

setup(
    name='de_stijl',
    version='0.0.1',
    packages=find_packages("src"),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    install_requires=[
        'scipy==1.8.0',
        'imgaug==0.4.0',
        'sklearn',
        'ipython==8.1.1',
        'colorthief==0.2.1',
        'Flask==2.0.3',
        'Flask-RESTful==0.3.9',
    ]
)
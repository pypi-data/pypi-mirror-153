from setuptools import setup


setup(
    name='vteklib',
    version='0.1.0',
    packages=['vteklib', 'vteklib.utils', 'vteklib.regressions'],
    install_requires=['numpy', 'matplotlib', 'pandas', 'sklearn', 'scipy'],
    url='https://github.com/mixx3/vteklib',
    license='BSD 2-Clause "Simplified"',
    author='Mike Parfenov',
    author_email='mmikee00800@gmail.com',
    description='Wrapper around matplotlib for easier 2D approximation & scientific-style plots'
)

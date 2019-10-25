from setuptools import setup

setup(
    name='Calculus Solids of Known Volume',
    version='0.8.1dev',
    packages=['calculus_solids','calculus_solids.web'],
    package_data = {
        'calculus_solids.web': ['static/*','static/**/*','templates/*'],
        'calculus_solids':['plotly_template.html']
    },
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires=[
        'Flask','numpy-stl','enum34','python-utils','numpy','sympy','pyparsing'
    ],
    long_description=open('README.md').read(),
    
)

from setuptools import setup

setup(name='dh-poetry-cypherpunkdev',
      version='0.2.5',
      description='Shim between dh-virtualenv and poetry',
      url='https://github.com/CypherpunkDev/dh-poetry',
      author='CypherpunkDev',
      author_email='maikelwever@gmail.com',
      license='MIT',
      zip_safe=False,
      packages=['dh_poetry'],
      entry_points={
          'console_scripts': ['dh-poetry=dh_poetry.command_line:main'],
      },
)

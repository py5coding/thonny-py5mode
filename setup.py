import pathlib
from setuptools import setup

version = pathlib.Path(__file__).parent.absolute()
version = version / 'thonnycontrib/thonny-py5mode/_version.py'
exec(open(version).read())

README = (pathlib.Path(__file__).parent / 'README.md').read_text()

setup(
  name='thonny-py5mode',
  version=__version__,
  description='py5 mode plugin for Thonny',
  long_description=README,
  long_description_content_type='text/markdown',
  url='https://github.com/tabreturn/thonny-py5mode',
  author='tabreturn',
  author_email='thonny-py5mode@tabreturn.com',
  license='MIT',
  classifiers=[
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    'Environment :: Plugins',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Text Editors :: Integrated Development Environments (IDE)'
  ],
  packages=[
    'thonnycontrib.backend',
    'thonnycontrib.kyanite_theme_syntax',
    'thonnycontrib.kyanite_theme_ui',
    'thonnycontrib.thonny-py5mode',
    'thonnycontrib.thonny-py5mode.py5colorpicker.tkcolorpicker'
  ],
  install_requires=[
    'install-jdk==1.1.0',
    'py5',
    'pyperclip==1.9.0'
  ]
)

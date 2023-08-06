from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Simple interface for working with intents and chatbots. A built upon version of Neuralnines package.'
LONG_DESCRIPTION = 'Simple interface for working with intents and chatbots. A built upon version of Neuralnines package.'

# Setting up
setup(
    name="neuralintentsplus",
    version=VERSION,
    author="Joshua Eworo",
    author_email="<eworojoshua@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/JoshuaEworo/neuralintents",
    packages=find_packages(),
    install_requires=['numpy', 'nltk', 'tensorflow'],
    keywords=['python', 'neural', 'machine learning', 'chatbots', 'chat', 'artificial intelligence', 'virtual assistant'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
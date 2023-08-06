from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='twyclip',
    version='1.0.2',
    description='TwyClip is a Python library for get Twitch clip download link.',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    # url="",
    author='John Doe',
    license='The Unlicense (Unlicense)',
    install_requires=['requests'],
    keywords=['twitch'],
    python_requires='>=3.8'
)
# python setup.py sdist bdist_wheel
# twine upload dist/*
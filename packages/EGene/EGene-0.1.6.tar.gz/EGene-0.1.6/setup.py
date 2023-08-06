from setuptools import setup
import io

with io.open('README.md', encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

print(LONG_DESCRIPTION)

setup(
    name="EGene",
    version="0.1.6",
    author="Ethan Anderson",
    author_email="telan4892@gmail.com",
    url="https://github.com/Elan456/EGene",
    install_requires=['pygame'],
    packages=["egene"],
    license="MIT",
    description="Tool for applying, visualizing, and training neural networks using a genetic algorithm",

    package_data={"": ["images/Icon.png"]},
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown'
)
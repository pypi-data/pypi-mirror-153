from setuptools import setup

__version__ = "1.4.1"

with open('requirements.txt') as file:
    requirements = list(filter(lambda x: x, [line.strip() for line in file.readlines()]))

setup(
    name="devops_post_service_project_2022",
    version=__version__,
    packages=['post_service'],
    install_requires=requirements
)

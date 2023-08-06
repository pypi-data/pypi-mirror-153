from setuptools import setup

__version__ = "1.2.1"

with open('requirements.txt') as file:
    requirements = list(filter(lambda x: x, [line.strip() for line in file.readlines()]))

setup(
    name="devops_event_service_project_2022_tim1",
    version=__version__,
    packages=['event_service'],
    install_requires=requirements
)

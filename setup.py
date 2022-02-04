""" Install the ovos_mpris_skills_interface package
"""
from setuptools import setup

setup(
    name='ovos_mpris_skills_interface',
    version='0.0.1',
    url='https://github.com/OpenVoiceOS/ovos_mpris_skills_interface',
    keywords='OVOS MPRIS daemon service',
    packages=['ovos_mpris_skills_interface'],
    install_requires=['dbus-next', 'mycroft-messagebus-client'],
    include_package_data=True,
    license='Apache',
    author='Aditya Mehra',
    author_email='aix.m@outlook.com',
    description='An MPRIS daemon that registers a MediaPlayer2 interface for multimedia skills and frameworks',
    entry_points={
        'console_scripts': [
            'ovos_mpris_skills_interface=ovos_mpris_skills_interface.__main__:main',
            ]
        }
)

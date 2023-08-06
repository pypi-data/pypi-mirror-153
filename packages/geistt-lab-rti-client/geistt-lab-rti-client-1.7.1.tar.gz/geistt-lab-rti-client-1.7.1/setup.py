import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='geistt-lab-rti-client',
    packages=[
        'geistt_lab_rti_client',
        'geistt_lab_rti_client.proto',
        'geistt_lab_rti_client.generated'
    ],
    version='1.7.1',
    license='Apache license 2.0',
    author='GEISTT AB',
    author_email='packages@geistt.com',
    url='https://gitlab.com/geistt/lab/rti',
    description='GEISTT Lab RTI Client',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=['RTI'],
    install_requires=[
        'protobuf',
        'socketclusterclient',
        'emitter.py'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

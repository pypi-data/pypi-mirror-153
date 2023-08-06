import sys
from pathlib import Path
import setuptools


long_description = (Path(__file__).parent / "README.md").read_text()

if sys.version_info < (3, 6):
    sys.exit('Python>=3.6 is required by forte-medical.')

setuptools.setup(
    name="forte.health",
    version='0.1.0',
    url="https://github.com/asyml/ForteHealth",
    description="NLP pipeline framework for biomedical and clinical domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License Version 2.0',
    packages=setuptools.find_namespace_packages(
        include=['fortex.health', 'ftx.*'],
        exclude=["scripts*", "examples*", "tests*"]
    ),
    namespace_packages=["fortex"],
    install_requires=[
        'forte~=0.2.0',
        "sortedcontainers==2.1.0",
        "numpy>=1.16.6",
        "jsonpickle==1.4",
        "pyyaml==5.4",
        "smart-open>=1.8.4",
        "typed_astunparse==2.1.4",
        "funcsigs==1.0.2",
        "mypy_extensions==0.4.3",
        "typed_ast>=1.4.3",
        "jsonschema==3.0.2",
        "texar-pytorch",
        'typing>=3.7.4;python_version<"3.5"',
        "typing-inspect>=0.6.0",
        'dataclasses~=0.7;python_version<"3.7"',
        'importlib-resources==5.1.4;python_version<"3.7"',
        'dataclasses~=0.7;python_version<"3.7"',
        "fastapi==0.65.2",
        "uvicorn==0.14.0",
    ],
    extras_require={
        "test": [
            "ddt",
            "testfixtures",
            "transformers==4.2.2",
            "protobuf==3.19.4",
        ],
    },
    entry_points={
        'console_scripts': [
            "forte-medical-train=forte_medical_cli.train:main",
            "forte-medical-process=forte_medical_cli.process:main",
            "forte-medical-evaluate=forte_medical_cli.evaluate:main",
        ]
    },
    include_package_data=True,
    python_requires='>=3.6'
)

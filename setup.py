from setuptools import setup,find_packages

setup(
    name="researchain",
    version='0.1.0',
    packages=find_packages(include=['researchain']),
    install_requires=[
        "git_manager>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            # "명령어=패키지.모듈:함수" 형태
            "researchain=researchain.cli:main",
        ],
    },
    author="seungeon lee",
    description="Research-AI efficiency tool"

)
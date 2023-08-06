import setuptools
import subprocess


def git(*args):
    return subprocess.check_output(["git"] + list(args))


# get latest tag
# latest = git("describe", "--tags").decode().strip()
# latest = latest.split('-')[0]
latest = "1.2.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commonroad_agent",
    version=latest,
    description="Agent simulation with behavior models for CommonRoad",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# EOF

from setuptools import find_packages, setup


def read_requirements(filename: str):
    with open(filename) as requirements_file:
        import re

        def fix_url_dependencies(req: str) -> str:
            """Pip and setuptools disagree about how URL dependencies should be handled."""
            m = re.match(
                r"^(git\+)?(https|ssh)://(git@)?github\.com/([\w-]+)/(?P<name>[\w-]+)\.git", req
            )
            if m is None:
                return req
            else:
                return f"{m.group('name')} @ {req}"

        requirements = []
        for line in requirements_file:
            line = line.strip()
            if line.startswith("#") or len(line) <= 0:
                continue
            requirements.append(fix_url_dependencies(line))
    return requirements


app_info = {}  # type: ignore
with open("geezlit/version.py", "r") as version_file:
    exec(version_file.read(), app_info)

setup(
    name=app_info["__title__"],
    version=app_info["__version__"],
    description=app_info["__description__"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=app_info["__url__"],
    author=app_info["__author__"],
    author_email=app_info["__author_email__"],
    license=app_info["__license__"],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_data={"geezlit": ["py.typed"]},
    install_requires=read_requirements("requirements.txt"),
    extras_require={"dev": read_requirements("dev-requirements.txt")},
    python_requires=">=3.5",
    entry_points={
        "console_scripts": ["geezlit=geezlit.cli:main"],
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="geez, transliteration",
)

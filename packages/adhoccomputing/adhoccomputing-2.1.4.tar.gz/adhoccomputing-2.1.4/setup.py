from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
  # TODO: Fix the configs in this part
  name='adhoccomputing',
  version='2.1.4',
  description="Ad Hoc Computing Library",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/cengwins/ahc',
  author='CengWins',
  author_email='ahc@ceng.metu.edu.tr',
  license='BSD 2-clause',
  packages=find_packages(),
  install_requires=[
    'matplotlib',
    'networkx',
    'setuptools',
  ],
  project_urls={
        "Bug Tracker": "https://github.com/cengwins/ahc/issues",
        "Simulator Website": "https://ahc.ceng.metu.edu.tr"
  },
  classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
  python_requires=">=3.8",
)



from setuptools import setup, find_packages


setup(name="tap-customerio",
      version="0.1.1",
      description="Singer.io tap for extracting data from customerio API",
      author="Stitch",
      url="http://singer.io",
      classifiers=["Programming Language :: Python :: 3 :: Only"],
      py_modules=["tap_customerio"],
      install_requires=[
        "singer-python==6.8.0",
        "requests==2.34.2",
        "backoff==2.2.1",
        "parameterized"
      ],
      extras_require={"dev": ["pylint", "ipdb", "pytest", "coverage"]},
      entry_points="""
          [console_scripts]
          tap-customerio=tap_customerio:main
      """,
      packages=find_packages(),
      package_data = {
          "tap_customerio": ["schemas/*.json"],
      },
      include_package_data=True,
)

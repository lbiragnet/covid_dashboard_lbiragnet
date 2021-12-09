from setuptools import setup, find_packages

with open("README.md", "r") as readme:
   user_manual = readme.read()

setup(
   name="covid19_dashboard_lbiragnet",
   version="0.0.2",
   author="Luc Biragnet",
   author_email="lucbiragnet@gmail.com",
   description="Covid-19 dashboard with access to live data and news articles",
   long_description=user_manual,
   long_description_content_type="text/markdown",
   url="https://github.com/lbiragnet/covid_dashboard_lbiragnet",
   py_modules=["main", "covid_data_handler", "covid_news_handling", "time_calculations"],
   packages=find_packages("src"),
   packages_dir={"":"src"},
   package_data={"srcpkg":["config/*.json", "datafiles/*.json", "*.csv"]},
   include_package_data=True,
   license="MIT",
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   python_requires=">=3.8",
)

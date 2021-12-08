from setuptools import setup

with open("README.md", "r") as readme:
   user_manual = readme.read()

setup(
   name="covid19_dashboard_lbiragnet",
   version="0.0.1",
   author="Luc Biragnet",
   author_email="lucbiragnet@gmail.com",
   description="Covid-19 dashboard with access to live data and news articles",
   long_description=user_manual,
   long_description_content_type="test/markdown",
   url="https://github.com/lbiragnet/Covid19-Dashboard-lbiragnet",
   py_modules=["main", "covid_data_handler", "covid_news_handling", "time_calculations"],
   package_dir={"": "src"},
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   python_requires=">=3.8",
)

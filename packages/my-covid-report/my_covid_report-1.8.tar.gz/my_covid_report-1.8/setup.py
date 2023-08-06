from distutils.core import setup
setup(
name="my_covid_report",
version="1.8",
description="covid-19 data analysis by WhaleG",
author="WhaleG",
license = 'MIT',
python_requires='>=3.7',
url='https://github.com/datoujinggzj/WhaleDataAnalysisProject',
py_modules=["covid_report.getdata","covid_report.data_processing","covid_report.covid_visualization"]
)

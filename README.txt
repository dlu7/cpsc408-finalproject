Debbie Lu
2292435
dlu@chapman.edu
CPSC 408
Final Project - Movie Database

Instructions:
Run movies.py

Deliverables:
schema.sql
movies.py
Presentation Slides
Final Report

References: 
https://stackoverflow.com/questions/290223/what-is-the-difference-between-bit-and-tinyint-in-mysql
https://stackoverflow.com/questions/24347895/regex-for-hour-minute-and-second-format-hhmmss
https://pynative.com/python-mysql-transaction-management-using-commit-rollback/#h-python-mysql-commit-rollback-and-setautocommit-to-manage-transactions
https://pandas.pydata.org/pandas-docs/stable/index.html

Notes:
Most of the data in the tables were generated using the Faker package. 

Known Errors:
Certain SQL statements will execute even when the user and/or movie does not exist, but others will rollback as intended.
Rollback is still implemented for these SQL statements despite this error.

Solution contains in banks.py file. To run this file you can provide Env variables or use the default values for new csv file name, header names, etc.

List of Environment variables that you can provide is given below:

- CSV_OUTPUT_FILE_NAME - New CSV filename that is combined from given csv files. Default is 'combined.csv'
- CSV_TIME_HEADER - Header name for transaction time. Default is 'transaction_time'
- CVS_TYPE_HEADER - Header name for transaction type. Default is 'transaction_type'
- CVS_AMOUNT_HEADER - Header name for transaction amount. Default is 'transaction_amount'
- CVS_TO_HEADER - Header name for transaction to. Default is 'transaction_to'
- CVS_FROM_HEADER - Header name for transaction from. Default is 'transaction_from'
- TRANSACTION_TIME_TO_FORMAT - Transaction time format in newly created file. Default is '%d.%m.%Y'
- CSV_FILES_AND_PARSERS - Json of csv_files as key and parsers as value. Currently available parsers are Parser1, Parser2, and Parser3 Default is '{"bank1.csv":"Parser1","bank2.csv":"Parser2","bank3.csv":"Parser3"}'

## Requirements
- python-dotenv
- pytest

--

### SOBERS Assignment

# Introduction
For this assingment our client has a website that takes personal export of banking history.
And displays it in the frontend.
There is already a version that runs for single bank.
But now you have the task to create a script that parses data from multiple banks.
In the future the client wants to add more banks.

# Assingment 
You are tasked to create script that will parse multiple csv's and create a unified csv.
There are 3 different csv's, this will increase in the future.
The client has as hard requirement that the result is stored as csv file.
But json and xml will be used in the future, maybe even storing the result in a database.

In the data folder there are 3 csv's with banking data.
Since the csv's come from different banks the layout of data can differ.
The bank statements have data from the month October.

# Scoring 
create a script according to above specified requirements.
You are allowed to take as much time as needed, But try to manage your time to around 1 or 2 hours.
Since we are Python shop the script must be done with Python.
Scoring is based on:
- Correctness
- Code archticture
- Maintainablity
- Testablity
- Extendablity
- Pythonicness of code

Test are not required, but plus points for tests.
This is moment for to show your skills. 

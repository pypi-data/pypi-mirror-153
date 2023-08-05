# Package ```nseinfopackage```
Date: 31-May2022
## Installation

Use the following for importing: ```from nseinfo import ni```

## Prerequisites
The ```pandas```  package will be imported as ```pd```.

## Features
This is a comprehensive app that will allow you to get the details of about 1800 stocks from the National Stock Exchange (NSE) India. This package is developed from the data that is shared by NSE. There are many methods with the help of which you can get the following details:

* Symbol of the company
* Name of the Company
* ISIN Number of the company
* Date of listing
* Paid up Value
* Market lot, and
* Face Value

## Methods of the Package
This package is powered by many useful methods. The following is the list of all the methods and their return types.

1. ```ni.getISINNumber(symbol)``` This method takes the string input (```symbol```) of the NSE stock as a string and returns the ISIN number of that stock as a string.
2. ```ni.getSymbol(isin)``` This method takes the string input (```isin```) of the NSE stock as a string and returns the SYMBOL of that stock as a string.
3. ```ni.getName(irs, value)``` This method takes two arguments - ```irs``` and ```value```. The name of the first argument - irs stands for ISIN or Symboe - hence irs. You can use either ISIN or SYMBOL to get the name of the company. Examples will be given below.
4. ```ni.getMarketLot(irs, value)``` This method helps you in getting the value of Market Lot, as an integer. Input to the method would be either ISIN or SYMBOL, and example of its usage is given below.
5. ```ni.getFaceValue(irs, value)``` This method helps you in getting the Face value of the underlying stock, as an integer. Input to the method would be either ISIN or SYMBOL, and example of its usage is given below.
6. ```ni.getPaidUpValue(irs, value)``` This method helps you in getting the Paid-up value of the underlying stock, as an integer. Input to the method would be either ISIN or SYMBOL, and example of its usage is given below.
7. ```ni.listedSince(irs, value)``` This method helps you in fetching the date since the stock was listed in the NSE exchange. Input to this would be, again, irs and value. Examples are shown below.
8. ```ni.getISINNumbers(symbols)``` This methods takes a list of strings (SYMBOLS) as the argument, and provides a list of corresponding ISIN values, in that order.
9. ```ni.getSymbols(isins)``` This methods takes a list of strings (ISIN) as the argument, and provides a list of corresponding SYMBOL values, in that order.

## Method details with examples
1. The ```ni.getISINNumber(symbol)``` method accepts ```symbol``` which is a string variable. It returns ```ISIN```, which is also a string, and any ISIN begins with ```INE```. Example:
  1. ```ni.getISINNumber('INFY')``` returns ```INE009A01021```
  1. ```ni.getISINNumber('M&M')``` returns ```INE101A01026```
1. The ```ni.getSymbol(isin)``` method accepts ```isin``` which is a string variable, and returns SYMBOL, which is also a string variable. Here are a couple of examples:
  1. ```ni.getSymbol('INE009A01021')``` returns 'INFY'
  1. ```ni.getSymbol('INE101A01026')``` returns 'M&M'
1. The ```getName(irs, value)``` method accepts two inputs - ```irs``` and ```value```. The ```irs``` can have one of the two values - 'SYMBOL' or 'ISIN'. Based on this the value of ```value``` changes. See the below exmaples for clarity:
  1. ```ni.getName('SYMBOL', 'INFY')``` will return "Infosys Limited"
  1. ```ni.getName('ISIN NUMBER', 'INE009A01021')``` will also return "Infosys Limited"
1. The method ```getMarketLot(irs, value)``` also accepts two inputs - ```irs``` and ```value```. The ```irs``` can have one of the two values - 'SYMBOL' or 'ISIN NUMBER'. Based on this the value of ```value``` changes. The return value is an integer. See the below exmaples:
  1. ```ni.getMarketLot('SYMBOL', 'INFY')``` will return integer value of 1.
  1. ```ni.getMarketLot('ISIN NUMBER', 'INE768C01010')``` will return integer value of 1.
1. The method ```ni.getFaceValue(irs, value)``` accepts two inputs - ```irs``` and ```value```. The ```irs``` can have one of the two values - 'SYMBOL' or 'ISIN NUMBER'. Based on this the value of ```value``` changes. The return value is an integer. See the below exmaples:
  1. ```ni.getFaceValue('ISIN NUMBER', 'INE768C01010')``` will return 10.
  1. ```ni.getFaceValue('SYMBOL', 'ICICIBANK')``` will return a value of 2.
1. The method ```ni.getPaidUpValue(irs, value)``` is also similar to the above methods. This method accepts two inputs - ```irs``` and ```value```. The ```irs``` can have one of the two values - 'SYMBOL' or 'ISIN NUMBER'. Based on this the value of ```value``` changes. The return value is an integer. See the below exmaples:
  1. ```ni.getPaidUpValue('SYMBOL', 'ICICIBANK')``` returns a value of 2.
  1. ```ni.getPaidUpValue('ISIN NUMBER', 'INE040A01034')``` returns a value of 1.
1. The ```ni.listedSince(irs, value)``` method, like the others, accepts two inputs - ```irs``` and ```value```. The ```irs``` can have one of the two values - 'SYMBOL' or 'ISIN NUMBER'. Based on this the value of ```value``` changes. The return value is string representation of date. Below are the examples:
  1. ```ni.listedSince('SYMBOL', 'INFY')``` will return '08-FEB-1995'.
  1. ```ni.listedSince('ISIN NUMBER', 'INE358U01012')``` returns '19-AUG-2019'
1. The method ```getISINNumbers(symbols)``` accept an array of symbols and return corresponding array of ISIN Numbers. Below are the examples.
  1. ```ni.getISINNumbers(['INFY','HDFCBANK', 'ICICIBANK'])``` returns ['INE009A01021', 'INE040A01034', 'INE090A01021']
1. The method ```getSymbols(isins)``` accept an array of ISIN Numbers and return corresponding arrays of SYMBOLS. Below is the typical example:
  1. ```ni.getSymbols(['INE009A01021', 'INE040A01034', 'INE090A01021'])``` returns ['INFY', 'HDFCBANK', 'ICICIBANK']
## Notes and Caveats
* The ISINs or SYMBOLS are limited to SERIES type 'EQ' or Equities only. 
* If there is an error in the input (ISIN Number or Symbol), the method returns an error 'Error! Some input values are incorrect or not found!' for all the methods other than ```ni.getSymbols()``` and ```ni.getISINNumbers()```. In case there are any errors with regards to the list of SYMBOLS or list of ISIN Numbers, then there is specific error with respect to that element, and the return will have a subset of the return value. For example, when you run the method ```ni.getSymbols(['INE009A01021', 'INE040A08034', 'INE090A01021'])```, the output will be ['INFY', 'ICICIBANK'], along with an error message 'Error! Some input values are incorrect or not found!'

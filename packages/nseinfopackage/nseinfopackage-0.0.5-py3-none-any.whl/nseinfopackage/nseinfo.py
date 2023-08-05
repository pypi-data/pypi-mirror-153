import pandas as pd
from . import data as dt

data = dt.return_data()
dff = pd.DataFrame(data, columns=["SYMBOL", "NAME OF COMPANY", "SERIES", "DATE OF LISTING", "PAID UP VALUE", "MARKET LOT", "ISIN NUMBER", "FACE VALUE"])
'''
This method will'''
def getISINNumber(symbol):
    result = dff[dff['SYMBOL'] == symbol]
    if result.empty:
        return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    else:
        return result['ISIN NUMBER'].iloc[0]

def getSymbol(isin):
    result = dff[dff['ISIN NUMBER'] == isin]
    if result.empty:
        return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    else:
        return result['SYMBOL'].iloc[0]

def getName(irs, value):
    if irs == 'SYMBOL':
        result = dff[dff['SYMBOL'] == value]
        if result.empty != True:
            return result['NAME OF COMPANY'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    elif irs == 'ISIN NUMBER':
        result = dff[dff['ISIN NUMBER'] == value]
        if result.empty != True:
            return result['NAME OF COMPANY'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    else:
        return 'Error! Wrong ISIN, SYMBOL or irs value provided!'

def getMarketLot(irs, value):
    if irs == 'SYMBOL':
        result = dff[dff['SYMBOL'] == value]
        if result.empty != True:
            return result['MARKET LOT'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    elif irs == 'ISIN NUMBER':
        result = dff[dff['ISIN NUMBER'] == value]
        if result.empty != True:
            return result['MARKET LOT'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    else:
        return 'Error! Wrong ISIN, SYMBOL or irs value provided!'

def getFaceValue(irs, value):
    if irs == 'SYMBOL':
        result = dff[dff['SYMBOL'] == value]
        if result.empty != True:
            return result['FACE VALUE'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    elif irs == 'ISIN NUMBER':
        result = dff[dff['ISIN NUMBER'] == value]
        if result.empty != True:
            return result['FACE VALUE'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    else:
        return 'Error! Wrong ISIN, SYMBOL or irs value provided!'

def getPaidUpValue(irs, value):
    if irs == 'SYMBOL':
        result = dff[dff['SYMBOL'] == value]
        if result.empty != True:
            return result['PAID UP VALUE'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    elif irs == 'ISIN NUMBER':
        result = dff[dff['ISIN NUMBER'] == value]
        if result.empty != True:
            return result['PAID UP VALUE'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    else:
        return 'Error! Wrong ISIN, SYMBOL or irs value provided!'


def listedSince(irs, value):
    if irs == 'SYMBOL':
        result = dff[dff['SYMBOL'] == value]
        if result.empty != True:
            return result['DATE OF LISTING'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    elif irs == 'ISIN NUMBER':
        result = dff[dff['ISIN NUMBER'] == value]
        if result.empty != True:
            return result['DATE OF LISTING'].iloc[0]
        else:
            return 'Error! Wrong ISIN, SYMBOL or irs value provided!'
    else:
        return 'Error! Wrong ISIN, SYMBOL or irs value provided!'


def getISINNumbers(symbols):
    result_list = []
    for symbol in symbols:
        result = getISINNumber(symbol)
        if result[0:3] == 'INE':
            result_list.append(result)
    if len(symbols) > len(result_list):
        print('Error! Some input values are incorrect or not found!')
    return result_list


def getSymbols(isins):
    result_list = []
    for isin in isins:
        result = getSymbol(isin)
        if result[0:3] != 'Err':
            result_list.append(result)
    if len(isins) > len(result_list):
        print('Error! Some input values are incorrect or not found!')
    return result_list




import os
import csv
import dateparser
# MX US EU

NAME_OF_SELF = "format_csvs.exe"

ABREVIACION_REGION_MEXICO = 'MX'
ABREVIACION_REGION_EUA = 'US'
ABREVIACION_REGION_EUROPEA = 'EU'

IDENTIFICADOR_BELGICA = "BE"
IDENTIFICADOR_ESPANIA = "ES"
IDENTIFICADOR_FRANCIA = "FR"
IDENTIFICADOR_ITALIA = "IT"
IDENTIFICADOR_MEXICO = "MX"
IDENTIFICADO_BELGICA2 = "NL"
IDENTIFICADOR_ALEMANIA = "s."
IDENTIFICADOR_ESTADOS_UNIDOS = "US"

NOMBRE_IDENTIFICADOR = "identificador"
NOMBRE_FECHA = "fecha"
NOMBRE_TIPO_MOVIMIENTO = "tipo_movimiento"
NOMBRE_SKU = "sku"
NOMBRE_ORDER_STATE = "order_state"
NOMBRE_CANTIDAD = "cantidad"
NOMBRE_VENTA_ANTES_IMP = "venta_antes_impuestos"
NOMBRE_VENTA_DESP_IMP = "venta_despues_impuestos"
NOMBRE_REGION = "region"

identificador = 1

HEADERS_INDEX = 7

INDEX_FECHA = 0
INDEX_TIPO_MOVIMIENTO = 2
INDEX_SKU = 4
INDEX_CANTIDAD = 6
INDEX_ORDER_STATE = 10

INDEX_SALE_BEFORE_TAX_BE_BE2 = 12
INDEX_SALE_AFTER_TAX_BE_BE2 = 22

INDEX_SALE_BEFORE_TAX_FR_ES_IT_MEX_AL_USA = 13
INDEX_SALE_AFTER_TAX_FR_ES_IT_AL = 26

INDEX_SALE_AFTER_TAX_MEX_USA = 28

def formatDate(dateData):
    date = dateparser.parse(dateData)
    year = str(date.year)
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
    else:
        day = str(date.day)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)
    formattedDate = month + '/' + day + '/' + year
    return formattedDate

def formatSaleEurope(saleData):
    formattedSaleData = ''
    for letter in saleData:
        if letter == ',':
            formattedSaleData += '.'
        else:
            formattedSaleData += letter
    return float(formattedSaleData)

def formatSaleMexico(saleData):
    formattedSaleData = ''
    for letter in saleData:
        if letter != ',':
            formattedSaleData += letter
    return float(formattedSaleData)

def formatColumns(fileName):
    global identificador
    finalRows = []
    with open(fileName, newline='', encoding='utf-8') as openFile:
        csvFile = csv.reader(openFile) # Here your csv file
        fileContents = list(csvFile)
        for rowIndex in range(len(fileContents)):
            row = []
            if rowIndex >= HEADERS_INDEX:
                if rowIndex == HEADERS_INDEX:
                    row.append(NOMBRE_IDENTIFICADOR)
                    row.append(NOMBRE_FECHA)
                    row.append(NOMBRE_TIPO_MOVIMIENTO)
                    row.append(NOMBRE_SKU)
                    row.append(NOMBRE_ORDER_STATE)
                    row.append(NOMBRE_CANTIDAD)
                    row.append(NOMBRE_VENTA_ANTES_IMP)
                    row.append(NOMBRE_VENTA_DESP_IMP)
                    row.append(NOMBRE_REGION)
                    finalRows.append(row)
                else:
                    region = ''
                    saleBeforeTax = 0.0
                    saleAfterTax = 0.0
                    suffixFile = fileName[-6] + fileName[-5]
                    if suffixFile == IDENTIFICADOR_BELGICA or suffixFile == IDENTIFICADO_BELGICA2 or suffixFile == IDENTIFICADOR_ALEMANIA or suffixFile == IDENTIFICADOR_ESPANIA or suffixFile == IDENTIFICADOR_FRANCIA or suffixFile == IDENTIFICADOR_ITALIA:
                        region = ABREVIACION_REGION_EUROPEA
                        if suffixFile == IDENTIFICADO_BELGICA2 or suffixFile == IDENTIFICADOR_BELGICA:
                            saleBeforeTax = formatSaleEurope(fileContents[rowIndex][INDEX_SALE_BEFORE_TAX_BE_BE2])
                            saleAfterTax = formatSaleEurope(fileContents[rowIndex][INDEX_SALE_AFTER_TAX_BE_BE2])
                        else:
                            saleBeforeTax = formatSaleEurope(fileContents[rowIndex][INDEX_SALE_BEFORE_TAX_FR_ES_IT_MEX_AL_USA])
                            saleAfterTax = formatSaleEurope(fileContents[rowIndex][INDEX_SALE_AFTER_TAX_FR_ES_IT_AL])
                    elif suffixFile == IDENTIFICADOR_MEXICO:
                        region = ABREVIACION_REGION_MEXICO
                        saleBeforeTax = formatSaleMexico(fileContents[rowIndex][INDEX_SALE_BEFORE_TAX_FR_ES_IT_MEX_AL_USA])
                        saleAfterTax = formatSaleMexico(fileContents[rowIndex][INDEX_SALE_AFTER_TAX_MEX_USA])

                    elif suffixFile == IDENTIFICADOR_ESTADOS_UNIDOS:
                        region = ABREVIACION_REGION_EUA
                        saleBeforeTax = fileContents[rowIndex][INDEX_SALE_BEFORE_TAX_FR_ES_IT_MEX_AL_USA]
                        saleAfterTax = fileContents[rowIndex][INDEX_SALE_AFTER_TAX_MEX_USA]

                    fecha = formatDate(fileContents[rowIndex][INDEX_FECHA])
                    row.append(identificador)
                    row.append(fecha)
                    row.append(fileContents[rowIndex][INDEX_TIPO_MOVIMIENTO])
                    row.append(fileContents[rowIndex][INDEX_SKU])
                    row.append(fileContents[rowIndex][INDEX_ORDER_STATE])
                    row.append(fileContents[rowIndex][INDEX_CANTIDAD])
                    row.append(saleBeforeTax)
                    row.append(saleAfterTax)
                    row.append(region)
                    identificador += 1
                    finalRows.append(row)
    with open(fileName, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(finalRows)


files = filter(os.path.isfile, os.listdir(os.curdir)) 
for fileName in files:
    if (fileName != NAME_OF_SELF):
        formatColumns(fileName)
        print(fileName + ': ' + 'done')
input('Press enter to exit')
from genProcess import *
import json
# jsonData = {'columndataTypes': '{"dwh_sales_sum_cust_code":"string","dwh_sales_sum_site_code":"string","dwh_sales_sum_item_code":"string","gross_sales_value":"number"}', 'oldColumnHeading': 'dwh_sales_sum_cust_code,dwh_sales_sum_site_code,dwh_sales_sum_item_code,gross_sales_value', 'dbDetails': {'DATABASETYPE': '1', 'URL': 'baseinfra.ctfyiiy5aacp.ap-southeast-1.rds.amazonaws.com/orcl', 'KEY': 'KaTaMxqkJ', 'NAME': 'appvisdev'}, 'advancedFormatting': '', 'columnHeading': 'Dwh Sales Sum Cust Code,Dwh Sales Sum Site Code,Dwh Sales Sum Item Code,Gross Sales Values', 'source_sql': ' SELECT DWH_SALES_SUM.CUST_CODE AS DWH_SALES_SUM_CUST_CODE, DWH_SALES_SUM.SITE_CODE AS DWH_SALES_SUM_SITE_CODE, DWH_SALES_SUM.ITEM_CODE AS DWH_SALES_SUM_ITEM_CODE, SUM(GROSS_SALES_VALUE) AS GROSS_SALES_VALUE FROM DWH_SALES_SUM GROUP BY DWH_SALES_SUM.CUST_CODE, DWH_SALES_SUM.SITE_CODE, DWH_SALES_SUM.ITEM_CODE', 'visualJson': '{"groups":["Dwh Sales Sum Cust Code"],"rows":["Dwh Sales Sum Site Code"],"columns":["Dwh Sales Sum Item Code"],"values":["Gross Sales Values"]}', 'OutputType': 'HTML'}

def getqueryData(jsonData):
    print("inside getQueryCall queryData()\n",jsonData)
    ic = IncentiveCalculation()
    
    returnStr = ic.getQueryData(jsonData, "true")
    # print("returnStr", returnStr)
    return returnStr
    
# queryData(jsonData)



import pandas as pd 
import cx_Oracle as db
import os
import json
from flask import request, make_response, Flask 
import urllib.parse
import datetime
from pandarallel import pandarallel
import numpy as np
from functools import partial
import traceback
# from proteus_services.resources import logger
import logger
import pyodbc as pyod 
#import mysql.connector as my_sql

class IncentiveCalculation:

    os.environ["LD_LIBRARY_PATH"] = "/lib/oracle/19.9/client64/lib/"
    os.environ["ORACLE_HOME"] = "/lib/oracle/19.9/client64/lib/"
    
    #For sun release uncomment below 2 lines and comment above 2 lines 
    #os.environ["LD_LIBRARY_PATH"] = "/data/usr/lib/oracle/19.9/client64/lib/"
    #os.environ["ORACLE_HOME"] = "/data/usr/lib/oracle/19.9/client64/lib/"
    
    pandarallel.initialize()
    
    df = None
    detSql = None
    sqlQuery = None
    lookupTableMap = {}
    queryStringMap = {}
    currentDetData = None
    CPU_COUNT = os.cpu_count()
    errorId = ""
    dbDetails = None
    calculationData=""
    val="" 
    group_style =""
    outputType="JSON"
    group=""
    colum=""
    pool = None
    isPool  = 'false'
    minPool = 2
    maxPool = 100
    timeout = 180
    
    def getConnection(self):
       
        if 'isPool' in self.dbDetails.keys():
            if self.dbDetails.get('IS_POOL') != None:
                self.isPool = self.dbDetails['IS_POOL']

        if 'minPool' in self.dbDetails.keys():
            if self.dbDetails.get('MIN_POOL') != None:
                self.minPool = int(self.dbDetails['MIN_POOL'])

        if 'maxPool' in self.dbDetails.keys():
            if self.dbDetails.get('MAX_POOL') != None:
                self.maxPool = int(self.dbDetails['MAX_POOL'])

        if 'timeout' in self.dbDetails.keys():
            if self.dbDetails.get('TIMEOUT') != None:
                self.timeout = int(self.dbDetails['TIMEOUT'])
                   
       #Change by shrutika on 06-07-21 [Start] for From schema get database detail and according to database detail connect databse.
        if self.dbDetails != None:
            if self.dbDetails['DATABASETYPE'] == '1':
                userName = self.dbDetails['NAME']
                password = self.dbDetails['KEY']
                url = self.dbDetails['URL']
                
                if self.isPool == 'true' :
                    pool = db.SessionPool(user = userName, password = password, dsn = url, min=self.minPool, max=self.maxPool, increment=1, encoding="UTF-8")
                else:
                    try:
                        pool = db.connect(user = userName, password = password, dsn = url)
                        pool.call_timeout= self.timeout * 1000 
                    except Exception as e :
                        print('Exception in db.connect', e)

            elif self.dbDetails['DATABASETYPE'] == '2':
                uid = self.dbDetails['NAME']
                pwd = self.dbDetails['KEY']
                host = self.dbDetails['URL']
                driver = "/opt/dremio-odbc/lib64/libdrillodbc_sb64.so"
                port = 31010
                pool = pyod.connect("Driver={};ConnectionType=Direct;HOST={};PORT={};AuthenticationType=Plain;UID={};PWD={}".format(driver,host,port,uid,pwd),autocommit=True)
            #Change by SwapnilB on 20-01-22 [Start] for From schema connect to SQL database
            elif self.dbDetails['DATABASETYPE'] == '3':
                uid = self.dbDetails['NAME']
                pwd = self.dbDetails['KEY']
                host = self.dbDetails['URL']
                database = self.dbDetails['DATABASE']
                port = 3306
                pool = my_sql.connect(host=host, database=database, port=port, user=uid, password=pwd)
                #Change by SwapnilB on 20-01-22 [End] for From schema connect to SQL database
        return pool
        #Change by shrutika on 06-07-21 [End] for From schema get database detail and according to database detail connect databse.

    def getQueryData(self,jsonData=None,isWebsocet=None):
        try:
            con = None
            logger.log(f'\n Print time on start : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            #domData = request.args.get('jsonData')
            # Added by Aditi on 17-01-22 for Convert Python Request Get to Post
            #domData = request.form['jsonData']
            if isWebsocet == "true" :
                print("jsonData in getQueryData:", jsonData, type(jsonData))
                domData = jsonData
            else:
                domData = request.get_data('jsonData', None)
                domData = domData[9:]

            self.calculationData = json.loads(domData)
            logger.log(f'\n Inside getQueryData jsonData : {self.calculationData}', "0")

            sql = self.calculationData['source_sql']
            
            self.dbDetails = self.calculationData['dbDetails']
            pool = self.getConnection()
            #Change by shrutika on 06-07-21 [Start] for From schema get database detail and according to database detail connect databse.
            #con = pool.acquire()
            if self.dbDetails != None:
                if self.dbDetails['DATABASETYPE'] == '1':
                    if self.isPool == 'true':
                        con = pool.acquire()
                    else:
                        con = pool
                elif self.dbDetails['DATABASETYPE'] == '2' or self.dbDetails['DATABASETYPE'] == '3':
                    con = pool
            #Change by shrutika on 06-07-21 [End] for From schema get database detail and according to database detail connect databse.

            logger.log(f'\n Print time for before executing source_sql : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            
            if 'update ' in sql or 'delete ' in sql:
                return self.getErrorXml("Invalid SQL" , "Update and Delete operations are not allowed in Visual.")
            else:        
                self.df = pd.read_sql(
                    sql, con
                )

            self.df.columns = self.df.columns.str.strip().str.lower()
            if con:
            #Change by shrutika on 06-07-21 [Start] for From schema get database detail and according to database detail connect databse.
                if self.dbDetails != None:
                    if self.dbDetails['DATABASETYPE'] == '1':
                        if self.isPool == 'true' :
                            pool.release(con)
                        
            #Change by shrutika on 06-07-21 [End] for From schema get database detail and according to database detail connect databse.
            logger.log(f'\n Print time for after executing source_sql : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

            udf_divide = partial(self.udf_divide)
            udf_round = partial(self.udf_round)
            
            #logger.log(f'\n Print sourcesql result ::: \n {self.df}', "0")

            if not self.df.empty:

                for key in self.calculationData:

                    if key == 'column':
                        detailArr = self.calculationData[key]
                        
                        for detail in detailArr:
                            self.currentDetData = detail

                            if "line_no" in detail:
                                self.errorId = 'errDetailRow_' + str(detail['line_no'])
                            
                            if detail['calc_type'] == 'S':
                                logger.log(f'\n Inside getQueryData calc_expression for type SQL : {detail["calc_expression"]}', "0")
                                self.detSql = detail['calc_expression']
                                logger.log(f'\n Print time for type SQL before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                
                                if detail['calc_expression'] != None:
                                    self.df[detail['col_name'].lower().strip()] = self.df.apply(lambda row : self.getSqlResult(row, pool, detail), axis=1)
                                else:
                                    self.df[detail['col_name'].lower().strip()] = self.df.parallel_apply(lambda x : None, axis=1)

                                logger.log(f'\n Print time for type SQL after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                            elif detail['calc_type'] == 'E':
                                logger.log(f'\n Inside getQueryData calc_expression for type EXPRESSION : {detail["calc_expression"]}', "0")
                                expr = detail['col_name'].lower().strip() + '=' + detail['calc_expression'].lower().strip()
                                logger.log(f'\n Print time for type EXPRESSION before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                
                                if detail['calc_expression'] != None:
                                    self.df = self.df.eval(expr)
                                else:
                                    self.df = self.df.eval(detail['col_name'].lower().strip() + '=' + None)

                                logger.log(f'\n Print time for type EXPRESSION after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                            elif detail['calc_type'] == 'L':
                                logger.log(f'\n Inside getQueryData calc_expression for type LOOKUP : {detail["calc_expression"]}', "0")
                                self.detSql = detail['calc_expression']
                                
                                logger.log(f'\n Print time for type LOOKUP before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                
                                if detail['calc_expression'] != None:
                                    self.df[detail['col_name'].lower().strip()] = self.df.apply(lambda row : self.getLookUpValue(row, pool), axis=1)
                                else:
                                    self.df[detail['col_name'].lower().strip()] = self.df.apply(lambda row : self.getLookUpValue(row, pool), axis=1)

                                logger.log(f'\n Print time for type LOOKUP after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")

                            elif detail['calc_type'] == 'C':
                                logger.log(f'\n Inside getQueryData calc_expression for type CONDITIONAL EXPRESSION : {detail["calc_expression"]}', "0")
                                logger.log(f'\n Print time for type CONDITIONAL EXPRESSION before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                
                                if detail['calc_expression'] != None:
                                    exprArr = detail['calc_expression'].lower().split(':')
                                    condition = exprArr[0]
                                    trueExpr = None
                                    falseExpr = None
                                    if exprArr[1] != None:
                                        trueExpr = exprArr[1]
                                    if exprArr[2] != None:
                                        falseExpr = exprArr[2]
                                    self.df[detail['col_name'].lower().strip()] = self.udf_if(self.df, condition, trueExpr, falseExpr)
                                else:
                                    self.df = self.df.eval(detail['col_name'].lower().strip() + ' = ' + None)

                                logger.log(f'\n Print time for type CONDITIONAL EXPRESSION after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                
                            elif detail['calc_type'] == 'U':
                                logger.log(f'\n Inside getQueryData calc_expression for type Cumulative Sum : {detail["calc_expression"]}', "0")
                                logger.log(f'\n Print time for type Cumulative Sum before performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                                
                                if detail['calc_expression'] != None:
                                    columnArrList = detail['calc_expression'].lower().split(',')
                                    cumsumColumn = columnArrList[0]
                                    if len(columnArrList) == 1:
                                        self.df[detail['col_name'].lower().strip()] = self.df[cumsumColumn].cumsum()
                                    else:
                                        del columnArrList[0]
                                        self.df[detail['col_name'].lower().strip()] = self.df.groupby(columnArrList)[cumsumColumn].cumsum()
                                else:
                                    self.df[detail['col_name'].lower().strip()] = self.df.parallel_apply(lambda x : None, axis=1)

                                logger.log(f'\n Print time for type Cumulative Sum after performing applyFunction : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")                                
                                
            else:
                returnErr = self.getErrorXml("No records found against the source sql", "")
                logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                return str(returnErr)
            
            #logger.log(f'\n End of query datatypes:::\n {self.df.dtypes}', "0")
            #Change by shrutika on 24-05-21 [Start] for display date format data in flex monster.
            self.df.columns = self.df.columns.str.strip().str.lower()
            
            if self.calculationData.get('sorting_col_name'):
                sortingColName = self.calculationData['sorting_col_name']
                if sortingColName != "":
                    sortingColName = sortingColName.lower().strip()
                    self.df.sort_values(by=[sortingColName], inplace=True, ascending=True)
            
            dbDataTypes = self.df.dtypes.to_json()
            #Added by shrutika on 05-06-21 [Satrt] for update case in process request.
            #self.df = self.df.to_json(orient='records')
            #logger.log(f'\n End of query data:::\n {self.df}', "0")
            
            if 'visualJson' in self.calculationData.keys():
                if self.calculationData.get('visualJson') != None:
                    visualJson = self.calculationData['visualJson']

            if 'OutputType' in self.calculationData.keys():
                if self.calculationData.get('OutputType') != None:
                    self.outputType = self.calculationData['OutputType']      
            
            if 'columnHeading' in self.calculationData.keys():
                if self.calculationData.get('columnHeading') != None:
                    columnHeading = self.calculationData['columnHeading']        
            
            if 'oldColumnHeading' in self.calculationData.keys():
                if self.calculationData.get('oldColumnHeading') != None:
                    oldColumnHeading = self.calculationData['oldColumnHeading']        

            if self.outputType == 'HTML':
                #logger.log(f'\n Print dataframe at end::: \n {self.df}', "0")
                visualJson1 = json.loads(visualJson)
                columnHeading = columnHeading.split(",")
                self.df.rename(columns=dict(zip(self.df.columns, columnHeading)), inplace=True)
                oldColumnHeading = oldColumnHeading.split(",")
            
                if 'groups' in visualJson1.keys():
                    if len(visualJson1.get('groups')) != 0:    
                        self.group = visualJson1['groups']

                if 'rows' in visualJson1.keys():
                    if len(visualJson1.get('rows')) != 0: 
                        row = visualJson1["rows"]
                
                if 'columns' in visualJson1.keys():
                    if len(visualJson1.get('columns')) != 0:
                        self.colum = visualJson1["columns"]
                
                if 'values' in visualJson1.keys():
                    if len(visualJson1.get('values')) != 0:
                        self.val = visualJson1["values"]
                        
                if len(self.group) != 0:
                    lst=[]
                    for label, df_obj in (self.df).groupby(self.group):
                        sum = df_obj[self.val].sum()
                        df_obj.loc['' + str(self.group[0])] = sum   
                        lst.append(df_obj)

                    final_df = pd.concat(lst)
                    final_df.loc[final_df[row[0]].isnull(), self.group[0]] = "Total "  
                    final_df.loc[''] = self.df[self.val].sum()
                    final_df.fillna('', inplace=True)
                    final_df.iloc[-1, final_df.columns.get_loc(self.group[0])] = 'Grand Total '
                    self.group_style = True
                    html_str = self.getTableHTML(final_df)
                    logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    return html_str
                    
                elif len(self.colum) == 0:
                    html_str = self.getTableHTML(self.df)
                    logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    return html_str
                    
                else:
                    final_pivot = pd.pivot_table(self.df, index=row, columns=self.colum, values=self.val)
                    html_str = self.getTableHTML(final_pivot)
                    logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                    return html_str
                    
            elif self.outputType == "JSON":                                                           
                self.df = self.df.to_json(orient='records', date_format='iso')
                #logger.log(f'\n Print dataframe at end::: \n {self.df}', "0")
                #Added by shrutika on 05-06-21 [End] for update case in process request.
                # print("dbDataTypes",dbDataTypes)
                data_set = {"dbDataTypesDetails": dbDataTypes, "allData":  self.df }
                logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                # print("data_set",data_set)
                #return self.df
                #return data_set 
                return json.dumps(data_set)
                #Change by shrutika on 24-05-21 [End] for display date format data in flex monster.
            
            elif self.outputType == "XML":               
                xml_Str = self.to_xml(self.df)
                xmlStr = '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n' + xml_Str + '\n</root>'
                logger.log(f'\n Print time on end : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
                return xmlStr

            else:
                pass
                
        except Exception as e:
            logger.log(f'\n In getQueryData exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = self.getErrorXml(descr, trace)
            logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
            return str(returnErr)
        finally:
            try:
                if self.pool:
                    if self.dbDetails != None:
                        if self.dbDetails['DATABASETYPE'] == '1':
                            if self.isPool == 'true' :
                                pool.close()
                            else:
                                con.close()
                        else:
                            con.close()
            except Exception as e: 
                logger.log(f'\n In getQueryData exception stacktrace : ', "1")
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = self.getErrorXml(descr, trace)
                logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                return str(returnErr)
    def getLookUpValue(self, row, pool):
        try:
            expr = self.detSql.split(',')
            lookUpTable = str(expr[0].strip())
            lookUpCol = expr[1].strip().lower()
            validateLookup = "false"
            isLookUpDateColValBlank = "false"
            lookupExpLen = len(expr)
            
            if lookupExpLen == 3:
                lookUpDateCol = expr[2].strip().lower()
                lookUpDateColVal = row[lookUpDateCol]
                validateLookup = "true"
                if str(lookUpDateColVal) == None or str(lookUpDateColVal) == '' or str(lookUpDateColVal) == 'NaT':
                    lookUpDateColVal = str('')
                    isLookUpDateColValBlank = "true"

            if lookUpTable != None and lookUpTable.startswith('\''):
                length = len(lookUpTable)
                lookUpTable = lookUpTable[1:length-1]
            else:
                lookUpTable = lookUpTable.lower()
                if  lookUpTable in row:
                    rowVal = row[lookUpTable]
                    lookUpTable = str(rowVal)
                else:
                    lookUpTable = ""
            
            rowVal = row[lookUpCol]

            isLookUpColValBlank = "false"
            if str(rowVal) == None or str(rowVal) == '' or str(rowVal) == 'NaT':
                rowVal = str('')
                isLookUpColValBlank = "true"

            if self.lookupTableMap == None or not ""+str(lookUpTable) in self.lookupTableMap:
                self.setLookUpData( lookUpTable, validateLookup, pool )

            if validateLookup == 'true':
                lookUpTable = lookUpTable + '_validate'

            dfLookUpDet = None
            resDataType = str('')
            isdfLookUpDet = "false"
            if self.lookupTableMap != None and ""+str(lookUpTable) in self.lookupTableMap:
                lookUpHeadDetMap = self.lookupTableMap[""+str(lookUpTable)]

                dfLookUpDet = lookUpHeadDetMap["lookUpDet"]

                resDataType = lookUpHeadDetMap["resDataType"]

                query = lookUpHeadDetMap["queryString"]
                if isLookUpDateColValBlank == "false" and isLookUpColValBlank == "false":
                    dfLookUpDet = dfLookUpDet.query( query )
                    isdfLookUpDet = "true"
                else:
                    isdfLookUpDet = "false"
            else:
                isdfLookUpDet = "false"

            if  isdfLookUpDet == "false" or dfLookUpDet.empty:
                if resDataType == 'N':
                    dfLookUpDet = 0
                    dfLookUpDet = pd.to_numeric(dfLookUpDet)
                elif resDataType == 'D':
                    dfLookUpDet = str('')
                    dfLookUpDet = pd.to_datetime(dfLookUpDet)
                elif resDataType == 'S':
                    dfLookUpDet = str('')
                else:
                    dfLookUpDet = str('')

            else:
                dfLookUpDet = dfLookUpDet.iloc[0:1,0:1]
                dfLookUpDet = dfLookUpDet.iat[0,0]

                if resDataType == 'N':
                    dfLookUpDet = pd.to_numeric(dfLookUpDet)
                elif resDataType == 'D':
                    dfLookUpDet = pd.to_datetime(dfLookUpDet)

            return dfLookUpDet
        except Exception as e:
            raise e

    def getSqlResult(self, row, pool, detail):
        try:
            #Change by shrutika on 06-07-21 [Start] for From schema get database detail and according to database detail connect databse.
            #con = pool.acquire()
            if self.dbDetails != None:
                if self.dbDetails['DATABASETYPE'] == '1':
                    if self.isPool == 'true':
                        con = pool.acquire()
                    else:
                        con = pool
                elif self.dbDetails['DATABASETYPE'] == '2' or self.dbDetails['DATABASETYPE'] == '3' :
                    con = pool
            #Change by shrutika on 06-07-21 [End] for From schema get database detail and according to database detail connect databse.

            colDbType = detail['col_datatype']
            self.sqlQuery = self.detSql
            splitColValue = None
            dfSqlResult = None
            newSql = None

            if self.sqlQuery.find("?") != -1:
                newSql = self.sqlQuery.split(':')
                self.sqlQuery = newSql[0]
                sqlInput = newSql[1].lower()
                columns = sqlInput.split(',')
                self.buildSqlQuery(self.sqlQuery, columns, row)

            if 'update ' in self.sqlQuery or 'delete ' in self.sqlQuery:
                return self.getErrorXml("Invalid SQL" , "Update and Delete operations are not allowed in Visual.")
            else:
                dfSqlResult = pd.read_sql(
                    self.sqlQuery, con
                )

            if not dfSqlResult.empty:
                dfSqlResult = dfSqlResult.iloc[0:1,0:1]
                dfSqlResult = dfSqlResult.iat[0,0]
            else:
                # Added by Mahesh Saggam on [02-JULY-21] to return values based on dbTypes Start
                if colDbType == 'N':
                    dfSqlResult = 0
                    dfSqlResult = pd.to_numeric(dfSqlResult)
                elif colDbType == 'D':
                    dfSqlResult = str('')
                    dfSqlResult = pd.to_datetime(dfSqlResult)
                else:
                    dfSqlResult = str('')
                # Added by Mahesh Saggam on [02-JULY-21] to return values based on dbTypes End
                    
            return dfSqlResult
        except Exception as e:
            raise e
        finally:
            try:
                if con:
                #Change by shrutika on 06-07-21 [Start] for From schema get database detail and according to database detail connect databse.
                    if self.dbDetails != None:
                        if self.dbDetails['DATABASETYPE'] == '1':
                            if self.isPool == 'true' :
                                pool.release(con)
                        
            except Exception as e :
                logger.log(f'\n In getQueryData exception stacktrace : ', "1")
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = self.getErrorXml(descr, trace)
                logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                return str(returnErr)

            #Change by shrutika on 06-07-21 [End] for From schema get database detail and according to database detail connect databse.

    def buildSqlQuery(self, sql, columns, row):
        ctr = 0
        if sql.find('?') != -1 and len(columns) > 0:
            indexPos = sql.find('?')
            rowVal = str(row[columns[ctr].strip()])

            if str(rowVal) == None or str(rowVal) == 'None': 
                rowVal = str('')

            if len(sql) - 1 != indexPos:
                sql = sql[:indexPos] + "'" + rowVal + "'" + sql[indexPos+1:]
            else:
                sql = sql[:-1] + "'" + rowVal + "'"

            columns.pop(ctr)
            self.sqlQuery = str(sql)
            if(sql.find('?') != -1):
                self.buildSqlQuery(sql, columns, row)

    def getErrorXml(self, descr, trace):

        if  self.currentDetData:
            colName = self.currentDetData['col_name']
            calcType = self.currentDetData['calc_type']
            
            errorXml = '''<Root>
                            <Header>
                                <editFlag>null</editFlag>
                            </Header>
                            <Errors>
                                <error column_name="'''+colName+'''" type="E" column_value="'''+calcType+'''">
                                    <message><![CDATA[Error occurred in calculation of '''+colName+''' column for column type '''+calcType+''']]></message>
                                    <description><![CDATA['''+descr+''']]></description>
                                    <trace><![CDATA['''+trace+''']]></trace>
                                    <type>E</type>
                                    <errorId>'''+self.errorId+'''</errorId>
                                </error>
                            </Errors>
                        </Root>'''

            return errorXml
        else:
            errorXml = '''<Root>
                            <Header>
                                <editFlag>null</editFlag>
                            </Header>
                            <Errors>
                                <error type="E">
                                    <message><![CDATA['''+descr+''']]></message>
                                    <trace><![CDATA['''+trace+''']]></trace>
                                    <type>E</type>
                                </error>
                            </Errors>
                        </Root>'''

            return errorXml

    def udf_divide(self, x, y):
        return x/y

    def udf_round(self, value, decimal):
        return round(value, decimal)

    def udf_if(self, df,condition,true_exp, false_exp):
        udf_divide = partial(self.udf_divide)
        udf_round = partial(self.udf_round)
        return np.where(df.eval(condition),df.eval(true_exp),df.eval(false_exp))

    def firstRowColVal(self, df):
        df = df.iloc[0:1,0:1]
        df = df.iat[0,0]
        return df
        
    def setLookUpData(self,lookUpTable,validateLookup, pool):
        try:
            #Change by shrutika on 06-07-21 [Start] for From schema get database detail and according to database detail connect databse.
            #con = pool.acquire()
            if self.dbDetails != None:
                if self.dbDetails['DATABASETYPE'] == '1':
                    if self.isPool == 'true':
                        con = pool.acquire()
                    else:
                        con = pool
                elif self.dbDetails['DATABASETYPE'] == '2' or self.dbDetails['DATABASETYPE'] == '3' :
                    con = pool
            #Change by shrutika on 06-07-21 [End] for From schema get database detail and according to database detail connect databse.

            dfLookUpHead = None
            dfLookUpDet = None
            queryString = ''

            lookUpSql = "SELECT LOOKUP_TYPE, KEY_DATA_TYPE, RESULT_DATA_TYPE FROM GENLOOKUP WHERE LOOKUP_TABLE = '" + lookUpTable + "'"
            dfLookUpHead = pd.read_sql ( lookUpSql, con )

            lookUpDetSql = "SELECT RESULT_VALUE, MIN_KEY_VALUE, MAX_KEY_VALUE, EFF_FROM, VALID_UPTO FROM GENLOOKUP_TABLE WHERE LOOKUP_TABLE = '" + lookUpTable + "'"    
            dfLookUpDet = pd.read_sql( lookUpDetSql, con )

            rowVal = ''
            rowVal = str(rowVal)

            lookUpDateColVal = ''
            lookUpDateColVal = str(lookUpDateColVal)

            if not dfLookUpHead.empty and not dfLookUpDet.empty:
                resDataType = dfLookUpHead['RESULT_DATA_TYPE'].iloc[0]
                lookUpType = dfLookUpHead['LOOKUP_TYPE'].iloc[0]
                keyDataType = dfLookUpHead['KEY_DATA_TYPE'].iloc[0]

                if lookUpType == 'F':
                    if keyDataType == 'N':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_numeric)
                        rowVal = pd.to_numeric(rowVal)

                    elif keyDataType == 'D':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_datetime)
                        rowVal = pd.to_datetime(rowVal)

                    queryString = '@rowVal == MIN_KEY_VALUE'
                elif lookUpType == 'S':
                    if keyDataType == 'N':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_numeric)
                        rowVal = pd.to_numeric(rowVal)

                    elif keyDataType == 'D':
                        dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]] = dfLookUpDet[["MIN_KEY_VALUE", "MAX_KEY_VALUE"]].apply(pd.to_datetime)
                        rowVal = pd.to_datetime(rowVal)

                if validateLookup == 'true':
                    dfLookUpDet[["EFF_FROM", "VALID_UPTO"]] = dfLookUpDet[["EFF_FROM", "VALID_UPTO"]].apply(pd.to_datetime)
                    lookUpDateColVal = pd.to_datetime(lookUpDateColVal)
                    if lookUpType == 'S':
                        queryString = '(@rowVal >= MIN_KEY_VALUE & @rowVal <= MAX_KEY_VALUE) & (@lookUpDateColVal >= EFF_FROM & @lookUpDateColVal <= VALID_UPTO)'
                    else:
                        queryString = '(@rowVal == MIN_KEY_VALUE) & (@lookUpDateColVal >= EFF_FROM & @lookUpDateColVal <= VALID_UPTO)'
                    lookUpTable = lookUpTable + '_validate'
                else:
                    if lookUpType == 'S':
                        queryString = '@rowVal >= MIN_KEY_VALUE & @rowVal <= MAX_KEY_VALUE'
                    else:
                        queryString = '@rowVal == MIN_KEY_VALUE'

                lookUpHeadDetMap = {}
                lookUpHeadDetMap["lookUpDet"] = dfLookUpDet
                lookUpHeadDetMap["resDataType"] = resDataType
                lookUpHeadDetMap["queryString"] = queryString
                self.lookupTableMap[lookUpTable] = lookUpHeadDetMap
        except Exception as e:
            raise e
        finally:
            if con:
            #Change by shrutika on 06-07-21 [Start] for From schema get database detail and according to database detail connect databse.
                try:
                    if self.dbDetails != None:
                        if self.dbDetails['DATABASETYPE'] == '1':
                            if self.isPool == 'true' :
                                pool.release(con)
                        
                except Exception as e :
                    logger.log(f'\n In getQueryData exception stacktrace : ', "1")
                    trace = traceback.format_exc()
                    descr = str(e)
                    returnErr = self.getErrorXml(descr, trace)
                    logger.log(f'\n Print exception returnSring inside getQueryData : {returnErr}', "0")
                    return str(returnErr)
            #Change by shrutika on 06-07-21 [End] for From schema get database detail and according to database detail connect databse.

    def is_json(self,a):                                               
        try:
            json.loads(a)
        except Exception as e:
            return False
        return True

    def to_xml(self, dt_frame):
        def row_xml(row):
            xml = ['<Detail>']
            for i, col_name in enumerate(row.index):
                xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
            xml.append('</Detail>')
            return '\n'.join(xml)
        res = '\n'.join(dt_frame.apply(row_xml, axis=1))
        return(res)

    def format_num(self, str):
        return "text-align:right !important"

    def getTableHTML(self,pivot):
        if self.group_style :
            pivot_style = (pivot).reset_index(drop=True).style.applymap(self.format_num, subset=self.val).format('{:.3f}', na_rep='', subset=self.val)
            
        else:
            pivot_style = (pivot).style.applymap(self.format_num, subset=self.val).format('{:.3f}', na_rep='', subset=self.val)
        
        pivot_style = (pivot_style).set_table_attributes('class= "insight_html_table"')
        html = pivot_style.render()
        # logger.log(f'\n html inside method pivotstyle  : {type(html), html}', "0")                      
        return html
            
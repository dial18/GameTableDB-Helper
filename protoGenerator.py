################################################################################
# contact : dial18@gmail.com
# YongPil Park
################################################################################

from xlrd import *
import os
from os import system
from ProtoUtil import *
import sys
import pkg_resources
import string
from google import *
from glob import *
#from precompile_pb2 import *

# this is for private usage - add indexMap
from afterProtoConvert import *

def getTypeName(name):
        return name.upper()

def getFieldName(name):
        return name.lower()

def getType(typenum):
        if( XL_CELL_TEXT == typenum):
            return 'TEXT'
        elif(XL_CELL_NUMBER == typenum):
            return 'NUMBER'
        elif(XL_CELL_DATE == typenum):
            return 'DATE'
        else:
            return 'Unknown'

def fieldSaveType(typevalue):
        if('int' == typevalue):
                return 'optional','int32',True
        elif('string' == typevalue):
                return 'optional','string',True
        elif('float' == typevalue):
                return 'optional','float',True
        elif('int[]' == typevalue):
                return 'repeated','int32',False
        elif('float[]' == typevalue):
                return 'repeated','float',False
        elif('string[]' == typevalue):
                return 'repeated','string',False
        else:
                if ( '[]' in typevalue):
                        return 'repeated',typevalue.replate('[]',''),False
                else:
                        return 'optional',typevalue,False
                        


###############################Write _DB data#####################################
class writeTable:
    tableName = None
    tableFieldName = None
    
    fieldNames = None
    fieldDatas = None
    fieldTypes = None
    tableLength = None

    xlsheet = None
    messageTable = None
    tableIndex = None

    def __init__(self,_xlsheet,_protocolMessageTable,_tableIndex):
        self.xlsheet = _xlsheet
        self.messageTable = _protocolMessageTable
        self.tableIndex = _tableIndex

        self.tableName = self.xlsheet.name
        self.tableFieldName = getFieldName(self.messageTable.getElemName())
        
        self.fieldNames = self.xlsheet.fieldNames
        self.fieldDatas = self.xlsheet.fieldDatas
        self.fieldTypes = self.xlsheet.fieldTypes
        self.tableLength = self.xlsheet.tableLength
    
    def convert(self,value,fieldType):
        if(fieldType =='string'):
            return '"'+value+'"'
        if(fieldType == 'int32'):
            if(type(value) == type('str')):
                    if(not len(value) == 0):
                            return str(int(string.atof(value)))
                    else:
                            return '0'
            else:
                    return str(int(value))
        else:
            return str(value)
            
    def writeFieldDataHelper(self,f,name,typeInfo,data):
        #single value
        if(typeInfo[2] == True):
            f.write('\t' + name + ' : ' + self.convert(data,typeInfo[1]) + '\n')
        #repeated value
        else:
            for a in str(data).split('/'):
                    f.write('\t' + name + ' : ' + self.convert(a,typeInfo[1]) + '\n')

    def writeFieldData(self,f):
        #write each field data to txt file
        seek = 0
        for j in range(self.tableLength):
            f.write(self.tableFieldName+'{\n')
            for i in range(len(self.fieldNames)):
                typeInfo = fieldSaveType(self.fieldTypes[i])
                self.writeFieldDataHelper(f,self.fieldNames[i],typeInfo,self.fieldDatas[seek])
                seek = seek + 1
            f.write('}\n')

    def writeToFile(self,f):
        f.write(getFieldName(self.messageTable.name) + '{\n')
        self.writeFieldData(f)
        f.write('}\n')

class writeDB:
        xlbook = None
        messageDB = None
        tableWriters = []
        
        def __init__(self,_xlbook,_messageDB):
                self.xlbook = _xlbook
                self.messageDB = _messageDB

                for i in range(len(self.xlbook.sheets)):
                        if not '!' in self.xlbook.sheets[i].name:
                                self.tableWriters.append(writeTable(self.xlbook.sheets[i],self.messageDB.messageTables[i],i + 1))

        def writeTableData(self,f):
                for tw in self.tableWriters:
                        tw.writeToFile(f)
                
        def writeToFile(self):
                f = open(self.xlbook.name+'_DB.txt','w')
                self.writeTableData(f)
############################################################################################## 

class protocolMessage:
    name = None
    fieldTypes = None
    fieldNames = None
    
    def __init__(self,_name,_fieldtypes,_fieldnames):
        self.name = _name.replace('!','')
        self.fieldTypes = _fieldtypes
        self.fieldNames = _fieldnames

    def writeFieldDef(self,f):
        for i in range(len(self.fieldTypes)):
            typeInfo = fieldSaveType(self.fieldTypes[i])
            f.write(typeInfo[0] + ' ' + typeInfo[1] + ' ' + self.fieldNames[i] + ' = ' + str(i+1) + ';\n')

    def writeToFile(self,f):
        f.write('message '+self.name+'\n{\n')
        self.writeFieldDef(f)
        f.write('}\n')

class protocolMessageTable:
    message = None
    xlsheet = None
    name = None

    def getElemName(self):
            return self.xlsheet.name + "Data"
            
    def __init__(self,_sheet):
        self.xlsheet = _sheet
        self.name = _sheet.name
        self.message = protocolMessage(self.getElemName(),self.xlsheet.fieldTypes,self.xlsheet.fieldNames)

    def writeMessageTable(self,f):
        f.write('message '+getTypeName(self.name)+'\n{\n')
        f.write('\trepeated '+self.message.name+' '+getFieldName(self.message.name)+' = 1;\n')
        f.write('}\n')

    def writeToFile(self,f):
        self.message.writeToFile(f)
        if(not '!' in self.name):
                self.writeMessageTable(f)

class protocolMessageDB:
     messageTables = []
     name = None
     
     def __init__(self,book):
             self.name = book.name
             for sh in book.sheets:
                     self.messageTables.append(protocolMessageTable(sh))

     def writeMessageDB(self,f):
             f.write('message ' + self.name + '\n{\n')
             counter = 1
             for tbl in self.messageTables:
                     if not '!' in tbl.name:
                             f.write('\toptional ' + getTypeName(tbl.name) + ' ' + getFieldName(tbl.name) + ' = ' + str(counter) + ';\n')
                             counter = counter + 1
             f.write('}\n')

     def writeToFile(self,book):
             f = open(self.name + '.proto','w')
#             f.write('import "Define.proto";')
             self.writeMessageDB(f)
             for tbl in self.messageTables:
                     tbl.writeToFile(f)
             
############################################################################################## 

class Xlsheet:
    sheet = None
    name = None
    fieldTypes = []
    fieldNames = []
    tableLength = None
    fieldDatas = []

    def __init__(self,sheet):
        self.sheet = sheet
        self.name = sheet.name
        self.parseSheet()

    def printSheet(self):
        for row_index in range(self.sheet.nrows):
            for col_index in range(self.sheet.ncols):
                print cellname(row_index,col_index),'-',
                print self.sheet.cell(row_index,col_index).value, getType(self.sheet.cell_type(row_index,col_index))

    def getFieldTypes(self):
        try:
                ret = []
                for col_index in range(self.sheet.ncols):
                        ret.append(self.sheet.cell(1,col_index).value.replace(' ',''))
                return ret
        except Exception as e:
                print("error occured : " + self.name + " : " + str(e))
                sys.exit(1)

    def getFieldNames(self):
        ret = []
        for col_index in range(self.sheet.ncols):
            ret.append(self.sheet.cell(0,col_index).value)
        return ret

    def getFieldDatas(self):
        if(self.sheet.nrows < 2):
                return []

        ret = []
        for row_index in range(2,self.sheet.nrows):
            for col_index in range(0,self.sheet.ncols):
                ret.append(self.sheet.cell(row_index,col_index).value)
        return ret;

    def parseSheet(self):
        self.tableLength = self.sheet.nrows - 2
        self.fieldTypes = self.getFieldTypes()
        self.fieldNames = self.getFieldNames()
        self.fieldDatas = self.getFieldDatas()

class XlBook:
    book = None
    sheets = []
    name = None

    def openbook(self,fname):
            a = fname.split('.')
            self.name = a[0] 
            print "BookName : " + self.name
            self.book = open_workbook(fname)
            for i in range(self.book.nsheets):
                    sh = self.book.sheet_by_index(i)
                    # pass sheet that include '@' in name or can assume empty
                    if('@' in sh.name or sh.ncols == 0 or sh.nrows == 0):
                            continue
                    else:
                            self.sheets.append(Xlsheet(sh))
            return self

    def printBook(self):
            for sh in sheets:
                    sh.printSheet()

if __name__ == "__main__" :
    if (len(sys.argv) < 4) :
        print 'please input xlsx file path, codeOutPath, dataOutPath'
        print 'ex) text.xlsx d:\\work\\project\\code\\db\\ d:\\work\\project\\bin\\table\\ '
        sys.exit(1)

    fname = sys.argv[1]
    code_output_path = sys.argv[2]
    data_output_path = sys.argv[3]
    
    transfer = XlBook()
    transfer.openbook(fname)

    protocolWriter = protocolMessageDB(transfer)
    protocolWriter.writeToFile(transfer)

    system('protoc --python_out=. ' + transfer.name+'.proto')
    system('protogen\protogen -i:' + transfer.name+'.proto' + ' -o:' + transfer.name+'.cs')

    addIndex = addIndexMap()
    addIndex.open(transfer.name+'.cs')
    addIndex.rewrite(transfer.name+'.cs')
    
    system('copy ' + transfer.name+'.cs' + ' ' + code_output_path)

    dbWriter = writeDB(transfer,protocolWriter)
    dbWriter.writeToFile()

    sys.path.append(os.getcwd())

    exec('from ' + transfer.name + '_pb2' + ' import *')
    exec('table = ' + transfer.name + '()')

    ReadFromText(dbWriter.xlbook.name + '_DB.txt',table)
    SaveToBin(data_output_path + transfer.name + '_DB.bytes',table)
    SaveToText(data_output_path + transfer.name + '_DB.txt',table)


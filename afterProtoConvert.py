################################################################################
# contact : dial18@gmail.com
# YongPil Park
################################################################################

import os
from os import system
from ProtoUtil import *
import sys
import string

def isDefaultType(typevalue):
    if('int' == typevalue):
        return True
    elif('string' == typevalue):
        return True
    elif('float' == typevalue):
        return True
    return False

class addIndexMap:
    lines = []
    def open(self,fname):
        f = open(fname,'r')
        self.lines = f.readlines()
        f.close()

    def process(self):
        newLines = []
        for c in range(0,len(self.lines)):
            line = self.lines[c]
            newLines.append(line)
            if 'private readonly global::System.Collections.Generic.List' in line:
                typeName = line.split('<')[1].split('>')[0]
                typeValue = line.split('=')[0].split('>')[1].replace(' ','')
                if not isDefaultType(typeName):
                    print 'add indexer : ' + typeName
                    print line
                    newLines = newLines + self.appendIndex(typeName,typeValue)
        return newLines

    def appendIndex(self,typeName,typeValue):
        res = []
        res.append('private System.Collections.Generic.Dictionary<int,' + typeName + '> _Map = new System.Collections.Generic.Dictionary<int,' + typeName + '>();\n')
        res.append('private bool mapInitialized = false;\n')
        res.append('private void buildMapInfo(){')
        res.append('    '+ typeName + ' [] arrayData = ' + typeValue +'.ToArray();\n')
        res.append('    for (int i = 0; i < ' + typeValue + '.Count; ++i){\n')
        res.append('         ' + typeName + ' msg = arrayData[i];\n')
        res.append('              _Map[msg.index] = msg;\n')
        res.append('    }\n')
        res.append('mapInitialized = true;\n')
        res.append('}\n')
        res.append('public ' + typeName + ' refByIndex(int index){\n')
        res.append('    if(!mapInitialized) buildMapInfo();\n')
        res.append('    if(_Map.ContainsKey(index)){\n')
        res.append('        return _Map[index];\n')
        res.append('    }\n')
        res.append('    return null;\n')
        res.append('}\n')
        return res

    def rewrite(self,fname):
        f = open(fname,'w')
        newLines = self.process()

        for c in range(0,len(newLines)):
            f.write(newLines[c])

        f.close()

if __name__ == "__main__" :
    if (len(sys.argv) == 1) :
        print 'please input cs file path'
        sys.exit(1)
    
    addIndex= addIndexMap()
    addIndex.open(sys.argv[1])
    addIndex.rewrite(sys.argv[1])

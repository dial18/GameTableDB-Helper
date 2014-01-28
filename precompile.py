import os
import sys
from os import system
from glob import *

# MCS = "/Editor/Data/MonoBleedingEdge/lib/mono/2.0/gmcs"
MCS = '"C:\\Program Files (x86)\\Unity\\Editor\\Data\\MonoBleedingEdge\\lib\\mono\\2.0\\gmcs"'
PRECOMPILER = 'precompile\\precompile.exe'
UnityEnginePath = "C:\\Program Files (x86)\\Unity\\Editor\\Data\\Managed\\UnityEngine.dll"
ProtoBuf ="protobuf-net.dll -r:Google.ProtocolBuffers.dll -r:Google.ProtocolBuffers.Serialization.dll"

def precompile(srcDir,dstDir,dllName):
    srcfiles = glob(srcDir + "*.cs")
    
    filepaths = ''
    for i in range(0,len(srcfiles)):
        filepaths = filepaths + ' ' + srcfiles[i]

    print 'sources:'
    print filepaths

    system(MCS + ' -target:library -out:' + dllName + ' -r:' + ProtoBuf + ' -define:USE_SOURCEDATA ' + filepaths)           
    system(PRECOMPILER + ' '+ dllName + ' -t:DataBuilder -o:DataBuilder.dll')    
    
    system('copy ' + dllName + ' ' + dstDir + '\\' + dllName)
    system('copy ' + 'DataBuilder.dll' + ' ' + dstDir + '\\' + 'DatBuilder.dll')

if __name__ == "__main__" :
     if (len(sys.argv) < 3) :
        print 'please input dll output fpath'
        sys.exit(1)        

     precompile(sys.argv[1],sys.argv[2],sys.argv[3])

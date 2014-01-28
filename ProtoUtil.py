################################################################################
# contact : dial18@gmail.com
# YongPil Park
################################################################################

import sys
from google import protobuf

def SaveToText(fname,msg):
    f = open(fname,'w')
    strToSave = protobuf.text_format.MessageToString(msg)
    print(strToSave)
    f.write(strToSave)
    f.close()


def ReadFromText(fname,msg):
    f = open(fname,'r')
    str  = f.read()
    print(str)
    f.close()
    protobuf.text_format.Merge(str,msg)

def SaveToBin(fname,msg):
    f = open(fname,'wb')
    f.write(msg.SerializeToString())
    f.close()

def ReadFromBin(fname,msg):
    f = open(fname,'rb')
    msg.ParseFromString(f.read())
    f.close()


if __name__ == "__main__":
    from CharacterTransition_pb2 import *

    stt = CharacterTransitionTable()
    # st = stt.transitTable.add()

    # st.eventID = eStop

    # t = st.eventTransits.add()
    # t1 = st.eventTransits.add()
    
    # t.currentID = Idle
    # t.newStateID = Idle
    # tv = t.preventStateID.append(Die)
    # tv1 = t.preventStateID.append(Jump)
    
    # t1.newStateID = Move
    # t1.currentID = Move
    # tv2 = t1.preventStateID.append(Die)

    
    for i in range(eCharacterEventCount):
        st = stt.transitTable.add()
        st.eventID = i
        t = st.eventTransits.add()
        t.currentID = Idle
        t.newStateID = Idle
        t.preventStateID.append(Die)
        t.preventStateID.append(Jump)

    SaveToText("CharacterSTT.txt",stt)

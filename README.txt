GameTableDB Builder - By Excel
YongPil Park

dial18@gmail.com

=================================================================

Purpose:

Easy to make GameDB Table by Excel and Google Protocol buffer.

Dependency:
Python2.6 or Python2.7

GoogleProtocolBuffer Python.
ProtoBuf-net(for use in unity3d)

How To Use:

path:\protoGenerator.py dbfileName.xlsx CodePath DataPath

then u can get a C# SourceFile and Textand Binaray Data Files.

see the makeTest.bat

How To Use In Unity3D:

you have to build Your customname.dll and DataBuilder.dll.

see the precompileTest.bat and precompile.py

about precopile see this page 
http://marcgravell.blogspot.kr/2012/07/introducing-protobuf-net-precompiler.html

After then u can use Your Table DB In Unity 3D 

Ex)

TextAsset bindata = Resources.Load("testDB") as TextAsset;
ms = new System.IO.MemoryStream(bindata.bytes);
testDB = ProtoBuf.Serializer.Deserialize<testDB>(ms);
ms.Close();

=================================================================
YongPil Park

dial18@gmail.com

@echo off
d:
cd \python\protoc-3.3.0-win32\bin
protoc.exe -I=D:\git\BlockServer\protobuf --python_out=D:\git\BlockServer\protobuf D:\git\BlockServer\protobuf/*.proto
pause
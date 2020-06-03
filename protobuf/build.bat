@echo off
c:
cd /protobuf-3.5.1/src
protoc.exe -I=C:/svnspace/BlockGameServer/protobuf --python_out=C:/svnspace/BlockGameServer/protobuf C:/svnspace/BlockGameServer/protobuf/login.proto
pause
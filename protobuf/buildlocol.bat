@echo off
e:
cd /Tranning/ProtoBuf/protobuf-python-3.3.0/protobuf-3.3.0/src
protoc -I=F:/Solutions/RemoteSVN/JiuLing/protobuf --python_out=F:/Solutions/RemoteSVN/JiuLing/protobuf F:/Solutions/RemoteSVN/JiuLing/protobuf/*.proto
pause
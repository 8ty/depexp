#!/bin/bash

#删除非Actions需要的模块
BiliClient_needs=("wasm_enc" "__init__.py" "asyncBiliApi.py" "asyncXliveWs.py")
params=''
for i in ${BiliClient_needs[@]};do params="$params\|$i"; done
delete_arr=(`ls ./BiliClient|grep -v ${params: 2}`)
for i in ${delete_arr[@]};do rm -rf "./BiliClient/${i}"; done

#安装Actions需要的依赖库
sudo -H pip3 install --upgrade setuptools >/dev/null
sudo -H pip3 install -r ./run_in_Actions/requirements.txt >/dev/null

#启动BiliExp
python3 BiliExp.py
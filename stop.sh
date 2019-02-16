#!/bin/bash

port=$1
pid=`ps -ef | grep "gunicorn -b 0.0.0.0:"$port|grep -v grep |awk '{print $2}'`

declare -a shutdowns
declare -a pids

pythonpid=`ps -ef|grep python|grep -v grep|awk '{print $2" "$3}'`
i=1
j=1
f=0
k=0

for ppid in $pid
do
shutdowns[$j]=$ppid
((j+=1))
done

for cpid in $pythonpid
do
    pids[$i]=$cpid
    ((f=i%2))
    if [[ $f > 0 ]];then
        ((i+=1))
    else
        for ppid in $pid
        do
            if [[ $cpid -eq $ppid ]]
            then
                ((k=i-1))
                shutdowns[$j]=${pids[${k}]}
                ((j+=1))
            fi
        done
        ((i+=1))
    fi
done

num=${#shutdowns[@]}
if [[ $num -eq 0 ]];then
    echo "no process found, exit"
    exit 0
fi

echo "Are you sure to kill the processes: ${shutdowns[@]}? (y/n) n"
read y

if [[ ! "x$y" == "xy" ]];then
    echo "no process was killed"
    exit 1
fi
kill -9 ${shutdowns[@]}
success=$?
if [[ $success -eq 0 ]];then
    echo "kill process successfully"
fi

exit $success
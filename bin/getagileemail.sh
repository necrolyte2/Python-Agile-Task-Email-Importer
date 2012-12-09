#!/bin/bash

user=$1
password=$2

if [ ! -f session ]
then
	echo "Creating session"
	curl -s -c session --data-urlencode user_session[login]=${user} --data-urlencode user_session[password]=${password} --data-urlencode commit=Login --data-urlencode user_session[remember_me]=0 https://agiletask.me/user_session > /dev/null
fi

email=`curl -s -b session https://agiletask.me/account/edit | egrep -o '\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b'`

echo $email

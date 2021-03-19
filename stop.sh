ps -ef | grep "/new_operation/bin/" | grep -v grep | awk '{print "kill -9 "$2}'|sh

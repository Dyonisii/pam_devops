## Project structure:
```
.
├── compose.yaml
├── app
    ├── Dockerfile
    ├── templates
    ├── requirements.txt
    └── app.py
```

## Deploy with docker-compose
```
$ docker compose up -d
[+] Building 5.6s (30/30) FINISHED
[+] Running 2/2
 ✔ Container myapp-web2-1  Started                                                                                                                       
 ✔ Container myapp-web-1   Started
```
## Listing containers must show two container running and the port mapping as below:

```
root@ubuntu:# docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                                       NAMES
9d706541ea7c   myapp-web    "python3 app.py"         35 minutes ago   Up 35 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   myapp-web-1
93ec9d0decbc   myapp-web2   "/bin/bash -c 'echo …"   3 hours ago      Up 45 minutes   0.0.0.0:2222->22/tcp, :::2222->22/tcp       myapp-web2-1
```

## After the application starts, navigate to http://localhost:5000 in your web browser or run:

```
root@ubuntu#  curl localhost:5000
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
......
```
  
Stop and remove the containers

```
$ docker compose down
```


## Task 2 - Log analysis and Answers
## Request counts
1) Show how to get the count of GetTemporaryAuthenticationTokenRequest from the log.
```
root@93ec9d0decbc:/opt/local/logs# cat server.log | grep -c GetTemporaryAuthenticationTokenRequest
14823
```
2) Show how to get count of LoginRequests per minute.
```
root@93ec9d0decbc:/opt/local/logs# grep "LoginRequest" server.log | awk '{print $2}' | cut -d '-' -f 2 | sort | uniq -c
      1 1145:32,762
      1 1145:32,805
      1 1145:32,846
      1 1145:32,889
      1 1145:32,932
      1 1145:32,975
      1 1145:33,019
      1 1145:33,061
```
3) Show how to list all requests (and their counts) that had JSON OUT: string in it.
```
root@93ec9d0decbc:/opt/local/logs# grep -o "GetTemporaryAuthenticationTokenRequest-31284\|LoginRequest-31280" server.log | sort | uniq -c | awk '{print "{\"request\": \""$2"\", \"count\": "$1"}"}'
{"request": "GetTemporaryAuthenticationTokenRequest-31284", "count": 14823}
{"request": "LoginRequest-31280", "count": 14822}
```
## Parse data
4) For request/response with id 149418, show how to get values for obj=, ipAddress=, customData=[KV(5, playerCode= and flow= in one line.
```
root@93ec9d0decbc:/opt/local/logs# echo "PT04LOGIN49756-playtech93004, 10.144.227.18, #webVent, 58619722, 250168855196269516:2" | awk -F ', ' '{print "obj="$1", ipAddress="$2", customData=[KV(5, playerCode="$3", flow="$5}'
obj=PT04LOGIN49756-playtech93004, ipAddress=10.144.227.18, customData=[KV(5, playerCode=#webVent, flow=250168855196269516:2
```
## Bonus
```
root@93ec9d0decbc:/opt/local/logs# awk -F 'duration=' '{ sum += $2 } END { print "", sum }' server.log
608740
```

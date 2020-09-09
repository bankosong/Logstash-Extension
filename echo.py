import json
import requests
import time

#Calculate Execution Time
start_time = time.time()
#set up ip
ip1 = "10.204.196.8"
ip2 = "10.204.197.7"

#set up URI
#local uri
#uri1 = "http://localhost:8090/API/nodestats.json"
#uri2 = "http://localhost:8090/API/nodestats2.json"
#uri3 = "http://localhost:8090/API/nodestats3.json"
#uri4 = "http://localhost:8090/API/nodestats4.json"
#REST API Logstash
uri1 = "http://10.204.196.8:9800/_node/stats/?pretty"
uri2 = "http://10.204.196.7:9800/_node/stats/?pretty"
uri3 = "http://10.204.196.8:9801/_node/stats/?pretty"
uri4 = "http://10.204.196.7:9801/_node/stats/?pretty"
########################################################
##############      Function here      #################

#function for load json
def loadjson(load):
    return json.loads(requests.get(load).text)

#function for set up the instances
def addInstance(setApi,*setInstance):
    for x in range(len(setInstance)):
        setApi = setApi[setInstance[x]]
    return setApi

#function for delete the instances
def delete(x,y):
    del x[y]
    return x

#function retrieve metric name and value
def extract(data):
    x = []
    y = []
    for i in data:
        x.append(i)
    for j in data.values():
        y.append(j)
    return x,y;

#convert megabytes to megamegabytes with 2 decimal places
def convertMB(x):
    x = x/1024/1024
    y = '{0:.2f}'.format(x)
    return y
########################################################
########################################################

########################################################
#################   Build data here  ###################

########################################################
#Build data 1
########################################################
p1 = loadjson(uri1)

#get status
status = addInstance(p1,"status")
if status == "yellow":
    stats = 1
elif status == "green":
    stats = 2
elif status == "red":
    stats = 0
print ("name=Custom Metrics|Logstash|"+ip1+"|Status|value, value="+str(stats))

#get total virtual memory in megabytes
promem = addInstance(p1,"process","mem","total_virtual_in_bytes")
promem = convertMB(promem)
print ("name=Custom Metrics|Logstash|"+ip1+"|process|mem|total_virtual_in_megamegabytes|value, value="+str(promem))

#get cpu percentage
procpu = addInstance(p1,"process","cpu","percent")
print ("name=Custom Metrics|Logstash|"+ip1+"|process|cpu|percent|value, value="+str(procpu))

#get cpu load average
proload = addInstance(p1,"process","cpu","load_average","1m")
print ("name=Custom Metrics|Logstash|"+ip1+"|process|cpu|load_average|value, value="+str(proload))

#get JVM count
jvm_count = addInstance(p1,"jvm","threads")
name,metric = extract(jvm_count)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip1+"|JVM|threads|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools young
jpools = addInstance(p1,"jvm","mem","pools","young")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip1+"|JVM|mem|pools|young|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools survivor
jpools = addInstance(p1,"jvm","mem","pools","survivor")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip1+"|JVM|mem|pools|survivor|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools old
jpools = addInstance(p1,"jvm","mem","pools","old")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip1+"|JVM|mem|pools|old|"+name[i]+"|value, value="+str(metric[i]))

#get JVM memory
jvm_mem = addInstance(p1,"jvm","mem")
jvm_mem = delete(jvm_mem,"pools")
name,metric = extract(jvm_mem)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip1+"|JVM|mem|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline
pipeline = addInstance(p1,"pipeline")
name,metric = extract(pipeline)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip1+"|Pipeline|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline main events
pipeline_event = addInstance(p1,"pipelines","main","events")
name,metric = extract(pipeline_event)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip1+"|Pipeline|main|events|"+name[i]+"|value, value="+str(metric[i]))

#get reloads
pipeline_reload = addInstance(p1,"reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip1+"|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline reloads
pipeline_reload = addInstance(p1,"pipelines","main","reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip1+"|Pipeline|main|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get events
events = addInstance(p1,"events")
name,metric = extract(events)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip1+"|Events|"+name[i]+"|value, value="+str(metric[i]))

########################################################
#Build data 2
########################################################
p2 = loadjson(uri2)

#get status
status = addInstance(p2,"status")
if status == "yellow":
    stats = 1
elif status == "green":
    stats = 2
elif status == "red":
    stats = 0
print ("name=Custom Metrics|Logstash|"+ip2+"|Status|value, value="+str(stats))

#get total virtual memory in megabytes
promem = addInstance(p2,"process","mem","total_virtual_in_bytes")
promem = convertMB(promem)
print ("name=Custom Metrics|Logstash|"+ip2+"|process|mem|total_virtual_in_megamegabytes|value, value="+str(promem))

#get cpu percentage
procpu = addInstance(p2,"process","cpu","percent")
print ("name=Custom Metrics|Logstash|"+ip2+"|process|cpu|percent|value, value="+str(procpu))

#get cpu load average
proload = addInstance(p2,"process","cpu","load_average","1m")
print ("name=Custom Metrics|Logstash|"+ip2+"|process|cpu|load_average|value, value="+str(proload))

#get JVM count
jvm_count = addInstance(p2,"jvm","threads")
name,metric = extract(jvm_count)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip2+"|JVM|threads|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools young
jpools = addInstance(p2,"jvm","mem","pools","young")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip2+"|JVM|mem|pools|young|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools survivor
jpools = addInstance(p2,"jvm","mem","pools","survivor")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip2+"|JVM|mem|pools|survivor|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools old
jpools = addInstance(p2,"jvm","mem","pools","old")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip2+"|JVM|mem|pools|old|"+name[i]+"|value, value="+str(metric[i]))

#get JVM memory
jvm_mem = addInstance(p2,"jvm","mem")
jvm_mem = delete(jvm_mem,"pools")
name,metric = extract(jvm_mem)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash|"+ip2+"|JVM|mem|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline
pipeline = addInstance(p2,"pipeline")
name,metric = extract(pipeline)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip2+"|Pipeline|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline main events
pipeline_event = addInstance(p2,"pipelines","main","events")
name,metric = extract(pipeline_event)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip2+"|Pipeline|main|events|"+name[i]+"|value, value="+str(metric[i]))

#get reloads
pipeline_reload = addInstance(p2,"reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip2+"|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline reloads
pipeline_reload = addInstance(p2,"pipelines","main","reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip2+"|Pipeline|main|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get events
events = addInstance(p2,"events")
name,metric = extract(events)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash|"+ip2+"|Events|"+name[i]+"|value, value="+str(metric[i]))

########################################################
#Build data 3
########################################################
p3 = loadjson(uri3)

#get status
status = addInstance(p3,"status")
if status == "yellow":
    stats = 1
elif status == "green":
    stats = 2
elif status == "red":
    stats = 0
print ("name=Custom Metrics|Logstash|"+ip1+"|Status|value, value="+str(stats))

#get total virtual memory in megabytes
promem = addInstance(p3,"process","mem","total_virtual_in_bytes")
promem = convertMB(promem)
print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|process|mem|total_virtual_in_megamegabytes|value, value="+str(promem))

#get cpu percentage
procpu = addInstance(p3,"process","cpu","percent")
print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|process|cpu|percent|value, value="+str(procpu))

#get cpu load average
proload = addInstance(p3,"process","cpu","load_average","1m")
print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|process|cpu|load_average|value, value="+str(proload))

#get JVM count
jvm_count = addInstance(p3,"jvm","threads")
name,metric = extract(jvm_count)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|JVM|threads|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools young
jpools = addInstance(p3,"jvm","mem","pools","young")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|JVM|mem|pools|young|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools survivor
jpools = addInstance(p3,"jvm","mem","pools","survivor")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|JVM|mem|pools|survivor|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools old
jpools = addInstance(p3,"jvm","mem","pools","old")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|JVM|mem|pools|old|"+name[i]+"|value, value="+str(metric[i]))

#get JVM memory
jvm_mem = addInstance(p3,"jvm","mem")
jvm_mem = delete(jvm_mem,"pools")
name,metric = extract(jvm_mem)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|JVM|mem|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline
pipeline = addInstance(p3,"pipeline")
name,metric = extract(pipeline)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|Pipeline|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline main events
pipeline_event = addInstance(p3,"pipelines","main","events")
name,metric = extract(pipeline_event)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|Pipeline|main|events|"+name[i]+"|value, value="+str(metric[i]))

#get reloads
pipeline_reload = addInstance(p3,"reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline reloads
pipeline_reload = addInstance(p3,"pipelines","main","reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|Pipeline|main|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get events
events = addInstance(p3,"events")
name,metric = extract(events)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip1+"|Events|"+name[i]+"|value, value="+str(metric[i]))

########################################################
#Build data 4
########################################################
p4 = loadjson(uri4)

#get status
status = addInstance(p4,"status")
if status == "yellow":
    stats = 1
elif status == "green":
    stats = 2
elif status == "red":
    stats = 0
print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|Status|value, value="+str(stats))

#get total virtual memory in megabytes
promem = addInstance(p4,"process","mem","total_virtual_in_bytes")
promem = convertMB(promem)
print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|process|mem|total_virtual_in_megamegabytes|value, value="+str(promem))

#get cpu percentage
procpu = addInstance(p4,"process","cpu","percent")
print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|process|cpu|percent|value, value="+str(procpu))

#get cpu load average
proload = addInstance(p4,"process","cpu","load_average","1m")
print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|process|cpu|load_average|value, value="+str(proload))

#get JVM count
jvm_count = addInstance(p4,"jvm","threads")
name,metric = extract(jvm_count)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|JVM|threads|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools young
jpools = addInstance(p4,"jvm","mem","pools","young")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|JVM|mem|pools|young|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools survivor
jpools = addInstance(p4,"jvm","mem","pools","survivor")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|JVM|mem|pools|survivor|"+name[i]+"|value, value="+str(metric[i]))

#get JVM pools old
jpools = addInstance(p4,"jvm","mem","pools","old")
name,metric = extract(jpools)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|JVM|mem|pools|old|"+name[i]+"|value, value="+str(metric[i]))

#get JVM memory
jvm_mem = addInstance(p4,"jvm","mem")
jvm_mem = delete(jvm_mem,"pools")
name,metric = extract(jvm_mem)
for i in range(len(name)):
    if "bytes" in name[i]:
        metric[i] = convertMB(metric[i])
        name[i] = name[i].replace("bytes","megabytes")
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|JVM|mem|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline
pipeline = addInstance(p4,"pipeline")
name,metric = extract(pipeline)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|Pipeline|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline main events
pipeline_event = addInstance(p4,"pipelines","main","events")
name,metric = extract(pipeline_event)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|Pipeline|main|events|"+name[i]+"|value, value="+str(metric[i]))

#get reloads
pipeline_reload = addInstance(p4,"reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get pipeline reloads
pipeline_reload = addInstance(p4,"pipelines","main","reloads")
name,metric = extract(pipeline_reload)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|Pipeline|main|Reloads|"+name[i]+"|value, value="+str(metric[i]))

#get events
events = addInstance(p4,"events")
name,metric = extract(events)
for i in range(len(name)):
    print ("name=Custom Metrics|Logstash filebeat|"+ip2+"|Events|"+name[i]+"|value, value="+str(metric[i]))
########################################################
########################################################
print("Execution Time : %s s" % (time.time() - start_time))

#!/usr/src/Python-2.7.13/env python
import requests
import requests.packages.urllib3
import json
import pandas as pd
from sqlalchemy import create_engine

requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import sys

import datetime
print (sys.version)

#engine = create_engine("mysql+pymysql://root:root@127.0.0.1/dashboard")


#create timeStamp 
timeStamp = '{:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now())



#api call HDS storage systems
r=requests.get("http://10.67.243.134:23450/ConfigurationManager/v1/objects/storages",auth=HTTPBasicAuth('restapi','rest123'),verify=False)
#print r.status_code
#print r.text
callback = r.text # returned content from api above# 
jsondata =  json.loads(callback) # callback data in json format#
storeList = jsondata.get('data' , 'not found') # gets value held at 'data' from api call#
id =[]
storagearrays = pd.DataFrame(storeList)
storagearrays["timeStamp"] = timeStamp
#storagearrays.to_sql('storageSystems', engine , if_exists='replace')
print(storagearrays)


        
for sid in range(len(storeList)): #sid=storageid#

        id.append(storeList[sid].get("storageDeviceId"))
        
            
listofpoolsReturn = []


# api call pools
for i in range(len(id)):

       r=requests.get("http://10.67.243.134:23450/ConfigurationManager/v1/objects/storages/" + id[i] + "/pools",auth=HTTPBasicAuth('restapi','rest123'),verify=False)
       content = json.loads(r.content)
       
       df = pd.DataFrame(content.get("data"))
       df["storageId"] = id[i]
       df["timeStamp"] = timeStamp
       listofpoolsReturn.append(df)
       
       
       
pooldf = pd.concat(listofpoolsReturn) #final dataframe
#pooldf.to_csv("pools.csv",sep=",") 
print(pooldf)      
ldev=""
listofldevdf = []
hostGroupName = ""
portId = ""
lun = ""
hostGroupNumber = ""

'''



for sid in range(len(id)):

            r=requests.get("https://10.240.0.122:23451/ConfigurationManager/v1/objects/storages/" + id[sid] + "/ldevs",auth=HTTPBasicAuth('maintenance','raid-maintenance'),verify=False)
            content = json.loads(r.content)
            ldev=(content.get("data"))
# api call ldevs
            for i in range(len(ldev)):
                status = ldev[i].get("status")
                blockCapacity = ldev[i].get("blockCapacity")
                isFullAllocationEnabled = ldev[i].get("isFullAllocationEnabled")
                ldevId = ldev[i].get("ldevId")
                ssid = ldev[i].get("ssid")
                resourceGroupId = ldev[i].get("resourceGroupId")
                dataReductionStatus = ldev[i].get("dataReductionStatus")
                poolId = ldev[i].get("poolId")
                clprId = ldev[i].get("clprId")
                label = ldev[i].get("label")
                numOfUsedBlock = ldev[i].get("numOfUsedBlock")
                dataReductionMode = ldev[i].get("dataReductionMode") 
                byteFormatCapacity = ldev[i].get("byteFormatCapacity")
                emulationType = ldev[i].get("emulationType")
                numOfPorts = ldev[i].get("numOfPorts")
                ports=ldev[i].get("ports", "no port")
                
                if ports != "no port":
                    
                
                    for j in range(len(ports)):
                        hostGroupName = ports[j].get("hostGroupName")
                        portId = ports[j].get("portId")
                        lun = ports[j].get("lun")
                        hostGroupNumber = ports[j].get("hostGroupNumber")
                    
                hostgroupDict = {"status":status,"blockCapacity":blockCapacity,"isFullAllocationEnabled":isFullAllocationEnabled,"ldevId":ldevId,"ssid":ssid,
                                 "resourceGroupId":resourceGroupId,"dataReductionStatus":dataReductionStatus,"poolId":poolId,"clprId":clprId,"label":label,"numOfUsedBlock":numOfUsedBlock,
                                 "dataReductionMode":dataReductionMode,"byteFormatCapacity":byteFormatCapacity,"emulationType":emulationType,"numOfPorts":numOfPorts,
                                 "hostGroupName":hostGroupName,"portId":portId,"lun":lun,"hostGroupNumber":hostGroupNumber}
                df = pd.DataFrame(hostgroupDict,index=[0])
                df["storageId"] = id[sid]
                df["timeStamp"] = timeStamp
                
                listofldevdf.append(df)

ldevdf = pd.concat(listofldevdf)
ldevdf.to_csv("ldev.csv",sep=",")
#print(ldevdf)


# api call PG
listofPGreturn = []
for i in range(len(id)):

       r=requests.get("https://10.240.0.122:23451/ConfigurationManager/v1/objects/storages/" + id[i] + "/parity-groups",auth=HTTPBasicAuth('maintenance','raid-maintenance'),verify=False)
       content = json.loads(r.content)
       
       df = pd.DataFrame(content.get("data"))
       df["storageId"] = id[i]
       df["timeStamp"] = timeStamp
       listofPGreturn.append(df)

paritygroupdf = pd.concat(listofPGreturn)
paritygroupdf.to_csv("paritygroups.csv",sep=",")
#print(paritygroupdf)
# api call host groups

listofhostgroupsreturned = []

for i in range(len(id)):

       r=requests.get("https://10.240.0.122:23451/ConfigurationManager/v1/objects/storages/" + id[i] + "/host-groups",auth=HTTPBasicAuth('maintenance','raid-maintenance'),verify=False)
       content = json.loads(r.content)
       
       df = pd.DataFrame(content.get("data"))
       df["storageId"] = id[i]
       df["timeStamp"] = timeStamp
       listofhostgroupsreturned.append(df)
      
       
       
hostgroupdf = pd.concat(listofhostgroupsreturned)
hostgroupdf.to_csv("hostgroups.csv",sep=",")
#print(hostgroupdf) 


listofPortsreturned = []

arrayPortFE  = {}

listOfPortIds = []
for i in range(len(id)):

       r=requests.get("https://10.240.0.122:23451/ConfigurationManager/v1/objects/storages/" + id[i] + "/ports",auth=HTTPBasicAuth('maintenance','raid-maintenance'),verify=False)
       content = json.loads(r.content)
       
       df = pd.DataFrame(content.get("data"))
       df["storageId"] = id[i]
       df["timeStamp"] = timeStamp
       listofPortsreturned.append(df)
       l = df['portID'].tolist()
       arrayPortFE.update({id[i] : l})
       l = []
Portpdf = pd.concat(listofPortsreturned)
'''
#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import sys
import csv
import time
import getpass
import ipaddress
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
gregory.dunlap / celtic_cow

go through the cma and check on fw logging
"""

"""
go through a cma and find gateways
"""
def get_gateways_per_cma(ip_addr, sid):
    print("in get_gateays_per_cma")

    gateways = {}

    gateways_result = apifunctions.api_call(ip_addr, "show-gateways-and-servers", {"details-level" : "full"}, sid)

    #print(json.dumps(gateways_result))

    for x in range(gateways_result['total']):

        gw = gateways_result['objects'][x]['name']

        print(gw)
        print(gateways_result['objects'][x]['type'])

        if(gateways_result['objects'][x]['type'] == "CpmiClusterMember"):

            #print(gateways_result['objects'][x]['ipv4-address'])

            ifaces = len(gateways_result['objects'][x]['interfaces'])

            #print(gateways_result['objects'][x]['interfaces'])
            for i in range(ifaces):
                #print(gateways_result['objects'][x]['interfaces'][i]['interface-name'])

                if(gateways_result['objects'][x]['interfaces'][i]['interface-name'] == "Mgmt"):
                    ip_info = gateways_result['objects'][x]['interfaces'][i]['ipv4-address']
                    #print(ip_info)
                    gateways[gw] = ip_info
        
        print("---------------------------------------------------------------------")
    return(gateways)
    #end_of for  x in range   ipv4-address

def script_to_run():
    pass

def get_results():
    pass

"""
main
"""
def main():
    print("start main")

    debug = 1

    ip_addr = "146.18.96.16" #input("enter IP of MDS : ")
    ip_cma  = "146.18.96.25" #input("enter IP of CMA : ")
    user    = "gdunlap" #input("enter P1 user id : ")
    password = "1qazxsw2" #getpass.getpass('Enter P1 Password : ')

    sid = apifunctions.login(user, password, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)
    
    gateway_info = {}

    gateway_info = get_gateways_per_cma(ip_addr, sid)

    print("***********************************************")
    print(gateway_info)
    print("***********************************************")

    #### Don't Need to publish 
    print("Starting Logout ZZZZZZZZ")
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)
#end of main


if __name__ == "__main__":
    main()

#end of program
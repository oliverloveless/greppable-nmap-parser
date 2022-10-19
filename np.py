#!/usr/bin/python
# python np.py blah.gnmap http
from sys import argv

filename = argv[1]
service = argv[2]

with open(filename, "r") as nmap_file:
    for line in nmap_file:
        if "Ports" not in line:
            continue
        elif service not in line:
            continue
        device_info, port_info = line.split("\t")
        split_line = device_info.split(" ")
        if split_line[2] != "()":
            ip = split_line[2][1:-1]
        else:
            ip = split_line[1]
        #done with split_line for device info now
        split_line = port_info.split(" ")[1:]
        for i in split_line:
            single_port_info = i.split("/") # number, status, protocol, blank, service name, rpc_info, version info
            if service in single_port_info[4].split("|"): # catches service labels like "ssl|https" without also including things like "http"
                print("{}:{}".format(ip, single_port_info[0])) # ip:port
        
        
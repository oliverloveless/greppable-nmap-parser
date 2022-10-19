#!/usr/bin/python3
# python np.py blah.gnmap http
# python np.py blah.gnmap smb > smb/targets.txt
# for i in http smb ssl dns; do mkdir $i; python np.py blah.gnmap $i > $i/targets.txt;done
# cat test.gnmap | np.py http | tee http/targets.txt
# do line 4 then:
# while read l; do sslscan $l | tee ssl/$l.sslscan;done<ssl/targets.txt # and whatever other tools you want to run.


from sys import argv, stdin

def parse_file(nmap_file, service):
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
            if service.lower() in single_port_info[4].split("|"): # catches service labels like "ssl|https" without also including things like "http"
                print("{}:{}".format(ip, single_port_info[0])) # ip:port
        
if not stdin.isatty():
    service = argv[1]
    parse_file(stdin, service)
else:
    filename = argv[1]
    service = argv[2]
    with open(filename, "r") as nmap_file:
        parse_file(nmap_file, service)

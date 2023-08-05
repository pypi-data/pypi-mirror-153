from modules.nmap import PortScanner
from modules.color import print_colored, colors, bcolors
from modules.outfile import output
from os import getuid

def is_root():
    if getuid() == 0:
        return True #return True if the user is root
    else:
        return False

# this function is for turning a list of hosts into a single string
def listToString(s): 
    str1 = " "
    return (str1.join(s))

#do a ping scan using nmap
def TestPing(target, evade):
    nm = PortScanner()
    if type(target) is list:
        target = listToString(target)
    if evade:
        resp = nm.scan(hosts=target, arguments="-sn -T 2 -f -g 53 --data-length 10")
    else:
        resp = nm.scan(hosts=target, arguments="-sn")
    return nm.all_hosts()

#do a arp scan using nmap
def TestArp(target, evade):
    nm = PortScanner()
    if type(target) is list:
        target = listToString(target)
    if evade:
        resp = nm.scan(hosts=target, arguments="-sn -PR -T 2 -f -g 53 --data-length 10")
    else:
        resp = nm.scan(hosts=target, arguments="-sn -PR")
    return nm.all_hosts()

def DiscoverHosts(target, scantype, scanspeed, evade):
    if scantype == "arp":
        if not is_root():
            print_colored("You must be root to do an arp scan!", colors.red)
            scantype = "ping"
    elif scantype == "ping":
        pass
    else:
        if is_root():
            print_colored("Unknown scan type: %s! Using arp scan instead..." % (scantype), colors.red)
            scantype = "arp"
        else:
            print_colored("Unknown scan type: %s! Using ping scan instead..." % (scantype), colors.red)
            scantype = "ping"

    print_colored("\n" + "-" * 60, colors.green)
    if type(target) is list:
        print_colored("\tScanning %d hosts using %s scan..." % (len(target), scantype), colors.green)
    else:
        print_colored("\tScanning %s using %s scan..." % (target, scantype), colors.green)
    print_colored("-" * 60 + "\n", colors.green)

    if type(target) is list:
        output.WriteToFile("\nScanning %d hosts using %s scan..." % (len(target), scantype))
    else:
        output.WriteToFile("\nScanning %s using %s scan..." % (target, scantype))
    
    if scantype == 'ping':
        OnlineHosts = TestPing(target, evade)
        return OnlineHosts

    elif scantype == 'arp':
        OnlineHosts = TestArp(target, evade)
        return OnlineHosts

#run a port scan on target using nmap
def PortScan(target, scanspeed, evade):
    print_colored("\n" + "-" * 60, colors.green)
    print_colored("\tRunning a portscan on host " + str(target) + "...", colors.green)
    print_colored("-" * 60 + "\n", colors.green)
    output.WriteToFile("\nPortscan on " + str(target) + " : ")
    nm = PortScanner()
    if is_root():
        if evade:
            resp = nm.scan(hosts=target, arguments="-sS -sV -O -Pn -T 2 -f -g 53 --data-length 10")
        else:
            resp = nm.scan(hosts=target, arguments="-sS -sV --host-timeout 60 -Pn -O -T %d" % (scanspeed))
    else:
        resp = nm.scan(hosts=target, arguments="-sV --host-timeout 60 -Pn -T %d" % (scanspeed))
    return nm

#analyse and print scan results
def AnalyseScanResults(nm,target):
    HostArray = []
    try:
        nm[target]

        try:
            mac = nm[target]['addresses']['mac']
        except:
            mac = 'Unknown'

        try:
            vendor = nm[target]['vendor'][mac]
        except:
            vendor = 'Unknown'

        try:
            os = nm[target]['osmatch'][0]['name']
        except:
            os = 'Unknown'

        try:
            accuracy = nm[target]['osmatch'][0]['accuracy']
        except:
            accuracy = 'Unknown'

        try:
            ostype = nm[target]['osmatch'][0]['osclass'][0]['type']
        except:
            ostype = 'Unknown'

        print_colored("MAC Address : %s\tVendor : %s" % (mac, vendor), colors.yellow)
        print_colored("OS : %s\tAccuracy : %s\tType : %s\n" % (os, accuracy,ostype), colors.yellow)

        output.WriteToFile("MAC Address : %s\tVendor : %s" % (mac, vendor))
        output.WriteToFile("OS : %s\tAccuracy : %s\tType : %s\n" % (os, accuracy,ostype))

        if nm[target]['status']['reason'] == 'localhost-response' or nm[target]['status']['reason'] == 'user-set':
            print_colored('Target ' + str(target) + ' seems to be us.', colors.underline)
            output.WriteToFile('Target ' + str(target) + ' seems to be us.')
        if len(nm[target].all_protocols()) == 0:
            print_colored("Target " + str(target) + " seems to have no open ports.", colors.red)
            output.WriteToFile("Target " + str(target) + " seems to have no open ports.")
        for proto in nm[target].all_protocols():
            for port in nm[target][proto].keys():
                                
                try:
                    if not len(nm[str(target)][proto][int(port)]['state']) == 0:
                        state = nm[str(target)][proto][int(port)]['state']
                    else:
                        state = 'Unknown'
                except:
                    state = 'Unknown'
                
                try:
                    if not len(nm[str(target)][proto][int(port)]['name']) == 0:
                        service = nm[str(target)][proto][int(port)]['name']
                    else:
                        service = 'Unknown'
                except:
                    service = 'Unknown'

                try:
                    if not len(nm[str(target)][proto][int(port)]['product']) == 0:
                        product = nm[str(target)][proto][int(port)]['product']
                    else:
                        product = 'Unknown'
                    
                except:
                    product = 'Unknown'

                try:
                    if not len(nm[str(target)][proto][int(port)]['version']) == 0:
                        version = nm[str(target)][proto][int(port)]['version']
                    else:
                        version = 'Unknown'
                except:
                    version = 'Unknown'

                print(
                    (
                        bcolors.cyan + "Port : " + bcolors.endc + "{0:10}" + 
                        bcolors.cyan + "State : " + bcolors.endc + "{1:10}" +
                        bcolors.cyan + "Service : " + bcolors.endc + "{2:15}" +
                        bcolors.cyan + "Product : " + bcolors.endc + "{3:20}" +
                        bcolors.cyan + "Version : " + bcolors.endc + "{4:15}"
                    ).format(str(port), state, service, product, version)
                )

                output.WriteToFile(
                    (
                        "Port : " + "{0:10}" + 
                        "State : " + "{1:10}" +
                        "Service : " + "{2:20}" +
                        "Product : " + "{3:20}" +
                        "Version : " + "{4:20}"
                    ).format(str(port), state, service, product, version)
                )

                if state == 'open':
                    HostArray.insert(len(HostArray), [target, port, service, product, version])

    except:
        print_colored("Target " + str(target) + " seems to have no open ports.", colors.red)
        output.WriteToFile("Target " + str(target) + " seems to have no open ports.")
    return HostArray

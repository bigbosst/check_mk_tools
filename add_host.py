#!/usr/bin/env python
import json, getopt, sys, pprint, requests
watourl = "https://url.for.wato.server/check_mk/webapi.py"
username = "automationuser"
password = "automationpassword"

def post( url, payload ):
    r = requests.post(url,data=payload)
    return json.loads(r.text)

def get( url ):
    r = requests.post(url)
    return json.loads(r.text)

def add_host( hostname, ipaddress, folder ):
    action = "add_host"
    url = watourl + '?action=' + action + '&_username=' + username + '&_secret=' + password
    data = json.dumps({"hostname": hostname, "folder": folder, "attributes": { "ipaddress": ipaddress } })
    result = post(url, "request=" + data)
    return result

def discover_services( hostname ):
    action = "discover_services"
    url = watourl + '?action=' + action + '&_username=' + username + '&_secret=' + password
    data = json.dumps({"hostname": hostname })
    result = post(url, "request=" + data)
    return result

def activate_changes():
    action = "activate_changes"
    url = watourl + '?action=' + action + '&_username=' + username + '&_secret=' + password
    result = get(url)
    return result

def display_help():
    print 'add_host.py -n <hostname> -s <shortname> -i <ipaddress> -f <folder>'
    print '  -n, --hostname         The full FQDN this field is required'
    print '  -s, --shortname        Generated from the given hostname by default'
    print '  -i, --ipaddress        Set to the FQDN by default'
    print '  -f, --folder           The host is added to the API folder in WATO by default'

def main(argv):
    hostname = ''
    shortname = ''
    ipaddress = ''
    folder = ''
    try:
        opts, args = getopt.getopt(argv,"hn:s:i:f:",["hostname=","shortname=","ipaddress=","folder="])
    except getopt.GetoptError:
        display_help()
        sys.exit(2)
    for opt, arg in opts:
        if (opt == '-h'):
            display_help()
            sys.exit()
        elif opt in ("-n", "--hostname"):
            hostname = arg
        elif opt in ("-s", "--shortname"):
            shortname = arg
        elif opt in ("-i", "--ipaddress"):
            ipaddress = arg
        elif opt in ("-i", "--folder"):
            folder = arg
    if (hostname == ''):
        display_help()
        sys.exit()
    if (folder == ''):
        folder = 'api'
    if (ipaddress == ''):
        ipaddress = hostname
    if (shortname == ''):
        shortname = hostname.rsplit('.',2)[0]

    msg = add_host(shortname,ipaddress,folder)
    if msg['result_code']:
        print "Error adding host %s" % msg['result']
        sys.exit(1)

    msg = discover_services(shortname)
    if msg['result_code']:
        print "Error Discovering Services %s " % msg['result']
        sys.exit(1)

    msg = activate_changes()
    if msg['result_code']:
        print "Error activating changes %s " % msg['result']
        sys.exit(1)

    print "%s added Successfully" % shortname
    sys.exit()
    
if __name__ == "__main__":
    main(sys.argv[1:])

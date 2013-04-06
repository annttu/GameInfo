#!/usr/bin/env python
from lib.database import OTTDStats, ConnectionError
from openttd.client import Client, M_UDP, M_TCP
#from openttd.grfdb import GrfDB
import openttd.date
import sys
import socket

def printUsage():
    print "usage: %s <ip:port>" % sys.argv[0]
    sys.exit(1)

def main():
    if len(sys.argv) == 0:
        printUsage()

    try:
        ip, port = sys.argv[1].split(':')
        port = int(port)
    except:
        printUsage()

    try:
        d = OTTDStats()
    except ConnectionError as e:
        print("Cannot connect to database")

    client = Client(ip, port)
    client.connect(M_UDP)
    try:
        gi=client.getGameInfo()
    except socket.error:
        print("Cannot Connect to server")
        return
    data = {"companies_on":0, "clients_on":0, "spectators_on":0}
    if not gi is None:
        for k in data.keys():
            data[k] = "%s" % getattr(gi, k)
        data["server"] = ip
        data["game_date"] = openttd.date.OpenTTDDate(ottddate=gi.game_date).toDate()
        data["start_date"] = openttd.date.OpenTTDDate(ottddate=gi.start_date).toDate()
        #print(data)
        d.addGameStats(**data)
    else:
        return
    if gi.companies_on > 0:
        #print ""
        #print "getting company info ..."
        if gi.clients_on < gi.clients_max:
            # try connecting using TCP
            try:
                client.connect(M_TCP)
                cis = client.getTCPCompanyInfo()
                using_tcp = True
            except Exception, e:
                print "exception when connecting using tcp, trying udp: %s" % e
                cisi = client.getCompanyInfo()
                cis = cisi.companies
                using_tcp = False
        else:
            cisi=client.getCompanyInfo()
            cis = cisi.companies
            using_tcp = False
        if not cis is None:
            for ci in cis:
                data = {"company_name":None, "inaugurated_year":None, "company_value":None, "money":None,
                        "income":None, "performance":None, "password_protected":False}
                for k in data.keys():
                    data[k] = getattr(ci, k)
                data["clients"] = 0
                if using_tcp:
                    #print(type(ci.clients))
                    data["clients"] = len(ci.clients.split(','))
                elif cisi.info_version < 5:
                    data["clients"] = len(ci.clients.split(','))
                #print(data)
                d.addCompanyStats(**data)
        else:
            return

    client.disconnect()

if __name__ == '__main__':
    main()

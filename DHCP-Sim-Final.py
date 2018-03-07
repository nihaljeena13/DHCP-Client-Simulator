#!/usr/bin/env python

#all the modules you need
import subprocess
import logging
import random
import sys


#logger function used from logging modules to supress warning messages generated from the Scapy
#which are of less important.
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)

#logger function needs to be used before importing Scapy module.
try:
    from scapy.all import *

except ImportError:
    print "Scapy package for Python is not installed on your system."
    print "Get it from https://pypi.python.org/pypi/scapy and try again."
    sys.exit()
    
#We are simulating DHCP clients and their MAC addresses and we want all the traffic generated
#and that comes to the interface "eth1" to go directly to the CPU.
print "\n! Make sure to run this program as ROOT !\n"

#change interface to Promisc mode so that it permits all the traffic from the DHCP clients.
net_iface = raw_input("Enter the interface where you want all your traffic to be received.: ")

subprocess.call(["ifconfig", net_iface, "promisc"], stdout=None, stderr=None, shell=False)

print "\nInterface %s was set to PROMISC mode." % net_iface



#Packets were broadcasted to every client and the reply could be received from any client
#so not necessary that the destination IP address will match.
conf.checkIPaddr = False



all_given_leases = []
server_id = []
client_mac = []

#to generate DHCP client packets and receive server packets.
def generate_dhcp_seq():
    global all_given_leases
    
    #x_id is the DHCP transaction id randomly created.
    #hw is the source mac address whose last 8 digits aare radomly created using str(RandMAC()) function in scapy.
    #hw_str converts MAC to string format.
    x_id = random.randrange(1, 1000000)
    hw = "00:00:5e" + str(RandMAC())[8:]
    hw_str = mac2str(hw)

    
    #DHCP discover packet sent to every server in the network
    #srpp function in Scapy is to send and receive a packet, when client sends a discover packet and the server
    #sends an offer packet back to the client, offering the virtual cliet IP address for which the client was looking for.
    dhcp_dis_pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=hw)/IP(src="0.0.0.0",dst="255.255.255.255") / UDP(sport=68,dport=67)/BOOTP(op=1, xid=x_id, chaddr=hw_str)/DHCP(options=[("message-type","discover"),("end")])

    answd = srp(dhcp_dis_pkt, iface=pkt_inf, timeout = 2.5, verbose=0)
    
    #print answd
    #print answd.summary()
    #print answd[0][1][BOOTP].yiaddr

    offered_ip = answd[0][1][BOOTP].yiaddr
    #print offered_ip
    
    #sending request to the server through srp function
    #which in return sends an ACK, giving client Ip address.
    dhcp_req_pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=hw)/IP(src="0.0.0.0",dst="255.255.255.255") / UDP(sport=68,dport=67)/BOOTP(op=1, xid=x_id, chaddr=hw_str)/DHCP(options=[("message-type","request"),("requested_addr", offered_ip),("end")])

    answr = srp(dhcp_req_pkt, iface=pkt_inf, timeout = 2.5, verbose=0)
    
    #print answr
    #print answr[0][1][IP].src
    #print answr[0][1][BOOTP].yiaddr
    

    offered_ip_ack = answr[0][1][BOOTP].yiaddr
    
    #extracting DHCP Server IP
    server_ip = answr[0][1][IP].src
    #print server_ip
    
    #Adding each leased IP to the list of leases
    all_given_leases.append(offered_ip_ack)

    #Adding the server IP to a list
    server_id.append(server_ip)

    client_mac.append(hw)    
    
    return all_given_leases, server_id, client_mac



def generate_dhcp_release(ip, hw, server):

    #x_id is generating random DHCP transaction id
    #hw_str is converting mac to string format.
    x_id = random.randrange(1, 1000000)
    hw_str = mac2str(hw)
    
    #Creating the RELEASE packet
    dhcp_rls_pkt = IP(src=ip,dst=server) / UDP(sport=68,dport=67)/BOOTP(chaddr=hw_str, ciaddr=ip, xid=x_id)/DHCP(options=[("message-type","release"),("server_id", server),("end")])
    
    #Sending the RELEASE packet
    send(dhcp_rls_pkt, verbose=0)



try:
    #Enter option for the first screen
    while True:
        print "\nUse this tool to:\ns - Simulate DHCP Clients\nr - Simulate DHCP Release\ne - Exit program\n"
        
        user_option_sim = raw_input("Enter your choice: ")
        
        if user_option_sim == "s":
            
            pkt_no = raw_input("\nNumber of DHCP clients to simulate: ")
            
            pkt_inf = raw_input("Interface on which to send packets: ")

            
            try:
                #Calling the function for the required number of times (pkt_no), to get the Ip address from the server.
                for i in range(0, int(pkt_no)):
                    all_leased_ips = generate_dhcp_seq()[0]
                      
                #print all_leased_ips
                
            except IndexError:
                print "No DHCP Server detected or connection is broken."
                print "Check your network settings and try again.\n"
                sys.exit()
                
            #List of all leased IPs, with their server id and Mac address.
            dhcp_leases = open("DHCP_Leases.txt", "w")

            
            #Print each leased IP to the file
            for index, each_ip in enumerate(all_leased_ips):
                
                print >>dhcp_leases, each_ip + "," + server_id[index] + "," + client_mac[index]
                
            dhcp_leases.close()
            
            continue

        elif user_option_sim == "r":
            while True:
                print "\ns - Release a single address\na - Release all addresses\ne - Exit to the previous screen\n"
                
                user_option_release = raw_input("Enter your choice: ")
                
                if user_option_release == "s":
                    print "\n"
                    
                    user_option_address = raw_input("Enter IP address to release: ")

                    
                    try:
                        #Check if required IP is in the list and run the release function for it
                        if user_option_address in all_leased_ips:
                            index = all_leased_ips.index(user_option_address)

                            generate_dhcp_release(user_option_address, client_mac[index], server_id[index])
                            
                            print "\nSending RELEASE packet...\n"
                            
                        else:
                            print "IP Address not in list.\n"
                            continue
                    
                    except (NameError, IndexError):
                        print "\nSimulating DHCP RELEASES cannot be done separately without first simulating the DHCP clients"
                        print "Restart the program and simulate the DHCP clients\n"
                        sys.exit()
                
                elif user_option_release == "a":

                    try:
                        #Check if required IP is in the list and run the release function for it
                        for user_option_address in all_leased_ips:
                            
                            index = all_leased_ips.index(user_option_address)

                            generate_dhcp_release(user_option_address, client_mac[index], server_id[index])
                            
                    except (NameError, IndexError):
                        print "\nSimulating DHCP RELEASES cannot be done seperately without first simulating the DHCP clients."
                        print "Restart the program and simulate DHCP Clients\n"
                        sys.exit()
                    
                    print "\nThe RELEASE packets have been sent.\n"
                    
                    #Erasing all leases from the file
                    open("DHCP_Leases.txt", "w").close()
                    
                    print "File 'DHCP_Leases.txt' has been cleared."
                    
                    continue
                
                else:
                    break
            
        else:
            print "Exiting... See ya Mate!!...\n\n"
            sys.exit()

except KeyboardInterrupt:
    print "\n\nProgram aborted by user. Exiting...\n"
    sys.exit()            

#End of program
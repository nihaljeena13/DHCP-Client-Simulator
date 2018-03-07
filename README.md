# DHCP-Client-Simulator
----Dynamically assigning unique IP addresses to clients for communication purposes in the network given by the server.----


--Dynamic Host Configuration protocol is a  cryptographic network protocol that assigns unique IP adrreses to the hosts and also provides other network addresses like subnet mask, default gateway and the DNS address It comes in two flavors i.e. client and server.

--For our computers to work over the network they need an IP address which has to be unique on the network.DHCP solves our problem by running DHCP client on each computer that will allow the computer to ask an IP address. Somewhere in the network there will e DHCP server. This is where the IP addresses are managed.DHCP servers cab be ran on routers or servers at home.

----Different steps to collect virtual IP addresses using Dynamic Host Configuration Protocol-:

-->When you turn your PC on, if it doesn't have an address it looks for a DHCP server. It just broadcasts messsage to everyone in the network hoping somewhere in the network there is a DHCP server. All the other devices looks at the message and drops it. This is the first step called DHCP discover.
-->When the DHCP server looks at the client's messge it offers an IP address to the client. If more then one offer is given it will choose the first one it receives. This is the second step called DHCP offer.
T-->he client then requests for an IP address that the DHCP server has offered. This is the third step called DHCP request.
-->The DHCP server will send the IP address along with the subnet mask, the default gateway and the DNS server.This is the fourth step called DHCP acknowledgment.

--The DHCP server keeps the record of all leased IP addresses that can be virtually assigned to different hosts. The server gives IP addresses to each clients with leased time . This will allow clients to renew its IP addresses. This is how our IP addresses is never wasted. Even when you are not using your computer your IP address is not being wasted. Pretty much evryone uses it evry single day without giving a second thought.

--This application assign IP addresses to cliets that do not exists. This program will also releases IP addresses. It will either release all the IP addrsses it receives from the server or the single address that the user specifies.
--Assumig that there is a DHCP server in the network. The user can simulate any number of DHCP clients. All the IP addreses obtained from the server are saved in the "dhcpleases.txt" file. After releasing ll the ddresses the dhcpleases.txt file is also cleared.
--We make use of Scapy module to send packets to the network. Packets like Discover and Request packets ares send to the server using python scapy module.

----Execution process:-
-->I have connected my virtual machine to router r1 in GNS3 topology. This router runs DHCP server and it is already configured.
-->Run the program in the virtual machine linux.
-->The first thing you have to enter interface where you all your traffic to enter.
-->Next we ask the user to enter his choice of selection, either to simulate DHCP clients or simulate DHCP release.
-->In simulating DHCP clients, you will be asked the number of clients you want to simulate.
-->Now check the DHCP_Leases.txt file in another terminal and you will see the saved IP address, IP adress of the server and the MAC address of the client.













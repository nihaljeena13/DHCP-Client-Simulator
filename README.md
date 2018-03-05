# DHCP-Client-Simulator
Dynamically assigning unique IP addresses to clients for communication purposes in the network given by the server.


Dynamic Host Configuration protocol is a  cryptographic network protocol that assigns unique IP adrreses to the hosts and also provides other network addresses like subnet mask, default gateway and the DNS address It comes in two flavors i.e. client and server.

For our computers to work over the network they need an IP address which has to be unique on the network.DHCp solves our problem by running Dhcp client on each computer that will allow the computer to ask an IP address. Somewhere in the network there will e DHCP server. This is where the IP addresses are managed.DHCP servers cab be ran on routers or servers at home.

Different steps to send data over a network uing DHCP-:

When you turn your PC on, if it doesn't have an address it looks for a DHCP server. It just broadcasts messsage to everyone in the network hoping somewhere in the network there is a DHCP server. All the other devices looks at the message and drops it. This is the first step called DHCP discover.
When the DHCP server looks at the client's messge it offers an IP address to the client. If more then one offer is give it will choose the first one it receives. This is the second step called DHCP offer.
The client then requests for an IP address that the DHCP server has offered. This is the third step called DHCP request.
The DHCP server will send the IP address along with the subnet mask, the default gateway and the DNS server.Tis is the fourth step called DHCP acknowledgment.

The DHCP server keeps the record of all leased IP addresses that can be virtually assigned to different hosts. The server gives IP addresses to each clients with leased time . This will allow clients to renew its IP addresses. This is how our IP addresses is never waasted. Even when you are not using your computer your IP address is not being wasted. Pretty much evryone uses it evry single day without giving a second thought.

This application assign IP addresses to cliets that do not exists. This program will also releases IP addresses. It will either release all the IP addrsses it receives from the server or the single address that the user specifies.
Assumig that there is a DHCP server in the network. The user can simulate any number of DHCP clients. All the IP addreses obtained from the server are saved in the "dhcpleases.txt" file. After releasing ll the ddresses the dhcpleases.txt file is also cleared.
We make use of Scapy module to send packets to the network. Packets like Discover and Request packets ares send to the server using python scapy module.












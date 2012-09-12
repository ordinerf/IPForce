#!/usr/bin/python
import os,sys, time, random, re, MySQLdb

#####################################################
#####################################################
#####################################################
#####################################################

F="/sbin/iptables"
G_NET_NAME="eth0"
G_NET_IP="XXX.XXX.XXX.XXX"
dbhost = "127.0.0.1"
dbuser = "root"
dbpassword = "secret"

#####################################################
#####################################################
#####################################################
#####################################################

conn = MySQLdb.connect (host = dbhost, user = dbuser, passwd = dbpassword, db = "iptables")
cursor = conn.cursor()
cursor.execute ("SELECT IP FROM banned")
banned = cursor.fetchall()

cursor.execute ("SELECT interface,sourceIP,destinationIP,destinationPORT,policy FROM rules WHERE direction='IN' AND protocole='TCP'")
rules_in = cursor.fetchall()

cursor.execute ("SELECT interface,sourceIP,destinationIP,destinationPORT,policy FROM rules WHERE direction='IN' AND protocole='UDP'")
rules_out = cursor.fetchall()
cursor.close()

#####################################################
#####################################################
#####################################################
#####################################################

#setup of modules and kernel config
os.system("/sbin/modprobe ip_tables")
os.system('echo "1" > /proc/sys/net/ipv4/ip_forward')
#ignore ICMP echo request sended to broadcast
os.system('echo "1" > /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts')
#SYN flood protection
os.system('echo "1" > /proc/sys/net/ipv4/tcp_syncookies')
#refuse source routed packets
os.system('echo "0" > /proc/sys/net/ipv4/conf/all/accept_source_route')
os.system('echo "1" > /proc/sys/net/ipv4/conf/all/secure_redirects')
#source validation by reversed path (RFC1812).
os.system('echo "1" > /proc/sys/net/ipv4/conf/all/rp_filter')
#log packets from incorrect sources
os.system('echo "1" > /proc/sys/net/ipv4/conf/all/log_martians')

##################
# INITIALIZATION #
##################

os.system('echo "Setup policy for standard chains..."')
os.system(F+" -P INPUT ACCEPT")
os.system(F+" -P FORWARD ACCEPT")
os.system(F+" -P OUTPUT ACCEPT")
os.system(F+" -t nat -P PREROUTING ACCEPT")
os.system(F+" -t nat -P OUTPUT ACCEPT")
os.system(F+" -t nat -P POSTROUTING ACCEPT")
os.system(F+" -t mangle -P PREROUTING ACCEPT")
os.system(F+" -t mangle -P OUTPUT ACCEPT")
os.system(F+" -t mangle -P INPUT ACCEPT")
os.system(F+" -t mangle -P FORWARD ACCEPT")
os.system(F+" -t mangle -P POSTROUTING ACCEPT")

os.system('echo "Cleaning rules for standard chains..."')
os.system(F+" -F")
os.system(F+" -t nat -F")
os.system(F+" -t mangle -F")

os.system('echo "Deleting all nonstandard chains..."')
os.system(F+" -X")
os.system(F+" -t nat -X")
os.system(F+" -t mangle -X")

os.system('echo "Setting up policy for standard chains..."')

os.system('echo "Creating extra chains rules..."')
os.system(F+" -N bad_packet")
os.system(F+" -N bad_tcp_packet")
os.system(F+" -N pakiety_icmp")
os.system(F+" -N tcp_in_filter")
os.system(F+" -N tcp_out_filter")
os.system(F+" -N udp_in_filter")
os.system(F+" -N udp_out_filter")

###############
# bad_packets #
###############

os.system('echo "Creating rules for chain bad_packet..."')
os.system(F+" -A bad_packet -p ALL -m state --state INVALID -j DROP")
os.system(F+" -A bad_packet -p tcp -j bad_tcp_packet")
os.system(F+" -A bad_packet -p ALL -j RETURN")

###################
# bad_tcp_packets #
###################

os.system('echo "Creating rules for chain bad_tcp_packet..."')
os.system(F+" -A bad_tcp_packet -p tcp -i G_NET_NAME -j RETURN")
os.system(F+" -A bad_tcp_packet -p tcp ! --syn -m state --state NEW -j DROP")
os.system(F+" -A bad_tcp_packet -p tcp --tcp-flags ALL NONE -j DROP")
os.system(F+" -A bad_tcp_packet -p tcp --tcp-flags ALL ALL -j DROP")
os.system(F+" -A bad_tcp_packet -p tcp --tcp-flags ALL FIN,URG,PSH -j DROP")
os.system(F+" -A bad_tcp_packet -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP")
os.system(F+" -A bad_tcp_packet -p tcp --tcp-flags SYN,RST SYN,RST -j DROP")
os.system(F+" -A bad_tcp_packet -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP")
os.system(F+" -A bad_tcp_packet -p tcp -j RETURN")

################
# icmp_packets #
################
os.system('echo "Creating rules for chain pakiety_icmp..."')
os.system(F+" -A pakiety_icmp --fragment -p ICMP -j DROP")
#ping and ping logging
os.system(F+" -A pakiety_icmp -p ICMP -s 0/0 --icmp-type 8 -j ACCEPT")
#ping - hash out in case of enabling above rules
os.system(F+" -A pakiety_icmp -p ICMP -s 0/0 --icmp-type 8 -j DROP")
os.system(F+" -A pakiety_icmp -p ICMP -s 0/0 --icmp-type 11 -j ACCEPT")
os.system(F+" -A pakiety_icmp -p ICMP -j RETURN")

######################
## BANNED
######################

for ip in banned:

	os.system(F+" -A tcp_in_filter -s "+ip[0]+" -j DROP")
	os.system(F+" -A udp_in_filter -s "+ip[0]+" -j DROP")

################
# tcp_incoming #
################

os.system('echo "Creating rules for chain tcp_in_filter..."')

for rules in rules_in:

	query = ""

	j = 0
	
	if rules[j] != None:

		query += "-i "+rules[j]+" "

	j = j+1
	
	if rules[j] != None:

		query += "--source "+rules[j]+" "

	j = j+1
        
	if rules[j] != None:

                query += "--destination "+rules[j]+" "

	j = j+1
	
	if rules[j] != None:

                query += "--dport "+rules[j]+" "

	j = j+1
        
	if rules[j] != None:

                query += "-j "+rules[j]+" "
	
	os.system(F+" -A tcp_in_filter -p TCP "+query)

os.system(F+" -A tcp_in_filter -p TCP -j RETURN")

################
# tcp_outgoing #
################

os.system('echo "Creating rules for chain tcp_out_filter..."')

os.system(F+" -A tcp_out_filter -p TCP -s 0/0 -j ACCEPT")

################
# udp_incoming #
################

os.system('echo "Creating rules for chain udp_in_filter..."')

for rules in rules_out:

        query = ""

        j = 0

        if rules[j] != None:

                query += "-i "+rules[j]+" "

        j = j+1

        if rules[j] != None:

                query += "--source "+rules[j]+" "

        j = j+1

        if rules[j] != None:

                query += "--destination "+rules[j]+" "

        j = j+1

        if rules[j] != None:

                query += "--dport "+rules[j]+" "

        j = j+1

        if rules[j] != None:

                query += "-j "+rules[j]+" "

        os.system(F+" -A udp_in_filter -p UDP "+query)

os.system(F+" -A udp_in_filter -p UDP -j RETURN")

################
# udp_outgoing #
################

os.system('echo "Creating rules for chain udp_out_filter..."')

os.system(F+" -A udp_out_filter -p UDP -s 0/0 -j ACCEPT")

#########
# INPUT #
#########

os.system('echo "Creating rules for chain INPUT..."')

os.system(F+" -A INPUT -p ALL -i lo -j ACCEPT")

os.system(F+" -A INPUT -p ALL -j bad_packet")

os.system(F+" -A INPUT -p ALL -d 224.0.0.1 -j DROP")

os.system(F+" -A INPUT -p ALL -i G_NET_NAME -m state --state ESTABLISHED,RELATED -j ACCEPT")

os.system(F+" -A INPUT -p ICMP -i G_NET_NAME -j pakiety_icmp")

os.system(F+" -A INPUT -p TCP -i G_NET_NAME -j tcp_in_filter")

os.system(F+" -A INPUT -p UDP -i G_NET_NAME -j udp_in_filter")

os.system(F+" -A INPUT -p ALL -d 255.255.255.255 -j DROP")


###########
# FORWARD #
###########

os.system('echo "Creating rules for chain FORWARD..."')

##########
# OUTPUT #
##########

os.system('echo "Creating rules for chain OUTPUT..."')

os.system(F+" -A OUTPUT -m state -p icmp --state INVALID -j DROP")

os.system(F+" -A OUTPUT -p ALL -s 127.0.0.1 -j ACCEPT")

os.system(F+" -A OUTPUT -p ALL -o lo -j ACCEPT")

os.system(F+" -A OUTPUT -p ALL -o G_NET_NAME -j ACCEPT")


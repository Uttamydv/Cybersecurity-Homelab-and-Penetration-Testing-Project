# Cybersecurity Homelab: Windows Server, Windows 10 Client, Kali Linux, and Metasploitable 2 Setup

## Overview

This project outlines the setup of a complete cybersecurity homelab featuring the following components:
- **Windows Server 2019**: Configured as a domain controller with **Active Directory**.
- **Windows 10 Client**: Joined to the domain to simulate a corporate environment.
- **Kali Linux**: Used for penetration testing and vulnerability scanning.
- **Metasploitable 2**: A vulnerable target machine used for performing attacks and exploiting its vulnerabilities.

The homelab allows you to test and practice key cybersecurity concepts such as **network security**, **Active Directory management**, **vulnerability scanning and Exploitation**, and **penetration testing**.

---

## Step 1: Set Up the Windows Server 2019 (Active Directory Domain Controller)

### 1.1 Install Windows Server on VMware

1. **Download Windows Server ISO** from Microsoft's official site.
2. **Create a new VM** in VMware with at least:
   - **2GB RAM**, **2 CPU cores**, **40GB disk**.
   - Attach the Windows Server ISO and complete the installation as like of opnsense.

3. Set an **Administrator password** and log into the Windows Server.

### 1.2 Configure Active Directory

1. **Assign a Static IP** (e.g., `192.168.1.10`).
2. **Install Active Directory Domain Services (AD DS)** via Server Manager.
3. **Promote the server to a domain controller**:
   - Set up a new domain (e.g., `lab.local`).

4. After restarting, open **Active Directory Users and Computers** to verify that AD is running.

---

## Step 2: Set Up Windows 10 Client VM

The Windows 10 client will be joined to the domain controlled by the Windows Server.

### 2.1 Install Windows 10 on VM

1. **Download Windows 10 OVA file** from Microsoft's site.
2. From **OVA package** you had a Pre-configured VM which can be imported directly and ready to use without running the intaller.
**Alternative**
1. **Download Windows 10 ISO file** from Microsoft's site.
2. **Create a new VM** in VMware with:
   - **1.5GB RAM**, **1 CPU core**, **40GB disk**.
3. Complete the installation with a local account similar to earlier iso installation and start the machine.

### 2.2 Join the Windows 10 Client to the Domain

1. Set the **DNS server** of the Windows 10 VM to the IP of the Windows Server (e.g., `192.168.1.10`).
2. Go to **System > About** and click **Join a domain**.
3. Enter the **domain name** (e.g., `lab.local`), and provide **Administrator credentials** to join the domain.
4. Reboot the VM and log in with **domain credentials**.

---

## Step 3: Set Up Kali Linux for Penetration Testing

**Kali Linux** will be used for penetration testing(attacking machine) in the homelab. It will be used to test attacks against both the **Windows Server** and **Metasploitable 2**.

### 3.1 Install Kali Linux on VM
- You can install kali from the **ISO** or through a pre-configured **OVA** file(Similar installation steps).
- Once installed, update the system:
   ```bash
   sudo apt update && sudo apt upgrade -y
## 3.2 Configure Kali Networking

### Configure the Network:

1. Set **Kali Linux** to use the same **internal network (LAN)** as the other VMs in the homelab (e.g., on OPNsense).
2. Ensure the network adapter is connected to the same network as the **Windows Server** and **Windows Client** VMs.

### Verify Connectivity:

Check if the **Kali Linux VM** can communicate with the other VMs in your network:
ping 192.168.1.10   # Ping Windows Server
ping 192.168.1.100  # Ping Windows 10 Client
ping 192.168.1.50   # Ping Metasploitable 2


---
---

## Step 4: Set Up Metasploitable 2 (Vulnerable Target Machine)

**Metasploitable 2** is a deliberately vulnerable Linux machine designed to be used for practicing penetration testing.

### 4.1 Install Metasploitable 2

1. **Download Metasploitable 2** from: [https://sourceforge.net/projects/metasploitable/](https://sourceforge.net/projects/metasploitable/).

2. **Import the VM into VMware**:
   - Open VMware and select **Import Appliance**.
   - Import the **Metasploitable 2 OVA** file.

3. **Start the VM** and log in:
   - **Username**: `msfadmin`
   - **Password**: `msfadmin`

---

### 4.2 Configure Networking for Metasploitable 2

1. Set the **network adapter** of Metasploitable 2 to the same internal network (LAN) as the other VMs.

   - In **VirtualBox** or **VMware**, configure the network adapter to match the settings of the other machines connected to your internal network.

### Verify Connectivity:

Ensure that **Metasploitable 2** can be pinged from **Kali Linux** and other VMs:
```bash
ping 192.168.1.50   # Ping Metasploitable 2

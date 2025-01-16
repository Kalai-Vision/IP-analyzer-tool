# IP Analyzer Tool

## Description:-
The **IP Analyzer Tool** is a Python-based application that helps users analyze IP addresses and domain names. The tool allows users to monitor and manage devices on a network, view configurations, and troubleshoot network issues. All through a user-friendly graphical interface built with Tkinter.

### Features:-
- **Ping Analyzer**:  Ping any IP address or domain and check if the host is active. Measures response time, TTL (Time to Live), and packet loss.
- **Traceroute**:  Trace the route of packets from your machine to a remote IP or domain and see the path and delays.
- **Port Scanner**:  Scan ports on a given IP address to check for open ports.
- **Internet Speed Test**:  Measure the speed of your internet connection using the speedtest-cli tool.
- **Configuration**:  View detailed network configuration (IP, DNS, etc.) of your system.
- **Device Management**:  Add, remove, and view devices using an SQLite database to store device information (IP address, device name, and type).
- **User-friendly Interface**:  Full-screen mode with clear controls.

### Requirements:-
To run this tool, make sure you have the following installed:
- Python 3.8
- PyCharm
- speedtest-cli (You can install or uninstall speedtest-cli using pip, or this app provides options to install and uninstall it)

### Required Python packages:-
- `tkinter`: Standard Python library for creating graphical user interfaces. It provides tools to build windows, buttons, text boxes, and other GUI elements.
- `subprocess`: Allows execution of external commands within Python, enabling interaction with system processes and retrieval of their output.
- `ipaddress`: A module for creating, manipulating, and validating IPv4 and IPv6 addresses and networks. It simplifies working with IP addresses in Python.
- `socket`: A module that enables low-level networking in Python, allowing the creation of network connections. It's essential for building client-server applications and facilitates communication between devices on a network.
- `sqlite3`: A lightweight disk-based database. This module allows Python applications to interact with SQLite databases, making it easy to store and retrieve data.
- `speedtest-cli` (optional): It allows you to measure the download and upload speeds of your internet connection using the Speedtest.net service. It is an external library that needs to be installed.
---

## How to Use:-
1. **Ping**: Enter the IP address or domain name and the number of packets. Click the "Ping IP/Domain" button.
2. **Traceroute**: Enter the target IP/domain and click the "Trace It" button.
3. **Port scan**: Enter the IP and port range, then click "Scan Open Port."
4. **Internet speed test**: Click the "Network Speed" button to measure your connection speed.
5. **Add device**: Enter in device details and click "Add New Device."
6. **View device details**: Click View Device Details" to display device information.
7. **Ping all**: Click "Ping All IP/Domain" to ping all devices in the database.
8. **Ping by ID**: Enter a specific ID and click "Ping My ID."
9. **Remove by ID**: Enter the ID of the device and click "Remove Device."
10. **Configuration**: Click "Network Status" to view the current Host configuration.

---

## Troubleshooting:-
- Ensure your internet connection is active for functions like pinging, traceroute, port scanning, and speed testing.
- If speedtest fails, check if `speedtest-cli` is installed properly.

---

## Video Demonstration:-

Here is a step-by-step demonstration of how to use the **IP Analyzer Tool**:

1. **Code Execution** :- Executing the full source code of the IP Analyzer Tool.
   


      https://github.com/user-attachments/assets/c9f0069d-5616-4713-a45e-68c3647fe4a4


2. **Ping** :- Pinging a specific IP address or domain to check its reachability and response time.  
   

      https://github.com/user-attachments/assets/51d0b5b5-d063-497a-8c00-86eca117924e


3. **Add Details** :- Adding a new device or IP address/domain to the database.  
   

      https://github.com/user-attachments/assets/8cb9cc37-689b-43cf-bf65-6868114bfeb7



4. **View Details** :- viewing the details of a device or IP address/domain in the database.  
   


      https://github.com/user-attachments/assets/dba3058f-2fd0-45c5-8576-40b4bd438313


5. **Ping Using ID** :- Pinging a device using its unique ID stored in the database.  
   

      https://github.com/user-attachments/assets/23413ede-1b6b-4198-8ea4-9b6dd09a3c7f



6. **Remove Using ID** :- Removing a device or IP/domain from the database by providing its specific ID.  
   

      https://github.com/user-attachments/assets/ba2180f4-737a-470a-8da3-9766b8894f42



7. **Ping All IP/Domain in the Database** :- Pinging all devices or IPs/domain stored in the database with just one click.  
   

      https://github.com/user-attachments/assets/126296eb-f8d7-44ff-b5e8-66a8d0b202a1



8. **Traceroute** :- Tracing the route using target IP/domain.  
   

      https://github.com/user-attachments/assets/63a53b7e-3673-46b8-bd2c-5a58b5930d23



9. **Scan Open Ports** :- Scanning a specified range of ports for open services using specific IP/domain.  
   **Video:1**

      https://github.com/user-attachments/assets/dca17d82-368b-4255-8e66-a38742966489

   **Video:2**

      https://github.com/user-attachments/assets/23c24c74-2d87-401c-a29f-ffc5a26c799f



10. **View Host Configuration** :- Viewing the host configuration, including IP address, subnet mask, and gateway.  
   

      https://github.com/user-attachments/assets/c79ac7f0-3aa2-4dd5-b501-66a1fff27bcc



11. **Check Internet Speed** :- Measuring the internet speed, including download & upload speed.  
    


      https://github.com/user-attachments/assets/16841c91-ce07-4c66-918e-85d01d884bce


12. **Install & Uninstall Speedtest-cli** :- Installing and uninstalling the **speedtest-cli** with buit-in options.



      https://github.com/user-attachments/assets/149b92de-6d89-48fe-baf4-fd2d6064f823


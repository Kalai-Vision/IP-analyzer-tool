from tkinter import *
import tkinter.messagebox as msg
from tkinter import ttk
import sqlite3
import subprocess
import ipaddress
import socket

# Initialize the Main Window
window=Tk()
window.attributes('-fullscreen',True)

# Create a frame for the Top Header
top_headframe=Frame(window,width=700,bd=0.2,bg='#61dafe')
top_headframe.pack(side=TOP)

# Create a label for the Heading
heading_label=Label(top_headframe,text='IP Analyzer Tool',font=('arial',25,'bold'),fg='white',bg='#2B3D51',relief='raised',width=69)
heading_label.grid(row=0,column=0,padx=0,pady=0)

########################################################################################################################
# Creating Table for Device Records in Health Check Database
conn=sqlite3.connect('health_check.db')
cursor=conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS devices
                (id INTEGER PRIMARY KEY,
                ip_address TEXT NOT NULL,
                device_name TEXT,
                device_type TEXT)""")
conn.commit()

########################################################################################################################
# Function to Validate IP Address or Domain Name
def check_valid_ip_domain():
    ip_domain = ip.get()
    try:
        ipaddress.ip_address(ip_domain)
        check()
        return True
    except ValueError:
        try:
            socket.gethostbyname(ip_domain)
            check()
            return True
        except socket.gaierror:
            msg.showinfo('Invalid Input', 'Please check if the IP or domain name is valid, '
                                          'or check your internet connection.')
            return False


# Function to Ping IP Address and Get Response Time
def ping(ip):
    num_pack = numpack.get()
    if not num_pack.isdigit():
        msg.showerror('Invalid Input','Please select the number of packect',icon='warning')
        return
    try:
        result = subprocess.run(['ping','-4','-n',numpack.get(),ip], stdout = subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
        if result.returncode == 0:
            response_time = result.stdout.split('Average =')[1].split()[0]
            ttl = result.stdout.split('TTL=')[1].split()[0]
            packet_loss = result.stdout.split('Lost =')[1].split()[0]
            return True, response_time,ttl,packet_loss
        else:
            return False
    except IndexError:
        return False, 'N/A', 'N/A', 'N/A'

########################################################################################################################
# Function to Perform Traceroute on IP Address or Domain
def traceroute():
    try:
        ipdo=trace_ip.get()
        tresult=subprocess.run(['tracert','-4',ipdo],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        if tresult.returncode == 0:
            return True,tresult.stdout
        else:
            msg.showerror("Error", "Traceroute failed. Please check the IP/Domain.")
    except Exception as e:
        msg.showerror("Exception occurred", str(e))
        return False

# Function to Display Traceroute Results
def show_traceroute():
    success, output = traceroute()
    if success:
        traceroute_output.config(state='normal')
        traceroute_output.delete('1.0', 'end')
        traceroute_output.insert('1.0', output)
        traceroute_output.config(state='disabled')
    else:
        msg.showerror("Error", "Failed to retrieve trace route")

########################################################################################################################
# Function to get network configuration
def netconfig():
    try:
        result = subprocess.run(['ipconfig', '/all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            msg.showerror("Command Error:", result.stderr)
            return False, 'N/A'
    except Exception as e:
        msg.showerror(f"Exception occurred: {e}")
        return False, None

# Function to show network configuration in a new window
def show_netconfig():
    success, output = netconfig()
    if success:
        window = Tk()
        window.geometry('650x650')
        window.title("Network Configuration")
        window.iconbitmap('winicon.ico')

        # Create a text widget to display the network configuration
        text = Text(window, wrap='word', font=('arial', 12,'bold'),fg='white',bg='#000000')
        text.insert('1.0', output)
        text.pack(expand=True, fill='both')
        text.config(state=DISABLED)
    else:
        msg.showerror("Error", "Failed to retrieve network configuration")

########################################################################################################################
# Function to get network speed test
def speedtest():
    try:
        result = subprocess.run(['speedtest-cli'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, 'N/A'
    except Exception as e:                                                                     
        return False, None

# Function to show network speed test in a new window
def show_speedtest():
    success, output = speedtest()
    if success:
        window = Tk()
        window.geometry('650x250')
        window.title ("Internet Speed")
        window.iconbitmap('winicon.ico')

        # Create a text widget to display the network speed
        text = Text(window, wrap='word', font=('arial', 12,'bold'),fg='white',bg='#000000')
        text.insert('1.0', output)
        text.pack(expand=True, fill='both')
        text.config(state=DISABLED)
    else:
        msg.showerror("Error", "Failed to retrieve network speed :-\n\n"
                     "1.Verifiy speedtest:-cli is installed or not\n\n "
                        "To Install -- ( click install button or 'pip install speedtest-cli' )\n\n" 
                     "2.Check your internet connection\n")

########################################################################################################################
# Function to Install & Uninstall Speedtest CLI
def installsp():
    try:
        result = subprocess.run(['pip','install','speedtest-cli'],capture_output=True)
        if result.returncode == 0:
            msg.showinfo('Speed test', 'Installed Successfully', icon='info')
            return True
        else:
            msg.showerror('Speed test', 'Installation Unsuccessful', icon='warning')
            return False
    except Exception as e:
        msg.showerror('Speed test', f'An error occurred: {e}', icon='warning')
        return False

def uninstallsp():
    try:
        result = subprocess.run(['pip','uninstall','speedtest-cli','-y'],capture_output=True)
        if result.returncode == 0:
            msg.showinfo('Speed test', 'Uninstalled Successfully', icon='info')
            return True
        else:
            msg.showerror('Speed test', 'Uninstallation Unsuccessful', icon='warning')
            return False
    except Exception as e:
        msg.showerror('Speed test', f'An error occurred: {e}', icon='warning')
        return False

########################################################################################################################
# Function to Scan Ports on a Given IP Address
def portscan():
    ip = portip.get()
    if not ip:
        msg.showerror("Error", "Please enter an IP address.")
        return
    try:
        fp_int=int(fp.get())
        tp_int=int(tp.get())
        output=""
        for port in range(fp_int,tp_int+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            sock.settimeout(0.5)
            if (result==0):
                output+= f"Port {port} : open\n"
            sock.close()
        return output

    except Exception as e:
        msg.showerror("Error", f"Failed to scan port {port}: {e}")

# Function to Display Port Scan Results
def show_portscan():
    output = portscan()
    if output:
        portscan_output.config(state='normal')
        portscan_output.delete('1.0', 'end')
        portscan_output.insert('1.0', output)
        portscan_output.config(state='disabled')
    else:
        portscan_output.config(state='normal')
        portscan_output.delete('1.0', 'end')
        portscan_output.insert('1.0', "No open ports found.")
        portscan_output.config(state='disabled')

########################################################################################################################
# Function to Check Device Status via Ping
def check():
    ip = ip_textbox.get()
    hostn = hostn_textbox.get()
    devicet_value = devicet.get()
    if not ip:
        msg.showerror("Error", "Please check your IP Address")
        return
    is_active, response_time, ttl ,packet_loss = ping(ip)

    tv.delete(*tv.get_children())
    if is_active:
        tv1.insert('', 'end', values=( '*',hostn, devicet_value,ip, 'Active', response_time ,ttl, packet_loss , 'N/A'))
    else:
        tv1.insert('', 'end', values=( '*',hostn, devicet_value,ip, 'Inactive', 'NILL','NILL', '100%','N/A'))

# Function to Check Status of All Devices in Database
def checkall():
    cursor.execute('SELECT id,ip_address, device_name, device_type FROM devices')
    devices = cursor.fetchall()

    tv.delete(*tv.get_children())

    for device in devices:
        id,ip,name,type=device
        is_active,response_time, ttl ,packet_loss = ping(ip)

        if is_active:
            status='Active'

        else :
            status='Inactive'
            response_time = 'NILL'
            ttl='NILL'
            packet_loss = '100%'

        tv1.insert('','end',value=(id,name,type,ip,status,response_time,ttl,packet_loss,'N/A'))

########################################################################################################################
# Function to Validate IP Address or Domain Name Before Adding
def add_valid_ip_domain():
    ip_domain = ip.get()
    try: 
        ipaddress.ip_address(ip_domain)
        addip()
        return True
    except ValueError:
        try:
            socket.gethostbyname(ip_domain)
            addip()
            return True
        except socket.gaierror:
            msg.showinfo('Invalid Input', "Please check if the IP or domain name is valid")
            return False

# Function to Add IP Address, Device Name, and Device Type to Database
def addip():
    conn = sqlite3.connect("health_check.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO devices
                    (ip_address,device_name,device_type) values (?,?,?)""",
                   (str(ip.get()), str(hostn.get()), str(devicet.get())))

    conn.commit()
    if cursor.rowcount > 0:
        msg.showinfo('Added', 'IP/Domain Added', icon='info')
        reset()
        viewip()

    else:
        msg.showerror('Error Found', 'IP/Domain Not Added', icon='warning')

# Function to Retrieve and Display All Device Records from the Database
def viewip():
    for i in tv.get_children():
        tv.delete(i)
    con = sqlite3.connect("health_check.db")
    cursor = con.cursor()
    cursor.execute('SELECT * FROM devices')
    data = cursor.fetchall()
    for i in data:
        tv.insert('', 'end', value=i)

    con.commit()

# Function to Remove a Device Record from the Database by ID
def removeip():
    conn = sqlite3.connect('health_check.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM devices where ID=?', (id.get(),))
    data = cursor.fetchall()
    for i in data:
        tv.insert('', 'end', value=i)
    cursor.close()
    conn.commit()

    if cursor.rowcount > 0:
        msg.showinfo('Confirmation Message', 'Deleted Successful', icon='info')
        reset()
        viewip()

    else:
        msg.showinfo('Error', 'IP/Domain Not Deleted', icon='warning')
    cursor.close()
    conn.commit()

# Function to Scan a Device by ID and Check Its Status
def idscan():
    conn = sqlite3.connect('health_check.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ip_address, device_name, device_type FROM devices where ID=?', (id.get(),))
    idata = cursor.fetchone()

    if idata:
        ip, hostn, devicet = idata
        is_active, response_time,ttl,packet_loss = ping(ip)

        if is_active:
            tv1.insert('', 'end', values=(id.get(), hostn, devicet,ip, 'Active', response_time ,ttl, packet_loss , 'N/A'))
        else:
            tv1.insert('', 'end', values=(id.get(), hostn, devicet,ip, 'Inactive', 'NILL','NIL', '100%','N/A'))

    else:
        msg.showerror("Error", "Device not found")

# Function to Update Device Type with Selected Value
def update(selected_value):
    devicet.set(selected_value)

# Function to Clear Input Fields and Reset Selections
def reset():
    hostn.set('')
    devicet.set('select')
    ip.set('')
    id.set('')
    numpack.set('select')
    trace_ip.set('')
    portip.set('')
    fp.set('From')
    tp.set('To')

# Function to Exit the Application
def exit():
    window.destroy()

################################################### Ping Frame #########################################################

# Frame for Ping Analyzer UI
ping_frame=Frame(window,bd=10,bg='#2B3D51',relief="raised", padx=10, pady=45)
ping_frame.place(x=10,y=50,relx=0,rely=0,anchor='nw')

# Title Label
ping_label=Label(window,text='Ping Analyzer',font=('arial',14,'bold'),fg='white',bg='red',relief='raised',width=20)
ping_label.place(x=0,y=40,relx=0.1,rely=0,anchor='nw')

# Device Type Selection
devicet=StringVar()
devicet.set('select')
devicet_lable=Label(ping_frame,text='Select Device',font=('arial',12,'bold'),fg='white',bg='#2B3D51',width=13)
devicet_lable.place(x=0,y=10,relx=0, rely=-0.425,anchor='nw')

types=['Pc','Switch','Router','Printer','Access Point','Website']
devicet_dropbox=OptionMenu(ping_frame,devicet,*types,command=update)
devicet_dropbox.place(relx=0.275, rely=-0.335,anchor='nw')

# Host Name Input
hostn=StringVar()
hostn.set('')
hostn_lable=Label(ping_frame,text='Host Name',font=('arial',12,'bold'),fg='white',bg='#2B3D51',width=13)
hostn_lable.grid(row=3,column=0,padx=0,pady=0)
hostn_textbox=Entry(ping_frame,font=('arial',12),bg='#DFEBF8',textvariable=hostn,width=20,bd=5,insertwidth=4)
hostn_textbox.grid(row=3,column=1,padx=10,pady=10)

# IP/Domain Input
ip=StringVar()
ip.set('')
ip_lable=Label(ping_frame,text='Enter IP/Domain ',font=('arial',12,'bold'),fg='white',bg='#2B3D51',width=13)
ip_lable.grid(row=4,column=0,padx=0,pady=0)
ip_textbox=Entry(ping_frame,font=('arial',12),bg='#DFEBF8',textvariable=ip,width=20,bd=5,insertwidth=4)
ip_textbox.grid(row=4,column=1,padx=0,pady=0)

# Number of Packets Selection
numpack= StringVar()
numpack.set('4')
numpack_lable=Label(ping_frame,text='No of packet ',font=('arial',12,'bold'),fg='white',bg='#2B3D51',width=13)
numpack_lable.grid(row=4,column=2,padx=0,pady=0)

num=['1','2','3','4','5','6','7','8','9','10']
numpack_dropbox=OptionMenu(ping_frame,numpack,*num)
numpack_dropbox.grid(row=4,column=3,padx=0,pady=0)

# Add Button
add_icon=PhotoImage(file='add.png')
add_button=Button(ping_frame,image=add_icon,command=add_valid_ip_domain,fg= 'white',bg='#ffffff',padx=10,pady=20)
add_button.place(y=50,relx=0.61, rely=0.450,anchor='ne')

# Scan Button
scan_icon=PhotoImage(file='ip_domain.png')
scan_button=Button(ping_frame,image=scan_icon,command=check_valid_ip_domain,fg='white',bg='#ffffff',padx=10,pady=20)
scan_button.place(x=0,y=50,relx=1.001, rely=0.450,anchor='ne')

# Function to Display Information About Ping
def ping_info():
    msg.showinfo("About ping","Ping is a network diagnostic tool used to test the reachability of a host on a network. "
        "It measures the time it takes for a packet of data to travel from your device to the target host "
        "and back.\n\n"
        "Key Points:\n"
        "- Function: Sends ICMP echo requests and waits for replies.\n"
        "- Usage: Helps determine if a device is online and how quickly it responds.\n\n"
        "Importance:\n"
        "- Network Troubleshooting: Identifies connectivity issues.\n"
        "- Performance Testing: Measures round-trip time and packet loss.")

piinfo_photo=PhotoImage(file='info.png')
piinfo_button=Button(ping_frame,image=piinfo_photo,command=ping_info)
piinfo_button.place(relx=0.1,rely=1.2,anchor='ne')

########################################################################################################################

# Button to Display All Device Records from the Database
view_image=PhotoImage(file='view.png')
view_button=Button(window,image=view_image,command=viewip,padx=10,pady=20)
view_button.place(relx=0.165,rely=0.586,anchor='center')

# Button to check the status of all devices
mul_image=PhotoImage(file='pingall.png')
mul_check_button=Button(window,image=mul_image,command=checkall,padx=10,pady=20)
mul_check_button.place(relx=0.3, rely=0.586,anchor='center')

# Input for entering Device ID
id=StringVar()
id.set('')
id_lable=Label(window,text='Enter ID ',font=('arial',12,'bold'),fg='#2B3D51',width=7)
id_lable.place(relx=0.04, rely=0.615)
id_textbox=Entry(window,font=('arial',12),bg='#DFEBF8',textvariable=id,width=15,bd=5,insertwidth=4)
id_textbox.place(relx=0.1, rely=0.615)

# Button to scan for the specified device in the database.
scanid_icon=PhotoImage(file='id.png')
scanid_button=Button(window,image=scanid_icon,command=idscan,fg='white',bg='#ffffff')
scanid_button.place(relx=0.1, rely=0.660)

# Button to Removes a device from the database using the ID.
remove_icon=PhotoImage(file='remove.png')
remove_button=Button(window,image=remove_icon,command=removeip,font=('arial',15,'bold'),fg='white',bg='#ffffff')
remove_button.place(relx=0.2, rely=0.660)

# Button to check network status
status_button=Button(window,text="Network Status",command=show_netconfig,font=('arial',11,'bold'),fg='white',bg='#93D9FF')
status_button.place(relx=0.01, rely=0.01)

# Button to check network speed
speed_button=Button(window,text="Network Speed",command=show_speedtest,font=('arial',11,'bold'),fg='white',bg='#93D9FF')
speed_button.place(relx=0.11, rely=0.01)

# Button to install speed test CLI
install_image=PhotoImage(file='install.png')
installspeed_button=Button(window,image=install_image,command=installsp)
installspeed_button.place(relx=0.200, rely=0.01,anchor='nw')

# Button to uninstall speed test CLI
uninstall_image=PhotoImage(file='uninstall.png')
uninstallspeed_button=Button(window,image=uninstall_image,command=uninstallsp)
uninstallspeed_button.place(relx=0.224, rely=0.01,anchor='nw')

######################################### Trace Frame ##################################################################

# Frame for Traceroute Scanner
trace_frame=Frame(window,bg='#2B3D51',bd=10,relief=RAISED,padx=10,pady=68)
trace_frame.place(relx=0,rely=0.9,x=10,y=73,anchor='sw')

# Label for Traceroute Scanner
trace_label=Label(window,text='Traceroute Scanner',font=('arial',14,'bold'),fg='white',bg='red',relief='raised',width=20)
trace_label.place(relx=0.060,rely=0.75,anchor='sw')

# Input for IP/Domain
trace_ip=StringVar()
trace_ip.set('')
trace_ip_lable=Label(trace_frame,text='Enter IP/Domain ',font=('arial',12,'bold'),fg='white',bg='#2B3D51',width=13)
trace_ip_lable.grid(row=4,column=0,padx=0,pady=0)
trace_ip_textbox=Entry(trace_frame,font=('arial',12),bg='#DFEBF8',textvariable=trace_ip,width=20,bd=5,insertwidth=4)
trace_ip_textbox.grid(row=4,column=1,padx=10,pady=10)

# Button to initiate Traceroute
trace_icon=PhotoImage(file='trace.png')
trace_button=Button(trace_frame,image=trace_icon,command=show_traceroute,padx=10,pady=20)
trace_button.place(x=0,y=0,relx=0.53, rely=1.6,anchor='sw')

# Create a text widget to display the traceroute output
traceroute_output = Text(window, wrap='word', font=('arial', 10 ,'bold'), fg='white', bg='#000000',bd=5, height=12, width=50)
traceroute_output.place(relx=0.420,rely=0.862, anchor='center')
traceroute_output.config(state='disabled')

# Function to display information about the Traceroute tool and its uses
def trace_info():
    msg.showinfo("About Traceroute","Traceroute (tracert) is a diagnostic tool used to find the path that data packets "
        "travel from one device to another on the internet. "
        "It helps identify the route and measure transit delays of packets across a network.\n\n"
        "Common Uses:\n"
        "- Network Troubleshooting\n"
        "- Performance Analysis\n"
        "- Routing Issues\n\n"
        "Limitations:\n"
        "- Some routers may not respond to traceroute requests.\n"
        "- Firewalls might block ICMP packets.")

# Button to show Traceroute info
tinfo_photo=PhotoImage(file='info.png')
tinfo_button=Button(trace_frame,image=tinfo_photo,command=trace_info)
tinfo_button.place(relx=0.1,rely=1.55,anchor='sw')

############################################### Port Scan ##############################################################
# Frame for Port Scanner
port_frame =Frame(window, bg='#2B3D51',bd=10,relief=RAISED, padx=20, pady=53)
port_frame.place(relx=0.992, rely=0.992, anchor='se')

# Label for Port Scanner
port_scanner=Label(window,text='Port scanner',font=('arial',14,'bold'),fg='white',bg='red',relief='raised',width=20)
port_scanner.place(x=0,y=0,relx=0.950,rely=0.75,anchor='se')

# Input for IP address
portip=StringVar()
portip.set('')
portip_lable=Label(port_frame,text='Enter IP ',font=('arial',14,'bold'),fg='white',bg='#2B3D51',width=10)
portip_lable.grid(row=0,column=0,padx=0,pady=0)
portip_textbox=Entry(port_frame,font=('arial',12),bg='#DFEBF8',textvariable=portip,bd=5,insertwidth=4,width=16)
portip_textbox.grid(row=0,column=1,padx=0,pady=10)

# Input for Port Range
portnu=StringVar()
portnu.set('')
portnu_lable=Label(port_frame,text='Port Range:',font=('arial',14,'bold'),fg='white',bg='#2B3D51',width=13)
portnu_lable.grid(row=12,column=0,padx=0,pady=0)

# From Port
fp=StringVar()
fp.set('From')
fp_textbox=Entry(port_frame,font=('arial',12),bg='#DFEBF8',textvariable=fp,width=7,bd=5,insertwidth=4)
fp_textbox.place(relx=0.75, rely=1,anchor='se')

# To Port
tp=StringVar()
tp.set('To')
tp_textbox=Entry(port_frame,font=('arial',12),bg='#DFEBF8',textvariable=tp,bd=5,width=7,insertwidth=4)
tp_textbox.place(relx=1, rely=1,anchor='se')

# Button to start port scanning
portsc_im=PhotoImage(file='port.png')
portsc_button=Button(port_frame,image=portsc_im,command=show_portscan)
portsc_button.place(x=0,y=0,relx=1.022, rely=1.6,anchor='se')

# Create a text widget to display the port output
portscan_output = Text(window, wrap='word', font=('arial', 12 ,'bold'), fg='white', bg='#000000',bd=6, height=10.1, width=24)
portscan_output.place(relx=0.640, rely=0.86, anchor='center')
portscan_output.config(state='disabled')

# Function to show information about ports
def port_info():
    msg.showinfo("About Port","A port number is a numerical unique number in networking that identifies a specific process or service on a device. \n"
                        "Port Range :  0 to 65535. \n"
                        "port always function with an IP address \n"
                        "port are essential for communication in TCP/IP Network.")

# Button to display information about ports
pinfo_photo=PhotoImage(file='info.png')
pinfo_button=Button(port_frame,image=pinfo_photo,command=port_info)
pinfo_button.place(relx=0.2,rely=1.58,anchor='se')

################################################## View list ###########################################################
# Frame for viewing device records
view_frame=Frame(window,bd=10, padx=0, pady=0, relief=RAISED,bg='#2B3D51' )
view_frame.place(relx=0.218, rely=0.438, anchor='center')

# Vertical scrollbar
scroll_y = Scrollbar(view_frame, orient=VERTICAL)

# Treeview for displaying device records
tv = ttk.Treeview(view_frame,height=7,columns=(('ID','IP/Domain', 'Device Name', 'Device Type')))

# Configure the scrollbar
scroll_y.pack(side=RIGHT, fill=Y)

# Setting the columns and headings for the Treeview
tv.heading('#1',text='ID')
tv.heading('#2',text='IP/Domaine')
tv.heading('#3',text='Device Name')
tv.heading('#4',text='Device Type')

# Configure column widths
tv.column('#0',width=0,stretch=NO)
tv.column('#1',width=85)
tv.column('#2',width=150)
tv.column('#3',width=150)
tv.column('#4',width=150)

# Pack the Treeview
tv.pack(fill=BOTH, expand=True)

# Link scrollbar to Treeview
scroll_y.config(command=tv.yview)

##################################### Scan results #####################################################################

# Frame for viewing detailed device status
view1_frame = Frame(window, bd=10, relief=RAISED, bg='#2B3D51' )
view1_frame.pack(side=TOP, ipadx=5,ipady=100,anchor='ne')

# Scrollbars
scroll_y = Scrollbar(view1_frame, orient=VERTICAL)
scroll_x = Scrollbar(view1_frame, orient=HORIZONTAL)

# Treeview for displaying detailed device status
tv1 = ttk.Treeview(view1_frame,height=11,columns=('ID','Host Name','Device Type','IP/Domain','Status','RTT','TTL','Packet loss'))

# Configure the scrollbar
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.pack(side=BOTTOM, fill=X)

# Setting the columns and headings for the Treeview
tv1.heading('#1',text='ID')
tv1.heading('#2',text='Host Name')
tv1.heading('#3',text='Device Type')
tv1.heading('#4',text='IP/Domain')
tv1.heading('#5',text='Status')
tv1.heading('#6',text='RTT')
tv1.heading('#7',text='TTL')
tv1.heading('#8',text='Packet Loss')

# Show only headings
tv1['show'] = 'headings'

# Configure column widths
tv1.column('#0',width=0,stretch=NO)
tv1.column('#1',width=77,anchor='center')
tv1.column('#2',width=100,anchor='center')
tv1.column('#3',width=100,anchor='center')
tv1.column('#4',width=160,anchor='center')
tv1.column('#5',width=100,anchor='center')
tv1.column('#6',width=60,anchor='center')
tv1.column('#7',width=60,anchor='center')
tv1.column('#8',width=70,anchor='center')
tv1.rowconfigure

# Pack the Treeview
tv1.pack(fill=BOTH, expand=True)

# Link scrollbars to Treeview
scroll_y.config(command=tv1.yview)
scroll_x.config(command=tv1.xview)

########################################################################################################################

# Buttons for reset
reset_button=Button(window,text='Rest',command=reset,font=('arial',12,'bold'),fg='red',bg='white')
reset_button.place(x=0,y=0,relx=0.92, rely=0.01)

# Buttons for exit
exit_button=Button(window,text='Exit',command=exit,font=('arial',12,'bold'),fg='white',bg='red')
exit_button.place(x=80,y=0,relx=0.9, rely=0.01)


window.mainloop()


# sd-agent-plugins

# ArcconfCLI.py

# GlusterPeerStatus.py
The command "gluster peer status" shows us the connected gluster servers and their state. 
`````
Number of Peers: 2

Hostname: Server1
Uuid: 12345678-1234-4567-89ab-cdefghij0123
State: Peer in Cluster (Connected)

Hostname: Server2
Uuid: 87654321-4321-7654-ba89-985632741abc
State: Peer in Cluster (Connected)
`````

GlusterPeerStatus.py splits the output and outputs it as a json structure. 
`````
"peer-count": 2
"peer-connected-count": 2,
"peer-disconnected-count": 0,
"peer-Server1-state": "Peer in Cluster (Connected)",
"peer-Server2-state": "Peer in Cluster (Connected)"
`````
## Set permissions
Sd-agent needs permission to execute the gluster command. 
Create the file "sd-agent" in the directory "/etc/sudoers.d/" with the content "sd-agent ALL=(ALL) NOPASSWD: /usr/sbin/gluster". 
Then restart the sd-agent - "sudo systemctl restart sd-agent.service".
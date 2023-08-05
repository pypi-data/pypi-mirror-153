# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 13:33:33 2020

@author: butkus
"""
import json
import socket
import time

class UdpLocator:
    """
    Locates Topas4 devices on the same local area network using UDP multicast
    Identifier:
        ALL
        
    """    
    def locate(self, identifier = 'ALL'):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        multicastAddress = ('239.0.0.181', 7415)
        localHostAddress = ('127.255.255.255', 7415) #works as loopback broadcast for reused sockets
        message = (identifier + '?').encode('UTF-8')
        devices = []
        
        # Send data both to multicast address and to localhost
        # localhost is for cases when server and client applications are running on the same PC, and PC might be not connected to the network
        sock.sendto(message, multicastAddress)
        sock.sendto(message, localHostAddress)

        while (True):
            sock.settimeout(2.0)
            sock
            try:
                data, sender = sock.recvfrom(4096)
            except socket.timeout:
                break
            
            try:
                description = json.loads(data.decode('UTF8'))
                description['IpAddress'] = sender[0]
                
                if 'SenderGuid' in description.keys():
                    description['SenderGUID'] = description['SenderGuid']
                    del description['SenderGuid']
                                    
                if 'SenderGUID' in description.keys():
                    devices.append(description)
                    
            except json.decoder.JSONDecodeError:
                print('bad data received by locator')
           
        sock.close()
        seen = set()
        #multiple answers from the same device are possible, and certain if server is located on the same PC
        uniqDevices = [obj for obj in devices if obj['SenderGUID'] not in seen and not seen.add(obj['SenderGUID'])]
                                                   
        return uniqDevices
    
if __name__ == '__main__':
    loc = UdpLocator()
    devs = loc.locate('ALL')

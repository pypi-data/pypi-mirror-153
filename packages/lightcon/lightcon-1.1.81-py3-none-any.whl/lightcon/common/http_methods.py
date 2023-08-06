# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 13:33:33 2020

@author: butkus
"""
import json
import urllib
import urllib.error
import urllib.request
import urllib.parse
import time

class HTTP_methods:    
    def _get (self, command):
        time_init = time.perf_counter()
        try:
            data = json.loads(urllib.request.urlopen(self.url+command).read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_string = e.read().decode('utf-8', 'ignore')
            print (error_string)
            return error_string
        
        if not self.silent:
            print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
        return data
        
    def _put (self, command, data):
        time_init = time.perf_counter()
        try:
            post_url = urllib.request.Request(url=self.url+command, data=data.encode('utf-8'), method='PUT')
    
            post_url.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(post_url) as f:
                pass
            if not self.silent:
                print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
            return f.status            
        except urllib.error.HTTPError as e:
            error_string = e.read().decode('utf-8', 'ignore')
            print (error_string)
            return error_string
        
        if not self.silent:
            print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
        return 200
    
        
    def _post (self, command, details={}):
        time_init = time.perf_counter()
        try:
            post_details = urllib.parse.urlencode(details).encode('UTF-8')
            
            post_url = urllib.request.Request(self.url+command, post_details)
            
            res = urllib.request.urlopen(post_url).read().decode('utf-8', 'ignore')
        except urllib.error.HTTPError as e:
            error_string = e.read().decode('utf-8', 'ignore')
            print (error_string)
            return error_string
        
        if not self.silent:
            print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
        return res
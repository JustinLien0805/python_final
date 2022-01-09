#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 10:33:51 2021

@author: fennieliang
"""

class Data_process: 
    
    def import_data(json_file):
        import json
        data = [json.loads(line) for line in open(json_file, 'r')]

        return data
    
    def db_conn():
        from getpass import getpass
        #getpass will make user's input invisible 
        #but not in the spyder console
         
        import mysql.connector

        mydb = mysql.connector.connect(
  
                    host="localhost",
                    user=input("Enter username: "),
                    password=getpass("Enter password: "),
                    database=input("Enter database:")
        #never hard code your user name and password 
        #in python
        
                ) 
        return (mydb)
 
    def host_conn():
        from getpass import getpass
        #getpass will make user's input invisible 
        #but not in the spyder console
        
        import mysql.connector

        host = mysql.connector.connect(
  
                    host="localhost",
                    user=input("Enter username: "),
                    password=getpass("Enter password: ")
        #never hard code your user name and password 
        #in python
        
                ) 
        return (host)       
            
   
        
#!/usr/bin/env python
# coding: utf-8

# # Run Spectractor from python script
# 
# - author : Sylvie Dagoret-campagne
# - affiliation : IJCLab/IN2P3/CNRS
# - update : September 2021 27 th



import sys

import contextlib
import os

import sys,getopt




if __name__ == "__main__":
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"n:h",['n=','help'])
    except getopt.GetoptError:
        print(' Exception bad getopt with :: '+sys.argv[0]+ ' -n <exposure number>')
        sys.exit(2)
        
   
    num=0

    
    # loop on options and their value
    for opt, arg in opts:


        if opt in ('-h', '--help'):
            print('help for usage : '+sys.argv[0]+ ' -n <exposure number>')
            sys.exit(2)
        elif opt in ('-n', '--number'):
            str_num = arg
            num=int(str_num)

        else:
            print(sys.argv[0]+ ' -n <number>')
            sys.exit(2)
                   
      
    






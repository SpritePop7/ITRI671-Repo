#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 00:55:36 2021

@author: sprite
"""

# Creating the blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify
from flask.wrappers import Request
from flask import request
import qrcode
from PIL import Image
import base64
import pymongo
import bcrypt


# development

# Part 1 - build the blockchain

class Blockchain:
    # needed componenets: genesisblock, chain, createblock, checks

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_Hash='0', hashcode='0', imgQRcode=0, site= "")

    def create_block(self, proof, prev_Hash, hashcode, imgQRcode, site):
        if site == "":
            site = "No URL given"
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'prev_hash': prev_Hash,
            'Data': hashcode,
            'NftRawQR': imgQRcode,
            'site': site
        }
        self.chain.append(block)
        return block


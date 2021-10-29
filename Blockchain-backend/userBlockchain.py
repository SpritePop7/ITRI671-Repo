#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 21:30:36 2021

@author: sprite
"""

import hashlib
import json
from flask import Flask, jsonify
from flask.wrappers import Request
from flask import request
import base64
import bcrypt
import datetime

class userBlockchain:


    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_Hash='0', username="GenesisNull", password=self.hash("GenesisNullPass"))

    def create_block(self, proof, prev_Hash, username, password):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'prev_hash': prev_Hash,
            'username': username,
            'password': password
        }
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]


    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            # this will determine the difficulty of mining(**2 make it harder but still easy)
            hash_operation = hashlib.sha256(
                str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hashString(self, data):
        data = data.encode('utf8')
        
        return str(hashlib.sha256(data).hexdigest())

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


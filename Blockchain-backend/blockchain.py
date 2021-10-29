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

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']

            # must be the same as the proofofwork
            hash_operation = hashlib.sha256(
                str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True
    
    def exists_in_chain(self, chain, checkHash):
        #prev_block = chain[0]
        data = ""
        block_index = 0
        while block_index < len(chain):
            block = chain[block_index]
            if block['Data'] == checkHash:
                data = block['NftRawQR']
                return data
            block_index += 1
        return data



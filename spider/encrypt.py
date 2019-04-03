# coding=utf-8
import base64
import binascii
import codecs
import json
import os

from Crypto.Cipher import AES


# https://github.com/darknessomi/musicbox/wiki/网易云音乐新版WebAPI分析
def aes_encrypt(text, secKey):
    text = json.dumps(text)
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, AES.MODE_CBC, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = str(base64.b64encode(ciphertext))[2:-1]
    return ciphertext


def rsa_encrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(codecs.encode(bytes(text, 'utf8'), encoding='hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def create_secretKey(size):
    return binascii.hexlify(os.urandom(size)).decode()[:16]


def gen_data():
    page = 1
    per_page = 20
    offset = (page - 1) * per_page
    text = {'rid': '', 'offset': offset, 'total': False, 'limit': per_page, 'csrf_token': ''}
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    secKey = create_secretKey(16)
    encText = aes_encrypt(aes_encrypt(text, nonce), secKey)
    encSecKey = rsa_encrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    return data

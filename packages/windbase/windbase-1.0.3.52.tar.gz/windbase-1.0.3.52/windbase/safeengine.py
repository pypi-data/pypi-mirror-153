# /*
#  * @Author: Guofeng He 
#  * @Date: 2022-05-31 22:09:42 
#  * @Last Modified by:   Guofeng He 
#  * @Last Modified time: 2022-05-31 22:09:42 
#  */
#coding=utf-8

'''

'''




import base64
from hashlib import md5
import hmac
import json
import logging
import os
import random
from re import X
import string
import time
from windbase import x25519 

from Crypto.Cipher import AES

class SafeEngine(object):
    '''
    auth_type : hmac(password)  signature(ca)
    #passwords = {node_id:password}
    '''
    def __init__(self,auth_type="hmac",self_key=None,peer_key_handle=None):
        '''
        _summary_

        Args:
            auth_type (str, optional): _description_. Defaults to "hmac".
            private_key (_type_, optional): _description_. Defaults to None.
            peer_key_handle (_type_, optional): get peer key function ,peer_key_handle(src_id),src_id should in message dict . Defaults to None.
        '''
        
        self.auth_type,self._self_key = auth_type,self_key
        self.get_peer_key = peer_key_handle

    def get_peer_key(self,org_id,node_id):
        logging.warning("Should define the get password method")
        return None

    def __ZeroPadding(self,data):
        data += b'\x00'
        while len(data) % 16 != 0:
            data += b'\x00'
        return data

    def __StripZeroPadding(self,data):
        data = data[:-1]
        while len(data) % 16 != 0:
            data = data.rstrip(b'\x00')
            if data[-1] != b"\x00":
                break
        return data

    def encrypt(self,secret:bytes,data:bytes)->bytes:

        aes = AES.new(secret,AES.MODE_ECB)
        return aes.encrypt(self.__ZeroPadding(data))

    def decrypt(self,secret:bytes,encdata:bytes)->bytes:
        aes = AES.new(secret,AES.MODE_ECB)
        return self.__StripZeroPadding(aes.decrypt(encdata))

    @staticmethod
    def create_salt_md5(msg:str)->str:
        '''
        create a message md5 with a salt , to avoid replay

        Args:
            msg (str): message tobe md5

        Returns:
            str: md5 with base64 encode
        '''
        salt = os.urandom(8)
        return base64.b64encode(salt+md5(salt+msg.encode()).digest())
    @staticmethod
    def verify_salt_md5(msg:str,msg_md5:str)->bool:
        '''
        create a message md5 with a salt , to avoid replay

        Args:
            msg (str): message tobe md5

        Returns:
            str: md5 with base64 encode
        '''
        combine = base64.b64decode(msg_md5.encode())
        salt=combine[:8]
        combined_md5 = combine[8:]
        if combined_md5 == md5(salt+msg.encode()).digest():
            return True
        else:
            return False
    @staticmethod
    def create_salt_token(shared_secret:bytes,factor:bytes=b"")->bytes:
        '''
        
        '''
        salt = os.urandom(8)
        hc = hmac.new(shared_secret,digestmod="sha1")
        hc.update(salt+factor)
        return base64.b64encode(salt+hc.digest())

    @staticmethod
    def verify_salt_token(shared_secret:bytes,token:bytes,factor:bytes=b""):
        '''
        
        '''
        combine = base64.b64decode(token)
        salt=combine[:8]
        combined_token = combine[8:]
        hc = hmac.new(shared_secret,digestmod="sha1")
        hc.update(salt+factor)
        if hc.digest()==combined_token:
            return True
        logging.warning("Token verify bad!")
        return False

    def create_token(self,shared_secret,factor=""):
        '''
        if password not provide ,use default password , node use it
        '''
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        timestamp = str(int(time.time()))
        hc = hmac.new(shared_secret,digestmod="sha1")
        hc.update(factor.encode()+salt.encode())
        return salt,timestamp,hc.hexdigest(),     

    def verify_token(self,salt,timestamp,token,shared_secret,factor=""):
        temptoken = hmac.new(shared_secret,factor.encode()+salt.encode(),digestmod="sha1").hexdigest()
        if not hmac.compare_digest(token,temptoken ):
            logging.warning("token verify bad!")
            return False
        return True

    def add_token(self,msg_body):
        shared_secret = self.get_peer_key(msg_body["org_id"],msg_body["dst_id"]).encode()
        salt,timestamp,token = self.create_token(shared_secret,msg_body["node_id"])
        msg_body.update({"salt":salt,"token":token,"timestamp":timestamp})
        return msg_body   

    
    def verify_msg(self,msg_body):
        shared_secret = self.get_peer_key(msg_body["org_id"],msg_body["src_id"]).encode()
        return self.verify_token(msg_body["salt"],msg_body["timestamp"],msg_body["token"],shared_secret,msg_body["node_id"])

class X25519(SafeEngine):
    def __init__(self, auth_type="hmac", self_key=None):
        super().__init__(auth_type, self_key)
        if not self_key:
            self.gen_private_key()
        pass

    def set_private_key(self,private_key):
        self._self_key = private_key

    def gen_private_key(self):
        self._self_key = os.urandom(32)

    def encrypt(self,peer_pub:bytes,data:bytes)->bytes:
        share_secret = self.get_shared_secret(peer_pub)
        return super().encrypt(share_secret,data)


    def decrypt(self,peer_pub:bytes,encdata:bytes)->bytes:
        share_secret = self.get_shared_secret(peer_pub)
        return super().decrypt(share_secret,encdata)


    @property
    def public_key(self):
        '''
        _summary_

        Args:
            encode (str, optional): bin | base64. Defaults to "bin".

        Returns:
            _type_: _description_
        '''

        return X25519.get_public_key(self._self_key,encoding="bin")

    @property
    def public_key_b64(self):
        '''
        _summary_

        Args:
            encode (str, optional): bin | base64. Defaults to "bin".

        Returns:
            _type_: _description_
        '''

        return X25519.get_public_key(self._self_key,encoding="base64")

    @staticmethod
    def get_public_key(private_key,encoding:str="bin"):
        '''
        _summary_

        Args:
            private_key (_type_): _description_
            encoding (str, optional): bin | base64. Defaults to "bin".

        Returns:
            _type_: _description_
        '''
        public_key = x25519.scalar_base_mult(private_key)
    
        return base64.b64encode(public_key) if encoding=="base64" else public_key

    @staticmethod
    def gen_keypair(encoding:str="bin")->bytes:
        '''
        gen x25519 key pair

        Args:
            encode (_type_, optional): bin | base64 . Defaults to bin.

        Returns:
            bytes: _description_
        '''
        private_key = os.urandom(32)
        public_key = x25519.scalar_base_mult(private_key)
        if encoding == "base64":
            return base64.b64encode(private_key),base64.b64encode(public_key)
        return private_key,public_key

    def get_shared_secret(self,peer_public_key):
        return x25519.scalar_mult(self._self_key, peer_public_key)





def main():
    pvk,pbk = X25519.gen_keypair(encoding="base64")
    print(pvk,pbk)


    pass

if __name__ == "__main__":
    main()
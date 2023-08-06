#coding=utf-8

# /*
#  * @Author: Guofeng He 
#  * @Date: 2022-05-31 21:49:39 
#  * @Last Modified by:   Guofeng He 
#  * @Last Modified time: 2022-05-31 21:49:39 
#  */


'''

'''

import base64
import logging
import time
import traceback
from windbase import MsgEngine
from windbase import X25519

SECURE_MSG_FMT={ "selfsign": ["src_id","dst_id","message"],
                "encsign":["src_id","dst_id","message"],
                "sign": ["src_id","dst_id","message"],}

SECURE_MSG_TYPE = {1:"selfsign",2:"encsign",3:"sign",}
SECURE_TAG_NAME={1:"src_id",2:"public_key",3:"message",4:"signature",5:"encmsg",6:"dst_id",7:"time"}
SECURE_TAG_TYPE={1:"str",2:"str",3:"str",4:"str",5:"bytes",6:"str",7:"str"}

class SecureMsg(MsgEngine): 
    def __init__(self,self_key=None,peer_key_handle=None,msg_handles:dict=None) -> None:
        '''
        _summary_

        Args:
            se (SafeEngine): application secure function engine
            msg_handles (dict): dict of handle to msgtype
        '''
        if not self_key:
            self_key,_=X25519.gen_keypair()
        self.se = X25519(self_key=self_key)
        self.get_peer_key = peer_key_handle
        super().__init__(SECURE_MSG_TYPE,msg_handles,tag_names=SECURE_TAG_NAME,tag_types=SECURE_TAG_TYPE)
        pass


    def msg_by_dict(self,msgtype,dictdata):
        return {key: dictdata.get(key,None) for key in SECURE_MSG_FMT[msgtype] }

    def encode(self,msgtype:str,dictdata:dict)->bytes:
        '''
        _summary_

        Args:
            msgtype (str): selfsign|encsign|sign
            dictdata (dict): "src_id","dst_id","message"

        Returns:
            bytes: _description_
        '''

        msg = {key: dictdata[key] for key in SECURE_MSG_FMT[msgtype] }
        if msgtype=="selfsign":
            reqbody = self.self_sign(msg)
        else:
            reqbody = self.add_sign(msg)
        if msgtype=="encsign":
            reqbody = self.encrypt(msg)
            reqbody.pop("message")
        return super().encode(msgtype, reqbody)

    def decode(self,bindata:bytes):
        '''
        _summary_

        Args:
            bindata (bytes): _description_

        Returns:
            msgtype(str),data(dict): 
        '''
        msgtype,msgdict = super().decode(bindata)
        if msgtype=="encsign":
            reqbody = self.decrypt(msgdict)
        if msgtype=="selfsign":
            if self.verify_self_sign(msgdict):
                return msgtype,msgdict
        else:
            if self.verify_sign(msgdict):
                return msgtype,msgdict
        return "",{}

    def encrypt(self,msg_body):
        peer_pubkey = self.get_peer_key(msg_body["dst_id"])
        encdata = self.se.encrypt(peer_pubkey,msg_body["message"].encode())
        msg_body.update({"encmsg":encdata})
        return msg_body

    def decrypt(self,msg_body):
        peer_pubkey = self.get_peer_key(msg_body["src_id"])
        data = self.se.decrypt(peer_pubkey,msg_body["encmsg"])
        msg_body.update({"message":data.decode()})
        return msg_body

    def add_sign(self,msg_body):
        peer_pubkey = self.get_peer_key(msg_body["dst_id"])
        shared_secret = self.se.get_shared_secret(peer_pubkey)
        token = X25519.create_salt_token(shared_secret,(msg_body["message"]+msg_body["src_id"]+msg_body["dst_id"]).encode())
        msg_body.update({"signature":token.decode(),"time":str(time.time())})
        return msg_body   

    def self_sign(self,msg_body:dict):
        peer_pubkey = self.get_peer_key(msg_body["dst_id"])
        shared_secret = self.se.get_shared_secret(peer_pubkey)
        token = X25519.create_salt_token(shared_secret,(msg_body["message"]+msg_body["src_id"]+msg_body["dst_id"]).encode())
        msg_body.update({"signature":token.decode(),"time":str(time.time()),"public_key":self.se.public_key_b64.decode()})
        return msg_body 

    def verify_self_sign(self,msg_body):
        peer_pubkey = base64.b64decode(msg_body["public_key"].encode())
        shared_secret = self.se.get_shared_secret(peer_pubkey)
        return X25519.verify_salt_token(shared_secret,msg_body["signature"],(msg_body["message"]+msg_body["src_id"]+msg_body["dst_id"]).encode())
        
    
    def verify_sign(self,msg_body):
        peer_pubkey = self.get_peer_key(msg_body["src_id"])
        if peer_pubkey:
            shared_secret = self.se.get_shared_secret(peer_pubkey)
            if self.se.verify_salt_token(shared_secret,msg_body["signature"],(msg_body["message"]+msg_body["src_id"]+msg_body["dst_id"]).encode()):
                return True
        # for some self-sign case 
        if "public_key" in msg_body.keys():
            peer_pubkey = base64.b64decode(msg_body["public_key"].encode())
            shared_secret = self.se.get_shared_secret(peer_pubkey)
            return X25519.verify_salt_token(shared_secret,msg_body["signature"],(msg_body["message"]+msg_body["src_id"]+msg_body["dst_id"]).encode())
        return False

    def process(self,bindata,addr,sock):
        if b"" == bindata:
            return
        try:
            msgtype,body = self.decode(bindata)
            logging.debug("received msgtype {} message:\n    {}".format(msgtype,body))
            if  msgtype and self.msghandle.get(msgtype,None):
                self.msghandle[msgtype](body,addr,sock)
            else:
                logging.debug("no message type or not handle for messagetype!")
                return        
        except Exception as exp:
            logging.warning(str(traceback.format_exc()))    




def main():
    pvk1,pbk1 = X25519.gen_keypair()
    pvk2,pbk2 = X25519.gen_keypair()
    peerKey = lambda x: pbk2
    peerKey2 = lambda x: pbk1
    msghandle = {"selfsign":lambda x: print("handle",x)}
    sme = SecureMsg(pvk1,peerKey,msghandle)
    sme2 = SecureMsg(pvk2,peerKey2)
    msg = {"message":"test","src_id":"src","dst_id":"dst"}
    sme.self_sign(msg)
    print(msg)
    print(sme.verify_self_sign(msg))
    msg = {"message":"test","src_id":"src","dst_id":"dst"}
    binmsg = sme.encode("selfsign",msg)
    print(binmsg)
    decodemsg = sme.decode(binmsg)
    print(decodemsg)
    binmsg = sme.encode("sign",msg)
    print(binmsg)
    decodemsg = sme2.decode(binmsg)
    print(decodemsg)
    binmsg = sme.encode("encsign",msg)
    print(binmsg)
    decodemsg = sme2.decode(binmsg)
    print(decodemsg)
    pass

if __name__ == "__main__":
    main()
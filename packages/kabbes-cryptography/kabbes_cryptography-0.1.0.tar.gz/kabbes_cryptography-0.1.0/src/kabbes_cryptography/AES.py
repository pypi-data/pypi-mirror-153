from parent_class import ParentClass
import os
import py_starter as ps
import kabbes_cryptography

from cryptography.hazmat.primitives.ciphers import ( Cipher, algorithms, modes )


class AES( ParentClass ):

    DEFAULT_ATT_VALUES = {
    'key': None,
    'key_bytes': 16,
    'iv': None,
    'iv_bytes': 12,
    'associated_data': "I don't really know what this signature is for".encode( kabbes_cryptography.DEFAULT_ENCODING ),
    'tag': None,
    'encrypted': None,
    }

    def __init__( self, **kwargs):

        ParentClass.__init__( self )

        kwargs = ps.replace_default_kwargs( AES.DEFAULT_ATT_VALUES, **kwargs )
        self.set_atts( kwargs )

    def get_key( self, set = False ):

        key = os.urandom( self.key_bytes )
        if set:
            self.key = key

        return self.key

    def get_iv( self, set = False ):

        iv = os.urandom( self.iv_bytes )
        if set:
            self.iv = iv

        return self.iv

    def prep_for_encrypt( self ):

        if self.key == None:
            self.get_key( set = True )
        if self.iv == None:
            self.get_iv( set = True )

    def encrypt( self, bytes_message ):

        encryptor = Cipher( algorithms.AES(self.key), modes.GCM(self.iv) ).encryptor()
        encryptor.authenticate_additional_data(self.associated_data)
        encrypted = encryptor.update( bytes_message ) + encryptor.finalize()

        self.encrypted = encrypted
        self.tag = encryptor.tag

    def decrypt( self ):

        decryptor = Cipher( algorithms.AES(self.key),  modes.GCM(self.iv, self.tag) ).decryptor()
        decryptor.authenticate_additional_data( self.associated_data )
        decrypted = decryptor.update( self.encrypted ) + decryptor.finalize()
        return decrypted



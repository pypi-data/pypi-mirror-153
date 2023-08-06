from parent_class import ParentClass
import py_starter as ps
import rsa
import kabbes_cryptography

class RSA( ParentClass ):

    DEFAULT_ATT_VALUES = {
    'public_Key': None,
    'private_Key': None,
    'Key_bits': 2048,
    'encrypted': None
    }

    def __init__( self, **kwargs):

        ParentClass.__init__( self )

        kwargs = ps.replace_default_kwargs( RSA.DEFAULT_ATT_VALUES, **kwargs )
        self.set_atts( kwargs )

    def import_private_Key( self, file_Path, set = False ):

        bytes = ps.read_text_file( file_Path.p, mode = 'rb' )
        private_Key = rsa.PrivateKey.load_pkcs1( bytes )
        if set:
            self.set_attr( 'private_Key', private_Key )

        return private_Key

    def import_public_Key( self, file_Path, set = False ):

        bytes = ps.read_text_file( file_Path.p, mode = 'rb' )
        public_Key = rsa.PublicKey.load_pkcs1( bytes )

        if set:
            self.set_attr( 'public_Key', public_Key )

        return public_Key

    def export_private_Key( self, file_Path ):

        self.export_Key( self.private_Key, file_Path )

    def export_public_Key( self, file_Path ):

        self.export_Key( self.public_Key, file_Path )

    def export_Key( self, Key, file_Path ):

        bytes = Key.save_pkcs1()
        if not file_Path.exists():
            ps.write_text_file( file_Path.p, string = bytes, mode = 'wb' )

        else:
            print ('Cannot export Key, Key already exists at ' + str(file_Path))

    def get_new_Keys( self, set = False ):

        public_Key, private_Key = rsa.newkeys( self.Key_bits )

        if set:
            self.public_Key = public_Key
            self.private_Key = private_Key

        return public_Key, private_Key

    def encrypt( self, bytes_message ):

        if self.public_Key != None:
            encrypted = rsa.encrypt( bytes_message, self.public_Key )
            self.encrypted = encrypted

        else:
            print ('Cannot encrypt, no public_Key has been loaded')

    def decrypt( self ):

        if self.private_Key != None:
            decrypted = rsa.decrypt( self.encrypted, self.private_Key )
            return decrypted

        else:
            print ('Cannot decrypt, no private_Key has been loaded')
            return None

from parent_class import ParentClass
import dir_ops as do
import py_starter as ps
import kabbes_cryptography

class Combined( ParentClass ):

    DEFAULT_ATT_VALUES = {
    'enc_aes_key' : None,
    'Dir': None
    }

    IO_FIELDS = [ 'encrypted','enc_aes_key','associated_data','iv','tag' ]

    def __init__( self, RSA_kwargs = {}, AES_kwargs = {}, **kwargs ):

        ParentClass.__init__( self )
        kwargs = ps.replace_default_kwargs( Combined.DEFAULT_ATT_VALUES, **kwargs )

        self.RSA = kabbes_cryptography.RSA( **RSA_kwargs )
        self.AES = kabbes_cryptography.AES( **AES_kwargs )

        self.set_atts( kwargs )


    def encrypt( self, bytes_message ):

        # 1. Get AES key, IV
        self.AES.prep_for_encrypt()

        # 2. Encrypt data with AES
        self.AES.encrypt( bytes_message )
        self.encrypted = self.AES.encrypted
        self.associated_data = self.AES.associated_data
        self.tag = self.AES.tag
        self.iv = self.AES.iv

        # 3. Encrypt the AES key using RSA
        self.RSA.encrypt( self.AES.key )
        self.enc_aes_key = self.RSA.encrypted

        # 4. Export
        self.export_to_Dir()

    def decrypt( self ):

        # 1. import the info from the directory
        self.import_from_Dir()

        # 2. Decrypt the AES key with RSA Private Key
        self.RSA.encrypted = self.enc_aes_key
        self.AES.key = self.RSA.decrypt()

        # 3. Use decrypted AES key to decrypt the message
        self.AES.iv = self.iv
        self.AES.tag = self.tag
        self.AES.associated_data = self.associated_data
        self.AES.encrypted = self.encrypted
        decrypted = self.AES.decrypt()

        return decrypted


    def import_from_Dir( self ):

        for field in self.IO_FIELDS:
            P = do.Path( self.Dir.join( field + '.txt' ) )

            if P.exists():
                bytes = ps.read_text_file( P.path, mode = 'rb' )
                self.set_attr( field, bytes )

            else:
                print ('Path ' + str(P) + ' does not exist')
                return

    def export_to_Dir( self ):

        for field in self.IO_FIELDS:
            P = do.Path( self.Dir.join( field + '.txt' ) )

            if self.has_attr( field ):
                
                bytes = self.get_attr( field )
                ps.write_text_file( P.path, string = bytes, mode = 'wb' )

            else:
                print ('Field ' + field + ' does not exist')
                return


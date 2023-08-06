[GitHub Pages](https://jameskabbes.github.io/cryptography)<br>
[PyPI](https://pypi.org/project/kabbes-cryptography)

# cryptography
Easy implementation of professional Python cryptography packages

<br> 

# Installation
`pip install kabbes_cryptography`


<br>

# Usage
For more in-depth documentation, read the information provided on the Pages. Or better yet, read the source code.

```python
import kabbes_cryptography as kcryp
import dir_ops as do
```

## RSA

```python
# Initializing RSA tokens
RSA_inst = kcryp.RSA()
RSA_inst.get_new_Keys( set = True )
RSA_inst.export_public_Key( do.Path( 'publickey' ) )
RSA_inst.export_private_Key( do.Path( 'privatekey' ) )
```

```python
#Encryption with RSA
RSA_inst.encrypt( bytes('test', encoding = 'utf-8') )
print (RSA_inst.encrypted)
```

```
>>> b'nb\\\x02|:M\x82\x8a\xe1\xc7U\xfd\x1e\xc5O\xcc\x7f\x06\xc2~\xaf\x85"\ -- ETC -- '
```

```python
#Decryption with RSA
dec_message = RSA_inst.decrypt()
print (dec_message.decode( 'utf-8' ))
```

```
>>> 'test'
```

## AES
```python
# Initializing AES
AES_inst = kcryp.AES()
AES_inst.prep_for_encrypt()
```

```python
AES_inst.encrypt( bytes('test', encoding = 'utf-8') )
print (AES_inst.encrypted)
```
```
>>> b'\xd1\xf8\x0b='
```
```python
dec_message = AES_inst.decrypt()
print (dec_message.decode( 'utf-8' ))
```
```
>>> 'test'
```

## Combined

```python
# Initializing Combined
Combined_inst = kcryp.Combined( Dir = do.Dir( do.get_cwd() ).join_Dir( path = 'CombinedEncryption' ) )
Combined_inst.RSA.import_private_Key( do.Path( 'privatekey' ), set=True )
Combined_inst.RSA.import_public_Key( do.Path( 'publickey' ), set=True )
```

```python
Combined_inst.encrypt( bytes('test', encoding = 'utf-8' ) )
print (Combined_inst.encrypted)
```

```
>>> b'\xdeA\xe7\x1e'
```

```python
dec_message = Combined_inst.decrypt()
print (dec_message.decode( 'utf-8 '))
```

```
>>> 'test'
```

<br>

# Author
James Kabbes

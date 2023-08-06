This is a simple script for encrypting and decryption file by chunk using `cryptography` package, decryption includes download from url.
Project repository url is not yet available, mostly because of its inactive development status.

Encrypting files:
```python
from chunkcrypt.cryptchunk import encrypt_file
# encrypt_file(key, file, output_file, chunk_size)

# encrypting without a provided key
encrypt_file(None, '/home/user/myfile.txt', '/home/user/encryfile.txt')
# "myfile.txt" is now encrypted and the encrypted file is located at "/home/user/encrytfile.txt"

# encrypting with a provided key
encrypt_file('CemuWNzkXti7OVAmFV0SIpZAxkF2wybK', '/home/user/myfile.txt', '/home/user/encrytfile.txt')

# specifying a chunksize, default is 1024
encrypt_file(None, '/home/user/myfile.txt', '/home/user/encryfile.txt', 2048)
# the length of bytes of a encrypted chunk is also written on the encrypted file on a 4 element array of bytes format
# this is needed since Fernet returns additional bytes whenever it encrypted data
```

Decrypting files:
```python
from chunkcrypt.cryptchunk import decrypt_file, downl_decrypt
# decrypt_file(key, encrypted_file, output_file)
# downl_decrypt(url, output_file, key, silent=True,  pre='', suff='', msg_v='')
# decryption can also be done on file encrypted using encrypt_file()

# decrypting a file
decrypt_file('CemuWNzkXti7OVAmFV0SIpZAxkF2wybK', '/home/user/encrytfile.txt', '/home/user/decryptfile.txt')

# decrypting from url, only works on direct download link or hotlink
downl_decrypt('https://sampledownl.com/download/encryptedfile.txt', '/home/user/decryptfile.txt', 'CemuWNzkXti7OVAmFV0SIpZAxkF2wybK')

# decrypting from url, with message
downl_decrypt(
    'https://sampledownl.com/download/encryptedfile.txt', 
    '/home/user/decryptfile.txt', 
    'CemuWNzkXti7OVAmFV0SIpZAxkF2wybK',
    False,
    ' * ',
    ' - Test',
    'MyFile'
)
# Output:
#  * Attempting to Download MyFile - Test
#  * Finished Downloading MyFile - Test
#  * Attempting to Decrypt Downloaded MyFile. Please wait, this might take a while depending on the size of file - Test
#  * Finished decrypting MyFile - Test
```
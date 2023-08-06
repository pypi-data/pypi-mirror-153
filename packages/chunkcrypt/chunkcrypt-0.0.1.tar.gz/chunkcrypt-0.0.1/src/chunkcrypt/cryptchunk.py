from cryptography.fernet import Fernet
from tempfile import TemporaryFile
from io import BytesIO
import requests
from math import floor

class InMemFile(BytesIO):
    def read(self, arg):
        return self.read1(arg)

    def __getattr__(self, name):
        return getattr(self, name)()

def encrypt_file(fer_key, in_path, out_path, def_ch=1024):
    fer_key = fer_key if isinstance(fer_key, str) else str(Fernet.generate_key(), 'utf-8')
    fer_obj = Fernet(fer_key)
    if def_ch > 3221225472:
        raise ValueError(f'This {def_ch} chunk size might be too large, please use below 3gb')
    with open(in_path, 'rb') as in_file, open(out_path, 'ab') as out_file:
        while rd_chk := in_file.read(def_ch):
            enc_chk = fer_obj.encrypt(rd_chk)
            ar_enc = len(enc_chk).to_bytes(4, 'big')
            out_file.write(ar_enc)
            out_file.write(enc_chk)
    return fer_key

def chk_decrypt(fer_obj, in_file, out_file, silent=True, pre='', suff='', msg_v=''):
    if not silent:
        print(f'{pre}Attempting to Decrypt Downloaded {msg_v}. Please wait, this might take a while depending on the size of file{suff}')
    while ar_enc := in_file.read(4):
        lengt_enc = int.from_bytes(ar_enc, 'big')
        dec_chk = fer_obj.decrypt(in_file.read(lengt_enc))
        out_file.write(dec_chk)
    if not silent:
        print(f'{pre}Finished decrypting {msg_v}{suff}')

def decrypt_file(fer_key, in_path, out_path):
    fer_obj = Fernet(fer_key)
    with open(in_path, 'rb') as in_file, open(out_path, 'ab') as out_file:
        chk_decrypt(fer_obj, in_file, out_file)

def downl_decrypt(dl_url, out_path, fer_key, silent=True, pre='', suff='', msg_v=''):
    fer_obj = Fernet(fer_key)
    with requests.get(dl_url, stream=True) as dl_cont, open(out_path, 'ab') as out_file:
        if not 'content-length' in dl_cont.headers:
            raise KeyError('\"content-length\" didn\'t found')
        total_sz = int(dl_cont.headers['content-length'])
        if not silent:
            print(f'{pre}Attempting to Download {msg_v}{suff}')
        if total_sz > 1048576:
            with TemporaryFile(mode='w+b') as temp_file:
                chk_sz = 1024
                total_dl = 0
                for dl_chunk in dl_cont.iter_content(chk_sz):
                    total_dl += len(dl_chunk)
                    per_dl = round((total_dl / total_sz) * 100, 2) if total_dl < total_sz else 100
                    if not silent:
                        print(f'{pre}Downloaded Progress: {per_dl}% {suff}    ', end='\r')
                    temp_file.write(dl_chunk)
                if not silent:
                    print('\n', end='\r')
                temp_file.seek(0)
                chk_decrypt(fer_obj, temp_file, out_file, silent, pre, suff, msg_v)
        else:
            with InMemFile(dl_cont.content) as in_mem:
                if not silent:
                    print(f'{pre}Finished Downloading{suff}')
                chk_decrypt(fer_obj, in_mem, out_file, silent, pre, suff, msg_v)

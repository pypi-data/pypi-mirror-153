import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import b2a_hex, a2b_hex
from base64 import b64encode, b64decode

BLOCK_SIZE = 16


def encrypt(data: bytes, key: str = None, mode=AES.MODE_ECB, block_size=BLOCK_SIZE):
    """
    按照给定的秘钥 AES 加密data
    :param data: 内容的字节流
    :param key:  秘钥
    :param mode: AES 加密类型
    :param block_size: 加密长度 It must be 16, 24 or 32 bytes long (respectively for *AES-128*,
        *AES-192* or *AES-256*)
    :return:
    """
    assert key is not None and len(key.strip()) > 0, "加密秘钥 key 不能 None 或者空字符"

    data = pad(data, block_size)
    key = pad(key.encode(encoding='utf-8'), block_size)

    cipher = AES.new(key, mode)
    # 为了避免结果直接保存出现编码转换问题，这里选择转换成hex来存
    return b2a_hex(cipher.encrypt(data))


def encrypt_file(file_path: str, key=None):
    """
    返回给定文件的加密内容，用户拿到之后可以按照自己的喜好保存
    :param file_path: 要加密的文件路径
    :param key: 加密秘钥
    :return: 加密后的文件内容的字节流
    """
    assert key is not None and len(key.strip()) > 0, "加密秘钥 key 不能 None 或者空字符"
    return encrypt(open(file_path, mode='rb').read(), key)


def decrypt(encrypted_data: bytes, key: str = None, mode=AES.MODE_ECB, block_size=BLOCK_SIZE):
    # 吧16进制转成2进制再处理
    assert key is not None and len(key.strip()) > 0, "加密秘钥 key 不能 None 或者空字符"

    key = pad(key.encode(encoding='utf-8'), block_size)
    cipher = AES.new(key, mode)

    encrypted_data = a2b_hex(encrypted_data)
    return unpad(cipher.decrypt(encrypted_data), block_size)


def md5(text: str, encoding="utf-8"):
    return hashlib.md5(text.encode(encoding)).hexdigest()


if __name__ == '__main__':
    pass
    # key = "shirkhan"
    # txt = b'hello world'
    # enc = encrypt(txt, key)
    # print(enc)
    # print(encrypt(txt, key))
    # print(decrypt(enc,key).decode())

    # path = './shir_encryption.py'
    # print(encrypt_file(path, key))

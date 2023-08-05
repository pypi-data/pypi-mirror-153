from os import urandom as os_urandom
from base64 import b64encode as base64_encode, b64decode as base64_decode
from random import choice as random_choice
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class Crypt:
    IV_START_VALUES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] # a = 1, b = 2..., A = 9, B = 10..., and etc.
    KEY_LENGTH = 32 # Not used in this class (only in BC Time), but leaving it here for information sake.
    IV_LENGTH = 16

    key = None
    data = None

    def __init__(self, key=None, data=None) -> None:
        self.key = key
        self.data = data

    def encrypt(self) -> str:
        if not self.__validate_data():
            return None
        iv, iv_start, iv_end = self.__get_iv_and_start_and_end()
        padder = padding.PKCS7(128).padder()
        data_to_encrypt = padder.update(str.encode(self.data)) + padder.finalize()
        key = str.encode(self.key)
        iv = str.encode(iv)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data_to_encrypt) + encryptor.finalize()
        encrypted_data = str(base64_encode(encrypted_data), 'utf-8')
        encrypted_data, equal_signs_count = self.__strip_equal_signs(encrypted_data)
        encrypted_data = iv_start + encrypted_data + iv_end + '='*equal_signs_count # This might result in no equal signs appended.
        return encrypted_data

    def decrypt(self) -> str:
        if not self.__validate_data():
            return None
        iv, encrypted_data = self.__extract_iv()
        if not iv or not encrypted_data:
            return None
        encrypted_data = base64_decode(encrypted_data)
        key = str.encode(self.key)
        iv = str.encode(iv)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        return str(decrypted_data, 'utf-8')

    def __extract_iv_start_length(self: str) -> tuple[int, str]:
        first_char = self.data[:1]
        if first_char not in self.IV_START_VALUES:
            return None, None
        encrypted_data = self.data[1:]
        iv_start_length = self.IV_START_VALUES.index(first_char) + 1
        return iv_start_length, encrypted_data

    def __extract_iv(self) -> tuple[str, str]:
        iv_start_length, encrypted_data = self.__extract_iv_start_length()
        if not iv_start_length or not encrypted_data:
            return None, None
        iv_end_length = self.IV_LENGTH - iv_start_length
        encrypted_data, equal_signs_count = self.__strip_equal_signs(encrypted_data)
        iv = encrypted_data[:iv_start_length]
        encrypted_data = encrypted_data[iv_start_length:]
        if iv_end_length > 0:
            iv += encrypted_data[iv_end_length*-1:]
        encrypted_data_length = len(encrypted_data)
        encrypted_data = encrypted_data[:encrypted_data_length - iv_end_length]
        encrypted_data += '='*equal_signs_count # This might result in no equal signs appended.
        if len(iv) != self.IV_LENGTH:
            return None, None
        return iv, encrypted_data

    def __strip_equal_signs(self, encrypted_data: str) -> tuple[str, int]:
        equal_signs_count = 0
        encrypted_data_length = len(encrypted_data)
        while encrypted_data[encrypted_data_length - 1] == '=':
            encrypted_data = encrypted_data[:encrypted_data_length - 1]
            encrypted_data_length = len(encrypted_data)
            equal_signs_count += 1
        return encrypted_data, equal_signs_count

    def __validate_data(self) -> bool:
        if not self.key or not self.data:
            return False
        return len(self.data) > self.IV_LENGTH

    def __get_iv_and_start_and_end(self) -> tuple[str, str, str]:
        iv = self.__get_random_iv()
        start_length = self.__get_random_iv_start_length()
        start = self.IV_START_VALUES[start_length - 1] + iv[:start_length]
        end = iv[start_length:]
        return iv, start, end

    def __get_random_iv(self) -> str:
        iv = base64_encode(os_urandom(24)).decode('utf-8')
        for search_value in ['+', '/']:
            iv = iv.replace(search_value, '')
        iv = iv[:self.IV_LENGTH]
        return iv if len(iv) == self.IV_LENGTH else None

    def __get_random_iv_start_length(self):
        start_value = random_choice(self.IV_START_VALUES)
        return self.IV_START_VALUES.index(start_value) + 1
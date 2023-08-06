#
# Author: Carles Mateo
#

import hashlib


class HashUtils:

    def hash_string_as_hexadecimal(self, s_text, i_last_chars=2):
        """
        Returns the MD5 representation of a utf-8 String in Hexadecimal String format.
        It outputs exact the same as Linux command md5sum:
        echo -n "Hello World" | md5sum
        or
        printf "Hello World" | md5sum
        :param s_text:
        :return: Boolean for Success, Hexadecimal Hash, the last characters from the hash (used for sharding)
        """

        b_success = True
        s_last_chars = ""
        s_hexadecimal = ""

        try:
            s_ascii = s_text.encode('utf-8')
            o_md5 = hashlib.md5(s_ascii)
            s_hexadecimal = o_md5.hexdigest()
            s_last_chars = s_hexadecimal[-i_last_chars:]
        except:
            b_success = False

        return b_success, s_hexadecimal, s_last_chars

from typing import Optional
from OpenSSL import SSL

# https://testssl.sh/openssl-iana.mapping.html
ciphersuite_names = {
    1: "NULL-MD5",
    2: "NULL-SHA",
    3: "EXP-RC4-MD5",
    4: "RC4-MD5",
    5: "RC4-SHA",
    6: "EXP-RC2-CBC-MD5",
    7: "IDEA-CBC-SHA",
    8: "EXP-DES-CBC-SHA",
    9: "DES-CBC-SHA",
    10: "DES-CBC3-SHA",
    11: "EXP-DH-DSS-DES-CBC-SHA",
    12: "DH-DSS-DES-CBC-SHA",
    13: "DH-DSS-DES-CBC3-SHA",
    14: "EXP-DH-RSA-DES-CBC-SHA",
    15: "DH-RSA-DES-CBC-SHA",
    16: "DH-RSA-DES-CBC3-SHA",
    17: "EXP-EDH-DSS-DES-CBC-SHA",
    18: "EDH-DSS-DES-CBC-SHA",
    19: "EDH-DSS-DES-CBC3-SHA",
    20: "EXP-EDH-RSA-DES-CBC-SHA",
    21: "EDH-RSA-DES-CBC-SHA",
    22: "EDH-RSA-DES-CBC3-SHA",
    23: "EXP-ADH-RC4-MD5",
    24: "ADH-RC4-MD5",
    25: "EXP-ADH-DES-CBC-SHA",
    26: "ADH-DES-CBC-SHA",
    27: "ADH-DES-CBC3-SHA",
    30: "KRB5-DES-CBC-SHA",
    31: "KRB5-DES-CBC3-SHA",
    32: "KRB5-RC4-SHA",
    33: "KRB5-IDEA-CBC-SHA",
    34: "KRB5-DES-CBC-MD5",
    35: "KRB5-DES-CBC3-MD5",
    36: "KRB5-RC4-MD5",
    37: "KRB5-IDEA-CBC-MD5",
    38: "EXP-KRB5-DES-CBC-SHA",
    39: "EXP-KRB5-RC2-CBC-SHA",
    40: "EXP-KRB5-RC4-SHA",
    41: "EXP-KRB5-DES-CBC-MD5",
    42: "EXP-KRB5-RC2-CBC-MD5",
    43: "EXP-KRB5-RC4-MD5",
    44: "PSK-NULL-SHA",
    45: "DHE-PSK-NULL-SHA",
    46: "RSA-PSK-NULL-SHA",
    47: "AES128-SHA",
    48: "DH-DSS-AES128-SHA",
    49: "DH-RSA-AES128-SHA",
    50: "DHE-DSS-AES128-SHA",
    51: "DHE-RSA-AES128-SHA",
    52: "ADH-AES128-SHA",
    53: "AES256-SHA",
    54: "DH-DSS-AES256-SHA",
    55: "DH-RSA-AES256-SHA",
    56: "DHE-DSS-AES256-SHA",
    57: "DHE-RSA-AES256-SHA",
    58: "ADH-AES256-SHA",
    59: "NULL-SHA256",
    60: "AES128-SHA256",
    61: "AES256-SHA256",
    62: "DH-DSS-AES128-SHA256",
    63: "DH-RSA-AES128-SHA256",
    64: "DHE-DSS-AES128-SHA256",
    65: "CAMELLIA128-SHA",
    66: "DH-DSS-CAMELLIA128-SHA",
    67: "DH-RSA-CAMELLIA128-SHA",
    68: "DHE-DSS-CAMELLIA128-SHA",
    69: "DHE-RSA-CAMELLIA128-SHA",
    70: "ADH-CAMELLIA128-SHA",
    96: "EXP1024-RC4-MD5",
    97: "EXP1024-RC2-CBC-MD5",
    98: "EXP1024-DES-CBC-SHA",
    99: "EXP1024-DHE-DSS-DES-CBC-SHA",
    100: "EXP1024-RC4-SHA",
    101: "EXP1024-DHE-DSS-RC4-SHA",
    102: "DHE-DSS-RC4-SHA",
    103: "DHE-RSA-AES128-SHA256",
    104: "DH-DSS-AES256-SHA256",
    105: "DH-RSA-AES256-SHA256",
    106: "DHE-DSS-AES256-SHA256",
    107: "DHE-RSA-AES256-SHA256",
    108: "ADH-AES128-SHA256",
    109: "ADH-AES256-SHA256",
    128: "GOST94-GOST89-GOST89",
    129: "GOST2001-GOST89-GOST89",
    130: "GOST94-NULL-GOST94",
    131: "GOST2001-GOST89-GOST89",
    132: "CAMELLIA256-SHA",
    133: "DH-DSS-CAMELLIA256-SHA",
    134: "DH-RSA-CAMELLIA256-SHA",
    135: "DHE-DSS-CAMELLIA256-SHA",
    136: "DHE-RSA-CAMELLIA256-SHA",
    137: "ADH-CAMELLIA256-SHA",
    138: "PSK-RC4-SHA",
    139: "PSK-3DES-EDE-CBC-SHA",
    140: "PSK-AES128-CBC-SHA",
    141: "PSK-AES256-CBC-SHA",
    150: "SEED-SHA",
    151: "DH-DSS-SEED-SHA",
    152: "DH-RSA-SEED-SHA",
    153: "DHE-DSS-SEED-SHA",
    154: "DHE-RSA-SEED-SHA",
    155: "ADH-SEED-SHA",
    156: "AES128-GCM-SHA256",
    157: "AES256-GCM-SHA384",
    158: "DHE-RSA-AES128-GCM-SHA256",
    159: "DHE-RSA-AES256-GCM-SHA384",
    160: "DH-RSA-AES128-GCM-SHA256",
    161: "DH-RSA-AES256-GCM-SHA384",
    162: "DHE-DSS-AES128-GCM-SHA256",
    163: "DHE-DSS-AES256-GCM-SHA384",
    164: "DH-DSS-AES128-GCM-SHA256",
    165: "DH-DSS-AES256-GCM-SHA384",
    166: "ADH-AES128-GCM-SHA256",
    167: "ADH-AES256-GCM-SHA384",
    186: "CAMELLIA128-SHA256",
    187: "DH-DSS-CAMELLIA128-SHA256",
    188: "DH-RSA-CAMELLIA128-SHA256",
    189: "DHE-DSS-CAMELLIA128-SHA256",
    190: "DHE-RSA-CAMELLIA128-SHA256",
    191: "ADH-CAMELLIA128-SHA256",
    # 22016: "TLS_FALLBACK_SCSV",
    4865: "TLS_AES_128_GCM_SHA256",
    4866: "TLS_AES_256_GCM_SHA384",
    4867: "TLS_CHACHA20_POLY1305_SHA256",
    4868: "TLS_AES_128_CCM_SHA256",
    4869: "TLS_AES_128_CCM_8_SHA256",
    49153: "ECDH-ECDSA-NULL-SHA",
    49154: "ECDH-ECDSA-RC4-SHA",
    49155: "ECDH-ECDSA-DES-CBC3-SHA",
    49156: "ECDH-ECDSA-AES128-SHA",
    49157: "ECDH-ECDSA-AES256-SHA",
    49158: "ECDHE-ECDSA-NULL-SHA",
    49159: "ECDHE-ECDSA-RC4-SHA",
    49160: "ECDHE-ECDSA-DES-CBC3-SHA",
    49161: "ECDHE-ECDSA-AES128-SHA",
    49162: "ECDHE-ECDSA-AES256-SHA",
    49163: "ECDH-RSA-NULL-SHA",
    49164: "ECDH-RSA-RC4-SHA",
    49165: "ECDH-RSA-DES-CBC3-SHA",
    49166: "ECDH-RSA-AES128-SHA",
    49167: "ECDH-RSA-AES256-SHA",
    49168: "ECDHE-RSA-NULL-SHA",
    49169: "ECDHE-RSA-RC4-SHA",
    49170: "ECDHE-RSA-DES-CBC3-SHA",
    49171: "ECDHE-RSA-AES128-SHA",
    49172: "ECDHE-RSA-AES256-SHA",
    49173: "AECDH-NULL-SHA",
    49174: "AECDH-RC4-SHA",
    49175: "AECDH-DES-CBC3-SHA",
    49176: "AECDH-AES128-SHA",
    49177: "AECDH-AES256-SHA",
    49178: "SRP-3DES-EDE-CBC-SHA",
    49179: "SRP-RSA-3DES-EDE-CBC-SHA",
    49180: "SRP-DSS-3DES-EDE-CBC-SHA",
    49181: "SRP-AES-128-CBC-SHA",
    49182: "SRP-RSA-AES-128-CBC-SHA",
    49183: "SRP-DSS-AES-128-CBC-SHA",
    49184: "SRP-AES-256-CBC-SHA",
    49185: "SRP-RSA-AES-256-CBC-SHA",
    49186: "SRP-DSS-AES-256-CBC-SHA",
    49187: "ECDHE-ECDSA-AES128-SHA256",
    49188: "ECDHE-ECDSA-AES256-SHA384",
    49189: "ECDH-ECDSA-AES128-SHA256",
    49190: "ECDH-ECDSA-AES256-SHA384",
    49191: "ECDHE-RSA-AES128-SHA256",
    49192: "ECDHE-RSA-AES256-SHA384",
    49193: "ECDH-RSA-AES128-SHA256",
    49194: "ECDH-RSA-AES256-SHA384",
    49195: "ECDHE-ECDSA-AES128-GCM-SHA256",
    49196: "ECDHE-ECDSA-AES256-GCM-SHA384",
    49197: "ECDH-ECDSA-AES128-GCM-SHA256",
    49198: "ECDH-ECDSA-AES256-GCM-SHA384",
    49199: "ECDHE-RSA-AES128-GCM-SHA256",
    49200: "ECDHE-RSA-AES256-GCM-SHA384",
    49201: "ECDH-RSA-AES128-GCM-SHA256",
    49202: "ECDH-RSA-AES256-GCM-SHA384",
    49203: "ECDHE-PSK-RC4-SHA",
    49204: "ECDHE-PSK-3DES-EDE-CBC-SHA",
    49205: "ECDHE-PSK-AES128-CBC-SHA",
    49206: "ECDHE-PSK-AES256-CBC-SHA",
    49207: "ECDHE-PSK-AES128-CBC-SHA256",
    49208: "ECDHE-PSK-AES256-CBC-SHA384",
    49209: "ECDHE-PSK-NULL-SHA",
    49210: "ECDHE-PSK-NULL-SHA256",
    49211: "ECDHE-PSK-NULL-SHA384",
    49266: "ECDHE-ECDSA-CAMELLIA128-SHA256",
    49267: "ECDHE-ECDSA-CAMELLIA256-SHA38",
    49268: "ECDH-ECDSA-CAMELLIA128-SHA256",
    49269: "ECDH-ECDSA-CAMELLIA256-SHA384",
    49270: "ECDHE-RSA-CAMELLIA128-SHA256",
    49271: "ECDHE-RSA-CAMELLIA256-SHA384",
    49272: "ECDH-RSA-CAMELLIA128-SHA256",
    49273: "ECDH-RSA-CAMELLIA256-SHA384",
    49300: "PSK-CAMELLIA128-SHA256",
    49301: "PSK-CAMELLIA256-SHA384",
    49302: "DHE-PSK-CAMELLIA128-SHA256",
    49303: "DHE-PSK-CAMELLIA256-SHA384",
    49304: "RSA-PSK-CAMELLIA128-SHA256",
    49305: "RSA-PSK-CAMELLIA256-SHA384",
    49306: "ECDHE-PSK-CAMELLIA128-SHA256",
    49307: "ECDHE-PSK-CAMELLIA256-SHA384",
    49308: "AES128-CCM",
    49309: "AES256-CCM",
    49310: "DHE-RSA-AES128-CCM",
    49311: "DHE-RSA-AES256-CCM",
    49312: "AES128-CCM8",
    49313: "AES256-CCM8",
    49314: "DHE-RSA-AES128-CCM8",
    49315: "DHE-RSA-AES256-CCM8",
    49316: "PSK-AES128-CCM",
    49317: "PSK-AES256-CCM",
    49318: "DHE-PSK-AES128-CCM",
    49319: "DHE-PSK-AES256-CCM",
    49320: "PSK-AES128-CCM8",
    49321: "PSK-AES256-CCM8",
    49322: "DHE-PSK-AES128-CCM8",
    49323: "DHE-PSK-AES256-CCM8",
    49324: "ECDHE-ECDSA-AES128-CCM",
    49325: "ECDHE-ECDSA-AES256-CCM",
    49326: "ECDHE-ECDSA-AES128-CCM8",
    49327: "ECDHE-ECDSA-AES256-CCM8",
    52243: "ECDHE-RSA-CHACHA20-POLY1305-OLD",
    52244: "ECDHE-ECDSA-CHACHA20-POLY1305-OLD",
    52245: "DHE-RSA-CHACHA20-POLY1305-OLD",
    52392: "ECDHE-RSA-CHACHA20-POLY1305",
    52393: "ECDHE-ECDSA-CHACHA20-POLY1305",
    52394: "DHE-RSA-CHACHA20-POLY1305",
    52395: "PSK-CHACHA20-POLY1305",
    52396: "ECDHE-PSK-CHACHA20-POLY1305",
    52397: "DHE-PSK-CHACHA20-POLY1305",
    52398: "RSA-PSK-CHACHA20-POLY1305",
    65280: "GOST-MD5",
    65281: "GOST-GOST94",
    65282: "GOST-GOST89MAC",
    65283: "GOST-GOST89STREAM",
    65664: "RC4-MD5",
    131200: "EXP-RC4-MD5",
    196736: "RC2-CBC-MD5",
    262272: "EXP-RC2-CBC-MD5",
    327808: "IDEA-CBC-MD5",
    393280: "DES-CBC-MD5",
    393536: "DES-CBC-SHA",
    458944: "DES-CBC3-MD5",
    459200: "DES-CBC3-SHA",
    524416: "RC4-64-MD5",
    16713728: "DES-CFB-M1",
    16713744: "NULL",
}

tls_13_ciphersuite_names = {
    4865: "TLS_AES_128_GCM_SHA256",
    4866: "TLS_AES_256_GCM_SHA384",
    4867: "TLS_CHACHA20_POLY1305_SHA256",
    4868: "TLS_AES_128_CCM_SHA256",
    4869: "TLS_AES_128_CCM_8_SHA256",
}

def get_cipher_name(num) -> Optional[str]:
    """
    get_get_cipher_name converts ciphersuite number to OpenSSL cipher name string.
    """
    if num in ciphersuite_names:
        return ciphersuite_names[num]


# Stolen from https://github.com/pyca/pyopenssl/pull/963 until it's merged
def set_ciphersuites(self, ciphersuites):
    """
    Set the list of TLS 1.3 ciphersuites to be used in this context.
    See the OpenSSL manual for more information (e.g.
    :manpage:`ciphers(1)`).
    :param bytes ciphersuites: An OpenSSL ciphersuites string.
    :return: None
    """
    ciphersuites = SSL._text_to_bytes_and_warn("ciphersuites", ciphersuites)

    if not isinstance(ciphersuites, bytes):
        raise TypeError("ciphersuites must be a byte string.")

    SSL._openssl_assert(
        SSL._lib.SSL_CTX_set_ciphersuites(self._context, ciphersuites) == 1
    )

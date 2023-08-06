from collections.abc import (
    Mapping,
)
import json
import os
import warnings

from cytoolz import (
    dissoc,
)
from platon_keyfile import (
    create_keyfile_json,
    decode_keyfile_json,
)
from platon_keys import (
    KeyAPI,
    keys,
)
from platon_keys.exceptions import (
    ValidationError,
)
from platon_utils.curried import (
    combomethod,
    hexstr_if_str,
    is_dict,
    keccak,
    text_if_str,
    to_bytes,
    to_int,
)
from hexbytes import (
    HexBytes,
)

from platon_account._utils.legacy_transactions import (
    Transaction,
    vrs_from,
)
from platon_account._utils.signing import (
    hash_of_signed_transaction,
    sign_message_hash,
    sign_transaction_dict,
    to_standard_signature_bytes,
    to_standard_v,
)
from platon_account._utils.typed_transactions import (
    TypedTransaction,
)
from platon_account.datastructures import (
    SignedMessage,
    SignedTransaction,
)
from platon_account.hdaccount import (
    PLATON_DEFAULT_PATH,
    generate_mnemonic,
    key_from_seed,
    seed_from_mnemonic,
)
from platon_account.messages import (
    SignableMessage,
    _hash_eip191_message,
)
from platon_account.signers.local import (
    LocalAccount,
)

DEFAULT_HRP = 'lat'


class Account(object):
    """
    The primary entry point for working with Platon private keys.

    It does **not** require a connection to an Platon node.
    """
    _keys = keys

    _default_kdf = os.getenv('platon_account_KDF', 'scrypt')

    # Enable unaudited features (off by default)
    _use_unaudited_hdwallet_features = False

    @classmethod
    def enable_unaudited_hdwallet_features(cls):
        """
        Use this flag to enable unaudited HD Wallet features.
        """
        cls._use_unaudited_hdwallet_features = True

    @combomethod
    def create(self, extra_entropy='', hrp=DEFAULT_HRP):
        r"""
        Creates a new private key, and returns it as a :class:`~platon_account.local.LocalAccount`.

        :param extra_entropy: Add extra randomness to whatever randomness your OS can provide
        :type extra_entropy: str or bytes or int
        :param str hrp: HRP used to generate the bech32 address
        :returns: an object with private key and convenience methods

        .. code-block:: python

            >>> from platon_account import Account
            >>> acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530', 'lat')
            >>> acct.address
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'
            >>> acct.key
            HexBytes('0x8676e9a8c86c8921e922e61e0bb6e9e9689aad4c99082620610b00140e5f21b8')

            # These methods are also available: sign_message(), sign_transaction(), encrypt()
            # They correspond to the same-named methods in Account.*
            # but without the private key argument
        """
        extra_key_bytes = text_if_str(to_bytes, extra_entropy)
        key_bytes = keccak(os.urandom(32) + extra_key_bytes)
        return self.from_key(key_bytes, hrp)

    @staticmethod
    def decrypt(keyfile_json, password):
        """
        Decrypts a private key.

        The key may have been encrypted using an Platon client or :meth:`~Account.encrypt`.

        :param keyfile_json: The encrypted key
        :type keyfile_json: dict or str
        :param str password: The password that was used to encrypt the key
        :returns: the raw private key
        :rtype: ~hexbytes.main.HexBytes

        .. doctest:: python

            >>> encrypted = {
            ... 'address': '5ce9454909639d2d17a3f753ce7d93fa0b9ab12e',
            ... 'crypto': {'cipher': 'aes-128-ctr',
            ...  'cipherparams': {'iv': '482ef54775b0cc59f25717711286f5c8'},
            ...  'ciphertext': 'cb636716a9fd46adbb31832d964df2082536edd5399a3393327dc89b0193a2be',
            ...  'kdf': 'scrypt',
            ...  'kdfparams': {},
            ...  'kdfparams': {'dklen': 32,
            ...                'n': 262144,
            ...                'p': 8,
            ...                'r': 1,
            ...                'salt': 'd3c9a9945000fcb6c9df0f854266d573'},
            ...  'mac': '4f626ec5e7fea391b2229348a65bfef532c2a4e8372c0a6a814505a350a7689d'},
            ... 'id': 'b812f3f9-78cc-462a-9e89-74418aa27cb0',
            ... 'version': 3}
            >>> Account.decrypt(encrypted, 'password')
            HexBytes('0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364')

        """
        if isinstance(keyfile_json, str):
            keyfile = json.loads(keyfile_json)
        elif is_dict(keyfile_json):
            keyfile = keyfile_json
        else:
            raise TypeError("The keyfile should be supplied as a JSON string, or a dictionary.")
        password_bytes = text_if_str(to_bytes, password)
        return HexBytes(decode_keyfile_json(keyfile, password_bytes))

    @classmethod
    def encrypt(cls, private_key, password, kdf=None, iterations=None):
        """
        Creates a dictionary with an encrypted version of your private key.
        To import this keyfile into Platon clients like gplaton and parity:
        encode this dictionary with :func:`json.dumps` and save it to disk where your
        client keeps key files.

        :param private_key: The raw private key
        :type private_key: hex str, bytes, int or :class:`platon_keys.datatypes.PrivateKey`
        :param str password: The password which you will need to unlock the account in your client
        :param str kdf: The key derivation function to use when encrypting your private key
        :param int iterations: The work factor for the key derivation function
        :returns: The data to use in your encrypted file
        :rtype: dict

        If kdf is not set, the default key derivation function falls back to the
        environment variable :envvar:`platon_account_KDF`. If that is not set, then
        'scrypt' will be used as the default.

        .. doctest:: python

            >>> from pprint import pprint
            >>> encrypted = Account.encrypt(
            ...     0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364,
            ...     'password'
            ... )
            >>> pprint(encrypted)
            {'address': '5ce9454909639d2d17a3f753ce7d93fa0b9ab12e',
             'crypto': {'cipher': 'aes-128-ctr',
                        'cipherparams': {'iv': '...'},
                        'ciphertext': '...',
                        'kdf': 'scrypt',
                        'kdfparams': {'dklen': 32,
                                      'n': 262144,
                                      'p': 8,
                                      'r': 1,
                                      'salt': '...'},
                        'mac': '...'},
             'id': '...',
             'version': 3}

            >>> with open('my-keyfile', 'w') as f: # doctest: +SKIP
            ...    f.write(json.dumps(encrypted))
        """
        if isinstance(private_key, keys.PrivateKey):
            key_bytes = private_key.to_bytes()
        else:
            key_bytes = HexBytes(private_key)

        if kdf is None:
            kdf = cls._default_kdf

        password_bytes = text_if_str(to_bytes, password)
        assert len(key_bytes) == 32

        return create_keyfile_json(key_bytes, password_bytes, kdf=kdf, iterations=iterations)

    @combomethod
    def from_key(self, private_key, hrp=DEFAULT_HRP):
        r"""
        Returns a convenient object for working with the given private key.

        :param private_key: The raw private key
        :type private_key: hex str, bytes, int or :class:`platon_keys.datatypes.PrivateKey`
        :param str hrp: HRP used to generate the bech32 address
        :return: object with methods for signing and encrypting
        :rtype: LocalAccount

        .. doctest:: python

            >>> acct = Account.from_key(
            ... 0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364, 'lat')
            >>> acct.address
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'
            >>> acct.key
            HexBytes('0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364')

            # These methods are also available: sign_message(), sign_transaction(), encrypt()
            # They correspond to the same-named methods in Account.*
            # but without the private key argument
        """
        key = self._parsePrivateKey(private_key)
        return LocalAccount(key, self, hrp)

    @combomethod
    def from_mnemonic(self,
                      mnemonic: str,
                      passphrase: str = "",
                      account_path: str = PLATON_DEFAULT_PATH,
                      hrp: str = DEFAULT_HRP):
        """
        Generate an account from a mnemonic.

        .. CAUTION:: This feature is experimental, unaudited, and likely to change soon

        :param str mnemonic: space-separated list of BIP39 mnemonic seed words
        :param str passphrase: Optional passphrase used to encrypt the mnemonic
        :param str account_path: Specify an alternate HD path for deriving the seed using
            BIP32 HD wallet key derivation.
        :param str hrp: HRP used to generate the bech32 address
        :return: object with methods for signing and encrypting
        :rtype: LocalAccount

        .. doctest:: python

            >>> from platon_account import Account
            >>> Account.enable_unaudited_hdwallet_features()
            >>> acct = Account.from_mnemonic(
            ...  "coral allow abandon recipe top tray caught video climb similar prepare bracket "
            ...  "antenna rubber announce gauge volume hub hood burden skill immense add acid")
            >>> acct.address
            'lat1qntd9mtg5myjlfhcn0pqfwvdfkudus45an7g07k'

            # These methods are also available: sign_message(), sign_transaction(), encrypt()
            # They correspond to the same-named methods in Account.*
            # but without the private key argument
        """
        if not self._use_unaudited_hdwallet_features:
            raise AttributeError(
                "The use of the Mnemonic features of Account is disabled by default until "
                "its API stabilizes. To use these features, please enable them by running "
                "`Account.enable_unaudited_hdwallet_features()` and try again."
            )
        seed = seed_from_mnemonic(mnemonic, passphrase)
        private_key = key_from_seed(seed, account_path)
        key = self._parsePrivateKey(private_key)
        return LocalAccount(key, self, hrp)

    @combomethod
    def create_with_mnemonic(self,
                             passphrase: str = "",
                             num_words: int = 12,
                             language: str = "english",
                             account_path: str = PLATON_DEFAULT_PATH,
                             hrp: str = DEFAULT_HRP):
        r"""
        Create a new private key and related mnemonic.

        .. CAUTION:: This feature is experimental, unaudited, and likely to change soon

        Creates a new private key, and returns it as a :class:`~platon_account.local.LocalAccount`,
        alongside the mnemonic that can used to regenerate it using any BIP39-compatible wallet.

        :param str passphrase: Extra passphrase to encrypt the seed phrase
        :param int num_words: Number of words to use with seed phrase. Default is 12 words.
                              Must be one of [12, 15, 18, 21, 24].
        :param str language: Language to use for BIP39 mnemonic seed phrase.
        :param str account_path: Specify an alternate HD path for deriving the seed using
            BIP32 HD wallet key derivation.
        :param str hrp: HRP used to generate the bech32 address
        :returns: A tuple consisting of an object with private key and convenience methods,
                  and the mnemonic seed phrase that can be used to restore the account.
        :rtype: (LocalAccount, str)

        .. doctest:: python

            >>> from platon_account import Account
            >>> Account.enable_unaudited_hdwallet_features()
            >>> acct, mnemonic = Account.create_with_mnemonic()
            >>> acct.address # doctest: +SKIP
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'
            >>> acct == Account.from_mnemonic(mnemonic)
            True

            # These methods are also available: sign_message(), sign_transaction(), encrypt()
            # They correspond to the same-named methods in Account.*
            # but without the private key argument
        """
        if not self._use_unaudited_hdwallet_features:
            raise AttributeError(
                "The use of the Mnemonic features of Account is disabled by default until "
                "its API stabilizes. To use these features, please enable them by running "
                "`Account.enable_unaudited_hdwallet_features()` and try again."
            )
        mnemonic = generate_mnemonic(num_words, language)
        return self.from_mnemonic(mnemonic, passphrase, account_path, hrp), mnemonic

    @combomethod
    def recover_message(self, signable_message: SignableMessage, vrs=None, signature=None):
        r"""
        Get the address of the account that signed the given message.
        You must specify exactly one of: vrs or signature

        :param signable_message: the message that was signed
        :param vrs: the three pieces generated by an elliptic curve signature
        :type vrs: tuple(v, r, s), each element is hex str, bytes or int
        :param signature: signature bytes concatenated as r+s+v
        :type signature: hex str or bytes or int
        :returns: address of signer, hex-encoded & checksummed
        :rtype: str

        .. doctest:: python

            >>> from platon_account.messages import encode_defunct
            >>> from platon_account import Account
            >>> message = encode_defunct(text="I♥SF")
            >>> vrs = (
            ...   28,
            ...   '0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb3',
            ...   '0x3e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce')
            >>> Account.recover_message(message, vrs=vrs)
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'


            # All of these recover calls are equivalent:

            # variations on vrs
            >>> vrs = (
            ...   '0x1c',
            ...   '0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb3',
            ...   '0x3e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce')
            >>> Account.recover_message(message, vrs=vrs)
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'

            >>> # Caution about this approach: likely problems if there are leading 0s
            >>> vrs = (
            ...   0x1c,
            ...   0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb3,
            ...   0x3e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce)
            >>> Account.recover_message(message, vrs=vrs)
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'

            >>> vrs = (
            ...   b'\x1c',
            ...   b'\xe6\xca\x9b\xbaX\xc8\x86\x11\xfa\xd6jl\xe8\xf9\x96\x90\x81\x95Y8\x07\xc4\xb3\x8b\xd5(\xd2\xcf\xf0\x9dN\xb3',  # noqa: E501
            ...   b'>[\xfb\xbfM>9\xb1\xa2\xfd\x81jv\x80\xc1\x9e\xbe\xba\xf3\xa1A\xb29\x93J\xd4<\xb3?\xce\xc8\xce')  # noqa: E501
            >>> Account.recover_message(message, vrs=vrs)
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'

            # variations on signature
            >>> signature = '0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb33e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce1c'  # noqa: E501
            >>> Account.recover_message(message, signature=signature)
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'
            >>> signature = b'\xe6\xca\x9b\xbaX\xc8\x86\x11\xfa\xd6jl\xe8\xf9\x96\x90\x81\x95Y8\x07\xc4\xb3\x8b\xd5(\xd2\xcf\xf0\x9dN\xb3>[\xfb\xbfM>9\xb1\xa2\xfd\x81jv\x80\xc1\x9e\xbe\xba\xf3\xa1A\xb29\x93J\xd4<\xb3?\xce\xc8\xce\x1c'  # noqa: E501
            >>> Account.recover_message(message, signature=signature)
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'
            >>> # Caution about this approach: likely problems if there are leading 0s
            >>> signature = 0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb33e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce1c  # noqa: E501
            >>> Account.recover_message(message, signature=signature)
            'lat1qtn552jgfvwwj69ar7afuulvnlg9e4vfwq7zpz5'
        """
        message_hash = _hash_eip191_message(signable_message)
        return self._recover_hash(message_hash, vrs, signature)

    @combomethod
    def _recover_hash(self, message_hash, vrs=None, signature=None, hrp=DEFAULT_HRP):
        hash_bytes = HexBytes(message_hash)
        if len(hash_bytes) != 32:
            raise ValueError("The message hash must be exactly 32-bytes")
        if vrs is not None:
            v, r, s = map(hexstr_if_str(to_int), vrs)
            v_standard = to_standard_v(v)
            signature_obj = self._keys.Signature(vrs=(v_standard, r, s))
        elif signature is not None:
            signature_bytes = HexBytes(signature)
            signature_bytes_standard = to_standard_signature_bytes(signature_bytes)
            signature_obj = self._keys.Signature(signature_bytes=signature_bytes_standard)
        else:
            raise TypeError("You must supply the vrs tuple or the signature bytes")
        pubkey = signature_obj.recover_public_key_from_msg_hash(hash_bytes)
        return pubkey.to_bech32_address(hrp)

    @combomethod
    def recover_transaction(self, serialized_transaction, hrp=DEFAULT_HRP):
        """
        Get the address of the account that signed this transaction.

        :param serialized_transaction: the complete signed transaction
        :type serialized_transaction: hex str, bytes or int
        :param str hrp: HRP used to generate the bech32 address
        :returns: address of signer, hex-encoded & checksummed
        :rtype: str

        .. doctest:: python

            >>> raw_transaction = '0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'  # noqa: E501
            >>> Account.recover_transaction(raw_transaction)
            'lat1q936ndcmqtkwpdfar67ccnrjjjwt2vhpreyjucx'
        """
        txn_bytes = HexBytes(serialized_transaction)
        if len(txn_bytes) > 0 and txn_bytes[0] <= 0x7f:
            # We are dealing with a typed transaction.
            typed_transaction = TypedTransaction.from_bytes(txn_bytes)
            msg_hash = typed_transaction.hash()
            vrs = typed_transaction.vrs()
            return self._recover_hash(msg_hash, vrs=vrs)

        txn = Transaction.from_bytes(txn_bytes)
        msg_hash = hash_of_signed_transaction(txn)
        return self._recover_hash(msg_hash, vrs=vrs_from(txn), hrp=hrp)

    def set_key_backend(self, backend):
        """
        Change the backend used by the underlying platon_keys library.

        *(The default is fine for most users)*

        :param backend: any backend that works in
            `platon_keys.KeyApi(backend) <https://github.com/platonnetwork/platon_keys/#keyapibackendnone>`_

        """
        self._keys = KeyAPI(backend)

    @combomethod
    def sign_message(self, signable_message: SignableMessage, private_key):
        r"""
        Sign the provided message.

        This API supports any messaging format that will encode to EIP-191_ messages.

        If you would like historical compatibility with
        :meth:`w3.platon.sign() <web3.platon.Platon.sign>`
        you can use :meth:`~platon_account.messages.encode_defunct`.

        Other options are the "validator", or "structured data" standards. (Both of these
        are in *DRAFT* status currently, so be aware that the implementation is not
        guaranteed to be stable). You can import all supported message encoders in
        ``platon_account.messages``.

        :param signable_message: the encoded message for signing
        :param private_key: the key to sign the message with
        :type private_key: hex str, bytes, int or :class:`platon_keys.datatypes.PrivateKey`
        :returns: Various details about the signature - most importantly the fields: v, r, and s
        :rtype: ~platon_account.datastructures.SignedMessage

        .. doctest:: python

            >>> msg = "I♥SF"
            >>> from platon_account.messages import encode_defunct
            >>> msghash = encode_defunct(text=msg)
            >>> msghash
            SignableMessage(version=b'E',
             header=b'thereum Signed Message:\n6',
             body=b'I\xe2\x99\xa5SF')
            >>> # If you're curious about the internal fields of SignableMessage, take a look at EIP-191, linked above  # noqa: E501
            >>> key = "0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364"
            >>> Account.sign_message(msghash, key)
            SignedMessage(messageHash=HexBytes('0x1476abb745d423bf09273f1afd887d951181d25adc66c4834a70491911b7f750'),
             r=104389933075820307925104709181714897380569894203213074526835978196648170704563,
             s=28205917190874851400050446352651915501321657673772411533993420917949420456142,
             v=28,
             signature=HexBytes('0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb33e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce1c'))

        """
        message_hash = _hash_eip191_message(signable_message)
        return self._sign_hash(message_hash, private_key)

    @combomethod
    def _sign_hash(self, message_hash, private_key):
        msg_hash_bytes = HexBytes(message_hash)
        if len(msg_hash_bytes) != 32:
            raise ValueError("The message hash must be exactly 32-bytes")

        key = self._parsePrivateKey(private_key)

        (v, r, s, platon_signature_bytes) = sign_message_hash(key, msg_hash_bytes)
        return SignedMessage(
            messageHash=msg_hash_bytes,
            r=r,
            s=s,
            v=v,
            signature=HexBytes(platon_signature_bytes),
        )

    @combomethod
    def sign_transaction(self, transaction_dict, private_key, hrp=DEFAULT_HRP):
        """
        Sign a transaction using a local private key.

        It produces signature details and the hex-encoded transaction suitable for broadcast using
        :meth:`w3.platon.sendRawTransaction() <web3.platon.Platon.sendRawTransaction>`.

        To create the transaction dict that calls a contract, use contract object:
        `my_contract.functions.my_function().buildTransaction()
        <http://web3py.readthedocs.io/en/latest/contracts.html#methods>`_

        :param dict transaction_dict: the transaction with keys:
          nonce, chainId, to, data, value, gas, and gasPrice.
        :param private_key: the private key to sign the data with
        :type private_key: hex str, bytes, int or :class:`platon_keys.datatypes.PrivateKey`
        :param str hrp: HRP used to generate the bech32 address
        :returns: Various details about the signature - most
          importantly the fields: v, r, and s
        :rtype: AttributeDict

        .. code-block:: python

            >>> # EIP-1559 dynamic fee transaction (more efficient and preferred over legacy txn)
            >>> dynamic_fee_transaction = {
                    "type": 2,  # Note that the explicit type is necessary for now
                    "gas": 100000,
                    "maxFeePerGas": 2000000000,
                    "maxPriorityFeePerGas": 2000000000,
                    "data": "0x616263646566",
                    "nonce": 34,
                    "to": "lat1qp9skc0tpkve3l3qsn20yr29aklvhwesf274lcs",
                    "value": "0x5af3107a4000",
                    "accessList": (
                        (
                            "0x0000000000000000000000000000000000000001",
                            (
                                "0x0100000000000000000000000000000000000000000000000000000000000000",  # noqa: E501
                            )
                        ),
                    ),
                    "chainId": 101,
                }
            >>> key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
            >>> signed = Account.sign_transaction(dynamic_fee_transaction, key)
            {'hash': HexBytes('0x126431f2a7fda003aada7c2ce52b0ce3cbdbb1896230d3333b9eea24f42d15b0'),
             'r': 110093478023675319011132687961420618950720745285952062287904334878381994888509,
             'rawTransaction': HexBytes('0x02f8b282076c2284773594008477359400830186a09409616c3d61b3331fc4109a9e41a8bdb7d9776609865af3107a400086616263646566f838f7940000000000000000000000000000000000000001e1a0010000000000000000000000000000000000000000000000000000000000000080a0f366b34a5c206859b9778b4c909207e53443cca9e0b82e0b94bc4b47e6434d3da04a731eda413a944d4ea2d2236671e586e57388d0e9d40db53044ae4089f2aec8'),  # noqa: E501
             's': 33674551144139401179914073499472892825822542092106065756005379322302694600392,
             'v': 0}
            >>> w3.platon.sendRawTransaction(signed.rawTransaction)

        .. code-block:: python

            >>> # legacy transaction (less efficient than EIP-1559 dynamic fee txn)
            >>> legacy_transaction = {
                    # Note that the address must be in checksum format or native bytes:
                    'to': 'lat1q7qgfljxl9qcz0d3gtnygnad2vf82c864uyjxq6',
                    'value': 1000000000,
                    'gas': 2000000,
                    'gasPrice': 234567897654321,
                    'nonce': 0,
                    'chainId': 1
                }
            >>> key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
            >>> signed = Account.sign_transaction(legacy_transaction, key)
            {'hash': HexBytes('0x6893a6ee8df79b0f5d64a180cd1ef35d030f3e296a5361cf04d02ce720d32ec5'),
             'r': 4487286261793418179817841024889747115779324305375823110249149479905075174044,
             'rawTransaction': HexBytes('0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'),  # noqa: E501
             's': 30785525769477805655994251009256770582792548537338581640010273753578382951464,
             'v': 37}
            >>> w3.platon.sendRawTransaction(signed.rawTransaction)

        .. code-block:: python

            >>> access_list_transaction = {
                    "gas": 100000,
                    "gasPrice": 1000000000,
                    "data": "0x616263646566",
                    "nonce": 34,
                    "to": "lat1qp9skc0tpkve3l3qsn20yr29aklvhwesf274lcs",
                    "value": "0x5af3107a4000",
                    "type": 1,
                    "accessList": (
                        (
                            "0x0000000000000000000000000000000000000001",
                            (
                                "0x0100000000000000000000000000000000000000000000000000000000000000",  # noqa: E501
                            )
                        ),
                    ),
                    "chainId": 1900,
                }
            >>> key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
            >>> signed = Account.sign_transaction(access_list_transaction, key)
            {'hash': HexBytes('0x2864ca20a74ca5e044067ad4139a22ff5a0853434f5f1dc00108f24ef5f1f783'),
             'r': 105940705063391628472351883894091935317142890114440570831409400676736873197702,
             'rawTransaction': HexBytes('0x01f8ad82076c22843b9aca00830186a09409616c3d61b3331fc4109a9e41a8bdb7d9776609865af3107a400086616263646566f838f7940000000000000000000000000000000000000001e1a0010000000000000000000000000000000000000000000000000000000000000080a0ea38506c4afe4bb402e030877fbe1011fa1da47aabcf215db8da8fee5d3af086a051e9af653b8eb98e74e894a766cf88904dbdb10b0bc1fbd12f18f661fa2797a4'),  # noqa: E501
             's': 37050226636175381535892585331727388340134760347943439553552848647212419749796,
             'v': 0}
            >>> w3.platon.sendRawTransaction(signed.rawTransaction)
        """
        if not isinstance(transaction_dict, Mapping):
            raise TypeError("transaction_dict must be dict-like, got %r" % transaction_dict)

        account = self.from_key(private_key, hrp=hrp)

        # allow from field, *only* if it matches the private key
        if 'from' in transaction_dict:
            if transaction_dict['from'] == account.address:
                sanitized_transaction = dissoc(transaction_dict, 'from')
            else:
                raise TypeError("from field must match key's %s, but it was %s" % (
                    account.address,
                    transaction_dict['from'],
                ))
        else:
            sanitized_transaction = transaction_dict

        # sign transaction
        (
            v,
            r,
            s,
            encoded_transaction,
        ) = sign_transaction_dict(account._key_obj, sanitized_transaction)
        transaction_hash = keccak(encoded_transaction)

        return SignedTransaction(
            rawTransaction=HexBytes(encoded_transaction),
            hash=HexBytes(transaction_hash),
            r=r,
            s=s,
            v=v,
        )

    @combomethod
    def _parsePrivateKey(self, key):
        """
        Generate a :class:`platon_keys.datatypes.PrivateKey` from the provided key.

        If the key is already of type :class:`platon_keys.datatypes.PrivateKey`, return the key.

        :param key: the private key from which a :class:`platon_keys.datatypes.PrivateKey`
                    will be generated
        :type key: hex str, bytes, int or :class:`platon_keys.datatypes.PrivateKey`
        :returns: the provided key represented as a :class:`platon_keys.datatypes.PrivateKey`
        """
        if isinstance(key, self._keys.PrivateKey):
            return key

        try:
            return self._keys.PrivateKey(HexBytes(key))
        except ValidationError as original_exception:
            raise ValueError(
                "The private key must be exactly 32 bytes long, instead of "
                "%d bytes." % len(key)
            ) from original_exception

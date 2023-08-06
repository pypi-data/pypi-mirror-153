import re
from typing import (
    Any,
    Iterable,
    Tuple,
)
from hexbytes import (
    HexBytes,
)
from platon_hash.fnv.fvn import fnv1_64

from platon_typing.abi import (
    Decodable,
    TypeStr,
)

from platon_typing import (
    HexStr,
)
from platon_utils import (
    is_bytes,
    is_bech32_address,
    remove_0x_prefix,
    to_canonical_address,
)

from platon_abi.decoding import (
    ContextFramesBytesIO,
    TupleDecoder,
)
from platon_abi.encoding import (
    TupleEncoder,
    WasmTupleEncoder,
)
from platon_abi.exceptions import (
    EncodingError,
)
from platon_abi.registry import (
    ABIRegistry,
)


import rlp

class BaseABICoder:
    """
    Base class for porcelain coding APIs.  These are classes which wrap
    instances of :class:`~platon_abi.registry.ABIRegistry` to provide last-mile
    coding functionality.
    """
    def __init__(self, registry: ABIRegistry):
        """
        Constructor.

        :param registry: The registry providing the encoders to be used when
            encoding values.
        """
        self._registry = registry


class ABIEncoder(BaseABICoder):
    """
    Wraps a registry to provide last-mile encoding functionality.
    """
    def encode_single(self, typ: TypeStr, arg: Any) -> bytes:
        """
        Encodes the python value ``arg`` as a binary value of the ABI type
        ``typ``.

        :param typ: The string representation of the ABI type that will be used
            for encoding e.g. ``'uint256'``, ``'bytes[]'``, ``'(int,int)'``,
            etc.
        :param arg: The python value to be encoded.

        :returns: The binary representation of the python value ``arg`` as a
            value of the ABI type ``typ``.
        """
        encoder = self._registry.get_encoder(typ)

        return encoder(arg)

    def encode_abi(self,
                   types: Iterable[TypeStr],
                   args: Iterable[Any],
                   identifier: str = None,
                   struct_dict: dict = None,
                   data: HexStr = None
                   ) -> bytes:
        """
        Encodes the python values in ``args`` as a sequence of binary values of
        the ABI types in ``types`` via the head-tail mechanism.

        :param types: An iterable of string representations of the ABI types
            that will be used for encoding e.g.  ``('uint256', 'bytes[]',
            '(int,int)')``
        :param args: An iterable of python values to be encoded.

        :returns: The head-tail encoded binary representation of the python
            values in ``args`` as values of the ABI types in ``types``.
        """
        encoders = [
            self._registry.get_encoder(type_str)
            for type_str in types
        ]

        encoder = TupleEncoder(encoders=encoders)
        encoded_arguments = encoder(args)

        if data:
            return HexBytes(data) + encoded_arguments

        return encoded_arguments


    def is_encodable(self, typ: TypeStr, arg: Any) -> bool:
        """
        Determines if the python value ``arg`` is encodable as a value of the
        ABI type ``typ``.

        :param typ: A string representation for the ABI type against which the
            python value ``arg`` will be checked e.g. ``'uint256'``,
            ``'bytes[]'``, ``'(int,int)'``, etc.
        :param arg: The python value whose encodability should be checked.

        :returns: ``True`` if ``arg`` is encodable as a value of the ABI type
            ``typ``.  Otherwise, ``False``.
        """
        encoder = self._registry.get_encoder(typ)

        try:
            encoder.validate_value(arg)
        except EncodingError:
            return False
        except AttributeError:
            try:
                encoder(arg)
            except EncodingError:
                return False

        return True

    def is_encodable_type(self, typ: TypeStr) -> bool:
        """
        Returns ``True`` if values for the ABI type ``typ`` can be encoded by
        this codec.

        :param typ: A string representation for the ABI type that will be
            checked for encodability e.g. ``'uint256'``, ``'bytes[]'``,
            ``'(int,int)'``, etc.

        :returns: ``True`` if values for ``typ`` can be encoded by this codec.
            Otherwise, ``False``.
        """
        return self._registry.has_encoder(typ)


class ABIDecoder(BaseABICoder):
    """
    Wraps a registry to provide last-mile decoding functionality.
    """
    stream_class = ContextFramesBytesIO

    def decode_single(self, typ: TypeStr, data: Decodable) -> Any:
        """
        Decodes the binary value ``data`` of the ABI type ``typ`` into its
        equivalent python value.

        :param typ: The string representation of the ABI type that will be used for
            decoding e.g. ``'uint256'``, ``'bytes[]'``, ``'(int,int)'``, etc.
        :param data: The binary value to be decoded.

        :returns: The equivalent python value of the ABI value represented in
            ``data``.
        """
        if not is_bytes(data):
            raise TypeError("The `data` value must be of bytes type.  Got {0}".format(type(data)))

        decoder = self._registry.get_decoder(typ)
        stream = self.stream_class(data)

        return decoder(stream)

    def decode_abi(self, types: Iterable[TypeStr], data: Decodable) -> Tuple[Any, ...]:
        """
        Decodes the binary value ``data`` as a sequence of values of the ABI types
        in ``types`` via the head-tail mechanism into a tuple of equivalent python
        values.

        :param types: An iterable of string representations of the ABI types that
            will be used for decoding e.g. ``('uint256', 'bytes[]', '(int,int)')``
        :param data: The binary value to be decoded.

        :returns: A tuple of equivalent python values for the ABI values
            represented in ``data``.
        """
        if not is_bytes(data):
            raise TypeError("The `data` value must be of bytes type.  Got {0}".format(type(data)))

        decoders = [
            self._registry.get_decoder(type_str)
            for type_str in types
        ]

        decoder = TupleDecoder(decoders=decoders)
        stream = self.stream_class(data)

        return decoder(stream)


class ABICodec(ABIEncoder, ABIDecoder):
    pass


class WasmABIEncoder(ABIEncoder):
    """
        Wraps a registry to provide last-mile encoding functionality.
    """
    def encode_single(self, typ: TypeStr, arg: Any, struct_dict: dict = None) -> bytes:
        """
        Encodes the python value ``arg`` as a binary value of the ABI type
        ``typ``.

        :param typ: The string representation of the ABI type that will be used
            for encoding e.g. ``'uint256'``, ``'bytes[]'``, ``'(int,int)'``,
            etc.
        :param arg: The python value to be encoded.

        :returns: The binary representation of the python value ``arg`` as a
            value of the ABI type ``typ``.
        """
        list_re = "(?:list|set)\<(.*)\>"
        map_re = "(?:map|pair)\<(.*),(.*)\>"

        # todo: move to registry encoder
        # todo: Support multidimensional arrays
        if typ.startswith("list") or typ.startswith("set"):
            matcher = re.match(list_re, typ)
            type_str = matcher.group(1)
            length = len(arg)
            return self.encode_single(f"{type_str}[{length}]", arg)

        elif typ.startswith("pair"):
            if type(arg) is not list and type(arg) is not tuple:
                raise TypeError(f"Value type error, expected list or tuple, actual value is {arg}")

            if len(arg) != 2:
                raise ValueError(f"Value error, expected length is 2, actual length is {len(arg)}")

            matcher = re.match(map_re, typ)
            encoded_key = self.encode_single(matcher.group(1), arg[0])
            encoded_value = self.encode_single(matcher.group(2), arg[1])
            return [encoded_key, encoded_value]

        elif typ.startswith("map"):
            if type(arg) is not list and type(arg) is not tuple:
                raise TypeError(f"Value type error, expected list or tuple, actual value is {arg}")

            matcher = re.match(map_re, typ)
            pair_type_str = f"pair<{matcher.group(1)},{matcher.group(2)}>"
            encoded_pairs = []

            for pair in arg:
                encoded_pairs.append(self.encode_single(pair_type_str, pair))
            return encoded_pairs

        elif struct_dict and struct_dict.get(typ):
            struct = struct_dict.get(typ)

            if not struct:
                raise ValueError(f"Struct {typ} not found")

            if type(arg) is not list and type(arg) is not tuple:
                raise TypeError(f"Value type error, expected list or tuple, actual value is {arg}")

            types = [input['type'] for input in struct['inputs']]
            encoded_struct = []

            for _type, _arg in zip(types, arg):
                encoded_struct.append(self.encode_single(_type, _arg, struct_dict))
            return encoded_struct

        elif typ.startswith("FixedHash"):
            if type(arg) is not str:
                raise TypeError(f"Value type error, expected str, actual value is {arg}")

            if typ == "FixedHash<20>" and is_bech32_address(arg):
                address_bytes = to_canonical_address(arg)
                return [remove_0x_prefix(hex(b)).zfill(2) for b in address_bytes]

            return arg

        else:
            encoder = self._registry.get_encoder(typ)
            return encoder(arg)

    def encode_abi(self,
                   types: Iterable[TypeStr],
                   args: Iterable[Any],
                   identifier: str = None,
                   struct_dict: dict = None,
                   data: HexStr = None
                   ) -> bytes:
        """
        Encodes the python values in ``args`` as a sequence of binary values of
        the ABI types in ``types`` via the head-tail mechanism.

        :param types: An iterable of string representations of the ABI types
            that will be used for encoding e.g.  ``('uint256', 'bytes[]',
            '(int,int)')``
        :param args: An iterable of python values to be encoded.

        :returns: The head-tail encoded binary representation of the python
            values in ``args`` as values of the ABI types in ``types``.
        """
        encoded_arguments = [self.encode_single(_type, arg, struct_dict) for _type, arg in zip(types, args)]

        if identifier:
            encoded_arguments.insert(0, fnv1_64(bytes(identifier, 'utf8')))

        # todo: 当前非init方法也会追加data
        encoded_data = rlp.encode(encoded_arguments)
        if data:
            encoded_data = rlp.encode([bytes.fromhex(data.decode('utf-8')), encoded_data])

        return HexBytes(encoded_data)


class WasmABIDecoder(ABIDecoder):

    def decode_single(self, typ: TypeStr, data: Decodable) -> Any:
        """
        Decodes the binary value ``data`` of the ABI type ``typ`` into its
        equivalent python value.

        :param typ: The string representation of the ABI type that will be used for
            decoding e.g. ``'uint256'``, ``'bytes[]'``, ``'(int,int)'``, etc.
        :param data: The binary value to be decoded.

        :returns: The equivalent python value of the ABI value represented in
            ``data``.
        """
        if not is_bytes(data):
            raise TypeError("The `data` value must be of bytes type.  Got {0}".format(type(data)))

        decoder = self._registry.get_decoder(typ)
        stream = self.stream_class(data)

        return decoder(stream)

    def decode_abi(self,
                   types: Iterable[TypeStr],
                   data: Decodable,
                   struct_dict: dict = None,
                   ) -> Tuple[Any, ...]:
        """
        Decodes the binary value ``data`` as a sequence of values of the ABI types
        in ``types`` via the head-tail mechanism into a tuple of equivalent python
        values.

        :param types: An iterable of string representations of the ABI types that
            will be used for decoding e.g. ``('uint256', 'bytes[]', '(int,int)')``
        :param data: The binary value to be decoded.

        :returns: A tuple of equivalent python values for the ABI values
            represented in ``data``.
        """
        if not is_bytes(data):
            raise TypeError("The `data` value must be of bytes type.  Got {0}".format(type(data)))

        encoded_arguments = [self.decode_single(_type, arg, struct_dict) for _type, arg in zip(types, args)]

        return decoder(stream)


class WasmABICodec(WasmABIEncoder, ABIDecoder):
    pass

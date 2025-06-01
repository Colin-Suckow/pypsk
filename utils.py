# Byte array to list of bits, LSB
def as_bits(data: bytearray) -> list[int]:
    result = []
    for byte in data:
        for i in range(8):
            result.append((byte >> i) & 1)
    return result

# Bit array to byte array, bit array should be LSB
def as_bytes(bits: list[int]) -> bytearray:
    result = bytearray()
    tmp = 0
    for i, bit in enumerate(bits):
        if i % 8 == 0 and i != 0:
            result.append(tmp)
            tmp = 0
        if bit > 0:
            tmp |= (1 << (i % 8))

    result.append(tmp)
    return result


# Diff encode the given bits
def diff_encode(bits: list[int]) -> list[int]:
    result = [0]
    for bit in bits:
        if bit > 0:
            result.append(int(not result[-1]))
        else:
            result.append(result[-1])
    return result

# Diff decode the given diff encoded bytes
def diff_decode(bits: list[int]) -> list[int]:
    result = []
    last = bits[0]
    for bit in bits[1:]:
        if bit == last:
            result.append(0)
            last = bit
        else:
            result.append(1)
            last = bit
    return result
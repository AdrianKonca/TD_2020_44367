from utilities import make_ordinal

def hamming_coding(bits):

    encoded_bits = [None] * 7
    parity_bits = [None] * 3

    parity_bits[0] = (bits[0] + bits[1] + bits[3]) % 2
    parity_bits[1] = (bits[0] + bits[2] + bits[3]) % 2
    parity_bits[2] = (bits[1] + bits[2] + bits[3]) % 2

    encoded_bits[0] = bool(parity_bits[0])
    encoded_bits[1] = bool(parity_bits[1])
    encoded_bits[2] = bits[0]
    encoded_bits[3] = bool(parity_bits[2])
    encoded_bits[4] = bits[1]
    encoded_bits[5] = bits[2]
    encoded_bits[6] = bits[3]

    return encoded_bits

def hamming_secded_coding(bits):

    encoded_bits = [None] * 8
    parity_bits = [None] * 4

    parity_bits[0] = (bits[0] + bits[1] + bits[3]) % 2
    parity_bits[1] = (bits[0] + bits[2] + bits[3]) % 2
    parity_bits[2] = (bits[1] + bits[2] + bits[3]) % 2
    parity_bits[3] = (bits[0] + bits[1] + bits[2]) % 2

    encoded_bits[0] = bool(parity_bits[0])
    encoded_bits[1] = bool(parity_bits[1])
    encoded_bits[2] = bits[0]
    encoded_bits[3] = bool(parity_bits[2])
    encoded_bits[4] = bits[1]
    encoded_bits[5] = bits[2]
    encoded_bits[6] = bits[3]
    encoded_bits[7] = bool(parity_bits[3])

    return encoded_bits


def hamming_decoding(bits):

    decoded_bits = [None] * 4
    parity_bits = [None] * 3

    parity_bits[0] = (bits[0] + bits[2] + bits[4] + bits[6]) % 2
    parity_bits[1] = (bits[1] + bits[2] + bits[5] + bits[6]) % 2
    parity_bits[2] = (bits[3] + bits[4] + bits[5] + bits[6]) % 2

    n = parity_bits[0] + parity_bits[1] * 2 + parity_bits[2] * 4 - 1
    if n >= 0:
        print('Hamming decoding found error at {} bit'.format(make_ordinal(n)))
        bits[n] = not bits[n]

    decoded_bits[0] = bits[2]
    decoded_bits[1] = bits[4]
    decoded_bits[2] = bits[5]
    decoded_bits[3] = bits[6]
    return decoded_bits

def hamming_secded_decoding(bits):

    decoded_bits = [None] * 4
    parity_bits = [None] * 4

    parity_bits[0] = (bits[0] + bits[2] + bits[4] + bits[6]) % 2
    parity_bits[1] = (bits[1] + bits[2] + bits[5] + bits[6]) % 2
    parity_bits[2] = (bits[3] + bits[4] + bits[5] + bits[6]) % 2

    parity_bits[3] = sum(bits[0:7]) % 2
    n = parity_bits[0] + parity_bits[1] * 2 + parity_bits[2] * 4 - 1

    if (n >= 0 and parity_bits[3] == bits[7]):
        print('Two errors detected at Hamming SECDED')
        return []
    elif (n >= 0 and parity_bits[3] != bits[7]):
        print('Hamming SECDED decoding found one error at {} bit'.format(make_ordinal(n)))
        bits[n] = not bits[n]
    elif (n < 0 and parity_bits[3] != bits[7]):
        print('Hamming SECDED decoding found one error - parity bit')

    decoded_bits[0] = bits[2]
    decoded_bits[1] = bits[4]
    decoded_bits[2] = bits[5]
    decoded_bits[3] = bits[6]
    return decoded_bits

def code_bit_stream(stream, method):

    if len(stream) % 4 != 0:
        raise Exception('Amount of bits not divisible by 4')

    coded_bits = []
    for i in range(0, len(stream) - 1, 4):
        bits_to_code = stream[i:i+4]
        coded_bits.append(method(bits_to_code))

    coded_stream = sum(coded_bits, [])

    return coded_stream

def decode_bit_stream(stream):
    method = None
    decoded_bits_count = None
    if len(stream) % 7 == 0:
        method = hamming_decoding
        decoded_bits_count = 7
    elif len(stream) % 8 == 0:
        method = hamming_secded_decoding
        decoded_bits_count = 8
    else:
        raise Exception('Amount of bits not divisible by 7 or 8')

    decoded_bits = []
    for i in range(0, len(stream) - 1, decoded_bits_count):
        bits_to_decode = stream[i:i + decoded_bits_count]
        decoded_bits.append(method(bits_to_decode))

    decoded_stream = sum(decoded_bits, [])
    return decoded_stream

def break_bit(bits, bit_index):
    bits[bit_index] = not bits[bit_index]
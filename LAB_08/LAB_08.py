def stringToBinaryStream(text, littleEndian = False):
    binaryStream = []
    for character in (text):
        binaryCharacter = format(ord(character), '08b')
        for bit in (binaryCharacter):
            binaryStream.append(bit == '1')
    if littleEndian:
        return binaryStream[::-1]
    return binaryStream

#https://stackoverflow.com/a/50992575
def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

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

def test_SECDED():
    for wrong_bit_a in range(0, 8):
        for wrong_bit_b in range(0, 7):
            if wrong_bit_a == wrong_bit_b:
                continue
            print("TESTING BIT A: {} TESTING BIT B: {}".format(wrong_bit_a, wrong_bit_b))
            for i in range(16):
                test_bits = [int(i%16 >= 8), int(i%8 >= 4), int(i%4 >= 2), i%2]
                print(test_bits)
                test_bits_coded = code_bit_stream(test_bits, hamming_secded_coding)
                print(test_bits_coded)
                print(decode_bit_stream(test_bits_coded))
                break_bit(test_bits_coded, wrong_bit_a)
                print(decode_bit_stream(test_bits_coded))
                break_bit(test_bits_coded, wrong_bit_b)
                print(decode_bit_stream(test_bits_coded))
                print()

def task(bits):
#HAMMING
    print(bits)
# [False, True, False, True, False, True, False, False, False, True, True, False, False, False, False, True, False, True, True, False, True, False, True, True]

    coded_bits = code_bit_stream(bits, hamming_coding)
    print(coded_bits)
# [False, True, False, False, True, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False, True, True, False, True, False, False, True, True, 
# True, False, False, True, True, False, False, True, True, False, False, True, True]

    break_bit(coded_bits, 6)
    print(decode_bit_stream(coded_bits))
# Hamming decoding found error at 6th bit
# [False, True, False, True, False, True, False, False, False, True, True, False, False, False, False, True, False, True, True, False, True, False, True, True]

#SECDED
    coded_bits = code_bit_stream(bits, hamming_secded_coding)
    print(coded_bits)
# [False, True, False, False, True, False, True, True, True, False, False, True, True, False, False, True, True, True, False, False, True, True, False, False, True, True, False, True, False, 
# False, True, False, True, True, False, False, True, True, False, False, False, True, True, False, False, True, True, False]

    print(decode_bit_stream(coded_bits))
# [False, True, False, True, False, True, False, False, False, True, True, False, False, False, False, True, False, True, True, False, True, False, True, True]

    break_bit(coded_bits, 2)
    print(decode_bit_stream(coded_bits))
# Hamming SECDED decoding found one error at 2nd bit
# [False, True, False, True, False, True, False, False, False, True, True, False, False, False, False, True, False, True, True, False, True, False, True, True]

    break_bit(coded_bits, 3)
    print(decode_bit_stream(coded_bits))
# Two errors detected at Hamming SECDED
# [False, True, False, False, False, True, True, False, False, False, False, True, False, True, True, False, True, False, True, True]

#test_SECDED()
#bits = [0, 1, 0, 0, 0, 0, 1, 1]
takBits = stringToBinaryStream('Tak')
task(takBits)
#Generalnie implementowałem na podstawie wikipedii, oraz kodu znaiezionego tutaj https://github.com/dominiccarrano/hamming
#Stąd moja macierz którą generuje ósmy bit różni się od Pana.
#Działa, ale nie wykonuje kroku z próbą poprawy w przypadku dwóch błędów.
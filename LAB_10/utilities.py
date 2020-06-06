def string_to_binary_stream(text, littleEndian = False):
    binaryStream = []
    for character in (text):
        binaryCharacter = format(ord(character), '08b')
        for bit in (binaryCharacter):
            binaryStream.append(bit == '1')
    if littleEndian:
        return binaryStream[::-1]
    return binaryStream

def binary_to_string_stream(binaryStream, littleEndian = False):
    if not littleEndian:
        binaryStream = binaryStream[::-1]
    values = [2 ** x for x in range(0, 8)]
    string = []
    for byte_index in range(0, len(binaryStream), 8):
        byte_bits = binaryStream[byte_index:byte_index + 8]
        byte = 0
        for bit, value in zip(byte_bits, values):
            byte += bit * value
        string.append(chr(byte))
    return ''.join(string[::-1])

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

#recreates tile function from numpy
def tile(value, count):
    return [value for _ in range(count)]

#recreates numpy linspace
def linspace(low, high, stepCount):
    stepCount = int(stepCount)
    step = (high - low) / (stepCount - 1)
    values = [low + step * i for i in range(stepCount)]
    return values

def prettify_binary_stream(binary_stream):
    
    numeric_list = ['1' if bit else '0' for bit in binary_stream]
    return ''.join(numeric_list)

def bit_error_rate(expected_bits, received_bits):
    total_error_count = 0
    for expected_bit, received_bit in zip(expected_bits, received_bits):
        if expected_bit != received_bit:
            total_error_count += 1
    return total_error_count/len(expected_bits)
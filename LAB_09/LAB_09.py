from utilities import string_to_binary_stream, binary_to_string_stream, prettify_binary_stream
from hamming import code_bit_stream, hamming_coding, decode_bit_stream
from modulation import modulation, demodulation
import matplotlib.pyplot as plt
from math import ceil
from utilities import linspace

def drawPlot(x, y, title, y_label, x_label = 'Time'):
    plt.plot(x, y, 1)
    plt.xlim(0, max(x))
    
    x_ticks = linspace(0, max(x), ceil(max(x)) / 1.4 + 1)
    for x_tick in x_ticks:
        plt.axvline(x_tick, color='k', linestyle='--', alpha = 0.5)
    plt.xticks(x_ticks)

    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)

def print_prettified_binary_stream(binary_stream):
    print(prettify_binary_stream(binary_stream))

def task(encoded_text, modulation_type):
    print('Encoded string ' + ENCODED_TEXT)
    
    data = string_to_binary_stream(ENCODED_TEXT)
    print("String after converting to binary:")
    print_prettified_binary_stream(data)

    coded_stream = code_bit_stream(data, hamming_coding)
    print("Binary stream after Hamming encoding:")
    print_prettified_binary_stream(coded_stream)

    information_samples, modulation_samples, time = modulation(coded_stream, modulation_type)

    plt.figure(figsize=(len(encoded_text) * 3, 9))
    
    plt.subplot(2, 1, 1)
    drawPlot(time, information_samples, 'TTL of coded stream', 'TTL')
    plt.yticks([0, 1])

    plt.subplot(2, 1, 2)
    drawPlot(time, modulation_samples, modulation_type.upper() + ' of coded stream', 'Amplitude')
    
    plt.tight_layout()

    filepath = 'Charts/output_{}.png'.format(modulation_type)
    print("To see modulation chart go to " + filepath)
    plt.savefig(filepath)

    coded_stream_after_demodulation = demodulation(modulation_samples, modulation_type)
    print("Binary stream after demodulation:")
    print_prettified_binary_stream(coded_stream_after_demodulation)

    decoded_stream = decode_bit_stream(coded_stream_after_demodulation)
    print("Binary stream after decoding:")
    print_prettified_binary_stream(decoded_stream)
    
    text = binary_to_string_stream(decoded_stream)
    print("Decoded text:")
    print(text)

if __name__ == "__main__":

    ENCODED_TEXT = 'Ala ma kota'
    modulation_types = {
        'ask': 'Amplitude Shift Keying',
        'psk': 'Phase Shift Keying',
        'fsk': 'Frequency Shift Keying',
    }

    for modulation_short, modulation_long in modulation_types.items():
        print()
        print("CURRENT METHOD OF MODULATION: " + modulation_long)
        task(ENCODED_TEXT, modulation_short)
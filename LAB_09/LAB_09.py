from utilities import string_to_binary_stream, binary_to_string_stream
from hamming import code_bit_stream, hamming_coding, decode_bit_stream
from modulation import modulation_ask, demodulation_ask
import matplotlib.pyplot as plt
from math import ceil
from utilities import linspace

def drawPlot(x, y, title, ylabel, xlabel = 'Time'):
    plt.plot(x, y, 1)
    plt.xlim(0, max(x))
    
    xticks = linspace(0, max(x), ceil(max(x)) / 1.4 + 1)
    for xtick in xticks:
        plt.axvline(xtick, color='k', linestyle='--', alpha = 0.5)
    plt.xticks(xticks)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

if __name__ == "__main__":

    ENCODED_TEXT = 'Ala ma kota'
    print('Encoded string ' + ENCODED_TEXT)
    
    data = string_to_binary_stream(ENCODED_TEXT)
    print("String after converting to binary:")
    print(data)

    coded_stream = code_bit_stream(data, hamming_coding)
    print("Binary stream after Hamming encoding:")
    print(coded_stream)

    information_samples, modulation_samples, time = modulation_ask(coded_stream)

    plt.figure(figsize=(32, 9))
    
    plt.subplot(2, 1, 1)
    drawPlot(time, information_samples, 'TTL of coded stream', 'TTL')
    plt.yticks([0, 1])

    plt.subplot(2, 1, 2)
    drawPlot(time, modulation_samples, 'Amplitude shift keying of coded stream', 'Amplitude')
    
    plt.tight_layout()

    print("To see modulation chart go to Charts/output.png")
    plt.savefig("Charts/output.png")

    coded_stream_after_demodulation = demodulation_ask(modulation_samples)
    print("Binary stream after demodulation:")
    print(coded_stream_after_demodulation)

    decoded_stream = decode_bit_stream(coded_stream_after_demodulation)
    print("Binary stream after decoding:")
    print(decoded_stream)
    
    text = binary_to_string_stream(decoded_stream)
    print("Decoded text:")
    print(text)
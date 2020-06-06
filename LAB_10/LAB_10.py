import matplotlib.pyplot as plt
import wave
import numpy as np

from scipy.io.wavfile import read as read_wav
from utilities import string_to_binary_stream, binary_to_string_stream, prettify_binary_stream, bit_error_rate
from hamming import code_bit_stream, hamming_coding, decode_bit_stream
from modulation import modulate, demodulate, SAMPLING_FREQUENCY, SAMPLES_PER_BIT
from math import ceil
from utilities import linspace
import numpy as np
from collections import namedtuple

###FFT

def filterNoise(filterParameter, amplitudes, frequencies):
    frequenciesFiltered = []
    amplitudesFiltered = []
    minimumAmplitude = max(amplitudes) / filterParameter
    for i, amplitude in enumerate(amplitudes):
        if (amplitude > minimumAmplitude):
            amplitudesFiltered.append(amplitude)
            frequenciesFiltered.append(frequencies[i])
    return frequenciesFiltered, amplitudesFiltered

def frequencyScaleCalculator(samplingFrequency, samplesCount):
	frequencies = []
	for i in range(samplesCount):
		frequencies.append(i * samplingFrequency / samplesCount / 2)
	return np.array(frequencies)

def convertToDecibelScale(amplitudes):
    return np.log10(amplitudes) * 10

def convertFftToAmplitudeSpectrum(fftValues):
    return abs(np.array(fftValues))/len(fftValues)

def drawAmplitudeSpectrum(frequencies, amplitudeSamples, title, subplot):
    plt.subplot(5, 1, subplot)
    plt.stem(frequencies, convertToDecibelScale(amplitudeSamples), markerfmt = 'C1o', use_line_collection=True)
    plt.title(title)
    plt.ylabel('Decibels')
    plt.xlabel('Frequency')
    plt.xscale('log')


def draw_amplitude_spectrum(modulation_samples, modulation_type, subplot):
    fft = np.fft.rfft(modulation_samples)

    frequency = frequencyScaleCalculator(SAMPLING_FREQUENCY, len(fft))

    modulation_spectrum = convertFftToAmplitudeSpectrum(fft)
    modulation_frequencies, amplitude_filtered_modulation_spectrum = filterNoise(1000, modulation_spectrum, frequency)

    drawAmplitudeSpectrum(modulation_frequencies, amplitude_filtered_modulation_spectrum, 'Amplitude spectrum of ' + modulation_type.upper(), subplot)

###_FFT_END

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

def apply_white_noise(modulation_samples, white_noise, alpha):
    modulation_samples_with_noise = []
    for i, sample in enumerate(modulation_samples):
        modulation_sample_with_noise = (sample * alpha) + ((1 - alpha) * white_noise[i])
        modulation_samples_with_noise.append(modulation_sample_with_noise)
    return modulation_samples_with_noise


def task_barebones(encoded_text, modulation_type, white_noise, alpha):
    
    data = string_to_binary_stream(encoded_text)

    coded_stream = code_bit_stream(data, hamming_coding)

    information_samples, modulation_samples, time = modulate(coded_stream, modulation_type)
    modulation_samples_with_noise = apply_white_noise(modulation_samples, white_noise, alpha)

    coded_stream_after_demodulation = demodulate(modulation_samples_with_noise, modulation_type)

    decoded_stream = decode_bit_stream(coded_stream_after_demodulation)

    bit_error_rate_value = bit_error_rate(coded_stream, coded_stream_after_demodulation)

    return bit_error_rate_value

def task(encoded_text, modulation_type, white_noise, alpha, expected_ber):
    print('Encoded string ' + encoded_text)
    
    data = string_to_binary_stream(encoded_text)
    print("String after converting to binary:")
    print_prettified_binary_stream(data)

    coded_stream = code_bit_stream(data, hamming_coding)
    print("Binary stream after Hamming encoding:")
    print_prettified_binary_stream(coded_stream)

    information_samples, modulation_samples, time = modulate(coded_stream, modulation_type)
    modulation_samples_with_noise = apply_white_noise(modulation_samples, white_noise, alpha)

    plt.figure(figsize=(len(encoded_text) * 3, 15))

    plt.subplot(5, 1, 1)
    drawPlot(time, information_samples, 'TTL of coded stream', 'TTL')
    plt.yticks([0, 1])

    plt.subplot(5, 1, 2)
    drawPlot(time, modulation_samples, modulation_type.upper() + ' of coded stream', 'Amplitude')

    draw_amplitude_spectrum(modulation_samples, modulation_type, 3)
    
    plt.subplot(5, 1, 4)
    drawPlot(time, modulation_samples_with_noise, '{} of coded stream with noise (alpha = {}) applied'.format(modulation_type.upper(), alpha), 'Amplitude')

    draw_amplitude_spectrum(modulation_samples_with_noise, modulation_type, 5)

    plt.tight_layout()

    filepath = 'Charts/output_{}_ber_{}.png'.format(modulation_type, expected_ber)
    print("To see modulation chart go to " + filepath)
    plt.savefig(filepath)

    coded_stream_after_demodulation = demodulate(modulation_samples_with_noise, modulation_type)
    print("Binary stream after demodulation:")
    print_prettified_binary_stream(coded_stream_after_demodulation)

    decoded_stream = decode_bit_stream(coded_stream_after_demodulation)
    print("Binary stream after decoding:")
    print_prettified_binary_stream(decoded_stream)

    bit_error_rate_value = bit_error_rate(coded_stream, coded_stream_after_demodulation)
    print("Bit error rate:")
    print(bit_error_rate_value)
    
    text = binary_to_string_stream(decoded_stream)
    print("Decoded text:")
    print(text)

    return bit_error_rate_value

def get_white_noise(noise_filename):

    sample_rate, white_noise_ndarray = read_wav(noise_filename)

    white_noise = list(white_noise_ndarray)

    white_noise_lower_limit = -2**15
    white_noise_upper_limit = 2**16

    white_noise_normalized = [(noise_level - white_noise_lower_limit)/white_noise_upper_limit for noise_level in white_noise]

    return white_noise_normalized

def bit_error_rate_vs_alpha(method, encoded_text, white_noise, min_alpha, max_alpha, step_count = 150):

    ber_values = []
    alphas = linspace(min_alpha, max_alpha, step_count)
    for alpha in alphas:
        print(alpha)
        ber_value = task_barebones(encoded_text, method, white_noise, alpha)
        ber_values.append(ber_value)

    plt.figure(figsize=(12, 7))
    plt.title('Bit error rate with increasing alpha for {} with {} points'.format(method, step_count))
    plt.ylabel('Bit error rate')
    plt.xlabel('Alpha')
    plt.plot(alphas, ber_values)
    plt.savefig('Charts/bit_error_rate_vs_alpha_{}.png'.format(method))

def stack_images(image_names, titles, output_file_name, figure_size):

    plt.figure(figsize=figure_size)

    for i, (image_name, title) in enumerate(zip(image_names, titles)):
        image = plt.imread(image_name)

        plt.subplot(1, 3, i + 1)
        plt.imshow(image)
        plt.xticks([], [])
        plt.yticks([], [])
        plt.title(title)

    plt.tight_layout()
    plt.savefig('Charts/{}_stacked.png'.format(output_file_name))

def main_task(encoded_text, white_noise):
    Modulation = namedtuple('Modulation', ['short_name', 'long_name', 'alpha_value', 'error_frequency'])
    modulations = [
        Modulation('ask', 'Amplitude Shift Keying', 0.937, 'high'),
        Modulation('ask', 'Amplitude Shift Keying', 0.9383, 'medium'),
        Modulation('ask', 'Amplitude Shift Keying', 0.9396, 'low'),
        Modulation('psk', 'Phase Shift Keying', 0.387, 'high'),
        Modulation('psk', 'Phase Shift Keying', 0.392, 'medium'),
        Modulation('psk', 'Phase Shift Keying', 0.395, 'low'),
        Modulation('fsk', 'Frequency Shift Keying', 0.096, 'high'),
        Modulation('fsk', 'Frequency Shift Keying', 0.108, 'medium'),
        Modulation('fsk', 'Frequency Shift Keying', 0.114, 'low'),
    ]

    for modulation in modulations:
        print()
        print("CURRENT METHOD OF MODULATION: {} ALPHA: {} EXPECTED BER: {}".format(modulation.long_name, modulation.alpha_value, modulation.error_frequency))
        task(encoded_text, modulation.short_name, white_noise, modulation.alpha_value, modulation.error_frequency)

    SUBPLOT_TITLES = [
            'LOW BIT ERROR RATE',
            'MEDIUM BIT ERROR RATE',
            'HIGH BIT ERROR RATE',
        ]
    figure_size = (len(ENCODED_TEXT) * 3 * 3, 16)
    for method in METHODS:
        stack_images(
            ['Charts/output_{}_ber_{}.png'.format(method, level) for level in LEVELS], 
            ['{} BIT ERROR RATE'.format(level.upper()) for level in LEVELS],
            method,
            figure_size
        )


def secondary_task(encoded_text, white_noise):
    ber_vs_alpha_parameters = [
        ('ask', 0.932, 0.942, 150),
        ('psk', 0.37, 0.41, 150),
        ('fsk', 0.06, 0.125, 150),
    ]

    for parameters in ber_vs_alpha_parameters:
        method, min_alpha, max_alpha, step_count = parameters
        bit_error_rate_vs_alpha(method, encoded_text, white_noise, min_alpha, max_alpha, step_count)

    stack_images(
        ['Charts/bit_error_rate_vs_alpha_{}.png'.format(method) for method in METHODS], 
        [''] * 3,
        'comparison',
        (40, 8)
    )

#Type: ask  Error frequency: high    Alpha: 0.937
#Type: ask  Error frequency: medium  Alpha: 0.9383
#Type: ask  Error frequency: low     Alpha: 0.9396
#Type: psk  Error frequency: high    Alpha: 0.387
#Type: psk  Error frequency: medium  Alpha: 0.392
#Type: psk  Error frequency: low     Alpha: 0.395
#Type: fsk  Error frequency: high    Alpha: 0.096
#Type: fsk  Error frequency: medium  Alpha: 0.108
#Type: fsk  Error frequency: low     Alpha: 0.114

if __name__ == "__main__":
    NOISE_FILENAME = 'whitenoisesound.wav'
    ENCODED_TEXT = 'Ala ma kota'
    RUN_MAIN_TASK = True
    RUN_BER_VS_ALPHA = False
    LEVELS = ['low', 'medium', 'high']
    METHODS = ['ask', 'psk', 'fsk']

    white_noise = get_white_noise(NOISE_FILENAME)

    if RUN_MAIN_TASK:
        main_task(ENCODED_TEXT, white_noise)
    if RUN_BER_VS_ALPHA:
        secondary_task(ENCODED_TEXT, white_noise)

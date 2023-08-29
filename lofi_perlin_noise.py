import pyaudio
import numpy as np
import pygame
import noise

# Audio setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WIDTH, HEIGHT = 400, 300  # Reducing resolution for speed

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def analyze_audio(data):
    fft_data = np.fft.fft(np.frombuffer(data, dtype=np.int16))
    frequencies = np.fft.fftfreq(CHUNK, 1.0 / RATE)

    bass = np.abs(fft_data[(frequencies >= 20) & (frequencies < 300)])
    mid = np.abs(fft_data[(frequencies >= 300) & (frequencies < 3000)])
    high = np.abs(fft_data[(frequencies >= 3000) & (frequencies < 20000)])

    return bass.mean(), mid.mean(), high.mean()

def turbulence(x, y, start_freq, num_octaves):
    total = 0.0
    amplitude = 1.0
    frequency = start_freq

    for _ in range(num_octaves):
        total += noise.pnoise2(x * frequency, y * frequency) * amplitude
        frequency *= 2
        amplitude *= 0.5

    return total

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        bass_intensity, mid_intensity, high_intensity = analyze_audio(audio_data)

        for x in range(0, WIDTH, 2):  # We step by 2 for both x and y to effectively halve the resolution.
            for y in range(0, HEIGHT, 2):
                # Use a lower frequency for larger blobs.
                r_val = (turbulence(x, y, 0.002, 3) * bass_intensity) % 255
                g_val = (turbulence(x, y, 0.002, 3) * mid_intensity) % 255
                b_val = (turbulence(x, y, 0.002, 3) * high_intensity) % 255

                color = (int(r_val), int(g_val), int(b_val))
                
                # Fill in the neighboring pixels with the same color to effectively upscale the result
                screen.set_at((x, y), color)
                screen.set_at((x + 1, y), color)
                screen.set_at((x, y + 1), color)
                screen.set_at((x + 1, y + 1), color)

        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()

import pyaudio
import numpy as np
import pygame
import math

# Audio setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WIDTH, HEIGHT = 800, 600

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


device_index = None
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['name'] == 'Your Audio Source Name Here' and dev['maxInputChannels'] > 0: # replace with your source name
        device_index = i
        break
def draw_tree(x1, y1, angle, depth, thickness, length_factor):
    if depth > 0:
        x2 = x1 + (math.cos(math.radians(angle)) * depth * 5.0 * length_factor)
        y2 = y1 - (math.sin(math.radians(angle)) * depth * 5.0 * length_factor)
        pygame.draw.line(screen, (255,255,255), (x1, y1), (x2, y2), max(1, int(thickness)))
        draw_tree(x2, y2, angle - angle_factor, depth - 1, thickness * 0.8, length_factor)
        draw_tree(x2, y2, angle + angle_factor, depth - 1, thickness * 0.8, length_factor)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        bass_intensity, mid_intensity, high_intensity = analyze_audio(audio_data)

        print(bass_intensity, mid_intensity, high_intensity)

        # Increase modulation effect for clearer change
        angle_factor = 15 + (bass_intensity / 1000.0) * 40
        length_factor = 0.8 + (mid_intensity / 10000.0) 
        thickness_factor = 2 + (high_intensity / 5000.0)

        screen.fill((0, 0, 0))
        draw_tree(WIDTH // 2, HEIGHT - HEIGHT//2, -90, 6, thickness_factor, length_factor)
        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()
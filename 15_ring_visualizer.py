import pyaudio
import numpy as np
import pygame
import math
pygame.init()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
WIDTH, HEIGHT = screen_width, screen_height
CENTER = (WIDTH // 2, HEIGHT // 2)
NUM_BANDS = 20
MIN_FREQ = 20
MAX_FREQ = 20000

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frequency Band Visualizer")

def analyze_audio(data):
    fft_data = np.fft.fft(np.frombuffer(data, dtype=np.int16))
    frequencies = np.fft.fftfreq(CHUNK, 1.0/RATE)
    log_spaced = np.logspace(np.log10(MIN_FREQ), np.log10(MAX_FREQ), NUM_BANDS + 1)
    band_means = []
    for i in range(NUM_BANDS):
        band_data = np.abs(fft_data[(frequencies >= log_spaced[i]) & (frequencies < log_spaced[i+1])])
        band_means.append(band_data.mean())
    return band_means

def draw_vibrating_ring(center, base_radius, intensity, frequency, phase, color):
    num_points = 100
    angle_step = 2 * math.pi / num_points

    points = []
    for i in range(num_points):
        displacement = math.sin(frequency * i + phase) * intensity
        radius = base_radius + displacement
        x = center[0] + radius * math.cos(i * angle_step)
        y = center[1] + radius * math.sin(i * angle_step)
        points.append((x, y))

    pygame.draw.lines(screen, color, True, points)

phase = 0
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        band_intensities = analyze_audio(audio_data)

        screen.fill((0, 0, 0))
        
        for i, intensity in enumerate(band_intensities):
            color = ((i * 12) % 255, (255 - i * 12) % 255, (i * 23) % 255)
            base_radius = 50 + i * 15
            draw_vibrating_ring(CENTER, base_radius, intensity / 5000, 10 + i, phase, color)

        phase += 0.1  # Increment phase to animate the sinusoidal vibration
        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()

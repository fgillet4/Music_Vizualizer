import pyaudio
import numpy as np
import pygame
import math

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frequency Band Visualizer")

def analyze_audio(data):
    fft_data = np.fft.fft(np.frombuffer(data, dtype=np.int16))
    frequencies = np.fft.fftfreq(CHUNK, 1.0/RATE)

    bass = np.abs(fft_data[(frequencies >= 20) & (frequencies < 300)])
    mid = np.abs(fft_data[(frequencies >= 300) & (frequencies < 3000)])
    high = np.abs(fft_data[(frequencies >= 3000) & (frequencies < 20000)])

    return bass.mean(), mid.mean(), high.mean()

def draw_vibrating_ring(center, base_radius, intensity, frequency, phase, color):
    num_points = 100
    angle_step = 2 * math.pi / num_points

    points = []
    for i in range(num_points):
        # Calculate the sinusoidal displacement for the current point
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
        bass_intensity, mid_intensity, high_intensity = analyze_audio(audio_data)

        screen.fill((0, 0, 0))

        # Bass - Outer Ring
        draw_vibrating_ring(CENTER, 200, bass_intensity / 5000, 10, phase, (255, 0, 0))

        # Mid - Middle Ring
        draw_vibrating_ring(CENTER, 150, mid_intensity / 5000, 20, phase, (0, 255, 0))

        # High - Inner Ring
        draw_vibrating_ring(CENTER, 100, high_intensity / 5000, 30, phase, (0, 0, 255))

        phase += 0.1  # Increment phase to animate the sinusoidal vibration
        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()

import pyaudio
import numpy as np
import pygame

# Constants
BUFFER_SIZE = 1024
WIDTH, HEIGHT = 800, 600
BASS_THRESHOLD = 100  # adjust as needed

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=BUFFER_SIZE)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bass Visualizer")

def analyze_audio(data):
    fft_data = np.fft.fft(np.frombuffer(data, dtype=np.int16))
    bass = np.mean(np.abs(fft_data[:BASS_THRESHOLD]))
    return bass

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        audio_data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
        bass_intensity = analyze_audio(audio_data)

        screen.fill((0, 0, 0))

        # Draw a circle with a size proportional to bass intensity
        radius = int(50 + bass_intensity / 200)  # Adjust the 200 for sensitivity
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), radius)

        pygame.display.flip()
        
except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()

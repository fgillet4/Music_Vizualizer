import pyaudio
import numpy as np
import pygame

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WIDTH, HEIGHT = 800, 600

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

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        bass_intensity, mid_intensity, high_intensity = analyze_audio(audio_data)

        screen.fill((0, 0, 0))

        # Bass - Circle size
        pygame.draw.circle(screen, (255, 0, 0), (WIDTH // 4, HEIGHT // 2), int(50 + bass_intensity / 500))

        # Mid - Rectangle width
        pygame.draw.rect(screen, (0, 255, 0), (WIDTH // 2 - int(mid_intensity / 500), HEIGHT // 4, int(mid_intensity / 50), HEIGHT // 2))

        # High - Triangle rotation (this is a bit more tricky, so for simplicity, I'm adjusting the position)
        points = [(WIDTH * 3 // 4, HEIGHT // 2), (WIDTH * 3 // 4 - 20, HEIGHT // 2 - int(high_intensity / 200)), (WIDTH * 3 // 4 + 20, HEIGHT // 2 - int(high_intensity / 200))]
        pygame.draw.polygon(screen, (0, 0, 255), points)

        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()

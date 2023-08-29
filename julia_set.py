import pygame
import numpy as np

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fractal parameters
MAX_ITER = 100
ZOOM = 250

# Colors for visualization
def color(n):
    r = int(n * 2.5 % 256)
    g = int(n * 5 % 256)
    b = int(n * 10 % 256)
    return r, g, b

# Drawing function
def draw_fractal(c, is_mandelbrot=False):
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            zx, zy = x / ZOOM - 1.5, y / ZOOM - 1.5
            if is_mandelbrot:
                cx, cy = zx, zy
            else:
                cx, cy = c
            n = MAX_ITER
            
            while abs(zx) < 2 and abs(zy) < 2 and n > 0:
                tmp = zx * zx - zy * zy + cx
                zy, zx = 2.0 * zx * zy + cy, tmp
                n -= 1
                
            # Set the pixel color based on how many iterations were used
            screen.set_at((x, y), color(n))

# Main loop
c = (-0.70176, -0.3842)  # Starting values for Julia fractal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Draw the fractals
    if np.allclose(c, (0, 0), atol=0.01):  # Check if close to Mandelbrot
        draw_fractal(c, is_mandelbrot=True)
    else:
        draw_fractal(c, is_mandelbrot=False)
    
    # Morphing logic (move c towards (0, 0) to transition to Mandelbrot)
    c = (c[0] * 0.99, c[1] * 0.99)
    if np.allclose(c, (0, 0), atol=0.01):  # Reset to Julia
        c = (-0.70176, -0.3842)
    
    pygame.display.flip()

pygame.quit()

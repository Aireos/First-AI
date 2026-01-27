#AKA Sand engine

import tkinter as tk
import pygame
import random
import sys

def get_screen_size():
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

def gravity(pixels):
    # Iterate from bottom to top to prevent a single grain from "teleporting" to the bottom in one frame
    for y in range(1, len(pixels[0])): 
        for x in range(1, len(pixels) - 1):
            if pixels[x][y] == True:
                # 1. Try to move directly down (y-1 because we are using a bottom-up grid)
                if pixels[x][y-1] == False:
                    pixels[x][y-1] = True
                    pixels[x][y] = False
                
                # 2. Try diagonal movement if blocked
                elif random.randint(0, 1) == 0:
                    if pixels[x+1][y-1] == False:
                        pixels[x+1][y-1] = True
                        pixels[x][y] = False
                    elif pixels[x-1][y-1] == False:
                        pixels[x-1][y-1] = True
                        pixels[x][y] = False
                else:
                    if pixels[x-1][y-1] == False:
                        pixels[x-1][y-1] = True
                        pixels[x][y] = False
                    elif pixels[x+1][y-1] == False:
                        pixels[x+1][y-1] = True
                        pixels[x][y] = False

def viewer():
    pygame.init()
    screen_w, screen_h = get_screen_size()
    # Scale down the resolution for better performance (cellular automata are intensive)
    scale = 10 
    cols, rows = screen_w // scale, screen_h // scale
    
    # Initialize grid: pixels[column][row]
    pixels = [[False for _ in range(rows)] for _ in range(cols)]
    
    screen = pygame.display.set_mode((screen_w, screen_h))
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill((0, 0, 0)) # Background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Handle Mouse Input (Place Sand)
        if pygame.mouse.get_pressed()[0]: # Left Click
            mx, my = pygame.mouse.get_pos()
            # Convert screen coordinates to grid indices
            grid_x, grid_y = mx // scale, (screen_h - my) // scale
            if 0 < grid_x < cols - 1 and 0 < grid_y < rows - 1:
                pixels[grid_x][grid_y] = True

        # Update Physics
        gravity(pixels)
        
        # Draw Pixels
        for x in range(cols):
            for y in range(rows):
                if pixels[x][y]:
                    # Draw a rectangle for each sand grain
                    # screen_h - (y * scale) flips the Y-axis so "gravity" pulls down
                    pygame.draw.rect(screen, (194, 178, 128), 
                                     (x * scale, screen_h - (y * scale), scale, scale))
        
        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS

    pygame.quit()
    sys.exit()

viewer()
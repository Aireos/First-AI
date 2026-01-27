import pygame
import numpy as np
import colorsys
import sys

# === SETTINGS ===
SCALE = 4         
BRUSH_SIZE = 10     
FPS = 144   
COLOR_CYCLE_SPEED = 0.005
# ================

def viewer():
    pygame.init()
    info = pygame.display.Info()
    sw, sh = info.current_w, info.current_h
    
    cols, rows = sw // SCALE, sh // SCALE
    x_offset = (sw - (cols * SCALE)) // 2
    y_offset = (sh - (rows * SCALE)) // 2
    
    screen = pygame.display.set_mode((sw, sh), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    canvas = pygame.Surface((cols, rows))
    clock = pygame.time.Clock()

    grid = np.zeros((cols, rows), dtype=np.uint32)
    hue = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # 1. COLOR CYCLE
        hue = (hue + COLOR_CYCLE_SPEED) % 1.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.8, 1.0)]
        current_color = (r << 16) | (g << 8) | b

        # 2. INPUT (Left click draw, Right click erase)
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] or mouse_pressed[2]:
            mx, my = pygame.mouse.get_pos()
            
            # --- FIX FOR TOP LEFT CORNER ---
            # Cast coordinates to integers *after* division/subtraction
            gx = int((mx - x_offset) / SCALE)
            gy = int((my - y_offset) / SCALE)
            # Ensure coordinates are within bounds before attempting numpy slicing
            if gx < 0 or gx >= cols or gy < 0 or gy >= rows:
                continue
            # -------------------------------
            
            y_idx, x_idx = np.ogrid[-BRUSH_SIZE:BRUSH_SIZE, -BRUSH_SIZE:BRUSH_SIZE]
            mask = x_idx**2 + y_idx**2 <= BRUSH_SIZE**2
            
            x_start, x_end = max(0, gx-BRUSH_SIZE), min(cols, gx+BRUSH_SIZE)
            y_start, y_end = max(0, gy-BRUSH_SIZE), min(rows, gy+BRUSH_SIZE)
            
            target = grid[x_start:x_end, y_start:y_end]
            th, tw = target.shape
            m_slice = mask[:th, :tw] 
            
            if mouse_pressed[0]: # Draw
                target[m_slice & (target == 0)] = current_color
            else: # Erase
                target[m_slice] = 0

        # 3. PHYSICS: Vectorized Row-by-Row Logic
        for y in range(rows - 2, -1, -1):
            row = grid[:, y]
            row_below = grid[:, y + 1]
            active_mask = (row > 0)
            if not np.any(active_mask): continue
            
            can_move_down = active_mask & (row_below == 0)
            grid[can_move_down, y + 1] = grid[can_move_down, y]
            grid[can_move_down, y] = 0
            
            still_active = active_mask & ~can_move_down
            if not np.any(still_active): continue
            
            dxs = [-1, 1] if (y + pygame.time.get_ticks() // 100) % 2 == 0 else [1, -1]
            for dx in dxs:
                nx = np.arange(cols) + dx
                valid_bounds = (nx >= 0) & (nx < cols)
                can_move_diag = np.zeros(cols, dtype=bool)
                can_move_diag[valid_bounds] = still_active[valid_bounds] & (grid[nx[valid_bounds], y + 1] == 0)
                
                if np.any(can_move_diag):
                    dest_x = (np.arange(cols) + dx)[can_move_diag]
                    orig_x = np.arange(cols)[can_move_diag]
                    grid[dest_x, y + 1] = grid[orig_x, y]
                    grid[orig_x, y] = 0
                    still_active[orig_x] = False
                if not np.any(still_active): break

        # 4. RENDERING: Scaled and Centered
        screen.fill((20, 20, 20)) # Background for the letterbox area
        pygame.surfarray.blit_array(canvas, grid)
        
        # Draw the simulation canvas at the calculated centered position
        if SCALE == 1:
            screen.blit(canvas, (x_offset, y_offset))
        else:
            scaled_canvas = pygame.transform.scale(canvas, (cols * SCALE, rows * SCALE))
            screen.blit(scaled_canvas, (x_offset, y_offset))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    viewer()

import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Drawing App")
    clock = pygame.time.Clock()
    
    # Drawing parameters
    brush_radius = 10
    current_color = 'blue'
    current_tool = 'brush'
    drawing = False
    start_pos = None
    
    # Color definitions
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255)
    }

    def draw_ui(surface, color, tool, radius):
        # Draw the interface elements
        panel = pygame.Surface((200, 160), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        surface.blit(panel, (10, 10))
        
        font = pygame.font.Font(None, 24)
        texts = [
            f"Color: {color}",
            f"Tool: {tool}",
            f"Size: {radius}",
            "--- Controls ---",
            "Colors: R,G,B,Y,C,M",
            "Tools: 1-Eraser,2-Brush",
            "3-Rect,4-Circle,5-Square",
            "6-R.Triangle,7-E.Triangle",
            "8-Rhombus,+/-: Size",
            "X: Clear, ESC: Exit"
        ]
        
        for i, text in enumerate(texts):
            text_color = (200, 200, 200) if i < 3 else (150, 150, 255)
            txt_surf = font.render(text, True, text_color)
            surface.blit(txt_surf, (20, 20 + i*20))

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
                # Color selection
                if event.key == pygame.K_r: current_color = 'red'
                elif event.key == pygame.K_g: current_color = 'green'
                elif event.key == pygame.K_b: current_color = 'blue'
                elif event.key == pygame.K_y: current_color = 'yellow'
                elif event.key == pygame.K_c: current_color = 'cyan'
                elif event.key == pygame.K_m: current_color = 'magenta'
                
                # Tool selection
                if event.key == pygame.K_1: current_tool = 'eraser'
                elif event.key == pygame.K_2: current_tool = 'brush'
                elif event.key == pygame.K_3: current_tool = 'rectangle'
                elif event.key == pygame.K_4: current_tool = 'circle'
                elif event.key == pygame.K_5: current_tool = 'square'
                elif event.key == pygame.K_6: current_tool = 'right_triangle'
                elif event.key == pygame.K_7: current_tool = 'equilateral_triangle'
                elif event.key == pygame.K_8: current_tool = 'rhombus'
                
                # Brush size control
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    brush_radius = min(50, brush_radius + 2)
                elif event.key == pygame.K_MINUS:
                    brush_radius = max(2, brush_radius - 2)
                
                # Clear screen
                if event.key == pygame.K_x:
                    screen.fill((0, 0, 0))

            # Mouse handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos
                drawing = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                if start_pos:
                    end_pos = event.pos
                    color = colors[current_color]
                    
                    # square painting
                    if current_tool == 'square':
                        side = max(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                        rect = pygame.Rect(start_pos, (side, side))
                        pygame.draw.rect(screen, color, rect, 2)
                        
                    # right triangle
                    elif current_tool == 'right_triangle':
                        points = [
                            start_pos,
                            (end_pos[0], start_pos[1]),
                            end_pos
                        ]
                        pygame.draw.polygon(screen, color, points, 2)
                    
                    # equilateral
                    elif current_tool == 'equilateral_triangle':
                        dx = end_pos[0] - start_pos[0]
                        height = int(abs(dx) * (3**0.5)/2)
                        points = [
                            start_pos,
                            (start_pos[0] + dx, start_pos[1]),
                            (start_pos[0] + dx//2, start_pos[1] - height)
                        ]
                        pygame.draw.polygon(screen, color, points, 2)
                    
                    # rhombus
                    elif current_tool == 'rhombus':
                        center = ((start_pos[0]+end_pos[0])//2, (start_pos[1]+end_pos[1])//2)
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        points = [
                            (center[0], start_pos[1]),
                            (end_pos[0], center[1]),
                            (center[0], end_pos[1]),
                            (start_pos[0], center[1])
                        ]
                        pygame.draw.polygon(screen, color, points, 2)
                        
                    # tools
                    elif current_tool == 'rectangle':
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(screen, color, rect, 2)
                    elif current_tool == 'circle':
                        radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                        pygame.draw.circle(screen, color, start_pos, radius, 2)
                        
                drawing = False
                start_pos = None
                
            if event.type == pygame.MOUSEMOTION and drawing and current_tool in ['brush', 'eraser']:
                color = (0, 0, 0) if current_tool == 'eraser' else colors[current_color]
                pygame.draw.circle(screen, color, event.pos, brush_radius)

        # Draw UI panel
        draw_ui(screen, current_color, current_tool, brush_radius)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
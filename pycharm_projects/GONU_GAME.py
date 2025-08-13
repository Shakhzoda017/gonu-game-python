import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Umul Gonu")

font = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()


class Player:
    def init(self):
        self.height = 35
        self.width = 50
        self.circle = 30
        self.cell = 4
        self.color = (255, 255, 255)


def draw_circle(x, y, color):
    pygame.draw.circle(screen, color, [x, y], 30)


def draw_small_circle(x, y, color):
    pygame.draw.circle(screen, color, [x, y], 10)  # small circle for possible moves


def show_message(message, color=(255, 255, 255)):
    text = font.render(message, True, color)
    screen.blit(text, (250, 20))


def show_turn(turn):
    msg = f"{turn} Turn"
    color = (255, 0, 0) if turn == "RED" else (255, 255, 0)
    text = font.render(msg, True, color)
    screen.blit(text, (30, 20))


def is_valid_move(start, end, all_positions):
    return end in moves_map.get(tuple(start), []) and end not in all_positions


def get_valid_moves(pos, all_positions):
    return [p for p in moves_map.get(tuple(pos), []) if p not in all_positions]


def check_win():
    red_moves = any(get_valid_moves(p, player_red + player_yellow) for p in player_red)
    yellow_moves = any(get_valid_moves(p, player_red + player_yellow) for p in player_yellow)

    if not red_moves and not yellow_moves:
        return "DRAW"
    elif not red_moves:
        return "YELLOW"
    elif not yellow_moves:
        return "RED"
    return None


def draw_possible_moves(piece, all_positions):
    valid = get_valid_moves(piece, all_positions)
    for move in valid:
        draw_small_circle(move[0], move[1], (0, 0, 255))


valid_positions = [
    (100, 100), (700, 100), (400, 400), (100, 700), (700, 700)
]

moves_map = {
    (100, 100): [(400, 400), (100, 700), (700, 100)],
    (700, 100): [(400, 400), (700, 700), (100, 100)],
    (400, 400): [(100, 100), (700, 100), (100, 700), (700, 700)],
    (100, 700): [(100, 100), (400, 400)],
    (700, 700): [(700, 100), (400, 400)],
}

player_red = [(100, 100), (700, 100)]
player_yellow = [(100, 700), (700, 700)]

selected_piece = None
turn = "RED"
game_over = False
winner = None
player = Player()
running = True

while running:
    screen.fill((0, 0, 0))

    for pos in valid_positions:
        pygame.draw.circle(screen, (255, 255, 255), pos, 50)

    pygame.draw.line(screen, (255, 0, 0), (100, 100), (700, 700))
    pygame.draw.line(screen, (255, 0, 0), (700, 100), (100, 100))
    pygame.draw.line(screen, (255, 0, 0), (100, 700), (100, 100))
    pygame.draw.line(screen, (255, 0, 0), (700, 700), (700, 100))
    pygame.draw.line(screen, (255, 0, 0), (700, 100), (100, 700))

    for pos in player_red:
        draw_circle(pos[0], pos[1], (255, 0, 0))
    for pos in player_yellow:
        draw_circle(pos[0], pos[1], (255, 255, 0))

    all_positions = player_red + player_yellow
    if selected_piece is not None:
        pieces = player_red if turn == "RED" else player_yellow
        draw_possible_moves(pieces[selected_piece], all_positions)

    if game_over:
        if winner == "RED":
            show_message("Red Wins!", (255, 0, 0))
        elif winner == "YELLOW":
            show_message("Yellow Wins!", (255, 255, 0))
        else:
            show_message("Game Over - Draw", (255, 255, 255))
    else:
        show_turn(turn)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            clicked_pos = None

            for pos in valid_positions:
                dx = pos[0] - mx
                dy = pos[1] - my
                if dx * dx + dy * dy <= 30 * 30:
                    clicked_pos = pos
                    break

            if clicked_pos:
                pieces = player_red if turn == "RED" else player_yellow
                all_positions = player_red + player_yellow
            if selected_piece is None:
                for idx, piece in enumerate(pieces):
                    if piece == clicked_pos:
                        selected_piece = idx
                        break
            else:
                if is_valid_move(pieces[selected_piece], clicked_pos, all_positions):
                    pieces[selected_piece] = clicked_pos
                    turn = "YELLOW" if turn == "RED" else "RED"
                    result = check_win()
                    if result:
                        game_over = True
                        winner = result
                selected_piece = None

            clock.tick(60)

pygame.quit()

import pygame
from pygame.draw import circle
import math
import enum

WIDTH, HEIGHT = 400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
font = pygame.font.Font(None, 30)
WIN.fill((60, 115, 154))


pegs = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}

hidden_eye = pygame.transform.scale(
    pygame.image.load("mastermind/assets/hide.jpg"), (20, 20)
)
visible_eye = pygame.transform.scale(
    pygame.image.load("mastermind/assets/show.jpg"), (20, 20)
)


def make_pegs(displacement: tuple[int, int] = (0, 0)):
    peg_objects = []
    dx, dy = displacement
    for num, key in enumerate(pegs):
        if key == "white" and displacement == (0, 0):
            peg_objects.append(circle(WIN, (255, 255, 255), (355 + dx, 625 + dy), 10))
        elif key == "black" or key == "white":
            continue
        else:
            peg_objects.append(
                circle(WIN, pegs[key], (70 + 50 * num + dx, 700 + dy), 10)
            )

    return peg_objects


def make_check_pegs(displacement: tuple[int, int] = (0, 0)):
    peg_objects = []
    dx, dy = displacement
    for num, col in enumerate([pegs["white"], pegs["red"], pegs["black"]]):
        peg_objects.append(circle(WIN, col, (150 + 50 * num + dx, 700 + dy - 475), 5))

    return peg_objects


def make_code(code: list[str | None], displacement: tuple[int, int] = (0, 0)):

    if code is not None and len(code) != 4:
        raise ValueError("Code must be 4 colors long")
    dx, dy = displacement
    code_objects = []
    for x, col in enumerate(code):
        code_objects.append(
            circle(
                WIN,
                pegs[col] if col is not None else (255, 255, 255),
                (125 + 50 * x + dx, 625 + dy),
                10,
            )
        )
    return code_objects


def draw_board_set_code(code: list[str | None], hidden: bool = False):
    WIN.fill((60, 115, 154))

    board_x = 25
    board_y = 50
    board_width = 350
    board_height = 700
    corner_radius = 20

    pygame.draw.rect(
        WIN,
        (139, 69, 19),
        (board_x, board_y, board_width, board_height),
        border_radius=corner_radius,
    )

    make_pegs()

    for x in range(4):
        for y in range(8):
            circle(WIN, (0, 0, 0), (board_x + 75 * x + 50, board_y + 50 * y + 50), 10)

    for a in range(8):
        for x in range(2):
            for y in range(2):
                circle(
                    WIN,
                    (0, 0, 0),
                    (board_x + 15 * x + 310, board_y + 15 * y + 50 * a + 40),
                    5,
                )

    pygame.draw.rect(WIN, (50, 50, 50), (60, 600, 280, 50), border_radius=10)
    if hidden:
        WIN.blit(hidden_eye, (30, 615))
        return make_code(["black", "black", "black", "black"])
    else:
        WIN.blit(visible_eye, (30, 615))
        return make_code(code)
    # return make_code(code)


def make_guess(guess: list[str | None], displacement: tuple[int, int] = (0, 0)):
    if guess is not None and len(guess) != 4:
        raise ValueError("Guess must be 4 colors long")
    dx, dy = displacement
    guess_objects = []
    for x, col in enumerate(guess):
        guess_objects.append(
            circle(
                WIN,
                pegs[col] if col is not None else (255, 255, 255),
                (125 + 50 * x + dx, 625 + dy),
                10,
            )
        )
    return guess_objects


def draw_board_guess(
    code: list[str | None],
    guess: list[str | None],
    guess_stage: int,
    prev_guesses: list[list[str | None]],
    check: bool = False,
):
    WIN.fill((255, 255, 255))

    board_x = 25
    board_y = 50
    board_width = 350
    board_height = 700
    corner_radius = 20

    pygame.draw.rect(
        WIN,
        (139, 69, 19),
        (board_x, board_y, board_width, board_height),
        border_radius=corner_radius,
    )

    make_pegs((0, -475))

    for y, ting in enumerate(prev_guesses):
        for x, col in enumerate(ting):
            if y == guess_stage - 1 and not check:
                circle(
                    WIN,
                    pegs[col] if col is not None else (255, 255, 255),
                    (board_x + 75 * x + 50, board_y + 50 * y + 250),
                    10,
                )
            else:
                circle(
                    WIN,
                    pegs[col] if col is not None else (0, 0, 0),
                    (board_x + 75 * x + 50, board_y + 50 * y + 250),
                    10,
                )

    for a in range(8):
        for x in range(2):
            for y in range(2):
                circle(
                    WIN,
                    (0, 0, 0),
                    (board_x + 15 * x + 310, board_y + 15 * y + 50 * a + 240),
                    5,
                )

    pygame.draw.rect(WIN, (50, 50, 50), (60, 100, 280, 50), border_radius=10)

    make_code(guess, (0, -500))


def draw_board_rate(
    prev_guesses: list[list[str | None]],
    prev_rates: list[list[str | None]],
    guess_stage: int,
):
    WIN.fill((255, 255, 255))

    board_x = 25
    board_y = 50
    board_width = 350
    board_height = 700
    corner_radius = 20

    pygame.draw.rect(
        WIN,
        (139, 69, 19),
        (board_x, board_y, board_width, board_height),
        border_radius=corner_radius,
    )

    for y, ting in enumerate(prev_guesses):
        for x, col in enumerate(ting):
            circle(
                WIN,
                pegs[col] if col is not None else (0, 0, 0),
                (board_x + 75 * x + 50, board_y + 50 * y + 250),
                10,
            )
    check_pegs = [[], [], [], [], [], [], [], []]
    for a, col_lst in enumerate(prev_rates):
        cnt = -1
        for x in range(2):
            for y in range(2):
                cnt += 1
                check_pegs[guess_stage].append(
                    circle(
                        WIN,
                        pegs[col_lst[cnt]] if col_lst[cnt] is not None else (0, 0, 0),
                        (board_x + 15 * x + 310, board_y + 15 * y + 50 * a + 240),
                        5,
                    )
                )

    pygame.draw.rect(WIN, (50, 50, 50), (60, 100, 280, 50), border_radius=10)

    make_code(prev_rates[guess_stage - 2], (0, -500))

    return check_pegs[guess_stage]


def move_peg(peg, x, y):
    peg.center = (peg.center[0] + x, peg.center[1] + y)


class states(str, enum.Enum):
    code = "code"
    guess = "guess"
    rate = "rate"


def main():
    run = True
    dragging = False
    move_color = None
    code_objects = draw_board_set_code([None, None, None, None])
    current_code = [None, None, None, None]
    hidden = False
    peg_objects = make_pegs()
    state = states.code
    actual_code = [None, None, None, None]
    guess_code = [None, None, None, None]
    guess_stage = 1
    prev_guesses = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]
    check_pegs = None
    prev_rates = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]
    rate_objects = None
    rate = [None, None, None, None]
    while run:
        mx, my = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if state == states.code:
                text = font.render("Set code", True, (0, 0, 0))
                text_rect = text.get_rect(center=(200, 550))
                WIN.blit(text, text_rect)
                checkbox = circle(WIN, (50, 200, 50), (200, 575), 10)
                pygame.draw.line(WIN, (0, 0, 0), (195, 575), (200, 580), 1)
                pygame.draw.line(WIN, (0, 0, 0), (200, 580), (203, 569), 1)
                for num, peg in enumerate(peg_objects):
                    if peg.collidepoint(mx, my):
                        dragging = mouse_down
                        move_color = pegs[list(pegs)[num]]
                if pygame.mouse.get_pressed()[0]:
                    if hidden_eye.get_rect(topleft=(30, 615)).collidepoint(mx, my):
                        hidden = not hidden
                        draw_board_set_code(current_code, hidden)
                    if (
                        checkbox.collidepoint(mx, my)
                        and current_code.count(None) == 0
                        and current_code.count("white") == 0
                    ):
                        actual_code = current_code.copy()
                        state = states.guess
                        peg_objects = make_pegs((0, -475))
                        code_objects = make_code(guess_code, (0, -500))
                if dragging:
                    draw_board_set_code(current_code, hidden)
                    circle(WIN, move_color, (mx, my), 10)
                    for num, code in enumerate(code_objects):
                        if code.collidepoint(mx, my) and not hidden:
                            current_code[num] = dict(zip(pegs.values(), pegs.keys()))[
                                move_color
                            ]
                            break
                    if not mouse_down:
                        dragging = False
                        move_color = None
                        draw_board_set_code(current_code, hidden)
            elif state == states.guess:
                current_code = [None, None, None, None]
                draw_board_guess(current_code, guess_code, guess_stage, prev_guesses)
                checkbox = circle(WIN, (50, 200, 50), (200, 575 - 500), 10)
                pygame.draw.line(WIN, (0, 0, 0), (195, 575 - 500), (200, 580 - 500), 1)
                pygame.draw.line(WIN, (0, 0, 0), (200, 580 - 500), (203, 569 - 500), 1)
                text = font.render("Make your guess", True, (0, 0, 0))
                text_rect = text.get_rect(center=(200, 175))
                WIN.blit(text, text_rect)
                for num, peg in enumerate(peg_objects):
                    if peg.collidepoint(mx, my):
                        dragging = mouse_down
                        move_color = pegs[list(pegs)[num]]
                if dragging:
                    draw_board_guess(
                        current_code, guess_code, guess_stage, prev_guesses
                    )
                    circle(WIN, move_color, (mx, my), 10)
                    for num, code in enumerate(code_objects):
                        if code.collidepoint(mx, my) and not hidden:
                            guess_code[num] = dict(zip(pegs.values(), pegs.keys()))[
                                move_color
                            ]
                            prev_guesses[guess_stage - 1][num] = guess_code[num]
                            break
                    if not mouse_down:
                        dragging = False
                        move_color = None
                        draw_board_guess(
                            current_code, guess_code, guess_stage, prev_guesses
                        )
                if pygame.mouse.get_pressed()[0]:
                    if checkbox.collidepoint(mx, my) and guess_code.count(None) == 0:
                        state = states.rate
                        guess_stage += 1
                        draw_board_guess(
                            current_code, guess_code, guess_stage, prev_guesses, True
                        )

                        # if guess_code == actual_code:
                        #     big_font = pygame.font.Font(None, 100)
                        #     text = font.render("Guesser wins", True, (255, 255, 255))
                        #     text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        #     WIN.blit(text, text_rect)
                        #     pygame.display.update()
                        #     pygame.time.delay(2000)
                        #     run = False
                        # elif guess_stage == 9:
                        #     big_font = pygame.font.Font(None, 100)
                        #     text = font.render("Codemaker wins", True, (255, 255, 255))
                        #     text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        #     WIN.blit(text, text_rect)
                        #     pygame.display.update()
                        #     pygame.time.delay(2000)
                        #     run = False
                        guess_code = [None, None, None, None]
            elif state == states.rate:
                rate_objects = draw_board_rate(prev_guesses, prev_rates, guess_stage)
                check_pegs = make_check_pegs()
                checkbox = circle(WIN, (50, 200, 50), (200, 575 - 500), 10)
                pygame.draw.line(WIN, (0, 0, 0), (195, 575 - 500), (200, 580 - 500), 1)
                pygame.draw.line(WIN, (0, 0, 0), (200, 580 - 500), (203, 569 - 500), 1)
                text = font.render("Make your correction", True, (0, 0, 0))
                text_rect = text.get_rect(center=(200, 175))
                WIN.blit(text, text_rect)
                for num, peg in enumerate(check_pegs):
                    if peg.collidepoint(mx, my):
                        dragging = mouse_down
                        move_color = [pegs["white"], pegs["red"], pegs["black"]][num]
                if dragging:
                    draw_board_rate(prev_guesses, prev_rates, guess_stage)
                    circle(WIN, move_color, (mx, my), 5)
                    for num, code in enumerate(code_objects):
                        if code.collidepoint(mx, my):
                            rate[num] = dict(zip(pegs.values(), pegs.keys()))[
                                move_color
                            ]
                            prev_rates[guess_stage - 2][num] = rate[num]
                            break
                    if not mouse_down:
                        dragging = False
                        move_color = None
                        draw_board_rate(prev_guesses, prev_rates, guess_stage)
                if checkbox.collidepoint(mx, my):
                    state = states.guess
        pygame.display.update()

    pygame.quit()


main()

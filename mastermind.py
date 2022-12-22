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


def make_code(
    code: list[str | None],
    displacement: tuple[int, int] = (0, 0),
    alternate_color: tuple[int, int, int] = (255, 255, 255),
):

    if code is not None and len(code) != 4:
        raise ValueError("Code must be 4 colors long")
    dx, dy = displacement
    code_objects = []
    for x, col in enumerate(code):
        code_objects.append(
            circle(
                WIN,
                pegs[col] if col is not None else alternate_color,
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
    prev_rates: list[list[str | None]] = None,
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

    check_pegs = [[], [], [], [], [], [], [], []]
    for a, col_lst in enumerate(prev_rates):
        cnt = -1
        for x in range(2):
            for y in range(2):
                cnt += 1
                check_pegs[guess_stage - 1].append(
                    circle(
                        WIN,
                        pegs[col_lst[cnt]] if col_lst[cnt] is not None else (0, 0, 0),
                        (board_x + 15 * x + 310, board_y + 15 * y + 50 * a + 240),
                        5,
                    )
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
                check_pegs[guess_stage - 1].append(
                    circle(
                        WIN,
                        pegs[col_lst[cnt]] if col_lst[cnt] is not None else (0, 0, 0),
                        (board_x + 15 * x + 310, board_y + 15 * y + 50 * a + 240),
                        5,
                    )
                )

    pygame.draw.rect(WIN, (50, 50, 50), (60, 100, 280, 50), border_radius=10)

    make_code(prev_rates[guess_stage - 2], (0, -500), (0, 0, 0))

    return check_pegs[guess_stage - 1]


def move_peg(peg, x, y):
    peg.center = (peg.center[0] + x, peg.center[1] + y)


class states(str, enum.Enum):
    code = "code"
    guess = "guess"
    rate = "rate"


class Board:
    def __init__(self):
        self.dragging = False
        self.move_color = None
        self.code_objects = draw_board_set_code([None, None, None, None])
        self.current_code = [None, None, None, None]
        self.hidden = False
        self.peg_objects = make_pegs()
        self.state = states.code
        self.actual_code = [None, None, None, None]
        self.guess_code = [None, None, None, None]
        self.guess_stage = 1
        self.prev_guesses = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
        ]
        self.check_pegs = None
        self.prev_rates = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
        ]
        self.rate_objects = None
        self.rate = [None, None, None, None]

    def make_pegs(self, displacement: tuple[int, int] = (0, 0)):
        peg_objects = []
        dx, dy = displacement
        for num, key in enumerate(pegs):
            if key == "white" and displacement == (0, 0):
                peg_objects.append(
                    circle(WIN, (255, 255, 255), (355 + dx, 625 + dy), 10)
                )
            elif key == "black" or key == "white":
                continue
            else:
                peg_objects.append(
                    circle(WIN, pegs[key], (70 + 50 * num + dx, 700 + dy), 10)
                )

        return peg_objects

    def draw_board_set_code(self, code):
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
                circle(
                    WIN, (0, 0, 0), (board_x + 75 * x + 50, board_y + 50 * y + 50), 10
                )

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
        if self.hidden:
            WIN.blit(hidden_eye, (30, 615))
            return make_code(["black", "black", "black", "black"])
        else:
            WIN.blit(visible_eye, (30, 615))
            return make_code(code)

    def draw_checkbox_code(self):
        checkbox = circle(WIN, (50, 200, 50), (200, 575), 10)
        pygame.draw.line(WIN, (0, 0, 0), (195, 575), (200, 580), 1)
        pygame.draw.line(WIN, (0, 0, 0), (200, 580), (203, 569), 1)
        return checkbox

    def make_text(self, text, pos, color=(0, 0, 0)):
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = pos
        WIN.blit(text, text_rect)

    def check_peg_drag(self, mouse_pos, mouse_down):
        mx, my = mouse_pos
        for num, peg in enumerate(self.peg_objects):
            if peg.collidepoint(mx, my):
                self.dragging = mouse_down
                self.move_color = pegs[list(pegs)[num]]

    def eye_click(self, mouse_pos):
        mx, my = mouse_pos
        if hidden_eye.get_rect(topleft=(30, 615)).collidepoint(mx, my):
            self.hidden = not self.hidden
            draw_board_set_code(self.current_code, self.hidden)

    def checkbox_click_code(
        self,
        mouse_pos,
        checkbox,
    ):
        mx, my = mouse_pos
        if (
            checkbox.collidepoint(mx, my)
            and self.current_code.count(None) == 0
            and self.current_code.count("white") == 0
        ):
            self.actual_code = self.current_code.copy()
            self.state = states.guess
            self.peg_objects = make_pegs((0, -475))
            self.code_objects = make_code(self.guess_code, (0, -500))

    def set_peg_code(self, mouse_pos, mouse_down):
        mx, my = mouse_pos
        if self.dragging:
            self.draw_board_set_code(self.current_code)
            circle(WIN, self.move_color, (mx, my), 10)
            for num, code in enumerate(self.code_objects):
                if code.collidepoint(mx, my) and not self.hidden:
                    self.current_code[num] = dict(zip(pegs.values(), pegs.keys()))[
                        self.move_color
                    ]
                    break

            if not mouse_down:
                self.dragging = False
                self.move_color = None
                self.draw_board_set_code(self.current_code)

        if self.dragging and mouse_down:
            for num, peg in enumerate(self.code_objects):
                if peg.collidepoint(mx, my):
                    self.current_code[num] = dict(zip(pegs.values(), pegs.keys()))[
                        self.move_color
                    ]


def main():
    run = True

    board = Board()

    while run:
        mx, my = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if board.state == states.code:
                board.make_text("Set code", (200, 550))
                checkbox = board.draw_checkbox_code()
                board.check_peg_drag((mx, my), mouse_down)

                if pygame.mouse.get_pressed()[0]:
                    board.eye_click((mx, my))

                    board.checkbox_click_code((mx, my), checkbox)

                board.set_peg_code((mx, my), mouse_down)

            elif board.state == states.guess:
                board.current_code = [None, None, None, None]
                draw_board_guess(
                    board.current_code,
                    board.guess_code,
                    board.guess_stage,
                    board.prev_guesses,
                    prev_rates=board.prev_rates,
                )
                checkbox = circle(WIN, (50, 200, 50), (200, 575 - 500), 10)
                pygame.draw.line(WIN, (0, 0, 0), (195, 575 - 500), (200, 580 - 500), 1)
                pygame.draw.line(WIN, (0, 0, 0), (200, 580 - 500), (203, 569 - 500), 1)
                text = font.render("Make your guess", True, (0, 0, 0))
                text_rect = text.get_rect(center=(200, 175))
                WIN.blit(text, text_rect)
                for num, peg in enumerate(board.peg_objects):
                    if peg.collidepoint(mx, my):
                        board.dragging = mouse_down
                        board.move_color = pegs[list(pegs)[num]]
                if board.dragging:
                    draw_board_guess(
                        board.current_code,
                        board.guess_code,
                        board.guess_stage,
                        board.prev_guesses,
                        prev_rates=board.prev_rates,
                    )
                    circle(WIN, board.move_color, (mx, my), 10)
                    for num, code in enumerate(board.code_objects):
                        if code.collidepoint(mx, my) and not board.hidden:
                            board.guess_code[num] = dict(
                                zip(pegs.values(), pegs.keys())
                            )[board.move_color]
                            board.prev_guesses[board.guess_stage - 1][
                                num
                            ] = board.guess_code[num]
                            break
                    if not mouse_down:
                        board.dragging = False
                        board.move_color = None
                        draw_board_guess(
                            board.current_code,
                            board.guess_code,
                            board.guess_stage,
                            board.prev_guesses,
                            prev_rates=board.prev_rates,
                        )
                if pygame.mouse.get_pressed()[0]:
                    if (
                        checkbox.collidepoint(mx, my)
                        and board.guess_code.count(None) == 0
                    ):
                        board.state = states.rate
                        board.guess_stage += 1

                        if board.guess_code == board.actual_code:
                            text = font.render("Guesser wins", True, (255, 255, 255))
                            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            WIN.blit(text, text_rect)
                            pygame.display.update()
                            pygame.time.delay(2000)
                            run = False
                        elif board.guess_stage == 9:
                            text = font.render("Codemaker wins", True, (255, 255, 255))
                            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            WIN.blit(text, text_rect)
                            pygame.display.update()
                            pygame.time.delay(2000)
                            run = False
                        draw_board_guess(
                            board.current_code,
                            board.guess_code,
                            board.guess_stage,
                            board.prev_guesses,
                            True,
                            prev_rates=board.prev_rates,
                        )
                        board.guess_code = [None, None, None, None]
            elif board.state == states.rate:
                board.rate_objects = draw_board_rate(
                    board.prev_guesses, board.prev_rates, board.guess_stage
                )
                board.check_pegs = make_check_pegs()
                checkbox = circle(WIN, (50, 200, 50), (200, 575 - 500), 10)
                pygame.draw.line(WIN, (0, 0, 0), (195, 575 - 500), (200, 580 - 500), 1)
                pygame.draw.line(WIN, (0, 0, 0), (200, 580 - 500), (203, 569 - 500), 1)
                text = font.render("Make your correction", True, (0, 0, 0))
                text_rect = text.get_rect(center=(200, 175))
                WIN.blit(text, text_rect)
                for num, peg in enumerate(board.check_pegs):
                    if peg.collidepoint(mx, my):
                        board.dragging = mouse_down
                        board.move_color = [pegs["white"], pegs["red"], pegs["black"]][
                            num
                        ]
                if board.dragging:
                    draw_board_rate(
                        board.prev_guesses, board.prev_rates, board.guess_stage
                    )
                    circle(WIN, board.move_color, (mx, my), 5)
                    for num, code in enumerate(board.code_objects):
                        if code.collidepoint(mx, my):
                            board.rate[num] = dict(zip(pegs.values(), pegs.keys()))[
                                board.move_color
                            ]
                            board.prev_rates[board.guess_stage - 2][num] = board.rate[
                                num
                            ]
                            break
                    if not mouse_down:
                        board.dragging = False
                        board.move_color = None
                        draw_board_rate(
                            board.prev_guesses, board.prev_rates, board.guess_stage
                        )
                if pygame.mouse.get_pressed()[0]:

                    # TODO: Fix this
                    if checkbox.collidepoint(mx, my):
                        board.state = states.guess
                        for num, peg in enumerate(board.rate):
                            if peg == None:
                                board.rate[num] = pegs["black"]

                            if peg == "red":
                                for guessed_peg in board.prev_guesses[
                                    board.guess_stage - 1
                                ]:
                                    if not guessed_peg == board.actual_code[num]:
                                        text = font.render(
                                            "You have made a wrong correction",
                                            True,
                                            (0, 0, 0),
                                        )
                                        text_rect = text.get_rect(center=(200, 250))
                                        WIN.blit(text, text_rect)
                                        pygame.display.update()
                                        pygame.time.delay(2000)
                                        board.state = states.rate
                                        break

                            elif peg == "white":
                                for guessed_peg in board.prev_guesses[
                                    board.guess_stage - 1
                                ]:
                                    if not (
                                        guessed_peg != board.actual_code[num]
                                        and guessed_peg in board.actual_code
                                    ):
                                        text = font.render(
                                            "You have made a wrong correction",
                                            True,
                                            (0, 0, 0),
                                        )
                                        text_rect = text.get_rect(center=(200, 250))
                                        WIN.blit(text, text_rect)
                                        pygame.display.update()
                                        pygame.time.delay(2000)
                                        board.state = states.rate
                                        break

                            elif peg == "black":
                                for guessed_peg in board.prev_guesses[
                                    board.guess_stage - 1
                                ]:
                                    if guessed_peg == board.actual_code[num]:
                                        text = font.render(
                                            "You have made a wrong correction",
                                            True,
                                            (0, 0, 0),
                                        )
                                        text_rect = text.get_rect(center=(200, 250))
                                        WIN.blit(text, text_rect)
                                        pygame.display.update()
                                        pygame.time.delay(2000)
                                        board.state = states.rate
                                        break
                        board.rate = [None, None, None, None]
                        draw_board_rate(
                            board.prev_guesses, board.prev_rates, board.guess_stage
                        )

        pygame.display.update()

    pygame.quit()


main()

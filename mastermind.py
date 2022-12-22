import enum
import math

import pygame
from pygame.draw import circle

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

hidden_eye = pygame.transform.scale(pygame.image.load("assets/hide.jpg"), (20, 20))
visible_eye = pygame.transform.scale(pygame.image.load("assets/show.jpg"), (20, 20))


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


class states(str, enum.Enum):
    code = "code"
    guess = "guess"
    rate = "rate"


class Board:
    def __init__(self):
        self.dragging = False
        self.move_color = None
        self.code_objects = [None, None, None, None]
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

    def make_code(
        self,
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

    def make_check_pegs(self, displacement: tuple[int, int] = (0, 0)):
        peg_objects = []
        dx, dy = displacement
        for num, col in enumerate([pegs["white"], pegs["red"], pegs["black"]]):
            peg_objects.append(
                circle(WIN, col, (150 + 50 * num + dx, 700 + dy - 475), 5)
            )

        return peg_objects

    def draw_big_peg_holes_code(self, displacement: tuple[int, int]):
        dx, dy = displacement
        for x in range(4):
            for y in range(8):
                circle(WIN, (0, 0, 0), (dx + 75 * x + 50, dy + 50 * y + 50), 10)

    def draw_small_peg_holes_code(self, displacement: tuple[int, int]):
        dx, dy = displacement
        for a in range(8):
            for x in range(2):
                for y in range(2):
                    circle(
                        WIN,
                        (0, 0, 0),
                        (dx + 15 * x + 310, dy + 15 * y + 50 * a + 40),
                        5,
                    )

    def draw_big_peg_holes_guess(self, displacement: tuple[int, int], check: bool):
        dx, dy = displacement
        for y, ting in enumerate(self.prev_guesses):
            for x, col in enumerate(ting):
                if y == self.guess_stage - 1 and not check:
                    circle(
                        WIN,
                        pegs[col] if col is not None else (255, 255, 255),
                        (dx + 75 * x + 50, dy + 50 * y + 250),
                        10,
                    )
                else:
                    circle(
                        WIN,
                        pegs[col] if col is not None else (0, 0, 0),
                        (dx + 75 * x + 50, dy + 50 * y + 250),
                        10,
                    )

    def hide_code(self, code):
        if self.hidden:
            WIN.blit(hidden_eye, (30, 615))
            return self.make_code(["black", "black", "black", "black"])
        else:
            WIN.blit(visible_eye, (30, 615))
            return self.make_code(code)

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

        self.make_pegs()

        self.draw_big_peg_holes_code((board_x, board_y))

        self.draw_small_peg_holes_code((board_x, board_y))

        pygame.draw.rect(WIN, (50, 50, 50), (60, 600, 280, 50), border_radius=10)

        return self.hide_code(code)

    def draw_checkbox(self, displacement: tuple[int, int] = (0, 0)):
        dx, dy = displacement
        checkbox = circle(WIN, (50, 200, 50), (200 + dx, 575 + dy), 10)
        pygame.draw.line(WIN, (0, 0, 0), (195 + dx, 575 + dy), (200 + dx, 580 + dy), 1)
        pygame.draw.line(WIN, (0, 0, 0), (200 + dx, 580 + dy), (203 + dx, 569 + dy), 1)
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
            self.draw_board_set_code(self.current_code)

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
            self.peg_objects = self.make_pegs((0, -475))
            self.code_objects = self.make_code(self.guess_code, (0, -500))
            self.current_code = [None, None, None, None]

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

    def draw_board_guess(self, check=False):

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

        self.make_pegs((0, -475))

        self.draw_big_peg_holes_guess((board_x, board_y), check)

        check_pegs = [[], [], [], [], [], [], [], []]
        for a, col_lst in enumerate(self.prev_rates):
            cnt = -1
            for x in range(2):
                for y in range(2):
                    cnt += 1
                    check_pegs[self.guess_stage - 1].append(
                        circle(
                            WIN,
                            pegs[col_lst[cnt]]
                            if col_lst[cnt] is not None
                            else (0, 0, 0),
                            (board_x + 15 * x + 310, board_y + 15 * y + 50 * a + 240),
                            5,
                        )
                    )

        pygame.draw.rect(WIN, (50, 50, 50), (60, 100, 280, 50), border_radius=10)

        self.make_code(self.guess_code, (0, -500))

    def guess_dragging(self, mouse_pos, mouse_down):
        mx, my = mouse_pos
        circle(WIN, self.move_color, (mx, my), 10)
        for num, code in enumerate(self.code_objects):
            if code.collidepoint(mx, my) and not self.hidden:
                self.guess_code[num] = dict(zip(pegs.values(), pegs.keys()))[
                    self.move_color
                ]
                self.prev_guesses[self.guess_stage - 1][num] = self.guess_code[num]
                break
        if not mouse_down:
            self.dragging = False
            self.move_color = None
            self.draw_board_guess()

    def check_guess(self):
        if self.guess_code == self.actual_code:
            text = font.render("Guesser wins", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WIN.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            return False
        elif self.guess_stage == 9:
            text = font.render("Codemaker wins", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WIN.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            return False
        return True

    def click_checkbox_guess(self, mouse_pos, checkbox):
        mx, my = mouse_pos
        if checkbox.collidepoint(mx, my) and self.guess_code.count(None) == 0:
            self.state = states.rate
            self.guess_stage += 1
            self.draw_board_guess(check=True)
            self.guess_code = [None, None, None, None]
            return self.check_guess()
        return True

    def draw_board_rate(self):
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

        for y, ting in enumerate(self.prev_guesses):
            for x, col in enumerate(ting):
                circle(
                    WIN,
                    pegs[col] if col is not None else (0, 0, 0),
                    (board_x + 75 * x + 50, board_y + 50 * y + 250),
                    10,
                )
        check_pegs = [[], [], [], [], [], [], [], []]
        for a, col_lst in enumerate(self.prev_rates):
            cnt = -1
            for x in range(2):
                for y in range(2):
                    cnt += 1
                    check_pegs[self.guess_stage - 1].append(
                        circle(
                            WIN,
                            pegs[col_lst[cnt]]
                            if col_lst[cnt] is not None
                            else (0, 0, 0),
                            (board_x + 15 * x + 310, board_y + 15 * y + 50 * a + 240),
                            5,
                        )
                    )

        pygame.draw.rect(WIN, (50, 50, 50), (60, 100, 280, 50), border_radius=10)

        self.make_code(self.prev_rates[self.guess_stage - 2], (0, -500), (0, 0, 0))

        return check_pegs[self.guess_stage - 1]

    def rate_peg_drag(self, mouse_pos, mouse_down):
        mx, my = mouse_pos
        for num, peg in enumerate(self.check_pegs):
            if peg.collidepoint(mx, my):
                self.dragging = mouse_down
                self.move_color = [pegs["white"], pegs["red"], pegs["black"]][num]

    def set_peg_rate(self, mouse_pos, mouse_down):
        mx, my = mouse_pos
        if self.dragging:
            self.draw_board_rate()
            circle(WIN, self.move_color, (mx, my), 5)
            for num, code in enumerate(self.code_objects):
                if code.collidepoint(mx, my):
                    self.rate[num] = dict(zip(pegs.values(), pegs.keys()))[
                        self.move_color
                    ]
                    self.prev_rates[self.guess_stage - 2][num] = self.rate[num]
                    break
            if not mouse_down:
                self.dragging = False
                self.move_color = None
                self.draw_board_rate()

    def click_checkbox_rate(self, mouse_pos, checkbox):
        mx, my = mouse_pos
        if checkbox.collidepoint(mx, my):
            red = 0
            white = 0
            black = 0

            for num, peg in enumerate(self.rate):
                if peg is None:
                    self.rate[num] = "black"
            for num, actual_peg in enumerate(self.actual_code):
                if self.prev_guesses[self.guess_stage - 2][num] == actual_peg:
                    red += 1
                elif (
                    self.prev_guesses[self.guess_stage - 2][num]
                    in self.actual_code[num:]
                ):
                    white += 1
                else:
                    black += 1

            if (
                self.rate.count("red") == red
                and self.rate.count("white") == white
                and self.rate.count("black") == black
            ):
                self.prev_rates[self.guess_stage - 2] = self.rate
                self.rate = [None, None, None, None]
                self.draw_board_rate()
                self.state = states.guess
            else:
                self.make_text("You have made a wrong correction", (200, 250))


def main():
    run = True

    board = Board()
    board.code_objects = board.draw_board_set_code([None, None, None, None])
    while run:
        mx, my = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if board.state == states.code:

                board.make_text("Set code", (200, 550))
                checkbox = board.draw_checkbox()
                board.check_peg_drag((mx, my), mouse_down)

                if pygame.mouse.get_pressed()[0]:
                    board.eye_click((mx, my))

                    board.checkbox_click_code((mx, my), checkbox)

                board.set_peg_code((mx, my), mouse_down)

            elif board.state == states.guess:

                board.draw_board_guess()
                checkbox = board.draw_checkbox((0, -500))
                board.make_text("Make your guess", (200, 175))
                board.check_peg_drag((mx, my), mouse_down)

                if board.dragging:
                    board.draw_board_guess()
                    board.guess_dragging((mx, my), mouse_down)

                if pygame.mouse.get_pressed()[0]:
                    run = board.click_checkbox_guess((mx, my), checkbox)
            elif board.state == states.rate:
                board.rate_objects = board.draw_board_rate()
                board.check_pegs = board.make_check_pegs()
                checkbox = board.draw_checkbox((0, -500))
                board.make_text("Make your correction", (200, 175), (0, 0, 0))
                board.rate_peg_drag((mx, my), mouse_down)

                board.set_peg_rate((mx, my), mouse_down)

                if pygame.mouse.get_pressed()[0]:
                    board.click_checkbox_rate((mx, my), checkbox)
                    # TODO: Fix this

        pygame.display.update()

    pygame.quit()


main()

from turtle import Turtle, Screen
import random
import time


class Snake:
    def __init__(self):
        self.old_position = (0.0, 0.0)
        self.current_direction = ""
        screen.listen()
        screen.onkeypress(self.look_up, 'Up')
        screen.onkeypress(self.look_down, 'Down')
        screen.onkeypress(self.look_left, 'Left')
        screen.onkeypress(self.look_right, 'Right')

        self.snake_squares = {
            1: Turtle(),
            2: Turtle(),
            3: Turtle(),
        }

        for square in self.snake_squares:
            self.design_square(self.snake_squares[square])
        self.snake_head = self.snake_squares[1]

    def design_square(self, current_square):
        current_square.penup()
        current_square.shape('square')
        current_square.color('white')
        current_square.shapesize(1.00)
        current_square.pensize(1)

    def add_square(self, new_score):
        square_amount = new_score + 3
        self.snake_squares[square_amount] = Turtle()
        self.design_square(self.snake_squares[square_amount])
        self.snake_squares[square_amount].setposition(self.old_position)

    def look_up(self):
        if self.current_direction == "down":
            return
        self.snake_head.setheading(90)
        self.current_direction = "up"


    def look_down(self):
        if self.current_direction == "up":
            return
        self.snake_head.setheading(270)
        self.current_direction = "down"

    def look_left(self):
        if self.current_direction == "right":
            return
        self.snake_head.setheading(180)
        self.current_direction = "left"

    def look_right(self):
        if self.current_direction == "left":
            return
        self.snake_head.setheading(0)
        self.current_direction = "right"

    def move(self):
        self.old_position = self.snake_head.position()
        self.snake_head.forward(10.00)

        all_square_positions = []

        for square in self.snake_squares:
            if square != 1:
                next_square = self.snake_squares[square]
                new_position = (round(self.old_position[0], 1), round(self.old_position[1], 1))
                self.old_position = next_square.position()
                next_square.setposition(new_position)
                all_square_positions.append(new_position)

        snake_head_pos = (round(self.snake_head.position()[0], 1), round(self.snake_head.position()[1], 1))
        return snake_head_pos, all_square_positions

    def check_self_hit(self, head_position, tail_positions):
        if head_position in tail_positions:
            return False
        else:
            return True


class Board:
    def __init__(self, height):
        self.score_board = Turtle()
        self.height = height

        self.score = 0

    def add_to_score(self, old_score):
        self.score_board.reset()
        self.score_board.hideturtle()
        self.score_board.setposition(0, self.height + 20)
        self.score_board.color('white')
        self.score = old_score + 1
        self.score_board.write(arg=f"Score: {self.score}", font=('Arial', 25, "normal"), align='center')
        return self.score

    def game_over(self):
        self.score_board.setposition(0.0, 100.0)
        self.score_board.write(arg=f"GAME OVER", font=('Arial', 20, "normal"), align='center')
        self.score_board.setposition(0.0, 70.0)
        self.score_board.write(arg=f"Your final Score: {self.score}", font=('Arial', 20, "normal"), align='center')


class Border:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.positive_borders = [self.width, self.height]
        self.negative_borders = [- self.width, - self.height]

    def check_borders(self, snake_position):
        no_hit = True
        for wall in self.positive_borders:
            if snake_position[0] >= wall:
                no_hit = False
            elif snake_position[1] >= wall:
                no_hit = False
            else:
                pass
        for wall in self.negative_borders:
            if snake_position[0] <= wall:
                no_hit = False
            elif snake_position[1] <= wall:
                no_hit = False
            else:
                pass
        return no_hit

    def print_border(self, width, height):
        line = Turtle()
        line.hideturtle()
        line.setposition(-float(width), -float(height))
        line.shape("circle")
        line.speed('fastest')
        line.color('white')
        for wall in range(4):
            line.forward(800)
            line.left(90)


class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.food = Turtle()
        self.food.hideturtle()
        self.food.speed('fastest')
        self.food.penup()
        self.food.pensize(3)
        self.food.shape('circle')
        self.food.color('purple')

    def create_food(self):
        self.food.showturtle()
        self.food.clear()
        return self.random_position()

    def random_position(self):
        x_min = -self.width + 10
        x_max = self.width - 10
        y_min = -self.height + 10
        y_max = self.height - 10

        x = 11
        y = 11
        while x % 10.00 != 0.00:
            x = float(random.randint(x_min, x_max))

        while y % 10.00 != 0.00:
            y = float(random.randint(y_min, y_max))

        self.food.setposition((x, y))

        x += 10.00
        y += 10.00

        all_possible_hits = []
        for hits in range(3):
            all_possible_hits.append((round(x, 1), round(y - 10.00, 1)))
            x -= 10.00

        for hits in range(3):
            all_possible_hits.append((round(x + 10.00, 1), round(y, 1)))
            y -= 10.00

        return all_possible_hits

    def erase_food(self):
        self.food.hideturtle()

 
screen = Screen()
screen.tracer(0)
field_width = 400
field_height = 400
screen.bgcolor("black")
border = Border(field_width, field_height)
border.print_border(field_width, field_height)
snake = Snake()
food = Food(field_width, field_height)

board = Board(field_height)
current_score = board.add_to_score(-1)
current_food_positions = food.create_food()
snake_alive = True
screen.update()

snake_path = []
while snake_alive:
    snake_speed = 0.030
    time.sleep(snake_speed)
    screen.update()
    snake_current_position, all_positions = snake.move()
    snake_path.append(snake_current_position)
    if snake.check_self_hit(snake_current_position, all_positions):
        if border.check_borders(snake_current_position):
            if snake_current_position in current_food_positions:
                current_score = board.add_to_score(current_score)
                snake.add_square(current_score)
                food.erase_food()
                current_food_positions = food.create_food()
                snake_speed -= 0.001
                screen.update()
        else:
            board.game_over()
            snake_alive = False
    else:
        board.game_over()
        snake_alive = False

screen.exitonclick()

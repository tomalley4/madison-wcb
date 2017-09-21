import random
import requests
import turtle

### Implementation details

# Global mutable state. Forgive me.
state = {
    'connected_to_bot': False,
    'window': None,
    'turtle': None,
}

# These measurements are in "steps", which are basically pixels.
WCB_WIDTH = 620
WCB_HEIGHT = 450

def make_cnc_request(endpoint):
    if state['connected_to_bot']:
        requests.get('http://localhost:4242/' + endpoint)


### Public API

def initialize():
    try:
        requests.get('http://localhost:4242/poll')
        state['connected_to_bot'] = True
    except requests.exceptions.ConnectionError:
        state['connected_to_bot'] = False

    # set up turtle
    state['window'] = turtle.Screen()
    state['window'].setup(width=WCB_WIDTH, height=WCB_HEIGHT)
    state['turtle'] = turtle.Turtle()
    state['turtle'].width(5)

    # set up watercolorbot brush
    brush_up()
    park()

def cleanup():
    brush_up()
    wash_brush()
    park()

def park():
    make_cnc_request("park")

def wash_brush():
    make_cnc_request("pen.wash")

def get_color(index):
    if index in range(0, 8):
        make_cnc_request("tool.color./" + str(index))

        colors = ["black", "red", "orange", "yellow", "green", "blue", "purple", "brown"]
        state['turtle'].color(colors[index])

    else:
        print("Color indexes must be between 0 and 7, but you gave me: " + index)

def brush_down():
    make_cnc_request("pen.down")
    state['turtle'].pendown()

    # Wiggle the turtle one step so that it marks a dot on the turtle canvas.
    state['turtle'].forward(1)
    state['turtle'].backward(1)

def brush_up():
    make_cnc_request("pen.up")
    state['turtle'].penup()

def move_to(x, y):
    make_cnc_request("coord/{0}/{1}".format(x, y))
    state['turtle'].goto(x, y)

def point_in_direction(angle):
    make_cnc_request("move.absturn./" + str(angle))
    state['turtle'].setheading(90 - angle)

def move_forward(num_steps):
    make_cnc_request("move.forward./" + str(num_steps))
    state['turtle'].forward(num_steps)

def turn_left(relative_angle):
    make_cnc_request("move.left./" + str(relative_angle))
    state['turtle'].left(relative_angle)

def turn_right(relative_angle):
    make_cnc_request("move.right./" + str(relative_angle))
    state['turtle'].right(relative_angle)

def get_position():
    return state['turtle'].position()


### Test program

def draw_flower(x, y):
    brush_up()
    wash_brush()
    get_color(5)

    move_to(x, y)
    for _ in range(15):
        for _ in range(5):
            turn_left(random.randrange(-90, 90))
            move_forward(random.randrange(5, 10))
            brush_down()
            brush_up()
            move_to(x, y)
        y = y + 3

    for _ in range(5):
        turn_left(random.randrange(-90, 90))
        move_forward(random.randrange(1, 6))
        brush_down()
        brush_up()
        move_to(x, y)


def flower_scene():
    initialize()
    wash_brush()
    get_color(4) # green

    # stem 1
    move_to(-100, -145)
    point_in_direction(20)
    brush_down()
    for _ in range(25):
        move_forward(5)
        turn_left(1)
    for _ in range(20):
        move_forward(5)
        turn_right(1)

    x1, y1 = get_position()
    brush_up()

    # stem 2
    move_to(-100, -145)
    point_in_direction(0)
    brush_down()
    for _ in range(25):
        move_forward(5)
        turn_left(1)

    x2, y2 = get_position()
    brush_up()

    # stem 3
    move_to(-30, -145)
    point_in_direction(0)
    brush_down()
    for _ in range(15):
        move_forward(5)
        turn_left(1)

    x3, y3 = get_position()

    # flowers
    draw_flower(x1, y1)
    draw_flower(x2, y2)
    draw_flower(x3, y3)

    wash_brush()
    park()


flower_scene()

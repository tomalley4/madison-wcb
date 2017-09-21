import requests
import turtle

### Implementation details

# Global mutable state. Forgive me.
state = {
    'connected_to_bot': False,
}

def make_cnc_request(endpoint):
    if state['connected_to_bot']:
        requests.get("http://localhost:4242/" + endpoint)

### Public API

def initialize():
    try:
        requests.get("http://localhost:4242/poll")
        state['connected_to_bot'] = True
    except requests.exceptions.ConnectionError:
        state['connected_to_bot'] = False

    brush_up()
    park()
    # reset turtle
    # TODO how to deal with scratch positions vs turtle positions? make a utility conversion function

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
    else:
        print("Color indexes must be between 0 and 7, but you gave me: " + index)

def brush_down():
    make_cnc_request("pen.down")

def brush_up():
    make_cnc_request("pen.up")

def move_to(x, y):
    make_cnc_request("coord/{0}/{1}".format(x, y))

def point_in_direction(angle):
    make_cnc_request("move.absturn./" + str(angle))

def move_forward(num_steps):
    make_cnc_request("move.forward./" + str(num_steps))

def turn_left(relative_angle):
    make_cnc_request("move.left./" + str(relative_angle))

def turn_right(relative_angle):
    make_cnc_request("move.right./" + str(relative_angle))

# Test program


def flower_scene():
    initialize()
    wash_brush()
    get_color(4) # green

    move_to(-100, -145)
    point_in_direction(20)

    # stem
    brush_down()
    for _ in range(25):
        move_forward(5)
        turn_left(1)
    for _ in range(20):
        move_forward(5)
        turn_right(1)






     # TODO record current x, y position - get them from turtle?
     # ugh shit

    # flower
    #brush_up()
    #wash_brush()
    #get_color(5)

    wash_brush()
    park()


flower_scene()

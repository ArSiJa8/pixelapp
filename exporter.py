def export_to_turtle(commands):
    turtle_code = [
        "import turtle",
        "t = turtle.Turtle()",
        "screen = turtle.Screen()",
        "screen.setup(800, 600)",
        "t.speed(0)",
        "",
        "# --- Begin generated drawing commands ---"
    ]

    for cmd in commands:
        if cmd["type"] == "move":
            x, y = cmd["x"], cmd["y"]
            turtle_code.append(f"t.penup(); t.goto({x}, {y}); t.pendown()")
        elif cmd["type"] == "line":
            x, y = cmd["x"], cmd["y"]
            turtle_code.append(f"t.goto({x}, {y})")
        elif cmd["type"] == "color":
            c = cmd["value"]
            turtle_code.append(f"t.color('{c}')")
        elif cmd["type"] == "pensize":
            s = cmd["value"]
            turtle_code.append(f"t.pensize({s})")

    turtle_code.append("# --- End drawing commands ---")
    turtle_code.append("turtle.done()")

    return "\n".join(turtle_code)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Diese Farben werden im Frontend genutzt — gleiche Reihenfolge wie dort
PALETTE = ["#2596be", "#f6f6f6", "#3f2a29", "#caa62c", "#9c6908", "#910102", "#f9d1c0", "#3f2a29"]

def grid_to_turtle_script(grid, pixel_size=40, canvas_width=8, canvas_height=8):
    """
    grid: list of 8 lists with hex color strings
    Erzeugt ein Turtle-Script, das das 8x8-Pixelbild zeichnet.
    Wir zeichnen gefüllte Quadrate, so dass das Script in pythonsandbox.com läuft.
    pixel_size: Größe pro Pixel in Turtle-Einheiten (kann angepasst werden)
    """
    lines = []
    lines.append("import turtle")
    lines.append("t = turtle.Turtle()")
    lines.append("screen = turtle.Screen()")
    # Setup so das Bild mittig und sichtbar ist
    width = pixel_size * canvas_width
    height = pixel_size * canvas_height
    lines.append(f"screen.setup(width={max(width+100,400)}, height={max(height+100,400)})")
    lines.append("t.speed(0)")
    lines.append("t.hideturtle()")
    lines.append("t.penup()")
    lines.append("")
    # Start oben-left coordinate relative to center:
    start_x = -width/2
    start_y = height/2
    # Function to draw square
    lines.append("def draw_square(x, y, size, color):")
    lines.append("    t.goto(x, y)")
    lines.append("    t.pendown()")
    lines.append("    t.fillcolor(color)")
    lines.append("    t.begin_fill()")
    lines.append("    for _ in range(4):")
    lines.append("        t.forward(size)")
    lines.append("        t.right(90)")
    lines.append("    t.end_fill()")
    lines.append("    t.penup()")
    lines.append("")
    # generate drawing commands
    for r in range(canvas_height):
        for c in range(canvas_width):
            color = grid[r][c]
            # compute top-left x,y for that pixel
            x = start_x + c * pixel_size
            y = start_y - r * pixel_size
            # turtle draws from current pos; use draw_square
            lines.append(f"draw_square({x}, {y}, {pixel_size}, '{color}')")
    lines.append("")
    lines.append("turtle.done()")
    return "\n".join(lines)

@app.route("/")
def index():
    return render_template("index.html", palette=PALETTE)

@app.route("/export_turtle", methods=["POST"])
def export_turtle():
    """
    Erwartet JSON: { "grid": [["#2596be", ...], ...] } 8x8
    Gibt zurück: { "script": "<large python script as text>" }
    """
    data = request.get_json(force=True)
    grid = data.get("grid")
    if not grid or len(grid) != 8 or any(len(row) != 8 for row in grid):
        return jsonify({"error": "grid must be 8x8"}), 400

    script = grid_to_turtle_script(grid)
    return jsonify({"script": script})

if __name__ == "__main__":
    # Port 5000 für lokal, Render override via environment if needed
    app.run(host="0.0.0.0", port=5000)

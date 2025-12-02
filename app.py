from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Palette (nur zur Anzeige im Frontend; nicht zwingend nötig für den Export)
PALETTE = ["#2596be", "#f6f6f6", "#3f2a29", "#caa62c", "#9c6908", "#910102", "#f9d1c0", "#3f2a29"]

def grid_to_turtle_script(grid, pixel_size=40):
    """
    Erzeugt ein reines, portables Turtle-Python-Script aus einem 8x8 Grid.
    grid: Liste von 8 Listen mit Farbhexstrings, z.B. "#2596be"
    pixel_size: Größe eines Pixels im Turtle-Script
    """
    # Schutz: stelle sicher, dass grid 8x8 ist
    if not grid or len(grid) != 8 or any(len(row) != 8 for row in grid):
        raise ValueError("grid must be 8x8")

    lines = []
    lines.append("import turtle")
    lines.append("")
    lines.append("# === Einstellungen ===")
    lines.append(f"PIXEL_SIZE = {int(pixel_size)}")
    lines.append("GRID_SIZE = 8")
    lines.append("")
    # Pixel-Array als Literal mit Hex-Farben einfügen
    lines.append("# === Hier ist dein 8x8 Pixel-Array (Hex-Farben) ===")
    lines.append("pixels = [")
    for row in grid:
        # format row as Python list of strings
        row_repr = "[" + ", ".join(repr(color) for color in row) + "]"
        lines.append(f"    {row_repr},")
    lines.append("]")
    lines.append("")
    # Zeichenfunktionen
    lines.append("t = turtle.Turtle()")
    lines.append("screen = turtle.Screen()")
    # setup so that the drawing fits and is centered
    total_w = pixel_size * 8
    total_h = pixel_size * 8
    screen_w = max(total_w + 100, 400)
    screen_h = max(total_h + 100, 400)
    lines.append(f"screen.setup(width={screen_w}, height={screen_h})")
    lines.append("t.speed(0)")
    lines.append("t.hideturtle()")
    lines.append("t.penup()")
    lines.append("")
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
    # Startkoordinaten (oben links relativ zum Zentrum)
    start_x = - (pixel_size * 8) / 2
    start_y = (pixel_size * 8) / 2
    lines.append(f"start_x = {start_x}")
    lines.append(f"start_y = {start_y}")
    lines.append("")
    lines.append("# --- Zeichnen ---")
    lines.append("for r in range(8):")
    lines.append("    for c in range(8):")
    lines.append("        color = pixels[r][c]")
    lines.append("        x = start_x + c * PIXEL_SIZE")
    lines.append("        y = start_y - r * PIXEL_SIZE")
    lines.append("        draw_square(x, y, PIXEL_SIZE, color)")
    lines.append("")
    lines.append("turtle.done()")
    return "\n".join(lines)


@app.route("/")
def index():
    return render_template("index.html", palette=PALETTE)

@app.route("/export_turtle", methods=["POST"])
def export_turtle():
    """
    Erwartet JSON: { "grid": [["#2596be", ...], ...] } (8x8)
    Liefert zurück: { "script": "<python script als text>" }
    """
    data = request.get_json(force=True)
    grid = data.get("grid")
    if not grid or len(grid) != 8 or any(len(row) != 8 for row in grid):
        return jsonify({"error": "grid must be 8x8"}), 400

    try:
        script = grid_to_turtle_script(grid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"script": script})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

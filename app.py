from flask import Flask, render_template, request, jsonify, send_file
import io
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/export_turtle", methods=["POST"])
def export_turtle():
    """
    Erwartet JSON: { "grid": [...] }
    Gibt Turtle-Script als Text zurück
    """
    data = request.get_json(force=True)
    grid = data.get("grid")
    pixel_size = data.get("pixel_size", 40)

    turtle_code = "import turtle\n\nscreen = turtle.Screen()\nscreen.setup(400,400)\nt = turtle.Turtle()\nt.speed('fastest')\nt.penup()\n"

    start_x = -((len(grid[0]) * pixel_size) / 2)
    start_y = ((len(grid) * pixel_size) / 2)

    for i, row in enumerate(grid):
        for j, color in enumerate(row):
            turtle_code += f"t.goto({start_x + j*pixel_size},{start_y - i*pixel_size})\nt.color('{color}')\nt.begin_fill()\nt.pendown()\nt.forward({pixel_size})\nt.right(90)\nt.forward({pixel_size})\nt.right(90)\nt.forward({pixel_size})\nt.right(90)\nt.forward({pixel_size})\nt.right(90)\nt.end_fill()\nt.penup()\n"

    turtle_code += "\nturtle.done()"

    return jsonify({"code": turtle_code})


@app.route("/export_arsip", methods=["POST"])
def export_arsip():
    data = request.get_json(force=True)
    grid = data.get("grid")

    if not grid or len(grid) != 8 or any(len(row) != 8 for row in grid):
        return jsonify({"error": "grid must be 8x8"}), 400

    arsip_data = {"version": 1, "pixel_size": 40, "grid": grid}
    mem = io.BytesIO()
    mem.write(json.dumps(arsip_data, indent=2).encode("utf-8"))
    mem.seek(0)

    return send_file(mem, mimetype="application/octet-stream", as_attachment=True, download_name="pixel_art.arsip")


@app.route("/import_arsip", methods=["POST"])
def import_arsip():
    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    f = request.files["file"]
    content = f.read().decode("utf-8")

    try:
        data = json.loads(content)
        grid = data.get("grid")
        if not grid or len(grid) != 8 or any(len(row) != 8 for row in grid):
            raise ValueError("grid invalid")
    except Exception as e:
        return jsonify({"error": "Invalid ARSIP file: " + str(e)}), 400

    return jsonify({"grid": grid})


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

# 8 Farben
colors = ["#2596be", "#f6f6f6", "#3f2a29", "#caa62c", "#9c6908", "#910102", "#f9d1c0", "#3f2a29"]
# Initial 8x8 Raster
grid = [[colors[0] for _ in range(8)] for _ in range(8)]

def nearest_color(rgb):
    r, g, b = rgb
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2],16) for i in (0,2,4))
    return min(colors, key=lambda c: sum((a-b)**2 for a,b in zip(hex_to_rgb(c),(r,g,b))))

@app.route("/")
def index():
    return render_template("index.html", grid=grid)

@app.route("/paint", methods=["POST"])
def paint():
    data = request.json
    row = data.get("row")
    col = data.get("col")
    color = data.get("color")
    if 0 <= row < 8 and 0 <= col < 8 and color in colors:
        grid[row][col] = color
        return jsonify({"status":"ok"})
    return jsonify({"status":"error"}), 400

@app.route("/reset", methods=["POST"])
def reset():
    global grid
    grid = [[colors[0] for _ in range(8)] for _ in range(8)]
    return jsonify({"status":"ok"})

@app.route("/upload", methods=["POST"])
def upload():
    global grid
    file = request.files.get("file")
    if not file:
        return jsonify({"status":"error", "message":"No file"}), 400
    # Bild auf 8x8 skalieren
    img = Image.open(file).convert("RGB").resize((8,8))
    for row in range(8):
        for col in range(8):
            grid[row][col] = nearest_color(img.getpixel((col,row)))
    return jsonify({"status":"ok"})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)

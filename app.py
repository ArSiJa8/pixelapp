from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 8x8 Raster initial
colors = ["#2596be", "#f6f6f6", "#3f2a29", "#caa62c", "#9c6908", "#910102", "#f9d1c0", "#3f2a29"]
grid = [[colors[0] for _ in range(8)] for _ in range(8)]

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
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route("/reset", methods=["POST"])
def reset():
    global grid
    grid = [[colors[0] for _ in range(8)] for _ in range(8)]
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, render_template, jsonify, send_file
import json
import io

app = Flask(__name__)

# Default-Palette
PALETTE = [
    "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
    "#FFFF00", "#FF00FF", "#00FFFF"
]

@app.route("/")
def index():
    # Wir geben Palette direkt als JS-Array im Template
    return render_template("index.html", palette=PALETTE)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text_output = data.get("text", "")
    return jsonify({"result": text_output})

@app.route("/export", methods=["POST"])
def export_arsip():
    data = request.json
    buffer = io.StringIO()
    json.dump(data, buffer)
    buffer.seek(0)
    return send_file(
        io.BytesIO(buffer.read().encode()),
        as_attachment=True,
        download_name="export.arsip",
        mimetype="application/json"
    )

@app.route("/import", methods=["POST"])
def import_arsip():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    content = json.load(file)
    return jsonify(content)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

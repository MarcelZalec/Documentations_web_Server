from flask import Flask, render_template, abort, request, jsonify
import os
import markdown
from help_functions import build_navigation
import json


app = Flask(__name__)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    
ALLOWED_DIRS = config["allowed_dirs"]

BASE_DIR = list(ALLOWED_DIRS.values())[0]   # Standard

@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>")
def browse(req_path):
    abs_path = os.path.join(BASE_DIR, req_path)

    # Pfad existiert nicht
    if not os.path.exists(abs_path):
        return abort(404)
    
    parent, breadcrumbs = build_navigation(req_path)

    # Wenn es ein Ordner ist → Liste anzeigen
    if os.path.isdir(abs_path):
        files = os.listdir(abs_path)
        files = sorted(files, key=str.lower)

        # Liste mit vollständigen Pfaden für Links
        folders = []
        files = []
        items = []
        for f in files:
            full = os.path.join(req_path, f)
            items.append(full.replace("\\", "/"))
        
        items = os.listdir(abs_path)


        for item in items:
            full_path = os.path.join(abs_path, item)
            web_path = os.path.join(req_path, item).replace("\\", "/")

            if os.path.isdir(full_path):
                folders.append(web_path)
            else:
                files.append(web_path)

            # Alphabetisch sortieren
            folders.sort(key=str.lower)
            files.sort(key=str.lower)


        return render_template("index.html", folders=folders, files=files, req_path=req_path, parent=parent, breadcrumbs=breadcrumbs)

    # Wenn es eine Datei ist → anzeigen
    if os.path.isfile(abs_path):
        parent, breadcrumbs = build_navigation(req_path)
        
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()

        html = markdown.markdown(
            content,
            extensions=["fenced_code", "codehilite"]
        )

        return render_template("show_file.html", filename=req_path, content=html, parent=parent, breadcrumbs=breadcrumbs)

    return abort(404)

@app.route("/change_base", methods=["POST"])
def change_base():
    global BASE_DIR
    data = request.json
    key = data.get("key")

    if key not in ALLOWED_DIRS:
        return jsonify({"error": "Ungültiger Ordner"}), 400

    BASE_DIR = ALLOWED_DIRS[key]
    return jsonify({"success": True, "new_base": BASE_DIR})

@app.context_processor
def inject_allowed_dirs():
    return dict(
        allowed_dirs=ALLOWED_DIRS,
        current_base=BASE_DIR
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
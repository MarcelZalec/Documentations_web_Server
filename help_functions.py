import os

def build_navigation(req_path: str):
    # Parent-Pfad berechnen (eine Ebene höher)
    # Beispiel:
    # ""                  -> parent = None
    # "Ordner"           -> parent = ""
    # "Ordner/Unter"     -> parent = "Ordner"
    if req_path:
        parent = os.path.dirname(req_path.rstrip("/"))
    else:
        parent = None

    # Breadcrumbs erzeugen
    breadcrumbs = []
    if req_path:
        parts = req_path.split("/")
        for i in range(len(parts)):
            breadcrumbs.append({
                "name": parts[i],
                "path": "/".join(parts[:i+1])
            })

    return parent, breadcrumbs
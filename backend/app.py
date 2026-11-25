from pathlib import Path
from flask import Flask
from .database import inicializar_banco
from .routes import registrar_rotas
from .paginas import registrar_paginas

ROOT_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(ROOT_DIR / "templates"),
    static_folder=str(ROOT_DIR / "frontend"),
    static_url_path="/static",
)

inicializar_banco()
registrar_paginas(app)   # páginas HTML
registrar_rotas(app)     # API em JSON

if __name__ == "__main__":
    app.run(debug=True)

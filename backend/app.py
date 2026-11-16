from pathlib import Path
from flask import Flask, render_template
from .database import inicializar_banco
from .routes import registrar_rotas

ROOT_DIR = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(ROOT_DIR / "templates"),
    static_folder=str(ROOT_DIR / "frontend"),
    static_url_path="/static",
)

inicializar_banco()
registrar_rotas(app)

@app.route("/")
def inicio():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

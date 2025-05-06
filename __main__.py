"""Fichier principal"""

import subprocess
import os


def run_streamlit_app():
    app_path = os.path.join("src", "App", "app.py")
    subprocess.run(
        ["streamlit", "run", app_path], env={**os.environ, "PYTHONPATH": "."}
    )


if __name__ == "__main__":
    run_streamlit_app()

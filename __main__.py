"""
Fichier principal
"""

import subprocess
import os
import sys

REQUIRED_PACKAGES = ["pandas", "numpy", "sklearn", "streamlit", "plotly"]


def check_and_install_packages():
    import importlib
    import time

    print("🔍 Vérification de la présence des packages requis...\n")
    missing_packages = []

    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package)
            print(f"✅ {package} est déjà installé.")
        except ImportError:
            print(f"❌ {package} est manquant.")
            missing_packages.append(package)

    if not missing_packages:
        print("\n🎉 Tous les packages sont installés. Lancement de l'application...")
        time.sleep(1)
        return

    print("\n📦 Il manque les packages suivants :")
    for pkg in missing_packages:
        print(f"  - {pkg}")

    print("\n🛠️ Que voulez-vous faire ?")
    print(
        "1️⃣  Installer tous les packages avec leur bonne version "
        "via requirements.txt (recommandé)"
    )
    print("2️⃣  Installer uniquement les packages manquants")
    print("3️⃣  Quitter")

    choix = input("\n👉 Entrez le numéro de votre choix (1 / 2 / 3) : ").strip()

    if choix == "1":
        print("\n📥 Installation via requirements.txt...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
            )
            print("\n✅ Installation terminée.")
        except subprocess.CalledProcessError:
            print("\n❌ Échec de l'installation avec requirements.txt.")
            sys.exit(1)

    elif choix == "2":
        for pkg in missing_packages:
            print(f"\n📥 Installation de {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print("\n✅ Installation terminée.")

    else:
        print("\n🚪 Fermeture de l'application.")
        sys.exit(0)


def run_streamlit_app():
    app_path = os.path.join("src", "App", "app.py")
    subprocess.run(
        ["streamlit", "run", app_path], env={**os.environ, "PYTHONPATH": "."}
    )


if __name__ == "__main__":
    check_and_install_packages()
    run_streamlit_app()

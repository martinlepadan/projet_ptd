"""
Fichier principal
"""

import subprocess
import os
import sys
import importlib
import time

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "sklearn",
    "streamlit",
    "plotly",
    "keyboard",
    "psutil",
]


def check_and_install_packages():

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


def ask_bonus_mode():
    print("\n✨ Partie BONUS : Réseau de Neurones (PyTorch) ✨")
    print("Souhaitez-vous activer la partie bonus utilisant le réseau de neurones ?")
    print(
        "⚠️  Cette partie nécessite PyTorch et peut prendre du temps à charger et "
        "ralentir l'application en général. ⚠️"
    )
    print("\n1️⃣  Oui, activer PyTorch et l'afficher dans l'application")
    print("2️⃣  Non, ignorer cette partie")

    choix = input("\n👉 Entrez votre choix (1 / 2) : ").strip()
    if choix == "1":
        print("\n🔍 Vérification de la présence de torch...\n")
        try:
            import torch

            print(f"✅ torch est déjà installé (version {torch.__version__})")
            if torch.__version__ < "2.6.0":
                print("⚠️  Version de torch inférieure à 2.6.0")
                ans = (
                    input("Souhaitez-vous mettre à jour torch ? (o/n) : ")
                    .strip()
                    .lower()
                )
                if ans == "o":
                    print("📥 Mise à jour de torch...")
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "--upgrade", "torch"]
                    )
                    print("✅ torch mis à jour.")
                else:
                    print("⏭️ Mise à jour de torch ignorée.")
                    print(
                        "Risque d'incompatibilité avec le code, "
                        "partie bonus non déployée."
                    )
                return False
        except ImportError:
            print("❌ torch n'est pas installé.")
            ans = input("Souhaitez-vous l'installer ? (o/n) : ").strip().lower()
            if ans == "o":
                print("📦 Installation de torch (CPU, version 2.6.0)...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "torch==2.6.0"]
                )
                print("✅ torch installé.")
            else:
                print("⏭️ Installation de torch ignorée.")
                return False
        return True
    else:
        print("⏭️ Partie réseau de neurones ignorée.")
        return False


def run_streamlit_app(bonus_mode):
    env = os.environ.copy()
    env["BONUS_MODE"] = "Oui" if bonus_mode else "Non"
    env["PYTHONPATH"] = "."
    app_path = os.path.join("src", "App", "app.py")
    subprocess.run(["streamlit", "run", app_path], env=env)


if __name__ == "__main__":
    check_and_install_packages()
    bonus = ask_bonus_mode()
    run_streamlit_app(bonus)

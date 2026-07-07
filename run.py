import os
import sys
import subprocess
import time

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def ejecutar_comando(comando):
    try:
        subprocess.run(comando, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"\n❌ Error al ejecutar: {comando}")
        input("\nPresiona Enter para continuar...")
        return False

def verificar_url_app():
    try:
        url_actual = subprocess.check_output("git remote get-url origin", shell=True, text=True).strip()
        if "ax-col/app" not in url_actual or "app-ax" in url_actual:
            print("\n⚙️ Git Shield: Corrigiendo enlace remoto de la App (app.git)...")
            subprocess.run("git remote set-url origin https://github.com/ax-col/app.git", shell=True)
            time.sleep(1)
    except Exception:
        pass

def main():
    verificar_url_app()
    # Detectamos automáticamente si estamos en celular o PC por la ruta actual
    en_celular = "storage" in os.getcwd() or "emulated" in os.getcwd()

    while True:
        limpiar_pantalla()
        print("==================================================")
        print("📱 SISTEMA DE CONTROL AX - JEFE APLICACIÓN (app)")
        print("==================================================")
        if en_celular:
            print("1. 🔥 Compilar Aplicación (Llamar compilar.sh)")
        else:
            print("1. 🚫 (Compilación deshabilitada en PC)")
        print("2. Ver Estado de la App (git status)")
        print("3. Descargar Cambios de la Nube (git pull)")
        print("4. Subir Cambios de la App (git add + commit + push)")
        print("5. Volver al Panel Líder")
        print("==================================================")
        opc = input("Selecciona una opción (1-5): ").strip()

        if opc == "1" and en_celular:
            limpiar_pantalla()
            if os.path.exists("compilar.sh"):
                subprocess.run("chmod +x compilar.sh", shell=True)
                ejecutar_comando("bash compilar.sh")
            else:
                print("❌ No se encontró compilar.sh en esta carpeta.")
            input("\nPresiona Enter para volver...")
        elif opc == "2":
            ejecutar_comando("git status")
            input("\nPresiona Enter para volver...")
        elif opc == "3":
            print("\n📥 Sincronizando entorno local...")
            ejecutar_comando("git pull origin main")
            input("\nPresiona Enter para volver...")
        elif opc == "4":
            msg = input("Mensaje del commit (deja vacío para usar por defecto): ").strip()
            if not msg:
                msg = "Update App Environment via run.py"
            
            print("\n➕ Indexando códigos fuente y APK...")
            time.sleep(1.5)
            if ejecutar_comando("git add ."):
                print("💬 Guardando historial local (Commit)...")
                time.sleep(1.5)
                if ejecutar_comando(f'git commit -m "{msg}"'):
                    print("🚀 Subiendo actualizaciones a GitHub...")
                    time.sleep(2)
                    ejecutar_comando("git push origin main")
            input("\nPresiona Enter para volver...")
        elif opc == "5":
            break

if __name__ == "__main__":
    main()

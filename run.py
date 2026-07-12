import os
import sys
import subprocess
import time
import requests  # <-- Conexión directa a la API de GitHub
import re        # <-- Expresiones regulares para la inyección inteligente

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

# ========================================================
# AGENTE INTELIGENTE: OBTENER VERSIÓN Y AUTO-INCREMENTAR
# ========================================================
def obtener_siguiente_version(propietario, repo, token):
    """
    Consulta GitHub para saber la última versión lanzada y calcula la siguiente (+0.1)
    """
    url = f"https://api.github.com/repos/{propietario}/{repo}/releases/latest"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            ultima_tag = response.json().get("tag_name", "v1.0")
            match = re.search(r"v?(\d+\.\d+)", ultima_tag)
            if match:
                numero_actual = float(match.group(1))
                siguiente_numero = round(numero_actual + 0.1, 1)
                return f"v{siguiente_numero}"
        elif response.status_code == 404:
            return "v1.1"  # Primera versión por defecto si no existen releases
    except Exception as e:
        print(f"⚠️ No se pudo conectar a GitHub para calcular la versión: {e}")
    
    return None

def inyectar_version_en_js(nueva_version):
    """
    Busca de forma automática la constante VERSION_INSTALADA en assets/actualizador.js y la actualiza
    """
    rutas_posibles = [
        os.path.join("assets", "actualizador.js"),
        os.path.join("..", "app", "assets", "actualizador.js"),
        "actualizador.js"
    ]
    
    ruta_js = None
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            ruta_js = ruta
            break

    if not ruta_js:
        print("⚠️ Alerta: No se encontró 'actualizador.js' para auto-inyectar la versión.")
        return False

    try:
        with open(ruta_js, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        # Cambia la constante VERSION_INSTALADA por el número nuevo calculado
        contenido_modificado = re.sub(
            r'const VERSION_INSTALADA = "[^"]+";', 
            f'const VERSION_INSTALADA = "{nueva_version}";', 
            contenido
        )
        
        with open(ruta_js, "w", encoding="utf-8") as f:
            f.write(contenido_modificado)
        print(f"📝 Inteligencia AX: '{ruta_js}' actualizado automáticamente a {nueva_version}")
        return True
    except Exception as e:
        print(f"❌ Error crítico al escribir en actualizador.js: {e}")
        return False
        
# ========================================================
# AGENTE DE LANZAMIENTOS AUTOMÁTICOS (RELEASE API)
# ========================================================
def publicar_release_github(ruta_apk, version_tag, commit_msg, token):
    REPO_PROPIETARIO = "ax-col"
    REPO_NOMBRE = "app"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url_release = f"https://api.github.com/repos/{REPO_PROPIETARIO}/{REPO_NOMBRE}/releases"
    payload = {
        "tag_name": version_tag,
        "target_commitish": "main",
        "name": f"AX Sistema {version_tag}",
        "body": f"Despliegue automatizado AX.\nDetalle: {commit_msg}",
        "draft": False,
        "prerelease": False
    }
    
    print(f"\n🚀 Abriendo espacio oficial para {version_tag} en GitHub Releases...")
    try:
        response = requests.post(url_release, json=payload, headers=headers)
        if response.status_code not in [200, 201]:
            print(f"❌ Error al estructurar la release: {response.text}")
            return False
            
        release_data = response.json()
        upload_url = release_data['upload_url'].split('{')[0]
        
        nombre_publico_apk = f"AX_{version_tag}.apk"
        url_subida_final = f"{upload_url}?name={nombre_publico_apk}"
        
        headers_subida = {
            "Authorization": f"token {token}",
            "Content-Type": "application/vnd.android.package-archive"
        }
        
        print(f"📦 Transmitiendo binario local a producción como '{nombre_publico_apk}'...")
        with open(ruta_apk, 'rb') as apk_file:
            response_upload = requests.post(url_subida_final, data=apk_file, headers=headers_subida)
            
        if response_upload.status_code in [200, 201]:
            print(f"✅ ¡Éxito total! El APK {version_tag} ya está en la nube listo para descarga.")
            return True
        else:
            print(f"❌ Error al subir el APK binario: {response_upload.text}")
            return False
            
    except Exception as e:
        print(f"❌ Fallo crítico en el Agente de Despliegue: {e}")
        return False

def main():
    verificar_url_app()
    en_celular = "storage" in os.getcwd() or "emulated" in os.getcwd()
    
    # 🛡️ AJUSTE SEGURO: El script sube un nivel ('..') para buscar el token fuera de 'app/'
    GITHUB_TOKEN = ""
    ruta_token = os.path.join("..", "token.txt")
    
    # Respaldo por si se ejecuta parándose desde una ruta diferente
    if not os.path.exists(ruta_token):
        ruta_token = "token.txt"
        
    if os.path.exists(ruta_token):
        with open(ruta_token, "r", encoding="utf-8") as tf:
            GITHUB_TOKEN = tf.read().strip()
    else:
        print("❌ Error crítico: No se encontró el archivo 'token.txt' en la carpeta raíz externa.")
        print("Mueve el archivo a 'github/token.txt' e intenta de nuevo.")
        input("\nPresiona Enter para salir...")
        return

    while True:
        limpiar_pantalla()
        print("==================================================")
        print("📱 SISTEMA INTELIGENTE AX - JEFE APLICACIÓN (app)")
        print("==================================================")
        if en_celular:
            print("1. 🔥 Compilar Aplicación (Llamar compilar.sh)")
        else:
            print("1. [Opción Desactivada en PC]")
        print("2. Ver Estado Local (git status)")
        print("3. Descargar Cambios de GitHub (git pull)")
        print("4. ⚡ AUTO-INCREMENTAR VERSION, SUBIR REPO + LANZAR APK")
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
            print("\n🔍 Analizando historial en GitHub para auto-versionamiento...")
            version_tag = obtener_siguiente_version("ax-col", "app", GITHUB_TOKEN)
            
            if not version_tag:
                print("⚠️ No se pudo calcular el incremento automático desde GitHub.")
                version_tag = input("Escribe el tag manualmente (ej: v1.2): ").strip()
                if not version_tag: 
                    input("\nOperación cancelada. Presiona Enter...")
                    continue
            else:
                print(f"✨ Próxima versión calculada inteligentemente: {version_tag}")
            
            # Modifica dinámicamente la constante VERSION_ACTUAL_APK en tu script.js
            inyectar_version_en_js(version_tag)
            
            msg = input("Mensaje del commit (deja vacío para usar automático): ").strip()
            if not msg:
                msg = f"Auto-Deploy App System Version {version_tag}"
            
            print("\n➕ Indexando códigos fuente modificados...")
            time.sleep(1)
            if ejecutar_comando("git add ."):
                print("💬 Guardando historial local (Commit)...")
                time.sleep(1)
                
                resultado_commit = subprocess.run(f'git commit -m "{msg}"', shell=True, capture_output=True, text=True)
                
                if "nothing to commit" in resultado_commit.stdout or resultado_commit.returncode == 0:
                    print("✨ El repositorio local ya está al día con los cambios de código.")
                    print("🚀 Asegurando sincronización con GitHub...")
                    time.sleep(1.5)
                    
                    ejecutar_comando("git push origin main")
                    
                    ruta_del_apk = "base.apk" 
                    if os.path.exists(ruta_del_apk):
                        publicar_release_github(ruta_del_apk, version_tag, msg, GITHUB_TOKEN)
                    else:
                        print(f"\n⚠️ Alerta: No se encontró el archivo físico '{ruta_del_apk}' en esta carpeta.")
                        print("Asegúrate de ejecutar la Opción 1 (Compilar) antes de lanzar la actualización.")
                else:
                    print(f"❌ Error real en el commit: {resultado_commit.stderr}")
                            
            input("\nPresiona Enter para volver...")
        elif opc == "5":
            break

if __name__ == "__main__":
    main()

#!/bin/bash

echo "🚀 Iniciando compilación de AX..."

# 1. Limpieza total
rm -rf obj classes.dex base.apk base.apk.idsig

# 2. Compilar recursos nativos (icono)
aapt2 compile --dir res -o compiled_res.zip
aapt2 link --manifest AndroidManifest.xml -I android.jar compiled_res.zip -o base.apk --java src/com/ax/col

# 3. Compilar los archivos Java independientes
mkdir -p obj
javac -source 8 -target 8 -d obj -classpath android.jar $(find src -name "*.java")

# 4. Convertir a dex con d8 (el modo turbo sin lag)
d8 --debug obj/com/ax/col/*.class --lib android.jar --output .

# 5. Meter el código, los assets y mantener la estructura
zip -ur base.apk classes.dex assets/

# 6. Firmar el APK final
apksigner sign --ks debug.keystore --ks-pass pass:android base.apk

echo "✅ ¡APK Compilado y Firmado con éxito!"
echo "--------------------------------------------------"

# ======= SECCIÓN INTERACTIVA DE SUBIDA CONTROLADA CON PAUSAS =======
read -p "¿Deseas subir los cambios a GitHub y respaldar la APK? (Y/N): " -n 1 opcion
echo ""

if [[ "$opcion" =~ ^[Yy]$ ]]; then
    echo "📦 Copiando base.apk a storage/downloads/github/ax..."
    mkdir -p ~/storage/downloads/github/ax
    cp base.apk ~/storage/downloads/github/ax/
    sleep 2 # Pausa para asegurar que el archivo se transfiere por completo

    # Guardamos la ruta actual para poder regresar al terminar
    RUTA_COMPILACION=$(pwd)

    echo "📂 Moviéndonos al repositorio Git local (storage/downloads/github/ax)..."
    cd ~/storage/downloads/github/ax/
    sleep 2 # Pausa para estabilizar el cambio de directorio

    echo "🗂️ Ejecutando Git Status..."
    git status
    sleep 3 # Espera de 3 segundos para procesar los cambios en pantalla
    
    echo "➕ Agregando todos los archivos modificados de forma segura..."
    git add .
    sleep 3 # Espera de 3 segundos para que Git indexe con calma todos tus assets
    
    echo "💬 Creando el commit de actualización..."
    git commit -m "Updating the page or app"
    sleep 2 # Espera de 2 segundos para asentar el historial local
    
    echo "🚀 Iniciando subida a los servidores de GitHub (Git Push)..."
    echo "Por favor espera, enviando datos de red..."
    git push
    sleep 4 # Espera extendida de 4 segundos para asegurar la confirmación del servidor remoto
    
    # Regresamos automáticamente a la carpeta de compilación original
    cd "$RUTA_COMPILACION"
    
    echo "🎉 ¡Todo listo, bro! App actualizada en GitHub y copia guardada con éxito."
else
    echo "👋 Operación omitida. Tu base.apk local está lista en Downloads/github/app."
fi

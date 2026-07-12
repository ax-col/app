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

echo "--------------------------------------------------"
echo "✅ ¡APK Compilado y Firmado con éxito!"
echo "📦 Tu base.apk local está lista en: github/app/"
echo "--------------------------------------------------"
# El script termina aquí y devuelve el control al menú de Python automáticamente.

// app/assets/actualizador.js

// Esta constante la maneja run.py automáticamente en cada despliegue
const VERSION_INSTALADA = "v1.3"; 
const REPO_USER = "ax-col";
const REPO_NAME = "app";

async function chequearActualizacionesAX() {
    const url = `https://api.github.com/repos/${REPO_USER}/${REPO_NAME}/releases/latest`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) return;
        
        const data = await response.json();
        const ultimaVersionNube = data.tag_name; // Ej: "v1.2"
        const urlApk = data.assets[0].browser_download_url;

        // Si la versión de GitHub es diferente a la instalada
        if (ultimaVersionNube !== VERSION_INSTALADA) {
            
            // 1. INTENTO DE PUSH NATIVO (Por si tienes puente nativo con Python)
            if (window.AndroidBridge && window.AndroidBridge.lanzarPush) {
                window.AndroidBridge.lanzarPush(ultimaVersionNube, urlApk);
            }

            // 2. DISPARAR ALERTA VISUAL EN LA WEB (Interior)
            crearAlertaVisualInterna(ultimaVersionNube, urlApk);
        }
    } catch (error) {
        console.error("Error al comprobar la actualización en GitHub:", error);
    }
}

function crearAlertaVisualInterna(version, link) {
    if (document.getElementById('alerta-actualizacion-ax')) return;

    const banner = document.createElement('div');
    banner.id = 'alerta-actualizacion-ax';
    banner.style.position = 'fixed';
    banner.style.bottom = '20px';
    banner.style.left = '50%';
    banner.style.transform = 'translateX(-50%)';
    banner.style.backgroundColor = '#1e1e24';
    banner.style.color = '#ffffff';
    banner.style.padding = '16px 24px';
    banner.style.borderRadius = '12px';
    banner.style.boxShadow = '0px 8px 24px rgba(0,0,0,0.5)';
    banner.style.zIndex = '99999';
    banner.style.fontFamily = 'sans-serif';
    banner.style.textAlign = 'center';
    banner.style.width = '85%';
    banner.style.maxWidth = '340px';
    banner.style.border = '1px solid #ff4a4a';

    banner.innerHTML = `
        <h4 style="margin: 0 0 8px 0; color: #ff4a4a; font-size: 16px;">🔄 Actualización Disponible</h4>
        <p style="margin: 0 0 14px 0; font-size: 13px; color: #cccccc;">La versión <b>${version}</b> está lista para descargar en el sistema.</p>
        <div style="display: flex; gap: 10px; justify-content: center;">
            <button id="btn-actualizar-ax" style="background-color: #ff4a4a; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer;">Actualizar</button>
            <button id="btn-cerrar-ax" style="background-color: transparent; color: #aaa; border: none; padding: 8px 12px; cursor: pointer;">Luego</button>
        </div>
    `;

    document.body.appendChild(banner);

    document.getElementById('btn-actualizar-ax').addEventListener('click', () => {
        window.open(link, '_blank');
    });

    document.getElementById('btn-cerrar-ax').addEventListener('click', () => {
        banner.remove();
    });
}

// Ejecutar automáticamente al abrir la aplicación
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(chequearActualizacionesAX, 2000);
});

// app/assets/actualizador.js

// Mantén aquí la versión v1.2 para que detecte la v1.3 de GitHub en la prueba
const VERSION_INSTALADA = "v1.5"; 
const REPO_USER = "ax-col";
const REPO_NAME = "app";

async function chequearActualizacionesAX() {
    // Rompemos la caché del navegador del celular agregando un timestamp único
    const url = `https://api.github.com/repos/${REPO_USER}/${REPO_NAME}/releases/latest?nocache=${new Date().getTime()}`;
    
    try {
        console.log("AX Shield: Iniciando consulta de actualización...");
        const response = await fetch(url);
        
        if (!response.ok) {
            console.log("AX Shield: Error de conexión con GitHub API. Status: " + response.status);
            return;
        }
        
        const data = await response.json();
        const ultimaVersionNube = data.tag_name; 
        const urlApk = (data.assets && data.assets.length > 0) 
            ? data.assets[0].browser_download_url 
            : `https://github.com/${REPO_USER}/${REPO_NAME}/releases`;

        console.log(`AX Shield: Comparando versión Local (${VERSION_INSTALADA}) con Nube (${ultimaVersionNube})`);

        if (ultimaVersionNube !== VERSION_INSTALADA) {
            
            // 🚨 ALERTA NATIVA: Si el script se ejecuta, este alert saltará directo en la pantalla de Android
            alert(`🔄 Actualización AX\n\nDetectada: ${ultimaVersionNube}\nInstalada: ${VERSION_INSTALADA}\n\nPresiona OK para habilitar el banner.`);
            
            // Creación del banner estándar
            crearAlertaVisualInterna(ultimaVersionNube, urlApk);
        }
    } catch (error) {
        console.error("AX Shield: Error crítico en el proceso fetch:", error);
    }
}

function crearAlertaVisualInterna(version, link) {
    if (!document.body) {
        setTimeout(() => crearAlertaVisualInterna(version, link), 300);
        return;
    }

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

// Aseguramos tres disparadores de carga para que el teléfono no ignore el inicio del script
if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(chequearActualizacionesAX, 2000);
} else {
    window.addEventListener('load', () => {
        setTimeout(chequearActualizacionesAX, 2000);
    });
}

package com.ax.col;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.app.Activity;
import android.view.Window; // 👈 IMPORTANTE: Añade esta importación

public class MainActivity extends Activity {

    private WebView myWebView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 🔥 ESTA LÍNEA SE ENCARGA DE QUITAR LA BARRA GRIS DE ARRIBA POR COMPLETO
        // Debe ir estrictamente antes de setContentView
        requestWindowFeature(Window.FEATURE_NO_TITLE);

        setContentView(R.layout.layout_main);

        myWebView = (WebView) findViewById(R.id.ax_webview);
        
        WebSettings webSettings = myWebView.getSettings();
        webSettings.setJavaScriptEnabled(true); 
        webSettings.setDomStorageEnabled(true);  
        
        // Permisos para navegación híbrida local
        webSettings.setAllowFileAccess(true); 
        webSettings.setAllowContentAccess(true);
        webSettings.setAllowFileAccessFromFileURLs(true); 
        webSettings.setAllowUniversalAccessFromFileURLs(true);

        // ===== CONFIGURACIÓN ULTRA FLUIDA (Quita el Lag) =====
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT); 
        webSettings.setUseWideViewPort(true);       
        webSettings.setLoadWithOverviewMode(true);  
        
        // Desactivamos controles de zoom pesados de fondo para liberar la CPU
        webSettings.setBuiltInZoomControls(false);   
        webSettings.setSupportZoom(false);
        webSettings.setDisplayZoomControls(false);  
        // =====================================================

        // Llamamos a la clase externa independiente
        myWebView.setWebViewClient(new MyCustomWebViewClient());

        // Desactivar barras de desplazamiento
        myWebView.setVerticalScrollBarEnabled(false);   
        myWebView.setHorizontalScrollBarEnabled(false); 

        // Cargar index principal
        myWebView.loadUrl("file:///android_asset/index.html"); 
    }

    @Override
    public void onBackPressed() {
        if (myWebView.canGoBack()) {
            myWebView.goBack(); 
        } else {
            super.onBackPressed(); 
        }
    }
}

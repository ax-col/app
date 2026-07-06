package com.ax.col;

import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;

public class MyCustomWebViewClient extends WebViewClient {
    
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        if (request != null && request.getUrl() != null) {
            String url = request.getUrl().toString();
            
            // Si el usuario da clic a un enlace interno de tus assets, se carga dentro de la app
            if (url.startsWith("file:///android_asset/")) {
                view.loadUrl(url);
                return true;
            }
            
            // Si da clic a un enlace externo (HTTP/HTTPS), dejamos que lo maneje el WebView de forma estándar
            if (url.startsWith("http://") || url.startsWith("https://")) {
                return false; 
            }
        }
        return false;
    }

    @SuppressWarnings("deprecation")
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, String url) {
        if (url != null) {
            if (url.startsWith("file:///android_asset/")) {
                view.loadUrl(url);
                return true;
            }
            if (url.startsWith("http://") || url.startsWith("https://")) {
                return false;
            }
        }
        return false;
    }
}

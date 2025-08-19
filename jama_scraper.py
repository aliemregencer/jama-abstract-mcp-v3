# jama_scraper.py
# Kullanım:
#   python jama_scraper.py "URL" -o va.json

import re, json, argparse, time, html, unicodedata
from typing import Dict, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- text utils --------------------
def clean(s: Optional[str]) -> str:
    if not s:
        return ""
    s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s).strip()
    # Bazı tarayıcı kombinasyonlarında U+2212 (−) karışabiliyor; ASCII tire yap:
    s = s.replace("\u2212", "-")
    return s

def norm_heading(h: str) -> Optional[str]:
    h = clean(h).lower().rstrip(":")
    MAP = {
        "importance":"importance",
        "objective":"objective",
        "design, setting, and participants":"dsp",
        "design, settings, and participants":"dsp",
        "design and participants":"dsp",
        "participants":"dsp",
        "intervention":"interventions",
        "interventions":"interventions",
        "main outcomes and measures":"moam",
        "outcomes":"moam",
        "results":"results",
        "conclusions and relevance":"conclusions",
        "conclusions":"conclusions",
        "meaning":"meaning",
        "trial registration":"trial_registration",
        # Yeni şablon için olası başlık varyantları:
        "setting":"settings_locations",
        "settings":"settings_locations",
        "location":"settings_locations",
        "locations":"settings_locations",
        "settings/locations":"settings_locations",
        "setting/locations":"settings_locations",
        "setting and locations":"settings_locations",
        "settings and locations":"settings_locations",
        "study setting":"settings_locations",
    }
    return MAP.get(h)

def pull_comparator(text: str) -> str:
    t = clean(text)
    for pat in [r"\bvs\.?\s+([^.;:]+)", r"\bversus\s+([^.;:]+)", r"\bcompared with\s+([^.;:]+)"]:
        m = re.search(pat, t, flags=re.I)
        if m: return clean(m.group(1))
    # JAMA örneğine özel failsafe
    if re.search(r"\bPR-?min\b", t, flags=re.I) and re.search(r"\bPR-?gym\b", t, flags=re.I):
        return "PR-gym"
    return ""

def pull_key_numbers(text: str) -> list:
    t = clean(text)
    pats = [
        r"\bn\s*=\s*\d{2,4}\b",
        r"\b\d{1,3}\s?%\b",
        r"\bp\s*[<=>]\s*0?\.\d+\b",
        r"\b(?:OR|RR|HR)\s*=\s*\d+(?:\.\d+)?\b",
        r"\bCI\s*\(?\d{1,2}%\)?\s*:\s*\d+(?:\.\d+)?\s*[–-]\s*\d+(?:\.\d+)?\b",
        r"\b[-+]?\d+(?:\.\d+)?\s*(?:m|km|min|days|weeks)\b",
    ]
    out = []
    for rgx in pats:
        out += [m.group(0) for m in re.finditer(rgx, t, flags=re.I)]
    # tekilleştir
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x); uniq.append(x)
    return uniq[:8]

# -------------------- selenium --------------------
def get_driver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-software-rasterizer")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    opts.add_argument("--log-level=3")
    opts.add_argument("--lang=en-US,en;q=0.9,tr;q=0.8")
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

def wait_for_load(drv: webdriver.Chrome, timeout: float = 15.0):
    end = time.time() + timeout
    while time.time() < end:
        if drv.execute_script("return document.readyState") == "complete":
            time.sleep(0.4); return
        time.sleep(0.2)

# -------------------- parsers --------------------
def parse_abstract_dom(soup: BeautifulSoup) -> Dict[str,str]:
    """#abstract içindeki <p><strong>H</strong> metin...</p> bloklarını sözlüğe döker."""
    out = {}
    abstract = soup.find(id="abstract") or soup.select_one("#abstract")
    if not abstract:
        return out
    for p in abstract.find_all("p", recursive=True):
        strong = p.find("strong")
        if not strong:
            continue
        key = norm_heading(strong.get_text(" ", strip=True))
        if not key:
            continue
        whole = p.get_text(" ", strip=True)
        # başlığı baştan kes
        content = re.sub(r"^\s*"+re.escape(strong.get_text(strip=True))+r"\s*:?\s*", "", whole, flags=re.I)
        out[key] = clean(content)
    return out

def parse_abstract_meta(soup: BeautifulSoup) -> Dict[str,str]:
    """<meta name="citation_abstract" content="...HTML..."> içindeki HTML'i parse eder."""
    out = {}
    meta = soup.find("meta", attrs={"name":"citation_abstract"})
    if not meta or not meta.get("content"):
        return out
    inner = BeautifulSoup(meta["content"], "lxml")
    # h3 -> p komşularını al
    for h in inner.find_all(["h3","strong"]):
        key = norm_heading(h.get_text(" ", strip=True))
        if not key:
            continue
        content = ""
        sib = h.find_next_sibling()
        if sib and sib.name == "p":
            content = sib.get_text(" ", strip=True)
        else:
            # p>strong yapısı
            par = h.parent if h.parent and h.parent.name == "p" else None
            if par:
                whole = par.get_text(" ", strip=True)
                content = re.sub(r"^\s*"+re.escape(h.get_text(strip=True))+r"\s*:?\s*", "", whole, flags=re.I)
        if content:
            out[key] = clean(content)
    return out

def parse_key_points(soup: BeautifulSoup) -> Dict[str,str]:
    """Key Points kutusu varsa Question/Findings/Meaning alanlarını döndürür."""
    out = {"question":"", "findings":"", "meaning":""}
    # "Key Points" başlığını arayıp yakınındaki p/strong bloklarını topla
    hdr = None
    for tag in soup.find_all(["h2","h3","h4"]):
        if clean(tag.get_text()).lower() == "key points":
            hdr = tag; break
    if not hdr:
        return out
    container = hdr.parent
    # Öncelik: aynı container içindeki strong başlıkları
    for p in container.find_all("p"):
        t = clean(p.get_text(" ", strip=True))
        # "Question. ..." gibi olabilir
        m = re.match(r"(question|findings|meaning)\.?\s*(.+)", t, flags=re.I)
        if m:
            k, v = m.group(1).lower(), clean(m.group(2))
            out[k] = v
    return out

# -------------------- smart pulls --------------------
_LOC_SNIPPET_RGX = re.compile(
    r"(?:(?:\d+\s+(?:center|centers|site|sites|unit|units|hospital|hospitals))"
    r"|(?:across the\s+[A-Za-z ,\-]+)"
    r"|(?:in\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)"
    r"|(?:multicenter|single-center|single centre|multicentre))",
    flags=re.I
)

def pull_settings_locations(sections: Dict[str,str]) -> str:
    """
    1) 'settings_locations' başlığı varsa onu döndür.
    2) Yoksa DSP (design/setting/participants) içinden lokasyon/merkez geçen ilk anlamlı cümleyi kırparak döndür.
    """
    if sections.get("settings_locations"):
        return clean(sections["settings_locations"])

    dsp = sections.get("dsp", "")
    if not dsp:
        return ""

    # Cümlelere böl ve anahtar desen içeren ilk cümleyi al
    sentences = re.split(r"(?<=[.!?])\s+", dsp)
    for s in sentences:
        if _LOC_SNIPPET_RGX.search(s):
            # Gereksiz detayları kısalt: 250 karakteri geçmesin
            s = clean(s)
            return s[:250]
    return ""

def pull_primary_outcome_from_text(moam: str, backup_texts: str = "") -> str:
    """
    Eğer MOAM içinde 'primary outcome/endpoint' ifadesi açıkça varsa onu alır.
    Yoksa yedek metinler içinde arar; yine yoksa MOAM'ı döndürür.
    """
    texts = [moam, backup_texts]
    for t in texts:
        tt = clean(t)
        m = re.search(r"(primary (?:outcome|endpoint)[^.;:]*[.;:]?)", tt, flags=re.I)
        if m:
            return clean(m.group(1))
    return clean(moam)

# -------------------- extraction --------------------
def extract_va(soup: BeautifulSoup) -> Dict:
    # 1) Abstract: DOM -> meta fallback
    secs = parse_abstract_dom(soup)
    if not secs:
        secs = parse_abstract_meta(soup)

    # 2) Key Points varsa
    kp = parse_key_points(soup)

    participants   = secs.get("dsp","")
    intervention   = secs.get("interventions","")
    moam_text      = secs.get("moam","")
    results        = secs.get("results","")
    importance     = secs.get("importance","")
    objective      = secs.get("objective","")
    conclusions    = secs.get("conclusions","") or secs.get("meaning","")

    # Key Points ile zenginleştir
    before         = kp["question"]  or importance
    findings_sum   = kp["findings"]  or results
    implications   = kp["meaning"]   or conclusions

    comparator     = pull_comparator(intervention) or pull_comparator(participants)

    # Yeni alan: Settings / Locations
    settings_locs  = pull_settings_locations(secs)

    # Primary outcome'u biraz daha akıllıca yakala; yoksa MOAM'a düş
    primary_outcome = pull_primary_outcome_from_text(moam_text, participants + " " + intervention)

    return {
        "the_study": {
            "participants": participants,
            "intervention": intervention,
            "comparator": comparator,
            "primary_outcome": primary_outcome,
            "settings_locations": settings_locs
        },
        "findings": {
            "summary": findings_sum,
            "key_numbers": pull_key_numbers(findings_sum)
        },
        "research_in_context": {
            "before": before,
            "added_value": objective,
            "implications": implications
        }
    }

def scrape(url: str) -> Dict:
    d = get_driver()
    try:
        d.get(url); wait_for_load(d)
        html_src = d.page_source
    finally:
        d.quit()
    soup = BeautifulSoup(html_src, "lxml")
    # Başlık: h1 -> og:title -> citation_title
    title = ""
    h1 = soup.find("h1")
    if h1: title = clean(h1.get_text(" ", strip=True))
    if not title:
        og = soup.find("meta", attrs={"property":"og:title"})
        if og and og.get("content"): title = clean(og["content"])
    if not title:
        ct = soup.find("meta", attrs={"name":"citation_title"})
        if ct and ct.get("content"): title = clean(ct["content"])

    va = extract_va(soup)
    return {"url": url, "title": title, "va": va}

# -------------------- cli --------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="JAMA makalesinden Visual Abstract JSON üretir.")
    ap.add_argument("url")
    ap.add_argument("-o", "--out", default="va.json")
    args = ap.parse_args()

    data = scrape(args.url)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON yazıldı: {args.out}")

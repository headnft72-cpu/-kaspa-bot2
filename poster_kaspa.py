cat > ~/xbot/poster_kaspa.py << 'PYEOF'
import os
import random
import time
import tweepy
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("X_API_KEY")
API_SECRET = os.getenv("X_API_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

def gerar_com_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except:
        return None

def gerar_tweet():
    temas = ["BlockDAG architecture","GhostDAG protocol","Kaspa mining","KAS tokenomics","Kaspa vs Bitcoin","KRC-20 smart contracts","Kaspa network speed","Kaspa decentralization"]
    tema = random.choice(temas)
    prompt = f"Write a unique tweet about {tema} related to Kaspa crypto. Max 240 chars. No hashtags. Max 1 emoji. Expert tone. Only return the tweet."
    resultado = gerar_com_gemini(prompt)
    if resultado:
        return resultado[:240]
    fallback = [
        "Kaspa's BlockDAG processes 1 block per second today, with roadmap targeting 100 blocks per second.",
        "GhostDAG doesn't discard parallel blocks, it orders them all, making Kaspa fundamentally more efficient.",
        "Kaspa mining attracts serious ASIC development because the network is designed for long-term proof of work.",
        "KRC-20 brings smart contracts to Kaspa without sacrificing base layer speed or security.",
        "Kaspa achieves near-instant finality through parallel block confirmation."
    ]
    return random.choice(fallback)

def gerar_thread():
    temas = ["How Kaspa BlockDAG works vs blockchain","Why GhostDAG is a breakthrough","Kaspa mining explained","Why Kaspa could be the future of proof of work","Kaspa vs Bitcoin technical comparison"]
    tema = random.choice(temas)
    prompt = f"Write a Twitter thread of 7 parts about: {tema}. Part 1 starts with THREAD. Parts 2-7 start with number/. Max 240 chars each. No hashtags. Separate with ###. Only return the parts."
    resultado = gerar_com_gemini(prompt)
    if resultado:
        partes = [p.strip() for p in resultado.split("###") if p.strip()]
        if len(partes) >= 4:
            return partes[:7]
    return [
        "THREAD 🧵 Why Kaspa is one of the most technically interesting crypto projects right now:",
        "1/ Kaspa uses BlockDAG instead of traditional blockchain. Blocks are created in parallel.",
        "2/ The GhostDAG protocol orders all parallel blocks into a coherent ledger.",
        "3/ This allows Kaspa to run at 1 block per second today.",
        "4/ Traditional blockchains discard competing blocks. Kaspa includes them all.",
        "5/ The result: near-instant confirmations and high throughput.",
        "6/ This is why many consider Kaspa the most advanced proof-of-work network today."
    ]

def gerar_artigo():
    temas = ["Complete guide to Kaspa BlockDAG","Understanding GhostDAG protocol","Kaspa mining complete guide","Why Kaspa is different from every crypto","Future of proof of work with Kaspa"]
    tema = random.choice(temas)
    prompt = f"Write a 12-part Twitter article about: {tema}. Part 1 starts with ARTICLE. Max 240 chars each. No hashtags. Separate with ###. Only return the parts."
    resultado = gerar_com_gemini(prompt)
    if resultado:
        partes = [p.strip() for p in resultado.split("###") if p.strip()]
        if len(partes) >= 6:
            return partes[:12]
    return None

def postar_tweet():
    texto = gerar_tweet()
    client.create_tweet(text=texto)
    print(f"Tweet: {texto[:80]}...")

def postar_thread():
    partes = gerar_thread()
    primeiro = client.create_tweet(text=partes[0])
    tweet_id = primeiro.data["id"]
    time.sleep(3)
    for parte in partes[1:]:
        r = client.create_tweet(text=parte, in_reply_to_tweet_id=tweet_id)
        tweet_id = r.data["id"]
        time.sleep(random.randint(3, 8))
    print(f"Thread: {len(partes)} partes.")

def postar_artigo():
    partes = gerar_artigo()
    if not partes:
        postar_tweet()
        return
    primeiro = client.create_tweet(text=partes[0])
    tweet_id = primeiro.data["id"]
    time.sleep(3)
    for parte in partes[1:]:
        r = client.create_tweet(text=parte, in_reply_to_tweet_id=tweet_id)
        tweet_id = r.data["id"]
        time.sleep(random.randint(4, 10))
    print(f"Artigo: {len(partes)} partes.")

posts_hoje = 0
ultimo_reset = time.strftime("%d")

def resetar_se_novo_dia():
    global posts_hoje, ultimo_reset
    hoje = time.strftime("%d")
    if hoje != ultimo_reset:
        posts_hoje = 0
        ultimo_reset = hoje
        print("Novo dia - contadores resetados.")

print("Bot Kaspa + Gemini iniciado!")

while True:
    try:
        resetar_se_novo_dia()
        if posts_hoje >= 28:
            print("Limite diario. Aguardando...")
            time.sleep(1800)
            continue
        acao = random.choices(["tweet","thread","artigo"], weights=[45,35,20])[0]
        if acao == "tweet":
            postar_tweet()
        elif acao == "thread":
            postar_thread()
        elif acao == "artigo":
            postar_artigo()
        posts_hoje += 1
        print(f"Posts hoje: {posts_hoje}/28")
        espera = random.randint(2700, 5400)
        print(f"Aguardando {espera/60:.0f} min...

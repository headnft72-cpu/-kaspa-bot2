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
        r = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        }, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except:
        return None

def gerar_tweet():
    temas = [
        "BlockDAG architecture advantages over traditional blockchain",
        "GhostDAG protocol and how it works",
        "Kaspa mining profitability and ASIC development",
        "KAS tokenomics and supply mechanics",
        "Kaspa network speed and scalability",
        "KRC-20 smart contracts on Kaspa",
        "Kaspa vs Bitcoin technical comparison",
        "Kaspa decentralization advantages",
        "Kaspa instant finality explained",
        "Future of BlockDAG technology"
    ]
    tema = random.choice(temas)
    prompt = f"""Write a unique, engaging tweet about: {tema}
Rules:
- Maximum 240 characters
- No hashtags
- Maximum 1 emoji
- Expert crypto tone
- Include a specific fact or number when possible
- Sound natural, not robotic
- Never start with "Kaspa is" or "Did you know"
Return only the tweet text."""

    resultado = gerar_com_gemini(prompt)
    if resultado:
        return resultado[:240]
    
    fallback = [
        "Kaspa's BlockDAG processes 1 block per second today, with the roadmap targeting 10 and eventually 100 blocks per second.",
        "GhostDAG doesn't discard parallel blocks — it orders them all, making Kaspa fundamentally more efficient than Bitcoin.",
        "Kaspa mining attracts serious ASIC development because the network is designed for long-term proof of work security.",
        "KRC-20 brings smart contract capability to Kaspa without sacrificing the base layer's speed or security.",
        "Kaspa achieves near-instant finality through parallel block confirmation — something linear blockchains can't match."
    ]
    return random.choice(fallback)

def gerar_thread():
    temas = [
        "How Kaspa's BlockDAG works vs traditional blockchain",
        "Why GhostDAG is a breakthrough in crypto consensus",
        "Kaspa mining explained for beginners",
        "Why Kaspa could be the future of proof of work",
        "Kaspa vs Bitcoin: technical deep dive"
    ]
    tema = random.choice(temas)
    prompt = f"""Write a Twitter thread of exactly 7 parts about: {tema}
Rules:
- Part 1: Hook starting with THREAD 🧵
- Parts 2-7: start with number like 2/ 3/ etc
- Each part maximum 240 characters
- Educational, engaging and clear
- Include real technical details
- No hashtags
- Make people want to read all parts
Separate each part with ### symbol.
Return only the 7 parts."""

    resultado = gerar_com_gemini(prompt)
    if resultado:
        partes = [p.strip() for p in resultado.split("###") if p.strip()]
        if len(partes) >= 4:
            return partes[:7]
    
    return [
        "THREAD 🧵 Why Kaspa is one of the most technically interesting crypto projects right now:",
        "1/ Kaspa uses BlockDAG instead of a traditional blockchain. This means blocks can be created in parallel, not just one after another.",
        "2/ The GhostDAG protocol orders all those parallel blocks into a coherent ledger — without discarding any of them.",
        "3/ This design allows Kaspa to run at 1 block per second today, with plans to scale much further.",
        "4/ Traditional blockchains discard competing blocks as orphans. Kaspa includes them, making the network far more efficient.",
        "5/ The result: near-instant confirmations, high throughput, and strong decentralization — all at the same time.",
        "6/ This is why many consider Kaspa the most technically advanced proof-of-work network in existence today."
    ]

def gerar_artigo():
    temas = [
        "Complete guide to Kaspa BlockDAG technology",
        "Understanding GhostDAG: the protocol behind Kaspa",
        "Kaspa mining: complete guide for 2025",
        "Why Kaspa is different from every other crypto",
        "The future of proof of work: why Kaspa matters"
    ]
    tema = random.choice(temas)
    prompt = f"""Write a detailed Twitter article thread of 12 parts about: {tema}
Rules:
- Part 1: Compelling title starting with ARTICLE 📝
- Parts 2-12: Deep, educational content
- Each part maximum 240 characters
- Professional and informative tone
- Include real technical details and facts
- No hashtags
- Each part should add new value
Separate each part with ### symbol.
Return only the 12 parts."""

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
        r = client.create_twe

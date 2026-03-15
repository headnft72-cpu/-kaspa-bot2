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
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_KEY
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except:
        return None

def gerar_tweet():
    temas = ["BlockDAG architecture","GhostDAG protocol","Kaspa mining","KAS tokenomics","Kaspa vs Bitcoin","KRC-20 smart contracts"]
    tema = random.choice(temas)
    prompt = "Write a unique tweet about " + tema + " related to Kaspa crypto. Max 240 chars. No hashtags. Max 1 emoji. Expert tone. Only return the tweet."
    resultado = gerar_com_gemini(prompt)
    if resultado:
        return resultado[:240]
    fallback = ["Kaspa BlockDAG processes 1 block per second today.","GhostDAG does not discard parallel blocks it orders them all.","Kaspa mining attracts serious ASIC development.","KRC-20 brings smart contracts to Kaspa.","Kaspa achieves near-instant finality."]
    return random.choice(fallback)

def gerar_thread():
    temas = ["How Kaspa BlockDAG works","Why GhostDAG is a breakthrough","Kaspa mining explained","Kaspa vs Bitcoin"]
    tema = random.choice(temas)
    prompt = "Write Twitter thread of 6 parts about: " + tema + ". Part 1 starts with THREAD. Parts 2-6 start with number/. Max 240 chars each. No hashtags. Separate with ###. Only return parts."
    resultado = gerar_com_gemini(prompt)
    if resultado:
        partes = [p.strip() for p in resultado.split("###") if p.strip()]
        if len(partes) >= 4:
            return partes[:6]
    return ["THREAD Why Kaspa is interesting:","1/ Kaspa uses BlockDAG instead of blockchain.","2/ GhostDAG orders all parallel blocks.","3/ Kaspa runs at 1 block per second.","4/ Traditional blockchains discard blocks. Kaspa includes them.","5/ Near-instant confirmations and high throughput."]

def gerar_artigo():
    temas = ["Complete guide to Kaspa BlockDAG","Understanding GhostDAG","Kaspa mining guide","Why Kaspa is unique"]
    tema = random.choice(temas)
    prompt = "Write 10-part Twitter article about: " + tema + ". Part 1 starts with ARTICLE. Max 240 chars each. No hashtags. Separate with ###. Only return parts."
    resultado = gerar_com_gemini(prompt)
    if resultado:
        partes = [p.strip() for p in resultado.split("###") if p.strip()]
        if len(partes) >= 5:
            return partes[:10]
    return None

def postar_tweet():
    texto = gerar_tweet()
    client.create_tweet(text=texto)
    print("Tweet: " + texto[:80])

def postar_thread():
    partes = gerar_thread()
    primeiro = client.create_tweet(text=partes[0])
    tweet_id = primeiro.data["id"]
    time.sleep(3)
    for parte in partes[1:]:
        r = client.create_tweet(text=parte, in_reply_to_tweet_id=tweet_id)
        tweet_id = r.data["id"]
        time.sleep(random.randint(3, 8))
    print("Thread: " + str(len(partes)) + " partes.")

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
    print("Artigo: " + str(len(partes)) + " partes.")

posts_hoje = 0
ultimo_reset = time.strftime("%d")

def resetar_se_novo_dia():
    global posts_hoje, ultimo_reset
    hoje = time.strftime("%d")
    if hoje != ultimo_reset:
        posts_hoje = 0
        ultimo_reset = hoje
        print("Novo dia - contadores resetados.")

print("Bot Kaspa Gemini iniciado!")

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
        print("Posts hoje: " + str(posts_hoje) + "/28")
        espera = random.randint(2700, 5400)
        print("Aguardando " + str(int(espera/60)) + " min...")
        time.sleep(espera)
    except Exception as e:
        print("Erro: " + str(e))
        time.sleep(600)
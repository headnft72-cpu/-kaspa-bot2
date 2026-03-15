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

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

def gerar_com_ia(prompt):
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        return r.json()["response"].strip()
    except:
        return None

def gerar_tweet():
    prompt = """Write a unique, informative tweet about Kaspa cryptocurrency.
Topics to choose from: BlockDAG architecture, GhostDAG protocol, KAS tokenomics, 
mining profitability, network speed, decentralization, smart contracts KRC-20.
Rules:
- Maximum 240 characters
- No hashtags
- Max 1 emoji
- Straight to the point
- Never repeat common phrases
- Sound like a crypto expert
Only return the tweet text, nothing else."""
    
    resultado = gerar_com_ia(prompt)
    if resultado:
        return resultado[:240]
    
    # fallback sem IA
    intros = ["Kaspa insight:", "Crypto fact:", "BlockDAG thought:", "Tech insight:"]
    techs = ["BlockDAG architecture", "GhostDAG consensus", "parallel block processing", "KRC-20 smart contracts"]
    benefits = ["enables massive scalability", "allows near-instant confirmations", "keeps decentralization strong"]
    comparisons = ["something traditional blockchains struggle with", "a new direction for crypto", "a powerful innovation"]
    return f"{random.choice(intros)} Kaspa's {random.choice(techs)} {random.choice(benefits)}, {random.choice(comparisons)}."

def gerar_thread():
    prompt = """Write a Twitter thread of exactly 6 parts about Kaspa cryptocurrency.
Choose one specific topic: BlockDAG vs Blockchain, How GhostDAG works, 
Kaspa mining explained, KAS tokenomics, Why Kaspa is unique, Kaspa vs Bitcoin.
Rules:
- Part 1 must start with: THREAD 🧵
- Parts 2-6 start with the number like: 2/
- Each part max 240 characters
- Educational and engaging tone
- No hashtags
- Facts and data when possible
Return only the 6 parts separated by the symbol ###, nothing else."""

    resultado = gerar_com_ia(prompt)
    if resultado:
        partes = [p.strip() for p in resultado.split("###") if p.strip()]
        if len(partes) >= 3:
            return partes[:6]
    
    # fallback sem IA
    ideias = [
        "Kaspa uses BlockDAG instead of a traditional blockchain.",
        "GhostDAG allows blocks to be processed in parallel.",
        "This dramatically increases throughput without sacrificing security.",
        "The network keeps full decentralization while scaling.",
        "Kaspa can process 1 block per second with plans for much more.",
        "This architecture could define the next generation of crypto networks."
    ]
    random.shuffle(ideias)
    thread = ["THREAD 🧵 Why Kaspa technology is fascinating:"]
    for i, ideia in enumerate(ideias, 1):
        thread.append(f"{i}/ {ideia}")
    return thread

def gerar_artigo():
    prompt = """Write a long Twitter article thread of exactly 12 parts about one Kaspa topic.
Choose from: Complete Kaspa BlockDAG guide, Kaspa vs Ethereum, Future of Kaspa, 
Kaspa mining complete guide, Understanding GhostDAG protocol.
Rules:
- Part 1: catchy title starting with ARTICLE 📝
- Parts 2-12: detailed educational content
- Each part max 240 characters
- Professional and informative tone
- Include real technical details
- No hashtags
Return only the 12 parts separated by ### symbol, nothing else."""

    resultado = gerar_com_ia(prompt)
    if resultado:
        partes = [p.strip() for p in resultado.split("###") if p.strip()]
        if len(partes) >= 6:
            return partes[:12]
    return None

def responder_posts():
    prompt = """Write a short, polite and educational reply to a tweet about Kaspa cryptocurrency.
Rules:
- Maximum 200 characters
- Friendly and informative tone
- Add value to the conversation
- No hashtags
- No controversy
- Sound human
Only return the reply text, nothing else."""

    try:
        tweets = client.search_recent_tweets(
            query="Kaspa OR $KAS OR BlockDAG -is:retweet lang:en",
            max_results=10
        )
        if not tweets.data:
            return False

        tweet = random.choice(tweets.data)
        
        resposta = gerar_com_ia(prompt)
        if not resposta:
            respostas = [
                "Kaspa's BlockDAG architecture is definitely worth studying closely.",
                "The GhostDAG protocol behind Kaspa is a fascinating technical achievement.",
                "Kaspa continues to push interesting boundaries in distributed systems.",
                "The technology behind Kaspa is one of the most innovative in crypto right now.",
                "BlockDAG design gives Kaspa unique scalability advantages worth exploring."
            ]
            resposta = random.choice(respostas)

        client.create_tweet(
            text=resposta[:200],
            in_reply_to_tweet_id=tweet.id
        )
        print(f"Resposta enviada: {resposta[:60]}...")
        return True

    except Exception as e:
        print(f"Erro ao responder: {e}")
        return False

def postar_tweet():
    texto = gerar_tweet()
    client.create_tweet(text=texto)
    print(f"Tweet enviado: {texto[:80]}...")

def postar_thread():
    partes = gerar_thread()
    primeiro = client.create_tweet(text=partes[0])
    tweet_id = primeiro.data["id"]
    time.sleep(3)
    for parte in partes[1:]:
        r = client.create_tweet(text=parte, in_reply_to_tweet_id=tweet_id)
        tweet_id = r.data["id"]
        time.sleep(random.randint(3, 8))
    print(f"Thread enviada com {len(partes)} partes.")

def postar_artigo():
    partes = gerar_artigo()
    if not partes:
        print("Artigo falhou, postando tweet no lugar.")
        postar_tweet()
        return
    primeiro = client.create_tweet(text=partes[0])
    tweet_id = primeiro.data["id"]
    time.sleep(3)
    for parte in partes[1:]:
        r = client.create_tweet(text=parte, in_reply_to_tweet_id=tweet_id)
        tweet_id = r.data["id"]
        time.sleep(random.randint(4, 10))
    print(f"Artigo postado com {len(partes)} partes.")

# controle diário
posts_hoje = 0
respostas_hoje = 0
ultimo_reset = time.strftime("%d")

def resetar_se_novo_dia():
    global posts_hoje, respostas_hoje, ultimo_reset
    hoje = time.strftime("%d")
    if hoje != ultimo_reset:
        posts_hoje = 0
        respostas_hoje = 0
        ultimo_reset = hoje
        print("Novo dia — contadores resetados.")

print("Bot Kaspa iniciado! Postando 24-32x por dia com IA.")

while True:
    try:
        resetar_se_novo_dia()

        # pesos: tweet=40%, thread=25%, artigo=15%, resposta=20%
        acao = random.choices(
            ["tweet", "thread", "artigo", "resposta"],
            weights=[50, 35, 15, 0]
        )[0]

        if posts_hoje >= 30 and acao != "resposta":
            print("Limite de posts atingido hoje. Aguardando amanhã.")
            time.sleep(1800)
            continue

        if respostas_hoje >= 15 and acao == "resposta":
            acao = "tweet"

        if acao == "tweet":
            postar_tweet()
            posts_hoje += 1

        elif acao == "thread":
            postar_thread()
            posts_hoje += 1

        elif acao == "artigo":
            postar_artigo()
            posts_hoje += 1

        elif acao == "resposta":
            ok = responder_posts()
            if ok:
                respostas_hoje += 1

        print(f"Posts hoje: {posts_hoje}/30 | Respostas: {respostas_hoje}/15")

        # intervalo entre 45min e 90min
        espera = random.randint(2700, 5400)
        print(f"Aguardando {espera/60:.0f} minutos...")
        time.sleep(espera)

    except Exception as e:
        print(f"Erro geral: {e}")
        time.sleep(600)

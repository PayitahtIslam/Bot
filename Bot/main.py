import instaloader
import requests
from discord_webhook import DiscordWebhook
import time

# Instagram Kullanıcı Adı (Takip Edilecek Hesap)
USERNAME = "payitaht.islam"

# Discord Webhook URL'si (Bunu kendi Webhook'unla değiştir)
WEBHOOK_URL = "https://discord.com/api/webhooks/1340914326764126330/Dt-mMzjfSLAWEKebI9CZy_fKjIMFT-JdyvmvDkhYBXdfukphi4UGC98wMAK7-A_AT7TD"

# Instaloader ile giriş yapmadan veri çekme
loader = instaloader.Instaloader()

# Önceki gönderiyi kaydetmek için
last_post_id = None

def get_latest_post():
    """Belirtilen Instagram hesabının en son gönderisini alır."""
    global last_post_id
    try:
        profile = instaloader.Profile.from_username(loader.context, USERNAME)
        latest_post = next(profile.get_posts())
        post_url = f"https://www.instagram.com/p/{latest_post.shortcode}/"

        if last_post_id != latest_post.shortcode:
            last_post_id = latest_post.shortcode
            return post_url
        else:
            return None
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

def send_to_discord(post_url):
    """Yeni bir Instagram gönderisini Discord'a yollar."""
    message = f"📸 Yeni Instagram gönderisi paylaşıldı!\n{post_url}"
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=message)
    webhook.execute()
    print("✅ Instagram postu başarıyla Discord'a gönderildi!")

# Sürekli Çalışan Döngü
while True:
    print("🔄 Instagram kontrol ediliyor...")
    new_post = get_latest_post()
    if new_post:
        send_to_discord(new_post)
    
    # 10 dakika bekleyerek tekrar kontrol et
    time.sleep(600)  # 600 saniye = 10 dakika

import redis

conn = redis.Redis(host='127.0.0.1', port=6379)

# 起始url的Key： chouti:start_urls
conn.lpush("chouti:start_urls", 'https://dig.chouti.com')

# v = conn.rpop("chouti:start_urls")

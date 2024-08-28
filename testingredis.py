import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.set('mykey', 'hello world',7000)
    
value = r.get('mykey')
print(value)

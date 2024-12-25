import redis, json

redis_client = redis.Redis(host='redis-server', port=6379, db=0, decode_responses=True)

def store_dict(key, my_dict):
    # Serialize dictionary to JSON and store in Redis
    redis_client.set(key, json.dumps(my_dict)) 

def set_value(key, value):
    # Serialize dictionary to JSON and store in Redis
    redis_client.set(key, value) 

def get_dict(key):
    # Retrieve and deserialize the dictionary
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def get_value(key):
    # Retrieve and deserialize the dictionary
    return redis_client.get(key)

def get_list(key):
    # Retrieve and deserialize the dictionary
    return redis_client.lrange(key, 0, -1)

def increment_with_lock(key, field):
    # Acquire a lock
    lock = redis_client.lock(f"{key}_lock", timeout=5)  # Set a timeout to avoid deadlocks
    try:
        if lock.acquire(blocking=True):
            # Perform your thread-safe operation here
            redis_client.hincrby(key, field, 1)
    finally:
        # Release the lock
        lock.release()

def modify_with_lock(key, new_value):
    # Acquire a lock
    lock = redis_client.lock(f"{key}_lock", timeout=5)  # Set a timeout to avoid deadlocks
    try:
        if lock.acquire(blocking=True):
            # Perform your thread-safe operation here
            store_dict(key, new_value)
    finally:
        # Release the lock
        lock.release()
    
def append_to_list(key, new_object_to_append):
    redis_client.rpush(key, json.dumps(new_object_to_append))

def add_to_list(list_key,items):
    # Use RPUSH to add items to the end of the list
    for item in items:
        redis_client.rpush(list_key, item)

# 2. Get all items from the list
def get_list(list_key):
    # Use LRANGE to get all items from the list
    return redis_client.lrange(list_key, 0, -1)

# 3. Remove a specific item from the list
def remove_from_list(list_key,item):
    # Use LREM to remove a specific item from the list
    redis_client.lrem(list_key, 0, item)

# 4. Clear the entire list
def clear_list(list_key):
    # Use DEL to delete the key entirely
    redis_client.delete(list_key)
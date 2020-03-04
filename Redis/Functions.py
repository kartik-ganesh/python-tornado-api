import redis


def find_all_redis():
    redis_functions = redis.Redis()
    users = redis_functions.keys("Employee:*")
    all_user = []
    for i in users:
        all_user.append(redis_functions.hgetall(str(i)))

    if all_user:
        return all_user
    else:
        return None


def find_by_id_redis(id):
    redis_functions = redis.Redis()
    user = redis_functions.hgetall("Employee:"+str(id))

    if user == {}:
        return None
    else:
        return user


def find_by_name_redis(name):
    redis_functions = redis.Redis()
    all_user = find_all_redis()
    user = []
    for i in all_user:
        if i['name'] == name:
            user.append(i)

    if user:
        return user
    else:
        return None


def post_in_redis(new_entry):
    redis_functions = redis.Redis()
    redis_functions.hmset("Employee:" + str(new_entry['id']), new_entry)


def delete_by_id_redis(id):
    redis_functions = redis.Redis()
    if find_by_id_redis(id) == {}:
        return False
    else:
        redis_functions.delete("Employee:" + str(id))
        return True


def update_by_id_redis(id, new_entry):
    redis_functions = redis.Redis()
    if find_by_id_redis(id) == {}:
        return False
    else:
        redis_functions.hmset("Employee:" + str(new_entry['id']), new_entry)
        return True



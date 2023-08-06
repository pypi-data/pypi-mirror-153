import time

import redis


def init_redis(url, **kwargs):
    if not url.lower().startswith(("redis://", "rediss://", "unix://")):
        url = 'redis://' + url

    connection_pool = redis.ConnectionPool.from_url(url, **kwargs)
    print(connection_pool)


# init_redis('127.0.0.1/3:6319')
# init_redis('127.0.0.1/3')
# init_redis('127.0.0.1:6379')
init_redis('localhost:6379', decode_responses=True)


def purchase_item(conn, buyerid, itemid, sellerid, lprice):
    buyer = "users:%s" % buyerid
    seller = "users:%s" % sellerid
    item = "%s.%s" % (itemid, sellerid)
    inventory = "inventory:%s" % buyerid
    end = time.time() + 10
    pipe = conn.pipeline()

    while time.time() < end:    # 条件变化时，重试以检查条件是否满足
        try:
            pipe.watch("market:", buyer)            # 监控条件变化
            price = pipe.zscore("market:", item)
            funds = int(pipe.hget(buyer, "funds"))
            if price != lprice or price > funds:    # 条件不满足，退出
                pipe.unwatch()
                return None

            pipe.multi()        # 开始事务
            pipe.hincrby(seller, "funds", int(price))
            pipe.hincrby(buyer, "funds", int(-price))
            pipe.sadd(inventory, itemid)
            pipe.zrem("market:", item)
            pipe.execute()      # 执行命令
            return True
        except redis.exceptions.WatchError:
            pass

    return False

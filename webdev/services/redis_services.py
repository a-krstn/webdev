import redis

from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def incr_views(post_id: int) -> None:
    """Увеличивает счетчик просмотров конкретного поста при его просмотре"""

    r.incr(f'post:{post_id}:views')


def get_views(pk: int) -> int:
    """Возвращает значение счетчика просмотров конкретного поста"""

    return int(r.get(f'post:{pk}:views')) if r.get(f'post:{pk}:views') else 0

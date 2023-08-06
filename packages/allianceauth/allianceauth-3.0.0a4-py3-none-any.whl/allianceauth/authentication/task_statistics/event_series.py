import datetime as dt
from typing import Optional, List

from redis import Redis
from pytz import utc

from django_redis import get_redis_connection


class EventSeries:
    """API for recording and analysing a series of events."""

    _ROOT_KEY = "ALLIANCEAUTH_EVENT_SERIES"

    def __init__(self, key_id: str, redis: Redis = None) -> None:
        self._redis = get_redis_connection("default") if not redis else redis
        if not isinstance(self._redis, Redis):
            raise TypeError(
                "This class requires a Redis client, but none was provided "
                "and the default Django cache backend is not Redis either."
            )
        self._key_id = str(key_id)
        self.clear()

    @property
    def _key_counter(self):
        return f"{self._ROOT_KEY}_{self._key_id}_COUNTER"

    @property
    def _key_sorted_set(self):
        return f"{self._ROOT_KEY}_{self._key_id}_SORTED_SET"

    def add(self, event_time: dt.datetime = None) -> None:
        """Add event.

        Args:
        - event_time: timestamp of event. Will use current time if not specified.
        """
        if not event_time:
            event_time = dt.datetime.utcnow()
        id = self._redis.incr(self._key_counter)
        self._redis.zadd(self._key_sorted_set, {id: event_time.timestamp()})

    def all(self) -> List[dt.datetime]:
        """List of all known events."""
        return [
            event[1]
            for event in self._redis.zrangebyscore(
                self._key_sorted_set,
                "-inf",
                "+inf",
                withscores=True,
                score_cast_func=self._cast_scores_to_dt,
            )
        ]

    def clear(self) -> None:
        """Clear all events."""
        self._redis.delete(self._key_sorted_set)
        self._redis.delete(self._key_counter)

    def count(self, earliest: dt.datetime = None, latest: dt.datetime = None) -> int:
        """Count of events, can be restricted to given timeframe.

        Args:
        - earliest: Date of first events to count(inclusive), or -infinite if not specified
        - latest: Date of last events to count(inclusive), or +infinite if not specified
        """
        min = "-inf" if not earliest else earliest.timestamp()
        max = "+inf" if not latest else latest.timestamp()
        return self._redis.zcount(self._key_sorted_set, min=min, max=max)

    def first_event(self, earliest: dt.datetime = None) -> Optional[dt.datetime]:
        """Date/Time of first event. Returns `None` if series has no events.

        Args:
        - earliest: Date of first events to count(inclusive), or any if not specified
        """
        min = "-inf" if not earliest else earliest.timestamp()
        event = self._redis.zrangebyscore(
            self._key_sorted_set,
            min,
            "+inf",
            withscores=True,
            start=0,
            num=1,
            score_cast_func=self._cast_scores_to_dt,
        )
        if not event:
            return None
        return event[0][1]

    @staticmethod
    def _cast_scores_to_dt(score) -> dt.datetime:
        return dt.datetime.fromtimestamp(float(score), tz=utc)

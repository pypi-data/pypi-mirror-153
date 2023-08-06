import hashlib
import json
import logging
import os
import threading
import time
from typing import Dict

import pickle
import canonicaljson
import fakeredis
import redis
from fastapi.encoders import jsonable_encoder


class CachingService:
    """CachingService for processed content"""

    def __init__(self, component_name: str, component_version: str, commit_hash: str, storage=fakeredis.FakeStrictRedis()):
        self.enabled = True
        self.connecting = False
        self.redis_host = os.environ.get('REDISHOST', 'localhost')
        self.redis_port = int(os.environ.get('REDISPORT', 6379))
        self.redis_password = os.environ.get('REDISPASSWORD', 'test123')
        self.component_name = component_name
        self.component_version = component_version
        self.commit_hash = commit_hash

        if self.redis_host != 'localhost':
            if self.component_name == '':
                logging.fatal("setting an empty component_name can lead to \
                              unwanted cache hits with other components ")
                self.enabled = False
            self.__init_redis_connection__()
        else:
            self.__db = storage

    def __init_redis_connection__(
            self,
            timeout=5):
        self.connecting = True
        try:
            self.__db = self.__redis_connect__(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password,
                timeout=timeout)
            self.enabled = True
            self.connecting = False
        except Exception:
            print(f"Connection to redis {self.redis_host}:{self.redis_port} failed! Trying again in 30 seconds.")
            self.enabled = False
            thread = threading.Thread(target=self.__wait_for_reconnect__, args=(30,), daemon=True)
            thread.start()

    def __wait_for_reconnect__(self, timeout):
        time.sleep(timeout)
        self.__init_redis_connection__()

    @ staticmethod
    def __redis_connect__(
            host: str,
            port: int,
            password: str,
            timeout) -> redis.client.Redis:
        client = redis.Redis(
            host=host,
            port=port,
            password=password,
            socket_timeout=timeout,
        )
        ping = client.ping()
        if ping is True:
            return client
        return None

    @ staticmethod
    def __create_hash_key__(hashable_request: str) -> str:
        m = hashlib.sha256()
        m.update(hashable_request)
        return m.hexdigest().lower()

    @ staticmethod
    def extend_dict(request: Dict, **kwargs) -> Dict:
        for key, value in kwargs.items():
            request[key] = value
        return request

    def get(self, request: Dict) -> str:
        """Returns output contentHashes for a request if hashKey exists in cache"""
        if not self.enabled:
            raise NoCacheHitException()
        request['component_name'] = self.component_name
        request['component_version'] = self.component_version
        request['commit_hash'] = self.commit_hash
        hashableRequest = canonicaljson.encode_canonical_json(request)
        hashKey = self.__create_hash_key__(hashableRequest)
        try:
            binaryContentHashes = self.__db.get(hashKey)
        except redis.ConnectionError:
            self.enabled = False
            if not self.connecting:
                self.__init_redis_connection__()
            raise NoCacheHitException()
        if binaryContentHashes is None:
            raise NoCacheHitException()
        outPutContentHashes = json.loads(pickle.loads(binaryContentHashes))
        return outPutContentHashes

    def set(self, request: Dict, response: Dict) -> str:
        if not self.enabled:
            if not self.connecting:
                self.__init_redis_connection__()
            raise CouldNotCacheContentException()
        """Loads contentHash for processed content to cache"""
        request['component_name'] = self.component_name
        request['component_version'] = self.component_version
        request['commit_hash'] = self.commit_hash
        hashableRequest = canonicaljson.encode_canonical_json(request)
        hashKey = self.__create_hash_key__(hashableRequest)
        try:
            binary_response = pickle.dumps(
                json.dumps(jsonable_encoder(response)))
            try:
                self.__db.set(hashKey, binary_response)
            except redis.ConnectionError:
                self.enabled = False
                if not self.connecting:
                    self.__init_redis_connection__()
                raise CouldNotCacheContentException()
            return hashKey
        except Exception:
            raise CouldNotCacheContentException()


class CouldNotCacheContentException(Exception):
    """Raised when content could not be cached"""
    pass


class NoCacheHitException(Exception):
    """Raised when no cache hit"""
    pass

import threading
from threading import Thread
from kafka import KafkaConsumer
import multiprocessing as mp
from queue import Queue
import json
from datetime import datetime
import time
import schedule


def create_worker_queue(n_worker: int):
    worker_queue = Queue(n_worker)
    for i in range(n_worker):
        worker_queue.put(i)
    return worker_queue


def get_next_worker(worker_queue: Queue):
    next_worker = worker_queue.get()
    worker_queue.put(next_worker)
    return next_worker, worker_queue


def get_key_worker(key: str, worker_key: dict, worker_queue: Queue):
    next_worker, _ = worker_key.get(key, [None, None])
    if next_worker is None:
        next_worker, worker_queue = get_next_worker(worker_queue)
        worker_key[key] = [next_worker, datetime.now()]
    return next_worker, worker_key, worker_queue


def cleanup_key_worker(worker_key: dict, cleanup_interval: int):
    def cleanup(worker_key: dict, cleanup_interval: int):
        current_time = datetime.now()
        delete_key = [
            key
            for key, [_, val] in worker_key.items()
            if (current_time - val).total_seconds() > cleanup_interval
        ]

        for key in delete_key:
            del worker_key[key]

    Thread(target=cleanup, args=[worker_key, cleanup_interval]).start()


def background_schedule(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    ScheduleThread().start()


def multiprocess_kafka_consumer(
    input_topic: list,
    group_id: str,
    n_worker: int,
    bootstrap_servers: str,
    callable_function: callable,
    cleanup_interval: int = None,
    **kwargs
):
    consumer = KafkaConsumer(
        *input_topic,
        group_id=group_id,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        **kwargs,
    )
    message_queue = [mp.Manager().Queue() for i in range(n_worker)]
    worker_queue = create_worker_queue(n_worker)
    worker_key = {}

    if cleanup_interval:
        schedule.every().second.do(
            cleanup_key_worker,
            worker_key=worker_key,
            cleanup_interval=cleanup_interval,
        )
        background_schedule(cleanup_interval)

    for i in range(n_worker):
        worker = mp.Process(
            target=callable_function,
            args=(message_queue[i],),
        )
        worker.daemon = True
        worker.start()

    for message in consumer:
        if message.key:
            next_worker, worker_key, worker_queue = get_key_worker(
                key=message.key,
                worker_key=worker_key,
                worker_queue=worker_queue,
            )
        else:
            next_worker, worker_queue = get_next_worker(worker_queue)
        message_queue[next_worker].put(message)

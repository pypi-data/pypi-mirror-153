import logging
import threading
import time
from typing import Any, Dict, Iterable, Mapping, Optional
import requests
from discord_lumberjack.message_creators import BasicMessageCreator, MessageCreator
from queue import Queue

logger = logging.getLogger(__name__)

_default_message_creator = BasicMessageCreator()


def _record_str(record: logging.LogRecord) -> str:
    msg = record.getMessage()
    return f'"{msg[:50]}"{"..." if len(msg) > 50 else ""}'


class DiscordHandler(logging.Handler):
    """A base class for logging handlers that send messages to Discord.

    Args:
            url (str): The URL to make the request to. This can be a webhook URL, a channel URL, a direct message URL, or any other URL that Discord supports.
            level (int, optional): The level at which to log. Defaults to logging.NOTSET.
            message_creator (MessageCreator, optional): An instance of MessageCreator or one of its subclasses that will be used to create the message to send from each log record. Defaults to one that sends messages in monospace.
            http_headers (Mapping[str, Any], optional): A mapping of HTTP headers to send with the request. Defaults to an empty mapping.
    """

    def __init__(
        self,
        url: str,
        level: int = logging.NOTSET,
        message_creator: MessageCreator = None,
        http_headers: Mapping[str, Any] = None,
        flush_on_exit: bool = True,
    ) -> None:
        super().__init__(level=level)
        self.__url = url
        self.__session = requests.Session()
        self.__message_creator = message_creator or _default_message_creator
        self.__session.headers.update(http_headers or {})
        self.__queue: Queue[logging.LogRecord] = Queue()
        self.__consumer_thread = threading.Thread(
            target=self.__consume, name="DiscordLumberjack", daemon=not flush_on_exit
        )
        self.__consumer_thread.start()
        self.__sentinel = logging.LogRecord("", 0, "", 0, None, None, None)
        if flush_on_exit:
            threading.Thread(
                target=self.__cleanup, name="DiscordLumberjackCleanup"
            ).start()
        self.__exception: Optional[Exception] = None
        self.addFilter(
            lambda r: not r.name.startswith("discord_lumberjack.")
            and r.thread != self.__consumer_thread.ident
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Log the messages to Discord.

        This method is non-blocking. The message will be send in the background.

        Args:
                record (logging.LogRecord): The log record to send.
        """
        logger.debug(f"Enqueuing message {_record_str(record)}")
        self.__queue.put(record)

    def transform_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a message before sending it to Discord.

        This method is called for each message that is sent to Discord. It is called before any fields are filtered out.

        This method may be overridden by subclasses to transform each message as desired by each handler. By default, it keeps the message as is.

        Args:
                message (Dict[str, Any]): The message to transform.

        Returns:
                Dict[str, Any]: The transformed message.
        """
        return message

    def prepare_messages(self, record: logging.LogRecord) -> Iterable[Dict[str, Any]]:
        """Given a log record, obtain all the message objects that will be sent to Discord.

        This method gets all the messages from the message creator and calls transform_message which may be overridden by subclasses to transform each message as desired by each handler.

        Args:
                record (logging.LogRecord): The log record to send.

        Returns:
                Iterable[Dict[str, Any]]: The messages to send to Discord.
        """
        return (
            self.transform_message(msg)
            for msg in self.__message_creator.messages(record, self.format)
        )

    def flush(self, raise_exceptions=True):
        """Block until all logged messages are sent to Discord.

        If an exception was raised while sending a message, it will be re-raised if `raise_exceptions` is True.

        You do not need to call this method to ensure all messages are sent before exiting the main thread unless you have set `flush_on_exit` in the constructor to False.

        Args:
                raise_exceptions (bool, optional): Whether to re-raise any exceptions that were raised while sending messages. Defaults to True.

        Raises:
                Exception: If an exception was raised while sending a message, and `raise_exceptions` is True.
        """
        logger.debug(f"Flushing: Waiting for queue to empty...")
        self.__queue.join()
        logger.debug("Flushing: Queue has been emptied.")
        if self.__exception and raise_exceptions:
            raise self.__exception

    def __consume(self) -> None:
        """In an infinite loop, consume a log record from the queue, convert it to its message objects, and send them to Discord."""
        while True:
            try:
                record = self.__queue.get()
                if record is self.__sentinel:
                    logger.debug("Consumer: Sentinel record received, exiting thread.")
                    return
                logger.debug(f"Consumer: Got message from queue: {_record_str(record)}")
                for msg in self.prepare_messages(record):
                    self.__send_message(msg)
            except Exception as e:
                logger.exception(
                    f"Consumer: Exception while consuming: {_record_str(record)}."
                )
                self.__exception = e
                self.handleError(record)
            finally:
                self.__queue.task_done()
                logger.debug(
                    f"Consumer: Finished processing message: {_record_str(record)}."
                )

    def __send_message(self, message: Mapping[str, Any]) -> None:
        """Send a message to Discord.

        Args:
                message (Mapping[str, Any]): The message object to send.
        """
        response = self.__retry_send(message)
        if response.status_code >= 300:
            raise RuntimeError(f"Failed to send message to Discord: {response.text}")

    def __retry_send(
        self, message: Mapping[str, Any], initial_interval=0.1
    ) -> requests.Response:
        """Send a message to Discord.

        If it was rejected due to "too many requests", keep trying with increasing intervals until it succeeds. This method is blocking.

        Args:
                message (Mapping[str, Any]): The message object to send.
                initial_interval (float, optional): The initial interval to wait before retrying. Defaults to 0.1.

        Returns:
                requests.Response: The response to the HTTP request.
        """
        retry_interval = initial_interval
        response = self.__session.post(self.__url, json=message)
        while response.status_code == 429:
            logger.warning(
                "Message was rejected due to too many requests. Waiting"
                f" {retry_interval} seconds..."
            )
            time.sleep(retry_interval)
            retry_interval *= 2
            response = self.__session.post(self.__url, json=message)
        return response

    def __cleanup(self):
        """Waits for main thread to exit, then enqueues a sentinel to indicate that all messages have been sent."""
        logger.debug("Cleanup: Waiting for main thread to exit...")
        threading.main_thread().join()
        logger.debug("Cleanup: Main thread exited. Signaling consumer to exit.")
        self.__queue.put(self.__sentinel)

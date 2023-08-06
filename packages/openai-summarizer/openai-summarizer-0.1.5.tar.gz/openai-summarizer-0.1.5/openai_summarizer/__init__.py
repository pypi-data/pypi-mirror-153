import os
import typing
import imaplib
import email
import random
from collections import namedtuple

import requests
import openai
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


OpenAIResponse = namedtuple('OpenAIResponse', ['id', 'model', 'choices', 'best_choice', 'object', 'created'])


class Email:
    """A simple representation of an email.
    """
    def __init__(
        self,
        subject: str,
        to: str,
        from_: str,
        date: str,
        parts: typing.Iterable[typing.Any]
    ):
        self.subject = subject
        self.to = to
        self.from_ = from_
        self.date = date
        self.parts = list(parts)

    def summarize(self, client: 'OpenAIClient'):
        """Summarize an email using some OpenAIClient.
        """
        if len(self.parts) == 0:
            return
        
        body = self.parts[0].get_payload(decode=True).decode().strip()
        text = f"Subject: {self.subject}\n Body: {body}"
        
        prefix_size = len(client.prefix)
        suffix_size = len(client.suffix)

        allowed_size = max(0, client.max_tokens - (prefix_size + suffix_size))
        current_size = len(text)

        # If text has more characters than the client allows,
        # randomly choose some 300 words in order, to retain and remove everything else.
        if current_size > allowed_size:
            
            words = text.split(" ")
            # Suppose on average a word is 5 letters long.
            # 50 words 
            random_indices = random.sample(range(300), min(300, len(words)))
            text = " ".join([word for (index, word) in enumerate(words) if index in random_indices])

        response = client.request(text)
        return response.best_choice


class CompletionConfig:
    """Configuration for OpenAI Completion API.

    OpenAI Completion API docs are available at https://beta.openai.com/docs/api-reference/completions/create

    """
    def __init__(
        self,
        engine: str = "text-davinci-002", 
        temperature: float = 0.7, 
        max_tokens: int = 64,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs
    ):
        self.__conf__engine = engine
        self.__conf__temperature = temperature
        self.__conf__max_tokens = max_tokens
        self.__conf__top_p = top_p
        self.__conf__frequency_penalty = frequency_penalty
        self.__conf__presence_penalty = presence_penalty

        for key, val in kwargs.items():
            setattr(self, f'__conf__{key}', val)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        result = dict()
        start_at = len(type(self).__name__ + "__conf__") + 1
        for key, val in self.__dict__.items():
            result[key[start_at:]] = val
        return result

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self)


class OpenAIClient:
    """A minimal client for OpenAI's Completion API.

    Accepts some configuration, an apikey and talks
    to the OpenAI Completion server.

    Attributes:
        prefix      Some static text to be sent before the actual prompt.
        suffix      Some static text to be sent after the actual prompt.
        description A textual description of the client's purpose.
    """

    prefix = ""
    suffix = ""
    description = ""

    def __init__(
            self, 
            apikey: str,
            config: CompletionConfig = CompletionConfig(),
            max_tokens: int = 4097
            ):

        self.config = config
        self.max_tokens = max_tokens

        openai.api_key = apikey
    
    def prompt(self, text):
        """Build a prompt given some text.
        """

        blocks = [block for block in [self.prefix, text, self.suffix] if len(block)]
        return "\n\n".join(blocks)
    
    def __str__(self):
        """Get the description for this client."""
        return self.description

    def request(self, text: str) -> OpenAIResponse:
        """Make request to the server, given some text.
        """

        params = {
            "prompt": self.prompt(text),
            **self.config.to_dict()
        }

        logger.debug("Requesting OpenAI Completion Engine with params: %s", params)
        
        raw_response = openai.Completion.create(
            **params
        )

        # If a completion is returned, choose the first one
        # to be the best choice.
        best_choice = None
        if len(raw_response.get("choices", [])):
            best_choice = raw_response.get("choices")[0]["text"]

        # Collect some metadata around this conversation.
        response = OpenAIResponse(
            id=raw_response.get("id"),
            model=raw_response.get("model"),
            object=raw_response.get("object"),
            choices=raw_response.get("choices"),
            created=raw_response.get("created"),
            best_choice=best_choice
        ) 
        return response


class SummarizerClient(OpenAIClient):
    """Summarize some text for a second-grade student.
    """

    prefix = "Summarize this for a second-grade student:"
    description = "Summarize some text for a second-grade student."


class EmailSummarizerClient(OpenAIClient):
    """Summarize some email text in less than 50 words.
    """
    prefix = "Summarize this email in less than 50 words."
    description = "Summarize an email in less than 50 words."


class Mailbox:
    """A representation for an email mailbox.

    Given the credentials for an email, and an IMAP server
    to talk to, establish a IMAP4_SSL connection when an instance is created.
    """
    def __init__(self, mailhost: str, username: str, password: str):
        self.mailhost = mailhost
        self.username = username
        self.mailbox = None
        self._login(password)
 
    def _login(self, password: str):
        """Given a password, login to the mailbox.
        """
        mailbox = imaplib.IMAP4_SSL(self.mailhost)
        mailbox.login(self.username, password)
        mailbox.select("INBOX")
        self.mailbox = mailbox
    
    def fetch_new_messages(self):
        """Get all unread emails from inbox.
        """
        _, msgs = self.mailbox.search(None, 'UNSEEN')
        for msggroup in msgs:
            for msg in msggroup.decode("utf-8").split(" "):
                msg = msg.encode("utf-8")
                if len(msg):
                    _, data = self.mailbox.fetch(msg, '(RFC822)')
                    _, bytes_data = data[0]
                    email_message = email.message_from_bytes(bytes_data)
                    parts = [
                        part for part in email_message.walk() 
                        if part.get_content_type() in ('text/plain')
                    ]
                    email_instance = Email(
                        subject=email_message['subject'],
                        to=email_message['to'],
                        from_=email_message['from'],
                        date=email_message['date'],
                        parts=parts
                    )
                    yield email_instance


"""
This module contains :class:`.Router`, an helper :class:`~royalnet.engineer.conversation.Conversation`.
"""

import abc
import logging

import royalnet.engineer.bullet as b
import royalnet.engineer.conversation as c
import royalnet.engineer.sentry as s
import royalnet.royaltyping as t

log = logging.getLogger(__name__)


class Router(c.Conversation, metaclass=abc.ABCMeta):
    """
    A conversation which delegates event handling to other conversations by matching the contents of the first message received to one or multiple regexes.
    """

    def __init__(self):
        self.by_pattern: dict[t.Pattern, t.ConversationProtocol] = {}
        """
        A :class:`dict` mapping regex patterns to conversations registered with this router.
        """

        self.by_name: dict[str, t.ConversationProtocol] = {}
        """
        A :class:`dict` mapping command names to conversations registered with this router.
        """

        self.by_command: dict[t.ConversationProtocol, t.List[str]] = {}
        """
        A :class:`dict` mapping conversations registered with this router to lists of command names.
        """

        self.else_convs: list[t.ConversationProtocol] = []
        """
        A :class:`list` of conversations to delegate event handling to in case no other pattern is matched.
        """

    def register_conversation(self, conv: t.ConversationProtocol, names: t.List[str],
                              patterns: t.List[t.Pattern]) -> None:
        """
        Registers a new conversation with the :class:`.Router`, allowing it to run if one of the specified ``patterns`` is matched.
        """

        log.debug(f"Registering {conv!r}...")

        log.debug("Names:")
        for name in names:
            log.debug(f"{name!r} → {conv!r}")
            self.by_name[name] = conv
        log.debug(f"{conv!r} → {names!r}")

        log.debug("Patterns:")
        for pattern in patterns:
            log.debug(f"{pattern.pattern!r} → {conv!r}")
            self.by_pattern[pattern] = conv

    async def run(self, _sentry: s.Sentry, _conv: t.ConversationProtocol, **kwargs) -> None:
        dispenser = _sentry.dispenser()

        log.debug(f"Locking {dispenser!r}...")
        with _sentry.dispenser().lock(self):

            log.debug(f"Awaiting a projectile...")
            projectile: b.Projectile = await _sentry

            log.debug(f"Received: {projectile!r}")

            log.debug(f"Ensuring the projectile is a MessageReceived: {projectile!r}")
            if not isinstance(projectile, b.MessageReceived):
                log.debug(f"Returning: {projectile!r} is not a message")
                return

            log.debug(f"Getting message of: {projectile!r}")
            if not (msg := await projectile.message):
                log.warning(f"Returning: {projectile!r} has no message")
                return

            log.debug(f"Getting message text of: {msg!r}")
            if not (text := await msg.text):
                log.debug(f"Returning: {msg!r} has no text")
                return

            log.debug(f"Message text is: {text!r}")

            for pattern in self.by_pattern.keys():
                log.debug(f"Trying to search for {pattern!r} in the text")
                match = pattern.search(text)
                if match:
                    conversation = self.by_pattern[pattern]
                    log.debug(f"Matched with {pattern!r}, running conversation {conversation}")
                    await conversation(
                        **match.groupdict(),
                        **kwargs,
                        _sentry=_sentry,
                        _conv=conversation,
                        _msg=msg,
                        _text=text,
                        _router=self,
                    )
                    return
            else:
                for conversation in self.else_convs:
                    log.debug(f"No matches found, running conversation {conversation}")
                    await conversation(
                        **kwargs,
                        _sentry=_sentry,
                        _conv=conversation,
                        _msg=msg,
                        _text=text,
                        _router=self,
                    )


__all__ = (
    "Router",
)

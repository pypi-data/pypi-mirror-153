"""
The PDA ("main" class) for the :mod:`royalnet_telethon` frontend.
"""

from __future__ import annotations

import enum
import logging

import discord
import discord as d
import royalnet.engineer as engi
import royalnet.royaltyping as t

from .bullet.projectiles import DiscordMessageReceived, DiscordMessageEdited, DiscordMessageDeleted

log = logging.getLogger(__name__)


class DiscordpyPDAMode(enum.Enum):
    """
    .. todo:: Document this.
    """

    GLOBAL = enum.auto()
    CHANNEL = enum.auto()
    USER = enum.auto()
    CHANNEL_USER = enum.auto()


class DiscordpyPDAImplementation(engi.ConversationListImplementation):
    """
    .. todo:: Document this.
    """

    @property
    def namespace(self):
        return "discordpy"

    def __init__(self, name: str, bot_token: str,
                 mode: DiscordpyPDAMode = DiscordpyPDAMode.CHANNEL_USER,
                 intents: discord.Intents = discord.Intents.default()):

        super().__init__(name=name)

        self.mode: DiscordpyPDAMode = mode
        """
        The mode to use for mapping dispensers.
        """

        self.bot_token: str = bot_token
        """
        .. todo:: Document this.
        """

        # noinspection PyMethodParameters
        class CustomClient(d.Client):
            async def on_ready(cli):
                log.debug("CustomClient is ready!")

            async def on_error(self, event_method, *args, **kwargs):
                log.error(f"An error occoured in CustomClient: {event_method!r} {args!r} {kwargs!r}")

            async def on_message(cli, message: d.Message):
                log.debug("Triggered on_message, putting in dispenser...")

                await self.put(
                    key=self._determine_key(message=message),
                    projectile=DiscordMessageReceived(event=message)
                )

            async def on_message_edit(cli, message: d.Message):
                log.debug("Triggered on_message_edit, putting in dispenser...")

                await self.put(
                    key=self._determine_key(message=message),
                    projectile=DiscordMessageEdited(event=message)
                )

            async def on_message_delete(cli, message: d.Message):
                log.debug("Triggered on_message_delete, putting in dispenser...")

                await self.put(
                    key=self._determine_key(message=message),
                    projectile=DiscordMessageDeleted(event=message)
                )

        self.client: d.Client = CustomClient(intents=intents)
        """
        .. todo:: Document this.        
        """

    def _determine_key(self, message: d.Message):
        """
        .. todo:: Document this.
        """

        if self.mode == DiscordpyPDAMode.GLOBAL:
            return None
        elif self.mode == DiscordpyPDAMode.USER:
            author: d.User = message.author
            return author.id
        elif self.mode == DiscordpyPDAMode.CHANNEL:
            channel: t.Union[d.DMChannel, d.TextChannel] = message.channel
            return channel.id
        elif self.mode == DiscordpyPDAMode.CHANNEL_USER:
            author: d.User = message.author
            channel: t.Union[d.DMChannel, d.TextChannel] = message.channel
            return author.id, channel.id
        else:
            raise TypeError("Invalid mode")

    async def run(self) -> t.NoReturn:
        await self.client.start(self.bot_token, bot=True, reconnect=True)


__all__ = (
    "DiscordpyPDAMode",
    "DiscordpyPDAImplementation",
)

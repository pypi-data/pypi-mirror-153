from __future__ import annotations

import datetime

import async_property as ap
import discord
import discord as d
import royalnet.engineer.bullet.contents as co
import royalnet.royaltyping as t

from royalnet_discordpy.formatting import ds_markdown_format


class DiscordMessage(co.Message):
    def __init__(self, msg: d.Message):
        super().__init__()
        self._msg: d.Message = msg

    def __hash__(self) -> int:
        return self._msg.id

    @ap.async_property
    async def text(self) -> t.Optional[str]:
        return self._msg.content

    @ap.async_property
    async def timestamp(self) -> t.Optional[datetime.datetime]:
        return max(self._msg.date, self._msg.edit_date)

    @ap.async_property
    async def reply_to(self) -> t.Optional[DiscordMessage]:
        return DiscordMessage(msg=self._msg.reference.cached_message)

    @ap.async_property
    async def channel(self) -> t.Optional[DiscordChannel]:
        return DiscordChannel(channel=self._msg.channel)

    @ap.async_property
    async def sender(self) -> t.Optional[DiscordUser]:
        sender: t.Union[d.User, d.Member] = self._msg.author
        return DiscordUser(user=sender)

    async def reply(self, *,
                    text: str = None,
                    files: t.List[t.BinaryIO] = None) -> t.Optional[DiscordMessage]:
        if files is None:
            files = []

        msg = await self._msg.reply(content=ds_markdown_format(text) if text else None,
                                    files=[discord.File(file) for file in files])
        return DiscordMessage(msg=msg)


class DiscordChannel(co.Channel):
    def __init__(self, channel: t.Union[d.DMChannel, d.TextChannel, d.GroupChannel]):
        super().__init__()
        self._channel: t.Union[d.DMChannel, d.TextChannel, d.GroupChannel] = channel

    def __hash__(self):
        return self._channel.id

    @ap.async_property
    async def name(self) -> t.Optional[str]:
        return self._channel.name

    @ap.async_property
    async def topic(self) -> t.Optional[str]:
        return self._channel.topic

    @ap.async_property
    async def users(self) -> t.List[DiscordUser]:
        return [DiscordUser(user=member) for member in self._channel.members]

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> t.Optional[DiscordMessage]:
        if files is None:
            files = []

        msg = await self._channel.send(content=ds_markdown_format(text), files=[discord.File(file) for file in files])
        return DiscordMessage(msg=msg)


class DiscordUser(co.User):
    def __init__(self, user: t.Union[d.User, d.Member]):
        super().__init__()
        self._user: t.Union[d.User, d.Member] = user

    def __hash__(self):
        return self._user.id

    @ap.async_property
    async def name(self) -> t.Optional[str]:
        return f"{self._user.mention}"

    async def slide(self) -> DiscordChannel:
        dm = self._user.dm_channel
        if dm is None:
            dm = await self._user.create_dm()
        return DiscordChannel(channel=dm)


__all__ = (
    "DiscordMessage",
    "DiscordChannel",
    "DiscordUser",
)

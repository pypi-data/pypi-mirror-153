from __future__ import annotations

import async_property as ap
import discord as d
import royalnet.engineer as engi

from .contents import DiscordMessage


class DiscordMessageReceived(engi.MessageReceived):
    def __init__(self, event: d.Message):
        super().__init__()
        self._event: d.Message = event

    def __hash__(self) -> int:
        return self._event.id

    @ap.async_cached_property
    async def message(self) -> DiscordMessage:
        return DiscordMessage(msg=self._event)


class DiscordMessageEdited(engi.MessageEdited):
    def __init__(self, event: d.Message):
        super().__init__()
        self._event: d.Message = event

    def __hash__(self) -> int:
        return self._event.id

    @ap.async_cached_property
    async def message(self) -> DiscordMessage:
        return DiscordMessage(msg=self._event)


class DiscordMessageDeleted(engi.MessageDeleted):
    def __init__(self, event: d.Message):
        super().__init__()
        self._event: d.Message = event

    def __hash__(self) -> int:
        return self._event.id

    @ap.async_cached_property
    async def message(self) -> DiscordMessage:
        return DiscordMessage(msg=self._event)


__all__ = (
    "DiscordMessageReceived",
    "DiscordMessageEdited",
    "DiscordMessageDeleted",
)

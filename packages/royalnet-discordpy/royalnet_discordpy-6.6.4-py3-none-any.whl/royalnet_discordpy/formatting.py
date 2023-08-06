def ds_markdown_format(string: str) -> str:
    """
    Format a string as Discord Markdown.

    The following characters will be considered control characters:
    - ``\uE01B``: start bold
    - ``\uE00B``: end bold
    - ``\uE011``: start italic
    - ``\uE001``: end italic
    - ``\uE012``: start underline
    - ``\uE002``: end underline
    - ``\uE015``: start strike
    - ``\uE005``: end strike
    - ``\uE01F``: start spoiler
    - ``\uE00F``: end spoiler
    - ``\uE01C``: start single-line code
    - ``\uE00C``: end single-line code
    - ``\uE01D``: start multi-line code
    - ``\uE00D``: end multi-line code

    :param string: The string to format.
    :return: The formatted string.

    .. warning:: For now, this is a Discordpy implementation detail.

    .. todo:: This may cause denial of service attacks from users!
    """

    string = string.replace("*", "\\*")
    string = string.replace("_", "\\_")
    string = string.replace("`", "\\`")
    string = string.replace("~", "\\~")

    string = string.replace("\uE01B", "**")
    string = string.replace("\uE00B", "**")
    string = string.replace("\uE011", "_")
    string = string.replace("\uE001", "_")
    string = string.replace("\uE015", "~~")
    string = string.replace("\uE005", "~~")
    string = string.replace("\uE012", "__")
    string = string.replace("\uE002", "__")
    string = string.replace("\uE01F", "||")
    string = string.replace("\uE00F", "||")
    string = string.replace("\uE01C", "`")
    string = string.replace("\uE00C", "`")
    string = string.replace("\uE01D", "```")
    string = string.replace("\uE00D", "```")
    return string

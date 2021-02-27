
def create_base_embed_template(title: str = "-", description: str = "-", url: str = None, timestamp: int = None,
                               color: int = None, footer: dict = None, image: dict = None, thumbnail: dict = False,
                               video: dict = None, provider: dict = None, author: dict = None,
                               fields: list = None) -> dict:
    """Создает базовый шаблон для Embed"""

    embed_dict = {
        "title": title,
        "description": description,
    }

    if url is not None:
        embed_dict["url"] = url

    if timestamp is not None:
        embed_dict["timestamp"] = timestamp

    if color is not None:
        embed_dict["color"] = color

    if footer is not None:
        embed_dict["footer"] = footer

    if image is not None:
        embed_dict["image"] = image

    if thumbnail is not None:
        embed_dict["thumbnail"] = thumbnail

    if video is not None:
        embed_dict["video"] = video

    if provider is not None:
        embed_dict["provider"] = provider

    if author is not None:
        embed_dict["author"] = author

    if fields is not None:
        embed_dict["fields"] = fields

    return embed_dict


def create_media_object_template(url: str, proxy_url: str = None, height: int = None, width: int = None) -> dict:
    """Создает шаблон для видео, картинок и превьюх"""
    return {
        "url": url,
        "proxy_url": proxy_url,
        "height": height,
        "width": width,
    }


def create_provider_template(name: str, url: str = None) -> dict:
    """Создает шаблок для провайдера"""
    return {
        "name": name,
        "url": url,
    }


def create_footer_template(text: str, icon_url: str = None, proxy_icon_url: str = None):
    """Создает шаблон для футера"""
    return {
        "text": text,
        "icon_url": icon_url,
        "proxy_icon_url": proxy_icon_url,
    }


def create_field_template(name: str = "-", value: str = "-", inline: bool = False) -> dict:
    """Шаблон для создания одного field для Embed"""
    return {
        "name": name,
        "value": value,
        "inline": inline,
    }

import re

URL_VALID_CHARS = "-._~:/?#[]@!%$&'()*+,;="


def is_valid_image_link(link: str) -> bool:
    link_pattern = re.compile(r"^(?P<protocol>http|https)://"
                              r"(?P<domain_and_path>[\w._~:/?#\[\]@!$&'()*+,;=-]+)"
                              r"(?P<img_extension>\.(png|jpeg|jpg))"
                              r"(?P<smth_else>[\w._~:/?#\[\]@!%$&'()*+,;=-]+)?$")
    if link_pattern.match(link) is None:
        return False
    else:
        return True

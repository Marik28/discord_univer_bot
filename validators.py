import re


def is_valid_image_link(link: str) -> bool:
    link_pattern = re.compile(r"^(?P<protocol>http|https)://"
                              r"(?P<domain_and_path>[\w/.-]+)"
                              r"(?P<img_extension>\.(png|jpeg|jpg))"
                              r"(?P<smth_else>.+)?$")
    if link_pattern.match(link) is None:
        return False
    else:
        return True

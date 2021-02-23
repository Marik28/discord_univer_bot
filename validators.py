import re

# URL_VALID_CHARS = "-._~:/?#[]@!%$&'()*+,;="
URL_VALID_CHARS = r"._~:/?#\[\]@!$&'()*+,;=-"


def is_valid_image_link(link: str) -> bool:
    link_pattern = re.compile(r"^(?P<protocol>http|https)://"
                              r"(?P<domain_and_path>[\w{0}]+)"
                              r"(?P<img_extension>\.(png|jpeg|jpg))"
                              r"(?P<smth_else>[\w{1}]+)?$".format(URL_VALID_CHARS, URL_VALID_CHARS))
    return link_pattern.match(link) is not None


# def is_valid_image_link(link: str) -> bool:
#     link_pattern = re.compile(r"^(?P<protocol>http|https)://"
#                               r"(?P<domain_and_path>[\w{}]+)"
#                               r"(?P<img_extension>\.(png|jpeg|jpg))"
#                               r"(?P<smth_else>[\w._~:/?#\[\]@!%$&'()*+,;=-]+)?$".format())
#     return link_pattern.match(link) is not None
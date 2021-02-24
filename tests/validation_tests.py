import unittest

from validators import is_valid_image_link


class TestValidation(unittest.TestCase):

    def test_valid_links(self):
        with open("anime_pics_links.txt", "r") as file:
            self.valid_images_links = [row.strip() for row in file.readlines()]
            print(self.valid_images_links)
        for link in self.valid_images_links:
            self.assertTrue(is_valid_image_link(link))

    def test_specific_link(self):
        self.assertTrue(is_valid_image_link("https://static.wikia.nocookie.net/va11-halla-cyberpunk-bartender-action"
                                            "/images/8/8e/Jill_%281%29.png/revision/latest?cb=20180221085343&path"
                                            "-prefix=ru"))

    def test_url_without_image_link(self):
        assert not is_valid_image_link("http://vk.com/")


if __name__ == '__main__':
    unittest.main()

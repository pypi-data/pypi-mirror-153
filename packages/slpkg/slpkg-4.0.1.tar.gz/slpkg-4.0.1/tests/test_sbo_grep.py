import unittest
from slpkg.sbo.greps import SBoGrep


class TestSBoGreps(unittest.TestCase):

    def setUp(self):
        self.grep = SBoGrep('Flask')

    def test_source(self):
        """Test package source
        """
        source = self.grep.source()
        flask_source = ('https://files.pythonhosted.org/packages/source/f'
                        '/flask/Flask-2.1.2.tar.gz')
        self.assertEqual(source, flask_source)

    def test_requires(self):
        """Test package requires
        """
        requires = self.grep.requires()
        flask_dep = ['werkzeug', 'python3-itsdangerous',
                     'click', 'python-importlib_metadata']
        self.assertListEqual(requires, flask_dep)

    def test_version(self):
        """Test package version
        """
        version = self.grep.version()
        flask_ver = '2.1.2'
        self.assertEqual(version, flask_ver)

    def test_checksum(self):
        """Test package checksum
        """
        checksum = self.grep.checksum()
        flask_md5 = ['93f1832e5be704ef6ff2a4124579cd85']
        self.assertListEqual(checksum, flask_md5)

    def test_description(self):
        """Test package description
        """
        desc = self.grep.description()
        flask_desc = 'Flask (Microframework for Python)'
        self.assertEqual(desc, flask_desc)


if __name__ == "__main__":
    unittest.main()

"""
Tests for WSGI Calculator
"""

import unittest
import subprocess
import http.client
import random


class WebTestCase(unittest.TestCase):
    """tests for the WSGI Calculator"""

    def setUp(self):
        self.server_process = subprocess.Popen(
            [
                "python",
                "calculator.py"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def tearDown(self):
        self.server_process.kill()
        self.server_process.communicate()

    def get_response(self, url):
        """
        Helper function to get a response from a given url, using http.client
        """

        conn = http.client.HTTPConnection('localhost:8080')
        conn.request('GET', url)

        response = conn.getresponse()
        self.assertEqual(200, response.getcode())

        conn.close()

        return response

    def test_add(self):
        """
        A call to /add/a/b yields a + b
        """

        a = random.randint(100, 10000)
        b = random.randint(100, 10000)

        path = "/add/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a + b).encode(), response.read())

    def test_multiply(self):
        """
        A call to /multiply/a/b yields a*b
        """

        a = random.randint(100, 10000)
        b = random.randint(100, 10000)

        path = "/multiply/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a*b).encode(), response.read())

    def test_subtract_positive_result(self):
        """
        A call to /subtract/a/b yields a - b, for a > b
        """

        a = random.randint(10000, 100000)
        b = random.randint(100, 1000)

        path = "/subtract/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a - b).encode(), response.read())

    def test_subtract_negative_result(self):
        """
        A call to /subtract/a/b yields a - b, for a < b
        """

        a = random.randint(100, 1000)
        b = random.randint(10000, 100000)

        path = "/subtract/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a - b).encode(), response.read())

    def test_divide(self):
        """
        A call to /divide/a/b yields a/b, for a % b = 0
        """

        result = random.randint(2, 10)

        b = random.randint(100, 1000)
        a = result * b

        path = "/divide/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(result).encode(), response.read())

    def test_index_instructions(self):
        """
        The index page at the root of the server shall include instructions
        on how to use the page.
        """

        response = self.get_response('/')
        self.assertEqual(200, response.getcode())

        # We're just testing if the word "add" is present in the index
        self.assertIn("add".encode(), response.read())


if __name__ == '__main__':
    unittest.main()

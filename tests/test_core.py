"""Tests for TokenStreamDeflater."""
import unittest
from agent_token_stream_deflater.core import TokenStreamDeflater, TokenStreamInflater

class TestTokenStreamDeflater(unittest.TestCase):
    def test_roundtrip_deflate_inflate(self):
        deflater = TokenStreamDeflater()
        inflater = TokenStreamInflater()
        text = "function execution parameters payload execution parameters"
        compressed = deflater.compress_chunk(text)
        self.assertTrue(len(compressed) <= len(text))
        recovered = inflater.decompress_chunk(compressed)
        self.assertEqual(text, recovered)

"""Core Token Stream Deflater."""
import zlib
from typing import Dict, List, Tuple

class TokenStreamDeflater:
    def __init__(self):
        self.dictionary: Dict[str, int] = {}
        self.next_id = 1
        self.max_dict_size = 254

    def compress_chunk(self, text: str) -> bytes:
        words = text.split(" ")
        out = bytearray()
        for i, w in enumerate(words):
            if w in self.dictionary:
                out.append(0x80)  # escape flag
                out.append(self.dictionary[w])
            else:
                if len(self.dictionary) < self.max_dict_size and len(w) > 3:
                    self.dictionary[w] = self.next_id
                    self.next_id += 1
                out.extend(w.encode("utf-8"))
            if i < len(words) - 1:
                out.append(0x20)  # space
        return bytes(out)

class TokenStreamInflater:
    def __init__(self):
        self.reverse_dict: Dict[int, str] = {}
        self.next_id = 1
        self.max_dict_size = 254

    def decompress_chunk(self, data: bytes) -> str:
        words = []
        curr = bytearray()
        i = 0
        while i < len(data):
            b = data[i]
            if b == 0x80 and i + 1 < len(data):
                symbol_id = data[i+1]
                word = self.reverse_dict.get(symbol_id, "")
                curr.extend(word.encode("utf-8"))
                i += 2
            elif b == 0x20:
                raw_word = curr.decode("utf-8", errors="replace")
                if len(self.reverse_dict) < self.max_dict_size and len(raw_word) > 3:
                    if self.next_id not in self.reverse_dict:
                        self.reverse_dict[self.next_id] = raw_word
                        self.next_id += 1
                words.append(raw_word)
                curr.clear()
                i += 1
            else:
                curr.append(b)
                i += 1

        if curr:
            raw_word = curr.decode("utf-8", errors="replace")
            if len(self.reverse_dict) < self.max_dict_size and len(raw_word) > 3:
                if self.next_id not in self.reverse_dict:
                    self.reverse_dict[self.next_id] = raw_word
                    self.next_id += 1
            words.append(raw_word)

        return " ".join(words)

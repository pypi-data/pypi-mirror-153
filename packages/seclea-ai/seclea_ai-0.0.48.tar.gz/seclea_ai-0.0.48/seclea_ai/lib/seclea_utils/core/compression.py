import enum
import zlib
from abc import ABC, abstractmethod

from zstandard import ZstdCompressor, ZstdDecompressor

from .exceptions import CompressionError, DecompressionError
from .typing import BytesStream


class Compression(ABC):
    def __init__(self, chunk_size=256 * (10**3), compression_ext=".NONE"):
        self.chunk_size = chunk_size
        self.extension = compression_ext

    @abstractmethod
    def compress(self, read_stream: BytesStream, write_stream: BytesStream):
        write_stream.write(read_stream.read())

    @abstractmethod
    def decompress(self, read_stream: BytesStream, write_stream: BytesStream):
        write_stream.write(read_stream.read())


# Start of concrete implementations #
class Zstd(Compression):
    def __init__(self):
        super().__init__(compression_ext=".ZSTD")
        self.cctx = ZstdCompressor()
        self.dctx = ZstdDecompressor()

    def compress(self, read_stream, write_stream):
        try:
            read_stream.seek(0, 2)
            size = read_stream.tell()
            read_stream.seek(0, 0)
            self.cctx.copy_stream(read_stream, write_stream, size=size, write_size=self.chunk_size)
        except Exception:
            raise CompressionError("An error occurred during compression.")

    def decompress(self, read_stream, write_stream):
        try:
            with self.dctx.stream_reader(read_stream) as rs:
                rb = rs.read(self.chunk_size)
                while rb:
                    write_stream.write(rb)
                    rb = rs.read(self.chunk_size)
        except Exception as e:
            raise DecompressionError(f"An error occurred during decompression: {e}")


#   REFERENCE IF WE WANT TO HAVE MORE CONTROL OVER COMPRESSION IN THE FUTURE   ###
# while rb:
#     i += 1
#     print((i * self.chunk_size) / (2000 * (10 ** 6)))
#     t = time()
#     rb = read_stream.read(self.chunk_size)
#     print(rb)
#     print("read:", time() - t)
#     t = time()
#     out = self.chunker.compress(rb)
#     for o in out:
#         print(o)
#     print("compress:", time() - t)
#     t = time()
#
#     wr = self.cctx.stream_writer(write_stream, write_size=self.chunk_size)
#     print("decl:", time() - t)
#     t = time()
#     for o in out:
#         print("iter:", time() - t)
#         t = time()
#         wr.write(o)
#         print("write-chunk", time() - t)
#         t = time()
#
#     t = time()
#     print("write:", time() - t)
#
# for out in self.chunker.finish():
#     write_stream.write(out)


class CompressionFactory(enum.Enum):
    NONE = (Compression,)
    ZSTD = Zstd


class FileCompressor:
    def compression(self, file_path_in: str, file_path_out: str):
        with open(file_path_in, mode="rb") as fin, open(file_path_out, mode="wb") as fout:
            data = fin.read()
            compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            fout.write(compressed_data)

    def decompression(self, file_path_in: str, file_path_out: str):
        with open(file_path_in, mode="rb") as fin, open(file_path_out, mode="wb") as fout:
            data = fin.read()
            decompressed_data = zlib.decompress(data)
            fout.write(decompressed_data)

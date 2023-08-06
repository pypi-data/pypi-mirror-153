import io, os, tempfile, base64, zlib, urllib.request, sys, ssl, html

from typing import TextIO
from Cryptodome.Cipher import AES
from tqdm import tqdm
import pyaes
from Cryptodome.Cipher import AES

from .helpers import ResultDownloadInfo
from .utils import printHtml


def getSecureData(dri: ResultDownloadInfo, name: str):
  try:
    if not dri:
      raise Exception("Download info missing from API response.")
    _storeDatasetResultIfMissing(name, dri.id, dri.signedDataUrl)
    rawDecryptedData = _decryptUnzipFile(dri.id, dri.key64, dri.iv64)
    return io.BytesIO(rawDecryptedData)
  except Exception as err:
    printHtml(f'Error fetching data. Please try again. ({html.escape(str(err))})')
    if dri:
      _clearTmpFile(dri.id)
    return None


def _tmpFilepath(dId: str):
  mbTempDir = os.path.join(tempfile.gettempdir(), 'modelbit')
  if not os.path.exists(mbTempDir):
    os.makedirs(mbTempDir)
  return os.path.join(mbTempDir, dId)


def _storeDatasetResultIfMissing(dName: str, dId: str, url: str):
  filepath = _tmpFilepath(dId)
  if os.path.exists(filepath):
    return

  printHtml(f'Downloading "{dName}"...')

  class DownloadProgressBar(tqdm):  # From https://github.com/tqdm/tqdm#hooks-and-callbacks

    def update_to(self, b: int = 1, bsize: int = 1, tsize: None = None):
      if tsize is not None:
        self.total = tsize
      self.update(b * bsize - self.n)  # type: ignore

  outputStream: TextIO = sys.stdout
  if os.getenv('MB_TXT_MODE'):
    outputStream = io.StringIO()
  with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc="", file=outputStream) as t:
    default_context = ssl._create_default_https_context  # type: ignore
    try:
      urllib.request.urlretrieve(url, filename=filepath, reporthook=t.update_to)  # type: ignore
    except:
      # In case client has local SSL cert issues: pull down encrypted file without cert checking
      _clearTmpFile(dId)
      ssl._create_default_https_context = ssl._create_unverified_context  # type: ignore
      urllib.request.urlretrieve(url, filename=filepath, reporthook=t.update_to)  # type: ignore
    finally:
      ssl._create_default_https_context = default_context  # type: ignore


def _clearTmpFile(dId: str):
  filepath = _tmpFilepath(dId)
  if os.path.exists(filepath):
    os.remove(filepath)


def _decryptUnzipFile(dId: str, key64: str, iv64: str):
  filepath = _tmpFilepath(dId)
  if not os.path.exists(filepath):
    printHtml(f"Error: Couldn't find local data at {filepath}")

  fileIn = open(filepath, 'rb')
  raw = fileIn.read()
  fileIn.close()

  try:
    cipher = AES.new(base64.b64decode(key64), AES.MODE_CBC, iv=base64.b64decode(iv64))  # type: ignore
    return zlib.decompress(cipher.decrypt(raw), zlib.MAX_WBITS | 32)
  except Exception:
    # Fallback needed to support: Windows 11 on Mac M1 in Parallels
    printHtml(f"Warning: Falling back to pure-Python decryption.")
    mode = pyaes.AESModeOfOperationCBC(base64.b64decode(key64), iv=base64.b64decode(iv64))  # type: ignore
    outStream = io.BytesIO()
    pyaes.decrypt_stream(mode, io.BytesIO(raw), outStream)  # type: ignore
    outStream.seek(0)
    return zlib.decompress(outStream.read(), zlib.MAX_WBITS | 32)

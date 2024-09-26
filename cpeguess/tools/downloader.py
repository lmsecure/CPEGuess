from tqdm import tqdm
import requests
import sys
import gzip
import shutil
import os

class CPEDownloader:
    @staticmethod
    def download(filename: str, url: str):
        print(f"Downloading CPE data from {url} ...")
        chunk_size = 1024
        try:
            resp = requests.get(url, stream=True)
            total = int(resp.headers.get('content-length', 0))
            with open(f"{filename}.gz", 'wb') as file, tqdm(
                desc=f"{filename}.gz",
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in resp.iter_content(chunk_size=chunk_size):
                    size = file.write(data)
                    bar.update(size)
        except Exception as e:
            print(e)
            sys.exit(1)

        try:
            with gzip.open(f"{filename}.gz", "rb") as cpe_gz:
                with open(filename, "wb") as cpe_xml:
                    shutil.copyfileobj(cpe_gz, cpe_xml)
            os.remove(f"{filename}.gz")
        except (FileNotFoundError, PermissionError) as e:
            print(e)
            sys.exit(1)

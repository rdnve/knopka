## another unofficial api for [knopka.com](https://knopka.com)

[![python-latest](https://img.shields.io/pypi/pyversions/knopka?logo=python&logoColor=FFE873)](https://www.python.org/downloads/)
[![pypi](https://img.shields.io/badge/pypi-0.0.1-blue?logo=pypi&logoColor=FFE873)](https://pypi.org/project/knopka/)
[![status](https://img.shields.io/pypi/status/knopka)](https://pypi.org/project/knopka/)
[![pypi_downloads](https://img.shields.io/pypi/dm/knopka)](https://pypi.org/project/knopka/)
[![license](https://img.shields.io/pypi/l/knopka)](https://github.com/rdnve/knopka/blob/master/LICENSE)


### installation

```bash
# via pypi (recommended)
$ python -m pip install -U knopka

# or using github w/ pip
$ python -m pip install git+https://github.com/rdnve/knopka.git

# or using github w/ poetry
$ poetry add git+https://github.com/rdnve/knopka.git
```

### retrieve documents by task identifier
```python
import typing as ty

from knopka import KnopkaAdapter
from knopka.library import Document

adapter: KnopkaAdapter = KnopkaAdapter(access_token="your-secret-token")
documents: ty.List[Document] = adapter.get_documents_from_ones(uid=1234567)

for x in documents:
    print(f"Document: {x.guid} ({x.type=!s}) {x.number=!s} {x.date=!s}")
```

### retrieve file metadata
```python
import typing as ty

from knopka import KnopkaAdapter
from knopka.library import Document, File

adapter: KnopkaAdapter = KnopkaAdapter(access_token="your-secret-token")
documents: ty.List[Document] = adapter.get_documents_from_ones(uid=1234567)

for document in documents:
    myfile: File = adapter.get_meta_from_file(uid=document.file_uid)
    print(f"Meta file: {myfile.name} type={myfile.type}")
```

### retrieve full file
```python
import typing as ty

from knopka import KnopkaAdapter
from knopka.library import Document, File

adapter: KnopkaAdapter = KnopkaAdapter(access_token="your-secret-token")
documents: ty.List[Document] = adapter.get_documents_from_ones(uid=1234567)

path: str = "/home/user/some_files"
for document in documents:
    myfile: File = adapter.get_file(uid=document.file_uid)

    print(f"File: {myfile.name} type={myfile.type} w/ size={myfile.size} bytes")
    path: str = myfile.save(path)
```

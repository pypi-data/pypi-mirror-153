# async_pycatbox

A simple Python library for uploading files to catbox.moe, and based off of cazqew's pycatbox, with the only significant change being that it's now supports asynchronous uploading.

API documentation [https://catbox.moe/tools.php](https://catbox.moe/tools.php)

Install the current version with [PyPI](https://pypi.org/project/clubhouse-api/):

```bash
pip install async_pycatbox
```

Or from Github:

```bash
https://github.com/challos/async_pycatbox
```

## Usage


```python
token = '' # this is your token, and it will default to an empty string (which is fine for catbox) if not set

uploader = Uploader(token=token)

upload = uploader.upload(file_type='py', file_raw=open('catbox/catbox/catbox.py', 'rb').read())
print(upload)
```

```

## Example

```python
from pycatbox import Uploader

uploader = Uploader(token='')

# single file
def single():
    upload = uploader.upload(file_type='py', file_raw=open('catbox/catbox/catbox.py', 'rb').read())
    return upload

# multiple files
def multiple(files):
    log = []
    for file in files:
        extension = str(file).split('.')[-1]
        upload = uploader.upload(file_type=extension, file_raw=open(file))
        log.append(upload)
    return log



files = ['catbox.py', 'test.py']
print(multiple(files))

#{'code': 200, 'file': 'https://files.catbox.moe/abcd.py'}

```

## Contributing

Bug reports and/or pull requests are welcome. I also copied most of this with minor changes/additions from cazqew's pycatbox (I was unable to make a pull/fork request due to being unable to find his Github page).

## License

The module is available as open source under the terms of the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)
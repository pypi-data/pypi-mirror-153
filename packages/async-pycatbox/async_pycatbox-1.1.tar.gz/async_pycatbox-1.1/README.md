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

## Example

```python
from async_pycatbox import Uploader
import asyncio

uploader = Uploader()

async def main():
    upload = await uploader.upload('py', open('test.py', 'rb').read())
    print(upload)

asyncio.run(main())
# https://files.catbox.moe/bav6l3.py
```

## Contributing

Bug reports and/or pull requests are welcome. I also copied most of this with minor changes/additions from cazqew's pycatbox (I was unable to make a pull/fork request due to being unable to find his Github page).

## License

The module is available as open source under the terms of the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)
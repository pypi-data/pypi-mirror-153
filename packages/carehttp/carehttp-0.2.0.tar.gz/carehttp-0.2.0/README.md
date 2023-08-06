📦 CareHttp
=======================

CareHttp cares your data.

It wraps from Requests and Retrying, retry several times when you encounter requests error.

Installation
-----

```bash
pip3 install carehttp
```

Usage
-----
example1 print the url:
```python
from carehttp import Carehttp

r = Carehttp().get(url='https://stackoverflow.com/', timeout=0.1)
print(r.text)

r = Carehttp().post('https://stackoverflow.com/', data={}, json={}, timeout=1)
print(r.text)
```
-----
example2 print a title:
```python

r = Carehttp(mark='title').get('https://stackoverflow.com/', timeout=1)
print(r.text)
```
-----
example3 custom retry setting:
```python
r = Carehttp(mark='title', tries=10, delay=1, max_delay=60).get('https://stackoverflow.com/', timeout=1)
print(r.text)
```

How to use carehttp
--------------

- It's a combination from [Requests] and [Retrying], only add a param **mark**
- Request part is exactly the same params with [Requests].
- Retry part termed params. Usage more like [Retry].
- If ignore **mark**, error displays the url, or else display the text of **mark**.

What else
--------------

-   More functions is planning.

License
-------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

  [Retrying]: https://github.com/rholder/retrying
  [Retry]: https://github.com/invl/retry
  [Requests]: https://github.com/psf/requests

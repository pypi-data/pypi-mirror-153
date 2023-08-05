# vk-paw | python vk.com API wrapper


![Maintenance](https://img.shields.io/maintenance/yes/2022?style=flat-square)
[![PyPI](https://img.shields.io/pypi/pyversions/vk-paw?style=flat-square)](https://pypi.org/project/vk-paw/)
[![Github CI](https://img.shields.io/github/checks-status/vk-paw/vk-paw/main?style=flat-square)](https://github.com/vk-paw/vk-paw/actions/)
[![Docs](https://img.shields.io/readthedocs/vk-paw?style=flat-square)](https://vk-paw.readthedocs.io/)


This is a vk.com (the largest Russian social network) python API wrapper. <br>
The goal is to support all API methods (current and future)  that can be accessed from server.


## Quickstart


#### Install


```bash
pip install vk-paw
```

#### Usage


```python
>>> import vk
>>> api = vk.API(access_token='...')
>>> api.users.get(user_ids=1)
[{'first_name': 'Pavel', 'last_name': 'Durov', 'id': 1}]
```

See official VK [documentation](https://dev.vk.com/method) for detailed API guide.


## More info


Read full documentation on [Read the Docs](https://vk-paw.readthedocs.org)


## Why this Fork?

This repository is a friendly fork of the cool work, started by [voronind](https://github.com/voronind/vk) (vk module creator)

Given the number of long-standing open issues and pull requests, and no clear path towards ensuring that maintenance of the package would continue or grow, this fork was created.

Contributions are most welcome.

# How to use

1. Create `conf` package
2. Create `conf/config.py` // Optional
3. Create `conf/config_deploy.py` // Optional
4. Add `logging.yaml` in `conf` // We have a default config, the logger file will write into `logs` directory as name `main.log`

## File Tree
```console
│   main.py
├───conf
│   │   config.py
│   │   config_deploy.py
│   │   logging.yaml
│   │   __init__.py
└───logs
        main.log
```

```python

import cuefig
from cuefig import logger

if __name__ == '__main__':
    logger.info("hi")
    print(f"username in conf/config.py: {cuefig.USERNAME}")
    print(f"password override in conf/config_deploy.py: {cuefig.PASSWORD}")
    print(f"Path var: {cuefig.ROOT_DIR}")
```

![img.png](https://raw.githubusercontent.com/FavorMylikes/cuefig/main/img/img.png)

- Here you can see, the config variable be `cue` as in very fast way. 
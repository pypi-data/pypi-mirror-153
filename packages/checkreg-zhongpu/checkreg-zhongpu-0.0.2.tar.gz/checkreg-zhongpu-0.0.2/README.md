# CheckReg
It can check whether a given email or phone number has been registered in websites.

## Supported Websites

### [dangdang](http://www.dangdang.com/)

```python
from checkreg import dangdang
x = dangdang.check_phone('13800112233')
```

The result `x` is a dictionary.
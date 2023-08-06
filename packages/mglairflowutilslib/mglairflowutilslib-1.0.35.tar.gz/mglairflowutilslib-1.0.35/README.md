
# Make sure you have upgraded version of pip
Windows
```
py -m pip install --upgrade pip
```

Linux/MAC OS
```
python3 -m pip install --upgrade pip
```

## Import package
```
from mglairflowutilslib import invoke_http_request
```

## Usage

```
url = 'http://example.com'
request_type = 'POST'
headers = {"Content-Type": "application/json"}
payload = {"foo": "bar"}
response, status = invoke_http_request(url, request_type, headers, payload)
```


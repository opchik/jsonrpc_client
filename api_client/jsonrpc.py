import json
import ssl
import urllib.request
import tempfile
import os
from django.conf import settings

class JsonRpcClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def call_method(self, method, params=None):
        if params is None:
            params = []

        request_data = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }).encode('utf-8')

        with tempfile.NamedTemporaryFile(delete=False) as cert_file, \
             tempfile.NamedTemporaryFile(delete=False) as key_file:
            cert_file.write(settings.CERTIFICATE.encode('utf-8'))
            key_file.write(settings.KEY.encode('utf-8'))
            cert_path = cert_file.name
            key_path = key_file.name

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        try:
            context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки сертификатов: {e}")
        finally:
            os.remove(cert_path)
            os.remove(key_path)

        req = urllib.request.Request(self.endpoint, data=request_data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req, context=context) as response:
                print(response)
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP ошибка: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Ошибка сети: {e.reason}")
        except json.JSONDecodeError:
            raise RuntimeError("Ошибка декодирования JSON ответа")

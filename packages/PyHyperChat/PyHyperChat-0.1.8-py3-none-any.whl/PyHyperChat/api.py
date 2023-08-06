import requests


class API:

    def __init__(self, ip, token: str, port=None, ssl_active=False):
        self.url = f"http{'s' if ssl_active else ''}://{ip}{f':{port}' if port else ''}"
        self.headers = {
            "Uuid-Cliente": token
        }
        self.api = {
            "lista_canales": "/bot/",
            "new_stats": f"/bot/stats/new"
        }

    def lista_canales(self):
        res = self.peticion_get(self.endpoint("lista_canales"))
        return res.get('data', None)

    def new_stats(self, data):
        res = self.peticion_post(self.endpoint("new_stats"), data)
        return res.get('data', None)

    def endpoint(self, nombre):
        if nombre not in self.api:
            return None
        return f"{self.url}{self.api[nombre]}"

    def peticion_post(self, endp, data=None):
        resp = requests.post(endp, json=data, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()

    def peticion_get(self, endp, data=None):
        resp = requests.get(endp, json=data, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()

from functools import wraps
from datetime import datetime
from .chat import ChatManager
from .api import API
import asyncio
import json


class Colors:
    INFO = "#FFFFFF"
    WARNING = "#FF9D00"
    ERROR = "#E22323"
    PASS = "#83E223"
    CLOUD = "#2596BE"

    @staticmethod
    def str_colored(string, color=INFO):
        return f"<span style='color: {color}'>{string}</span>"


class HyperChat:

    def __init__(self, token):
        self.host = "79.116.16.224:8519"
        self.ssl = False
        self.token = token
        self.rutas = {}
        self.api = API(self.host, self.token, ssl_active=self.ssl)
        self.chat_manager = None
        self.rutas_res = {}

        @self.handler(commands=["help"])
        def help(request):
            if len(request.get('message').split(" ")) == 1:
                self.send(request, '\n'.join([f"/{x}" for x in self.rutas.keys()]))
                return
            command = request.get('message').split(" ")[-1]
            if command in self.rutas:
                self.send(request, self.rutas[command].__doc__)
            else:
                self.send(request, "Command not implemented")

    def run(self):
        self.chat_manager = ChatManager(self, self.host, self.token, self.api.lista_canales(), ssl_active=self.ssl)
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        finally:
            loop.close()

    def handler(self, commands: list):
        def decorator(f):
            @wraps(f)
            def wrapper(*args):
                start_time = datetime.utcnow()
                request = args[0]
                request['commands'] = commands
                f(request)
                end_time = datetime.utcnow()
                total_time = (end_time - start_time).microseconds
                length_data = len(''.join(
                    [comm if not isinstance(comm, dict) else json.dumps(comm) for comm in self.rutas_res[commands[0]]]))
                self.rutas_res[commands[0]] = []
                final_data = dict(content_length=length_data,
                                  start=start_time.strftime("%Y/%m/%d %H:%M:%S"),
                                  end=end_time.strftime("%Y/%m/%d %H:%M:%S"),
                                  total_time=total_time,
                                  channel=request.get('channel'),
                                  sender=request.get('sender', {}).get('uuid'),
                                  command=request.get('ciphered'),
                                  nonce=request.get('ciphered_nonce'),
                                  tag=request.get('ciphered_tag'))
                self.api.new_stats(final_data)
            for comm in commands:
                self.rutas[comm] = wrapper
            self.rutas_res[commands[0]] = []
            return wrapper
        return decorator

    def send(self, request, mensaje, callback_function=None, display_color=Colors.INFO):
        commands = request.get('commands')
        token = request.get("channel")
        sender = request.get("sender", {}).get("uuid")
        chat = self.chat_manager.chat(token)
        mensaje = f"<span style='color: {display_color}'>{mensaje}</span>"
        chat.enviar(mensaje, sender, callback_function)
        self.rutas_res[commands[0]].append(mensaje)

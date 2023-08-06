from threading import Thread
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from websocket._exceptions import WebSocketConnectionClosedException
from datetime import datetime
import websocket
import json


class Chat:

    def __init__(self, hyper_chat, server_host, token, password, session_token, ssl_active=False):
        self.hyper_chat = hyper_chat
        self.server_host = server_host
        self.token = token
        self.password = password
        self.session_token = session_token
        self.ssl_active = ssl_active
        self.sock_connected = False
        self.sock = None
        self.menssages = []
        self.errors = []
        self.hilo = Thread(target=self.__start_ws)
        self.hilo.daemon = True
        self.hilo.start()
        self.status_check = "<connection_status>"
        self.pendientes = []
        self.callback_function = {}

    def enviar(self, mensaje: str, callback_user=None, callback_function=None):
        hashtags = {}
        for palabra in mensaje.split(" "):
            if palabra.startswith("#") and palabra[1:]:
                hashtag, n, t = self.__cifrar_mensaje(mensaje)
                hashtags[hashtag] = dict(nonce=n, tag=t)
        mensaje, nonce, tag = self.__cifrar_mensaje(mensaje)
        mensaje = {
            "message": mensaje,
            "channel": self.token,
            "hashtags": hashtags,
            "nonce": nonce,
            "tag": tag,
            "sendtime": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "bot": True
        }
        if self.sock_connected:
            self.sock.send(json.dumps(mensaje))
            if callback_function:
                self.callback_function[callback_user] = callback_function
        else:
            self.pendientes.append(mensaje)

    def __on_message(self, ws, message):
        mensaje = json.loads(message)

        msg_content = mensaje.get('message', None)
        file_data = mensaje.get('file', None)
        ciphered_msg = mensaje.get('message')

        if file_data or mensaje.get('bot', False):
            return

        mensaje['message'] = self.__descifrar_mensaje(mensaje.get('message'),
                                                      mensaje.get('nonce'),
                                                      mensaje.get('tag'))
        hashtags = []
        for hashtag, values in mensaje.get('hashtags').items():
            hashtags.append(self.__descifrar_mensaje(hashtag,
                                                     values.get('nonce'),
                                                     values.get('tag')))
        mensaje['hashtags'] = hashtags
        
        if not msg_content or mensaje.get('message') == self.status_check:
            return

        if mensaje.get('message').startswith('/') or self.callback_function.get(mensaje.get('sender', {}).get('uuid')):
            command = mensaje.get('message')[1:].split(" ")[0]
            if command in self.hyper_chat.rutas.keys():
                if f := self.hyper_chat.rutas.get(command, None):
                    mensaje.update(dict(ciphered=ciphered_msg,
                                        ciphered_nonce=mensaje.get('nonce'),
                                        ciphered_tag=mensaje.get('tag')))
                    f(mensaje)
            elif self.callback_function.get(mensaje.get('sender', {}).get('uuid')):
                mensaje.update(dict(ciphered=ciphered_msg,
                                    ciphered_nonce=mensaje.get('nonce'),
                                    ciphered_tag=mensaje.get('tag')))
                f = self.callback_function.pop(mensaje.get('sender', {}).get('uuid'))
                f(mensaje)

    def __on_close(self, ws, close_status_code, close_msg):
        self.sock_connected = False

    def __on_open(self, ws):
        self.sock_connected = True
        mensaje, nonce, tag = self.__cifrar_mensaje(self.status_check)
        payload = {
            "message": mensaje,
            "channel": self.token,
            "hashtags": {},
            "nonce": nonce,
            "tag": tag,
            "bot": True
        }
        ws.send(json.dumps(payload))
        for mensaje_pendiente in self.pendientes:
            ws.send(json.dumps(mensaje_pendiente))
        self.pendientes = []

    def __cifrar_mensaje(self, mensaje):
        key = SHA256.new(self.password.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(mensaje.encode())
        cipher_b64 = b64encode(ciphertext).decode()
        nonce_b64 = b64encode(nonce).decode()
        tag_b64 = b64encode(tag).decode()
        return cipher_b64, nonce_b64, tag_b64

    def __descifrar_mensaje(self, ciphertext, nonce, tag):
        ciphertext = b64decode(ciphertext.encode())
        nonce = b64decode(nonce.encode())
        tag = b64decode(tag.encode())
        key = SHA256.new(self.password.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        mensaje = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            return mensaje.decode()
        except:
            return None

    def __start_ws(self):
        websocket.enableTrace(False)
        while True:
            try:
                if not self.sock_connected:
                    self.sock = websocket.WebSocketApp(f"ws{'s' if self.ssl_active else ''}://{self.server_host}/ws/{self.token}/{self.session_token}",
                                                       on_open=self.__on_open,
                                                       on_message=self.__on_message,
                                                       on_close=self.__on_close)
                    self.sock.run_forever()
            except WebSocketConnectionClosedException:
                pass


class ChatManager:

    def __init__(self, hyper_chat, server_host, token, canales, ssl_active=False):
        self.hyper_chat = hyper_chat
        self.chats = {}
        for canal, password in canales.items():
            self.chats[canal] = Chat(self.hyper_chat, server_host, canal, password, token, ssl_active)

    def nuevo(self, chat: Chat):
        if chat.token not in self.chats.keys():
            self.chats[chat.token] = chat

    def chat(self, token: str):
        for chat_token, chat in self.chats.items():
            if chat_token == token:
                return chat

import json

from twisted.internet import ssl
from autobahn.twisted.websocket import connectWS
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory
from typing import Union


class LunoWebSocketClient():
	class LunoClientProtocol(WebSocketClientProtocol):
		callback = None

		def onMessage(self, payload: Union[str, bytes], isBinary: bool) -> None:
			print(payload)
			if self.callback is not None:
				if isBinary:
					data = payload.decode()
				else:
					data = payload

				self.callback(json.loads(data))

	def subscribe(self, callback: 'Function', pair: str):
		LunoWebSocketClient.LunoClientProtocol.callback = callback

		factory = WebSocketClientFactory(f'wss://ws.luno.com/api/1/stream/{pair}')
		factory.protocol = LunoWebSocketClient.LunoClientProtocol

		contextFactory = ssl.ClientContextFactory()
		connectWS(factory, contextFactory)

import treq

from typing import Dict
from luno.clients.abc import LunoClientBase
from luno.decorators import requires_authentication
from luno.exceptions import UnsupportedHttpVerbException
from twisted.internet.defer import Deferred
from twisted.internet.defer import inlineCallbacks


class LunoAsyncClient(LunoClientBase):
	def __init__(self, api_key: str=None, secret: str=None) -> None:
		self.api_key = api_key
		self.secret = secret
		
	@inlineCallbacks
	def _fetch_resource(self, method: str, suffix: str, params: Dict={}) -> Deferred:
		"""Helper function to make API requests

		Args:
		    method: The http verb i.e. get, post, put, delete
		    suffix: The uri suffix
		    params: A dict of query params

		Returns:
		    A twisted deferred
		"""
		url = f'{self.BASE_URI}{suffix}'
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		auth = (api_key, secret)

		resp = yield treq.request(method, url, params=params, headers=headers, auth=auth)
		data = yield resp.json()
		return data

	def ticker(self, pair: str) -> Deferred:
		"""Returns the latest ticker indicators

		Args:
			pair: A currency pair

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'ticker', {'pair': pair})

	def tickers(self) -> Deferred:
		"""Returns the latest ticker indicators from all active Luno exchanges

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'tickers')

	def order_book(self, pair: str) -> Deferred:
		"""Returns a list of bids and asks in the order book. Ask orders are sorted by price ascending. 
		Bid orders are sorted by price descending. Note that multiple orders at the same price are not necessarily conflated

		Args:
			pair: Currency pair e.g. XBTZAR

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'orderbook', {'pair': pair})

	def trades(self, pair: str, since: int=None) -> Deferred:
		"""Returns a list of the most recent trades. At most 100 results are returned per call

		Args:
			pair: Currency pair e.g. XBTZAR
			since: Fetch trades executed after this time, specified as a Unix timestamp in milliseconds

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		params = {'pair': pair}
		if since is not None:
			params['since'] = since
			
		return self._fetch_resource('get', 'trades', params)

	@requires_authentication
	def accounts(self, currency: str, name: str) -> Deferred:
		"""Create an additional account for the specified currency

		Args:
			currency: The currency code for the account you want to create e.g. XBT, IDR, MYR, ZAR
			name: The label to use for this account e.g. "Trading ACC".

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('post', 'trades', {'pair': pair, 'name': name})

	@requires_authentication
	def balance(self) -> Deferred:
		"""Return the list of all accounts and their respective balances

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'balance')

	@requires_authentication
	def transactions(self, account_id: int, min_row: int, max_row: int) -> Deferred:
		"""Return a list of transaction entries from an account.

		Transaction entry rows are numbered sequentially starting from 1, where 1 is the oldest entry. 
		The range of rows to return are specified with the min_row (inclusive) and max_row (exclusive) parameters. 
		At most 1000 rows can be requested per call.

		If min_row or max_row is non-positive, the range wraps around the most recent row. 

		For example, to fetch the 100 most recent rows, use min_row=-100 and max_row=0

		Args:
			account_id: Account ID
			min_row: Minimum of the row range to return (inclusive)
			max_row: Maximum of the row range to return (exclusive)

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource(
			'get', f'accounts/{account_id}/transactions', {'min_row': min_row, 'max_row': max_row})


	@requires_authentication
	def list_orders(self) -> Deferred:
		"""Trading on the market is done by submitting trade orders. 
		
		After a new order has been created, it is submitted for processing by the order matching engine.
		The order then either matches against an existing order in the order book and is filled or it rests in the order book until it is stopped. 

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'listorders')


	@requires_authentication
	def post_limit_order(
		self,
		pair: str,
		kind: str,
		volume: str,
		price: str,
		base_account_id: str=None,
		counter_account_id: str=None) -> Deferred:
		"""Create a new trade order

		If no base_account_id or counter_account_id are specified, your default base currency or counter currency account will be used. You can find your account IDs by calling the Balances API.
		
		Args:
			pair: The currency pair to trade e.g. XBTZAR
			kind: "BID" for a bid (buy) limit order or "ASK" for an ask (sell) limit order.
			volume: unt of Bitcoin to buy or sell as a decimal string in units of BTC e.g. "1.423".
			price: mit price as a decimal string in units of ZAR/BTC e.g. "1200".
			base_account_id: The base currency account to use in the trade.
			counter_account_id: The counter currency account to use in the trade.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		params = {
			'pair': pair,
			'type': kind,
			'volume': volume,
			'price': price
		}

		if base_account_id is not None:
			params['base_account_id'] = base_account_id,
		
		if counter_account_id is not None:
			params['counter_account_id'] = counter_account_id

		return self._fetch_resource('post', 'postorder', params)

	@requires_authentication
	def post_market_order(
		self,
		pair: str,
		kind: str,
		counter_volume: str=None,
		base_volume: str=None,
		base_account_id: str=None,
		counter_account_id: str=None) -> Deferred:
		"""
		Create a new market order.

		If no base_account_id or counter_account_id are specified, your default base currency or counter currency account will be used. You can find your account IDs by calling the Balances API.
		
		Note:
			A market order executes immediately, and either buys as much bitcoin that can be bought for a set amount of fiat currency, or sells a set amount of bitcoin for as much fiat as possible.
		
		Args:
			pair: The currency pair to trade e.g. XBTZAR
			kind: "BUY" to buy bitcoin, or "SELL" to sell bitcoin.
			counter_volume: - Required if kind is "BUY". Amount of local currency (e.g. ZAR, MYR) to spend as a decimal string in units of the local currency e.g. "100.50".
			base_volume: - Required if kind is "SELL". Amount of Bitcoin to sell as a decimal string in units of BTC e.g. "1.423".
			base_account_id: The base currency account to use in the trade.
			counter_account_id: The counter currency account to use in the trade.

		Returns:
			A twisted deferred which will eventually return a python dict
		"""
		if kind == 'BUY' and counter_volume is None:
			raise ValueError(f"counter_volume is required if the order type is 'BUY'")

		if kind == 'SELL' and base_volume is None:
			raise ValueError(f"base_volume is required if the order type is 'SELL'")

		params = {
			'pair': pair,
			'type': kind,
			'counter_volume': counter_volume,
			'base_volume': base_volume
		}

		if base_account_id is not None:
			params['base_account_id'] = base_account_id

		if counter_account_id is not None:
			params['counter_account_id'] = counter_account_id

		return self._fetch_resource('post', 'marketorder', params)

	@requires_authentication
	def cancel_order(self, order_id: str) -> Deferred:
		"""Request to stop an order.
			
		Args:
			order_id: The order reference as a string e.g. BXMC2CJ7HNB88U4

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('post', 'marketorder', {'order_id': order_id})

	@requires_authentication
	def get_order(self, order_id: str) -> Deferred:
		"""Get an order by its id.
			
		Args:
			order_id: The order ID

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', f'orders/{order_id}')

	@requires_authentication
	def list_trades(
		self,
		pair: str,
		since: int=None,
		limit: int=None) -> Deferred:
		"""Returns a list of your recent trades for a given pair, sorted by oldest first.

		Note:
			- The 'type' in the response indicates the type of order that you placed in order to participate in the trade. Possible types include BID and ASK.
			- If is_buy in the response is true, then the order which completed the trade (market taker) was a bid order.
			- Results of this query may lag behind the latest data.
			
		Args:
			pair: Filter to trades of this currency pair e.g. XBTZAR
			since: Filter to trades on or after this timestamp, e.g. 1470810728478
			limit: Limit to this number of trades (min 1, max 100, default 100)

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		params = {'pair': pair}

		if since is not None:
			params['since'] = since
			
		if limit is not None:
			params['limit'] = limit

		return self._fetch_resource('get', 'listtrades', params=params)

	@requires_authentication
	def fee_info(self, pair: str) -> Deferred:
		"""Returns your fees and 30 day trading volume (as of midnight) for a given pair.

		Args:
			pair: Filter to trades of this currency pair e.g. XBTZAR

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'fee_info', params={'pair': pair})

	@requires_authentication
	def receive_addresses(self, asset: str, address: str=None) -> Deferred:
		"""Returns the default receive address associated with your account and the amount received via the address. 
		You can specify an optional address parameter to return information for a non-default receive address. 
		In the response, total_received is the total confirmed Bitcoin amount received excluding unconfirmed transactions. 
		The total_unconfirmed is the total sum of unconfirmed receive transactions.

		Args:
			asset: Currency code of the asset e.g. XBT
			address: Specific Bitcoin address to retrieve. If not provided, the default address will be used.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'funding_address', params={'asset': asset, 'address': address})

	@requires_authentication
	def create_receive_address(self, asset: str) -> Deferred:
		"""Allocates a new receive address to your account. 
		There is a rate limit of 1 address per hour, but bursts of up to 10 addresses are allowed.

		Args:
			asset: Currency code of the asset e.g. XBT

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('post', 'funding_address', params={'asset': asset})

	@requires_authentication
	def withdrawals(self) -> Deferred:
		"""Returns a list of withdrawal requests.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', 'withdrawals')

	@requires_authentication
	def create_withdrawal_request(self) -> Deferred:
		"""Creates a new withdrawal request

		Args:
			kind: Withdrawal types e.g. ZAR_EFT, NAD_EFT, KES_MPESA, MYR_IBG, IDR_LLG
			amount: Amount to withdraw. The currency depends on the type.
			beneficiary_id: The beneficiary ID of the bank account the withdrawal will be paid out to. This parameter is required if you have multiple bank accounts. Your bank account beneficiary ID can be found by clicking on the beneficiary name on the Beneficiaries page. 

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		params = {
			'type': kind,
			'amount': amount,
			'beneficiary_id': beneficiary_id,
		}
		
		return self._fetch_resource('post', 'withdrawals', params=params)

	@requires_authentication
	def withdrawal_request_status(self, withdrawal_id: int) -> Deferred:
		"""Returns the status of a particular withdrawal request.

		Args:
			withdrawal_id: Withdrawal ID to retrieve.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('post', 'withdrawals', {'id': withdrawal_id})

	@requires_authentication
	def cancel_withdrawal_request(self, withdrawal_id: int) -> Deferred:
		"""Cancel a withdrawal request. This can only be done if the request is still in state PENDING.

		Args:
			withdrawal_id: ID of the withdrawal to cancel.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('delete', 'withdrawals', {'id': withdrawal_id})

	@requires_authentication
	def send(
		self,
		amount: str,
		currency: str,
		address: str,
		description: str=None,
		message: str=None) -> Deferred:
		"""

		Args:
			amount: Amount to send as a decimal string.
			currency: Currency to send e.g. XBT
			address: Destination Bitcoin address or email address to send to.
			description: Description for the transaction to record on the account statement.
			message: Message to send to the recipient. This is only relevant when sending to an email address.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		params = {
			'amount': amount,
			'currency': currency,
			'address': address
		}

		if description is not None:
			params['description'] = description
		
		if message is not None:
			params['message'] = message

		return self._fetch_resource('post', 'withdrawals', params)

	@requires_authentication
	def create_quote(
		self,
		kind: str,
		base_amount: str,
		pair: str) -> Deferred:
		"""Creates a new quote to buy or sell a particular amount.

		You can specify either the exact amount that you want to pay or the exact amount that you want too receive.
		For example, to buy exactly 0.1 Bitcoin using ZAR, you would create a quote to BUY 0.1 XBTZAR. The returned quote includes the appropriate ZAR amount. 
		To buy Bitcoin using exactly ZAR 100, you would create a quote to SELL 100 ZARXBT. 
		The returned quote specifies the Bitcoin as the counter amount that will be returned.
		An error is returned if your account is not verified for the currency pair, or if your account would have insufficient balance to ever exercise the quote. 

		Args:
			kind: Possible types: BUY, SELL
			base_amount: Amount to buy or sell in the pair base currency.
			pair: Currency pair to trade e.g. XBTZAR, XBTMYR. The pair can also be flipped if you want to buy or sell the counter currency (e.g. ZARXBT).

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		params = {
			'type': kind,
			'base_amount': base_amount,
			'pair': pair
		}

		return self._fetch_resource('post', 'quotes', params)


	@requires_authentication
	def get_quote(
		self,
		quote_id: int) -> Deferred:
		"""Get the latest status of a quote.

		Args:
			quote_id: ID of the quote to retrieve.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('get', f'quotes/{quote_id}')

	@requires_authentication
	def exercise_quote(
		self,
		quote_id: int) -> Deferred:
		"""Exercise a quote to perform the trade. 

		If there is sufficient balance available in your account, it will be debited and the counter amount credited.
		An error is returned if the quote has expired or if you have insufficient available balance.

		Args:
			quote_id: ID of the quote to retrieve.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('put', f'quotes/{quote_id}')

	@requires_authentication
	def discard_quote(
		self,
		quote_id: int) -> Deferred:
		"""Discard a quote. Once a quote has been discarded, it cannot be exercised even if it has not expired yet.

		Args:
			quote_id: ID of the quote to retrieve.

		Returns:
		    A twisted deferred which will eventually return a python dict
		"""
		return self._fetch_resource('delete', f'quotes/{quote_id}')
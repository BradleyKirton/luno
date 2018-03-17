from requests import Session
from requests.auth import HTTPBasicAuth
from luno.clients.abc import LunoClientBase
from luno.decorators import requires_authentication
from luno.exceptions import UnsupportedHttpVerbException

from typing import Dict


class LunoSyncClient(LunoClientBase):
	def __init__(self, api_key: str=None, secret: str=None) -> None:
		self.api_key = api_key
		self.secret = secret
		self.session = Session()
		
		if api_key is not None and secret is not None:
			self.session.auth = HTTPBasicAuth(api_key, secret)

	def _fetch_resource(self, method: str, suffix: str, params: Dict={}) -> Dict:
		url = f'{self.BASE_URI}{suffix}'
		if method == 'get':
			resp = self.session.get(url, params=params)
		elif method == 'post':
			resp = self.session.post(url, params=params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
		elif method == 'delete':
			resp = self.session.delete(url, params=params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
		elif method == 'put':
			resp = self.session.put(url, params=params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
		else:
			raise UnsupportedHttpVerbException(f'http verb {method} is not supported')

		resp.raise_for_status()

		return resp.json()

	def ticker(self, pair: str) -> Dict:
		"""Returns the latest ticker indicators

		Args:
			pair: A currency pair

		Returns:
		    A python dict of ticker indicators
		"""
		return self._fetch_resource('get', 'ticker', {'pair': pair})

	def tickers(self) -> Dict:
		"""Returns the latest ticker indicators from all active Luno exchanges

		Returns:
		    A python dict of ticker indicators
		"""
		return self._fetch_resource('get', 'tickers')

	def order_book(self, pair: str) -> Dict:
		"""Returns a list of bids and asks in the order book. Ask orders are sorted by price ascending. 
		Bid orders are sorted by price descending. Note that multiple orders at the same price are not necessarily conflated

		Args:
			pair: Currency pair e.g. XBTZAR

		Returns:
		    A python dict of orders data
		"""
		return self._fetch_resource('get', 'orderbook', {'pair': pair})

	def trades(self, pair: str, since: int=None) -> Dict:
		"""Returns a list of the most recent trades. At most 100 results are returned per call

		Args:
			pair: Currency pair e.g. XBTZAR
			since: Fetch trades executed after this time, specified as a Unix timestamp in milliseconds

		Returns:
		    A python dict of trade data
		"""
		params = {'pair': pair}
		if since is not None:
			params['since'] = since
			
		return self._fetch_resource('get', 'trades', params)

	@requires_authentication
	def accounts(self, currency: str, name: str) -> Dict:
		"""Create an additional account for the specified currency

		Args:
			currency: The currency code for the account you want to create e.g. XBT, IDR, MYR, ZAR
			name: The label to use for this account e.g. "Trading ACC".

		Returns:
		    A python dict of account data
		"""
		return self._fetch_resource('post', 'accounts', {'currency': currency, 'name': name})

	@requires_authentication
	def balance(self) -> Dict:
		"""Return the list of all accounts and their respective balances

		Returns:
		    A python dict of balance data
		"""
		return self._fetch_resource('get', 'balance')

	@requires_authentication
	def transactions(self, account_id: int, min_row: int, max_row: int) -> Dict:
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
		    A python dict of transaction data
		"""
		return self._fetch_resource(
			'get', f'accounts/{account_id}/transactions', {'min_row': min_row, 'max_row': max_row})


	@requires_authentication
	def list_orders(self) -> Dict:
		"""Trading on the market is done by submitting trade orders. 
		
		After a new order has been created, it is submitted for processing by the order matching engine.
		The order then either matches against an existing order in the order book and is filled or it rests in the order book until it is stopped. 

		Returns:
		    A python dict of orders data
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
		counter_account_id: str=None) -> Dict:
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
		    A python dict of order data
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
		counter_volume: str,
		base_volume: str,
		base_account_id: str=None,
		counter_account_id: str=None) -> Dict:
		"""
		Create a new market order.

		If no base_account_id or counter_account_id are specified, your default base currency or counter currency account will be used. You can find your account IDs by calling the Balances API.
		
		Note:
			A market order executes immediately, and either buys as much bitcoin that can be bought for a set amount of fiat currency, or sells a set amount of bitcoin for as much fiat as possible.
		
		Args:
			pair: The currency pair to trade e.g. XBTZAR
			kind: "BUY" to buy bitcoin, or "SELL" to sell bitcoin.
			counter_volume: - if type is "BUY" 	For a "BUY" order: amount of local currency (e.g. ZAR, MYR) to spend as a decimal string in units of the local currency e.g. "100.50".
			base_volume: - if type is "SELL" 	For a "SELL" order: amount of Bitcoin to sell as a decimal string in units of BTC e.g. "1.423".
			base_account_id: The base currency account to use in the trade.
			counter_account_id: The counter currency account to use in the trade.

		Returns:
			A python dict of order data		
		"""
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
	def cancel_order(self, order_id: str) -> Dict:
		"""Request to stop an order.
			
		Args:
			order_id: The order reference as a string e.g. BXMC2CJ7HNB88U4

		Returns:
		    A python dict indicating success or failure
		"""
		return self._fetch_resource('post', 'stoporder', {'order_id': order_id})

	@requires_authentication
	def get_order(self, order_id: str) -> Dict:
		"""Get an order by its id.
			
		Args:
			order_id: The order ID

		Returns:
		    A python dict of order data
		"""
		return self._fetch_resource('get', f'orders/{order_id}')

	@requires_authentication
	def list_trades(
		self,
		pair: str,
		since: int=None,
		limit: int=None) -> Dict:
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
		    A python dict of order data
		"""
		params = {'pair': pair}

		if since is not None:
			params['since'] = since
			
		if limit is not None:
			params['limit'] = limit

		return self._fetch_resource('get', 'listtrades', params=params)

	@requires_authentication
	def fee_info(self, pair: str) -> Dict:
		"""Returns your fees and 30 day trading volume (as of midnight) for a given pair.

		Args:
			pair: Filter to trades of this currency pair e.g. XBTZAR

		Returns:
		    A python dict of fee data
		"""
		return self._fetch_resource('get', 'fee_info', params={'pair': pair})

	@requires_authentication
	def receive_addresses(self, asset: str, address: str=None) -> Dict:
		"""Returns the default receive address associated with your account and the amount received via the address. 
		You can specify an optional address parameter to return information for a non-default receive address. 
		In the response, total_received is the total confirmed Bitcoin amount received excluding unconfirmed transactions. 
		The total_unconfirmed is the total sum of unconfirmed receive transactions.

		Args:
			asset: Currency code of the asset e.g. XBT
			address: Specific Bitcoin address to retrieve. If not provided, the default address will be used.

		Returns:
		    A python dict of addresses
		"""
		return self._fetch_resource('get', 'funding_address', params={'asset': asset, 'address': address})

	@requires_authentication
	def create_receive_address(self, asset: str) -> Dict:
		"""Allocates a new receive address to your account. 
		There is a rate limit of 1 address per hour, but bursts of up to 10 addresses are allowed.

		Args:
			asset: Currency code of the asset e.g. XBT

		Returns:
		    A python dict of address data
		"""
		return self._fetch_resource('post', 'funding_address', params={'asset': asset})

	@requires_authentication
	def withdrawals(self) -> Dict:
		"""Returns a list of withdrawal requests.

		Returns:
		    A python dict of withdrawal data
		"""
		return self._fetch_resource('get', 'withdrawals')

	@requires_authentication
	def create_withdrawal_request(self, kind: str, amount: str, beneficiary_id: str=None) -> Dict:
		"""Creates a new withdrawal request

		Args:
			kind: Withdrawal types e.g. ZAR_EFT, NAD_EFT, KES_MPESA, MYR_IBG, IDR_LLG
			amount: Amount to withdraw. The currency depends on the type.
			beneficiary_id: The beneficiary ID of the bank account the withdrawal will be paid out to. This parameter is required if you have multiple bank accounts. Your bank account beneficiary ID can be found by clicking on the beneficiary name on the Beneficiaries page. 

		Returns:
		    A python dict of withdrawal request data
		"""
		params = {
			'type': kind,
			'amount': amount,
			'beneficiary_id': beneficiary_id,
		}
		
		return self._fetch_resource('post', 'withdrawals', params=params)

	@requires_authentication
	def withdrawal_request_status(self, withdrawal_id: int) -> Dict:
		"""Returns the status of a particular withdrawal request.

		Args:
			withdrawal_id: Withdrawal ID to retrieve.

		Returns:
		    A python dict of withdrawal request data
		"""
		return self._fetch_resource('get', f'withdrawals/{withdrawal_id}')

	@requires_authentication
	def cancel_withdrawal_request(self, withdrawal_id: int) -> Dict:
		"""Cancel a withdrawal request. This can only be done if the request is still in state PENDING.

		Args:
			withdrawal_id: ID of the withdrawal to cancel.

		Returns:
		    A python dict of withdrawal request data
		"""
		return self._fetch_resource('delete', f'withdrawals/{withdrawal_id}')

	@requires_authentication
	def send(
		self,
		amount: str,
		currency: str,
		address: str,
		description: str=None,
		message: str=None) -> Dict:
		"""

		Args:
			amount: Amount to send as a decimal string.
			currency: Currency to send e.g. XBT
			address: Destination Bitcoin address or email address to send to.
			description: Description for the transaction to record on the account statement.
			message: Message to send to the recipient. This is only relevant when sending to an email address.

		Returns:
		    A python dict of indicating the status of the send request
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

		return self._fetch_resource('post', 'send', params)

	@requires_authentication
	def create_quote(
		self,
		kind: str,
		base_amount: str,
		pair: str) -> Dict:
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
		    A python dict of quote data
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
		quote_id: int) -> Dict:
		"""Get the latest status of a quote.

		Args:
			quote_id: ID of the quote to retrieve.

		Returns:
		    A python dict of quote data
		"""
		return self._fetch_resource('get', f'quotes/{quote_id}')

	@requires_authentication
	def exercise_quote(
		self,
		quote_id: int) -> Dict:
		"""Exercise a quote to perform the trade. 

		If there is sufficient balance available in your account, it will be debited and the counter amount credited.
		An error is returned if the quote has expired or if you have insufficient available balance.

		Args:
			quote_id: ID of the quote to retrieve.

		Returns:
		    A python dict of quote data
		"""
		return self._fetch_resource('put', f'quotes/{quote_id}')

	@requires_authentication
	def discard_quote(
		self,
		quote_id: int) -> Dict:
		"""Discard a quote. Once a quote has been discarded, it cannot be exercised even if it has not expired yet.

		Args:
			quote_id: ID of the quote to retrieve.

		Returns:
		    A python dict of quote data
		"""
		return self._fetch_resource('delete', f'quotes/{quote_id}')
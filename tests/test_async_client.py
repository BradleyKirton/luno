from luno.clients.asynchronous import LunoAsyncClient
from luno.exceptions import UnauthorisedResourceException

import pytest
import pytest_twisted


class Response:
    def raise_for_status(self) -> None:
        pass

    def json(self):
        return {}


@pytest.fixture
def response():
    """Provides a response object as a fixture"""
    return Response()


@pytest.fixture
def client():
    """Provides an authorized client as a fixture"""
    return LunoAsyncClient()


@pytest.fixture
def uclient():
    """Provides an unauthorized client as a fixture"""
    return LunoAsyncClient("api_key", "secret")


@pytest_twisted.inlineCallbacks
def test_ticker(mocker, response, client) -> None:
    """Test the ticker method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}ticker"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield client.ticker(pair="XBTZAR")

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_tickers(mocker, response, client) -> None:
    """Test the test_tickers method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}tickers"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield client.tickers()

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_order_book(mocker, response, client) -> None:
    """Test the test_order_book method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}orderbook"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield client.order_book(pair="XBTZAR")

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_trades(mocker, response, client) -> None:
    """Test the test_trades method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}trades"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield client.trades(pair="XBTZAR", since=100)

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_private_resource_raises(mocker, response, client) -> None:
    """Tests that accessing a private resource raises the UnauthorisedResourceException
    exception when accessing it with an unathenticated client"""
    url = f"{LunoAsyncClient.BASE_URI}accounts"
    data = {}

    mocker.patch("treq.request", return_value=response)

    with pytest.raises(UnauthorisedResourceException):
        response = yield client.accounts(currency="ZAR", name="testing")


@pytest_twisted.inlineCallbacks
def test_accounts(mocker, response, uclient) -> None:
    """Test the test_accounts method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}accounts"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield uclient.accounts(currency="ZAR", name="testing")

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_balance(mocker, response, uclient) -> None:
    """Test the test_balance method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}balance"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield uclient.balance()

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_transactions(mocker, response, uclient) -> None:
    """Test the test_transactions method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}accounts/1/transactions"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield uclient.transactions(1, 1, 1)

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_list_orders(mocker, response, uclient) -> None:
    """Test the test_list_orders method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}listorders"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield uclient.list_orders()

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_post_limit_order(mocker, response, uclient) -> None:
    """Test the test_post_limit_order method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}postorder"
    data = {}

    mocker.patch("treq.request", return_value=response)
    kwargs = {
        "pair": "test",
        "kind": "test",
        "volume": "test",
        "price": "test",
        "base_account_id": "test",
        "counter_account_id": "test",
    }

    response = yield uclient.post_limit_order(**kwargs)
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_post_market_order(mocker, response, uclient) -> None:
    """Test the test_post_market_order method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}marketorder"
    data = {}

    mocker.patch("treq.request", return_value=response)
    kwargs = {
        "pair": "test",
        "kind": "test",
        "counter_volume": "test",
        "base_volume": "test",
        "base_account_id": "test",
        "counter_account_id": "test",
    }

    response = yield uclient.post_market_order(**kwargs)
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_cancel_order(mocker, response, uclient) -> None:
    """Test the test_cancel_order method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}stoporder"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.cancel_order(order_id="1234")
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_get_order(mocker, response, uclient) -> None:
    """Test the test_get_order method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}orders/1234"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.get_order(order_id="1234")
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_list_trades(mocker, response, uclient) -> None:
    """Test the test_list_trades method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}listtrades"
    data = {}

    mocker.patch("treq.request", return_value=response)
    kwargs = {"pair": "test", "since": "test", "limit": "test"}

    response = yield uclient.list_trades(**kwargs)
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_fee_info(mocker, response, uclient) -> None:
    """Test the test_fee_info method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}fee_info"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield uclient.fee_info(pair="XBTZAR")

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_receive_addresses(mocker, response, uclient) -> None:
    """Test the test_receive_addresses method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}funding_address"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.receive_addresses(asset="test", address="test")
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_create_receive_address(mocker, response, uclient) -> None:
    """Test the test_create_receive_address method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}funding_address"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield uclient.create_receive_address(asset="test")

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_withdrawals(mocker, response, uclient) -> None:
    """Test the test_withdrawals method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}withdrawals"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.withdrawals()
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_create_withdrawal_request(mocker, response, uclient) -> None:
    """Test the test_create_withdrawal_request method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}withdrawals"
    data = {}

    mocker.patch("treq.request", return_value=response)
    kwargs = {"kind": "test", "amount": "test", "beneficiary_id": "test"}

    response = yield uclient.create_withdrawal_request(**kwargs)
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_withdrawal_request_status(mocker, response, uclient) -> None:
    """Test the test_withdrawal_request_status method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}withdrawals/1234"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.withdrawal_request_status(withdrawal_id="1234")
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_cancel_withdrawal_request(mocker, response, uclient) -> None:
    """Test the test_cancel_withdrawal_request method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}withdrawals/1234"
    data = {}

    mocker.patch("treq.request", return_value=response)
    response = yield uclient.cancel_withdrawal_request(withdrawal_id="1234")

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_send(mocker, response, uclient) -> None:
    """Test the (client method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}send"
    data = {}

    mocker.patch("treq.request", return_value=response)
    kwargs = {
        "amount": "test",
        "currency": "test",
        "address": "test",
        "description": "test",
        "message": "test",
    }

    response = yield uclient.send(**kwargs)

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_create_quote(mocker, response, uclient) -> None:
    """Test the test_create_quote method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}quotes"
    data = {}

    mocker.patch("treq.request", return_value=response)
    kwargs = {"kind": "test", "base_amount": "test", "pair": "test"}

    response = yield uclient.create_quote(**kwargs)

    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_get_quote(mocker, response, uclient) -> None:
    """Test the test_get_quote method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}quotes/1"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.get_quote(quote_id=1)
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_exercise_quote(mocker, response, uclient) -> None:
    """Test the test_exercise_quote method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}quotes/1"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.exercise_quote(quote_id=1)
    message = f"expected response {data}, received {response}"
    assert data == response, message


@pytest_twisted.inlineCallbacks
def test_discard_quote(mocker, response, uclient) -> None:
    """Test the test_discard_quote method of the sync client"""
    url = f"{LunoAsyncClient.BASE_URI}quotes/1"
    data = {}

    mocker.patch("treq.request", return_value=response)

    response = yield uclient.discard_quote(quote_id=1)
    message = f"expected response {data}, received {response}"
    assert data == response, message

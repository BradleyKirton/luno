import pytest
import requests_mock

from luno.exceptions import UnauthorisedResourceException
from luno.clients.sync import LunoSyncClient


@pytest.fixture
def client():
    """Provides an authorized client as a fixture"""
    return LunoSyncClient('api_key', 'secret')


@pytest.fixture
def uclient():
    """Provides an unauthorized client as a fixture"""
    return LunoSyncClient()


def test_ticker(client) -> None:
    """Test the ticker method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}ticker'
    data = {}

    with requests_mock.mock() as m:
        m.get(url, json=data)
        response = client.ticker(pair='XBTZAR')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message

def test_tickers(client) -> None:
    """Test the test_tickers method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}tickers'
    data = {}

    with requests_mock.mock() as m:
        m.get(url, json=data)
        response = client.tickers()
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_order_book(client) -> None:
    """Test the test_order_book method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}orderbook'
    data = {}

    with requests_mock.mock() as m:
        m.get(url, json=data)
        response = client.order_book(pair='XBTZAR')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_trades(client) -> None:
    """Test the test_trades method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}trades'
    data = {}

    with requests_mock.mock() as m:
        m.get(url, json=data)
        response = client.trades(pair='XBTZAR', since=100)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_accounts(client) -> None:
    """Test the test_accounts method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}accounts'
    data = {}

    with requests_mock.mock() as m:
        m.post(url, json=data)

        response = client.accounts(currency='ZAR', name='testing')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_balance(client) -> None:
    """Test the test_balance method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}balance'
    data = {}

    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.balance()
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_transactions(client) -> None:
    """Test the test_transactions method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}accounts/1/transactions'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.transactions(1, 1, 1)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_list_orders(client) -> None:
    """Test the test_list_orders method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}listorders'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.list_orders()
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_post_limit_order(client) -> None:
    """Test the test_post_limit_order method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}postorder'
    data = {}
    
    with requests_mock.mock() as m:
        m.post(url, json=data)

        kwargs = {
            'pair': 'test',
            'kind': 'test',
            'volume': 'test',
            'price': 'test',
            'base_account_id': 'test',
            'counter_account_id': 'test'
        }

        response = client.post_limit_order(**kwargs)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_post_market_order(client) -> None:
    """Test the test_post_market_order method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}marketorder'
    data = {}
    
    with requests_mock.mock() as m:
        m.post(url, json=data)

        kwargs = {
            'pair': 'test',
            'kind': 'test',
            'counter_volume': 'test',
            'base_volume': 'test',
            'base_account_id': 'test',
            'counter_account_id': 'test'
        }

        response = client.post_market_order(**kwargs)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_cancel_order(client) -> None:
    """Test the test_cancel_order method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}stoporder'
    data = {}
    
    with requests_mock.mock() as m:
        m.post(url, json=data)

        response = client.cancel_order(order_id='1234')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_get_order(client) -> None:
    """Test the test_get_order method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}orders/1234'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.get_order(order_id='1234')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message
    

def test_list_trades(client) -> None:
    """Test the test_list_trades method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}listtrades'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        kwargs = {
            'pair': 'test',
            'since': 'test',
            'limit': 'test'    
        }

        response = client.list_trades(**kwargs)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message
    

def test_fee_info(client) -> None:
    """Test the test_fee_info method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}fee_info'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.fee_info(pair='XBTZAR')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_receive_addresses(client) -> None:
    """Test the test_receive_addresses method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}funding_address'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.receive_addresses(asset='test', address='test')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_create_receive_address(client) -> None:
    """Test the test_create_receive_address method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}funding_address'
    data = {}
    
    with requests_mock.mock() as m:
        m.post(url, json=data)

        response = client.create_receive_address(asset='test')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_withdrawals(client) -> None:
    """Test the test_withdrawals method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}withdrawals'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.withdrawals()
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_create_withdrawal_request(client) -> None:
    """Test the test_create_withdrawal_request method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}withdrawals'
    data = {}
    
    with requests_mock.mock() as m:
        m.post(url, json=data)

        kwargs = {
            'kind': 'test',
            'amount': 'test',
            'beneficiary_id': 'test'
        }

        response = client.create_withdrawal_request(**kwargs)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_withdrawal_request_status(client) -> None:
    """Test the test_withdrawal_request_status method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}withdrawals/1234'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.withdrawal_request_status(withdrawal_id='1234')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_cancel_withdrawal_request(client) -> None:
    """Test the test_cancel_withdrawal_request method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}withdrawals/1234'
    data = {}
    
    with requests_mock.mock() as m:
        m.delete(url, json=data)

        response = client.cancel_withdrawal_request(withdrawal_id='1234')
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_send(client) -> None:
    """Test the (client method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}send'
    data = {}
    
    with requests_mock.mock() as m:
        m.post(url, json=data)

        kwargs = {
            'amount': 'test',
            'currency': 'test',
            'address': 'test',
            'description': 'test',
            'message': 'test'
        }

        response = client.send(**kwargs)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_create_quote(client) -> None:
    """Test the test_create_quote method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}quotes'
    data = {}
    
    with requests_mock.mock() as m:
        m.post(url, json=data)

        kwargs = {
            'kind': 'test',
            'base_amount': 'test',
            'pair': 'test'
        }

        response = client.create_quote(**kwargs)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_get_quote(client) -> None:
    """Test the test_get_quote method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}quotes/1'
    data = {}
    
    with requests_mock.mock() as m:
        m.get(url, json=data)

        response = client.get_quote(quote_id=1)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_exercise_quote(client) -> None:
    """Test the test_exercise_quote method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}quotes/1'
    data = {}
    
    with requests_mock.mock() as m:
        m.put(url, json=data)

        response = client.exercise_quote(quote_id=1)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message


def test_discard_quote(client) -> None:
    """Test the test_discard_quote method of the sync client"""
    url = f'{LunoSyncClient.BASE_URI}quotes/1'
    data = {}
    
    with requests_mock.mock() as m:
        m.delete(url, json=data)

        response = client.discard_quote(quote_id=1)
        
        message = (f"expected reponse {data}, received {response}")
        assert data == response, message

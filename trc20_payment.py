import requests

from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider


# TRC20 лимит коммисии (ставить от 16, иначе транзакция может не пройти)
TRC20_FEE_LIMIT = 20_000_000 # Лимит 20 TRX

# USDT TRC20 Contract Address
USDT_CONTRACT_ADDRESS = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'

# API ключ от TronGrid
TRON_GRID_API_KEY = ''

ABI = [{
     "outputs":[
        {
           "type":"bool"
        }
     ],
     "inputs":[
        {
           "name":"_to",
           "type":"address"
        },
        {
           "name":"_value",
           "type":"uint256"
        }
     ],
     "name":"transfer",
     "stateMutability":"Nonpayable",
     "type":"Function"
  }]


class TRCToken:
    """Класс для взаимодействия с токенами TRC20 и TRX."""
    
    TRONSCAN_API_URL = "https://apilist.tronscan.org/api/account"
    
    def __init__(self):
        self.tron = Tron(HTTPProvider(api_key=TRON_GRID_API_KEY))

    @staticmethod
    def create_trc20_address():
        """Создать новый адрес TRC20"""
        private_key = PrivateKey.random()
        address = private_key.public_key.to_base58check_address()
        return private_key.hex(), address

    def _get_token_balance(self, address, token_symbol):
        """Получить баланс адреса"""
        payload = {"address": address}
        try:
            response = requests.get(self.TRONSCAN_API_URL, params=payload)
            data = response.json()
            if token_symbol == "trx":
                balances = data["tokenBalances"]
            else:
                balances = data["trc20token_balances"]
            token_balance = next((item for item in balances if item["tokenAbbr"] == token_symbol), None)
        except Exception as e:
            return 0
        
        if token_balance:
            if token_symbol == "USDT":
                return int(token_balance["balance"]) / 1_000_000
            return int(token_balance["balance"])
        return 0

    def get_trc20_balance(self, address, token_symbol="USDT"):
        """Получить баланс TRC20"""
        return self._get_token_balance(address, token_symbol)

    def get_trx_balance(self, address, token_symbol="trx"):
        """Получуть баланс TRX"""
        return self._get_token_balance(address, token_symbol)

    def transfer_all_trc20(self, from_address, private_key, to_address):
        """Отправить весь баланс trc20 на указанный адрес"""
        sender_key = PrivateKey(bytes.fromhex(private_key))
        balance = int(self.get_trc20_balance(from_address) * (10**6))
        if balance == 0:
            return False, False
        contract = self.tron.get_contract(USDT_CONTRACT_ADDRESS)
        contract.abi = ABI
        tx = (contract.functions.transfer(to_address, balance)
              .with_owner(sender_key.public_key.to_base58check_address())
              .fee_limit(TRC20_FEE_LIMIT)
              .build()
              .sign(sender_key))
        broadcasted_tx = tx.broadcast().wait()
        try:
            return broadcasted_tx['result'], broadcasted_tx['id']
        except Exception:
            return False, False

    def send_trx(self, private_key_str, to_address, from_address, amount):
        """Отправить TRX на указанный адрес."""
        private_key = PrivateKey(bytes.fromhex(private_key_str))
        txn = (self.tron.trx.transfer(from_address, to_address, amount)
               .build()
               .sign(private_key))
        return txn.broadcast().wait()
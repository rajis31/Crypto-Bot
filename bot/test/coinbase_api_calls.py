from coinbase.wallet.client import Client
import config

client = Client(config.api_key, config.api_secret)
print(client)

# Get list of accounts
accounts = client.get_accounts()
assert isinstance(accounts.data, list)
print(accounts)
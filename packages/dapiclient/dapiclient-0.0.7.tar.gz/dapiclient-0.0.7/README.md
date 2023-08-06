A very basic DAPI client. Only supports retrieving from some JSON-RPC and gRPC
endpoints. No validation of anything. No submitting of data, tx creation,
signing, etc.

# Requirements

```
python3
python3-venv
```

# Quickstart


```
git clone https://github.com/mayoreee/dapi-client-py.git
cd dapi-client-py
python3 -m venv dapiclient-venv
source dapiclient-venv/bin/activate
pip install -r requirements.txt
python install .

# Check masternode list
python dapiclient/test-mndiscovery.py

# Check DAPI client functionality
python dapiclient/test-dapiclient.py
```

# Examples


## Layer 1

```python
from dapiclient.client import DAPIClient

client = DAPIClient()

current_block_hash = client.getBestBlockHash()
print(current_block_hash)

height = 0
genesis_block_hash = client.getBlockHash(height)
print(genesis_block_hash)
```


## Layer 2

```python
from dapiclient.client import DAPIClient
import cbor2

client = DAPIClient()

id = client.getIdentity('C7id2mah2RkiroiTy6h134hLgS6A47jhh5x91tvw16bz')
print(id)

# Retrieve DPNS contract
contract = client.getDataContract('ARQGUnPH3YMK8FZuqwUjnTWEF6Zu4Cf3sT6e1Ruu1RXk')
print(contract)

# Retrieve 5 domain names from DPNS
docs = client.getDocuments(
    'ARQGUnPH3YMK8FZuqwUjnTWEF6Zu4Cf3sT6e1Ruu1RXk',
    'note',
    limit=1
)
print('{} documents retrieved'.format(len(docs)))
for doc in docs:
    print('Document:\n\t{}\n'.format(cbor2.loads(doc)))
```

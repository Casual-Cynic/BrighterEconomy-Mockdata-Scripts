# Example Transaction Data
# {
#   "id": "",
#   "type": "TRANSFER",
#   "participants": "PLAYERS",
#   "uuidFrom": "",
#   "uuidTo": "",
#   "money": 1234,
#   "itemPurchased": null,
#   "timestamp": 1735528500
# }

# {
#   "id": "",
#   "type": "PURCHASE",
#   "participants": "PLAYERS",
#   "uuidFrom": "",
#   "uuidTo": "",
#   "money": 1234,
#   "itemPurchased": {
#     "item": "minecraft:diamond",
#     "count": 1,
#     "nbt": null
#   },
#   "timestamp": 1735528500
# }

# {
#   "id": "",
#   "type": "MODIFY",
#   "participants": "FROM_NULL",
#   "uuidFrom": null,
#   "uuidTo": "",
#   "money": 1234,
#   "itemPurchased": null,
#   "timestamp": 1735528500
# }

import json
import uuid
from dataclasses import dataclass
import dataclasses
import time
import datetime
import random

from pydantic import BaseModel, RootModel, TypeAdapter
from typing import TypeAlias, Union


# takes the current UNIX timestamp and returns one up to 10 days in the future
# if it needs to be readable it returns it in the datetime format
def random_time(readable=False):

    rndTimestamp = int(time.time()) + random.randint(0, 799201)
    if readable == False:
        return rndTimestamp
    else:
        return str(datetime.datetime.fromtimestamp(rndTimestamp))



# Sets up my data models to serialize to
class ItemPurchased(BaseModel):
    item: str
    count: int
    nbt: Union[str, None]

class PurchaseEntry(BaseModel):
    id: str
    type: str
    participants: str
    uuidFrom: Union[str, None]
    uuidTo: Union[str, None]
    nameFrom: Union[str, None]
    nameTo: Union[str, None]
    money: int
    itemPurchased: Union[ItemPurchased, None]
    timestamp: int

class TransactionEntries(BaseModel):
    RootModel: list[PurchaseEntry]



# This is bringing in the UUIDs from the player data being used in the Webapp
placeholderUUIDS: list[str] = []
uuidNameDict: dict[str, str] = {}
with open("assets/MOCK_PLAYER_DATA.json", 'r') as f:
    pData = json.load(f)
    for entry in pData:
        placeholderUUIDS.append(entry["uuid"])

with open("assets/MOCK_PLAYER_DATA.json", 'r') as f:
    pData = json.load(f)
    for entry in pData:
        uuidNameDict[entry["uuid"]] = entry["username"]





# Populating the Models to auto populate with random data
def makeTransferEntry():
    toUUID = random.choice(placeholderUUIDS)
    fromUUID = random.choice(placeholderUUIDS)
    while toUUID == fromUUID:
        fromUUID = random.choice(placeholderUUIDS)

    transferEntry = PurchaseEntry(
        id=str(uuid.uuid4()),
        type="TRANSFER",
        participants="PLAYERS",
        uuidFrom=str(fromUUID),
        uuidTo=str(toUUID),
        nameFrom=str(uuidNameDict[fromUUID]),
        nameTo=str(uuidNameDict[toUUID]),
        money=random.randint(1, 501),
        itemPurchased=None,
        timestamp=int(random_time())
    )
    return transferEntry

def makePurchaseEntry():
    toUUID = random.choice(placeholderUUIDS)
    fromUUID = random.choice(placeholderUUIDS)
    while toUUID == fromUUID:
        fromUUID = random.choice(placeholderUUIDS)
    
    item1 = ItemPurchased(
        item="minecraft:diamond_sword",
        count="1",
        nbt='{components: {"minecraft:enchantments": {levels: {"minecraft:mending": 1, "minecraft:looting": 3, "minecraft:fire_aspect": 1}}}, count: 1, id: "minecraft:diamond_sword"}'
    )

    item2 = ItemPurchased(
        item="minecraft:dirt",
        count=random.randint(1, 65),
        nbt=None
    )

    item3 = ItemPurchased(
        item="minecraft:nautilus_shell",
        count=random.randint(1, 65),
        nbt=None
    )

    items: list[ItemPurchased] = [item1, item2, item3]

    purchaseEntry = PurchaseEntry(
        id=str(uuid.uuid4()),
        type="PURCHASE",
        participants="PLAYERS",
        uuidFrom=str(fromUUID),
        uuidTo=str(toUUID),
        nameFrom=str(uuidNameDict[fromUUID]),
        nameTo=str(uuidNameDict[toUUID]),
        money=random.randint(1, 501),
        itemPurchased=random.choice(items),
        timestamp=int(random_time())
    )
    return purchaseEntry

def makeModifyEntry():
    toUUID: str = str(random.choice(placeholderUUIDS))

    modifyEntry = PurchaseEntry(
        id=str(uuid.uuid4()),
        type="MODIFY",
        participants="FROM_NULL",
        uuidFrom=None,
        uuidTo=toUUID,
        nameFrom=None,
        nameTo=str(uuidNameDict[toUUID]),
        money=random.randint(1, 501),
        itemPurchased=None,
        timestamp=int(random_time())
    )
    return modifyEntry


entryCount = int(input("How many entries? "))

transactionData = []
i = 0
while i <= entryCount:
    type_choice = random.randint(0, 2)
    if type_choice == 0:
        transactionData.append(makeTransferEntry())
    elif type_choice == 1:
        transactionData.append(makePurchaseEntry())
    elif type_choice == 2:
        transactionData.append(makeModifyEntry())
    i += 1

jTransactionData = TransactionEntries(RootModel=transactionData)

json_Data = jTransactionData.model_dump_json()

with open("./MOCK_TRANSACTION_DATA.json", "w") as f:
    f.write(json_Data)
import json
import uuid
from dataclasses import dataclass
import dataclasses
import time
import datetime
import random

from pydantic import BaseModel, RootModel, TypeAdapter
from typing import TypeAlias, Union, List


# takes the current UNIX timestamp and returns one up to 10 days in the future
# if it needs to be readable it returns it in the datetime format
def random_time(readable=False):

    rndTimestamp = int(time.time()) + random.randint(0, 799201)
    if readable == False:
        return rndTimestamp
    else:
        return str(datetime.datetime.fromtimestamp(rndTimestamp))

# Sets up my data models to serialize to

class Enchantment(BaseModel):
    id: str
    level: Union[int, None]
    name: Union[str, None]

class ItemStack(BaseModel):
    item: str
    count: int
    name: Union[str, None]
    customName: Union[str, None]
    enchantments: List[Enchantment]
    lore: Union[str, None]

class PurchaseEntry(BaseModel):
    id: str
    type: str
    shopId: Union[str, None]
    participants: str
    uuidFrom: Union[str, None]
    uuidTo: Union[str, None]
    nameFrom: Union[str, None]
    nameTo: Union[str, None]
    money: int
    itemStack: Union[ItemStack, None]
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

# This is bringing in the UUIDs from the shop data being used in the Webapp
shopUUIDS: list [str] = []
uuidItemStackDict: dict[str, ItemStack] = {}
uuidOwnerDict: dict[str, str] = {}
with open("assets/MOCK_SHOP_DATA.json", "r") as f:
    sData = json.load(f)
    for entry in sData:
        shopUUIDS.append(entry["id"])

with open("assets/MOCK_SHOP_DATA.json", "r") as f:
    sData = json.load(f)
    for entry in sData:
        uuidItemStackDict[entry["id"]] = entry["itemStack"]

with open("assets/MOCK_SHOP_DATA.json", "r") as f:
    sData = json.load(f)
    for entry in sData:
        uuidOwnerDict[entry["id"]] = entry["ownerUuid"]



# Populating the Models to auto populate with random data
def makeTransferEntry():
    toUUID = random.choice(placeholderUUIDS)
    fromUUID = random.choice(placeholderUUIDS)
    while toUUID == fromUUID:
        fromUUID = random.choice(placeholderUUIDS)

    transferEntry = PurchaseEntry(
        id=str(uuid.uuid4()),
        type="TRANSFER",
        shopId=None,
        participants="PLAYERS",
        uuidFrom=str(fromUUID),
        uuidTo=str(toUUID),
        nameFrom=str(uuidNameDict[fromUUID]),
        nameTo=str(uuidNameDict[toUUID]),
        money=random.randint(1, 501),
        itemStack=None,
        timestamp=int(random_time())
    )
    return transferEntry

def makePurchaseEntry():
    shopUUID = random.choice(shopUUIDS)
    toUUID = uuidOwnerDict[shopUUID]
    fromUUID = random.choice(placeholderUUIDS)
    while toUUID == fromUUID:
        fromUUID = random.choice(placeholderUUIDS)

    purchaseEntry = PurchaseEntry(
        id=str(uuid.uuid4()),
        type="PURCHASE",
        shopId=str(shopUUID),
        participants="PLAYERS",
        uuidFrom=str(fromUUID),
        uuidTo=str(toUUID),
        nameFrom=str(uuidNameDict[fromUUID]),
        nameTo=str(uuidNameDict[toUUID]),
        money=random.randint(1, 501),
        itemStack=uuidItemStackDict[shopUUID],
        timestamp=int(random_time())
    )
    return purchaseEntry

def makeModifyEntry():
    toUUID: str = str(random.choice(placeholderUUIDS))

    modifyEntry = PurchaseEntry(
        id=str(uuid.uuid4()),
        type="MODIFY",
        shopId=None,
        participants="FROM_NULL",
        uuidFrom=None,
        uuidTo=toUUID,
        nameFrom=None,
        nameTo=str(uuidNameDict[toUUID]),
        money=random.randint(1, 501),
        itemStack=None,
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
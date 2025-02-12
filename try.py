mydict = {"BTC":{"position":3}}

# mydict.setdefault("ETH", 0)
mydict["ETH"] = mydict.get("ETH", 0) + 5
print(mydict)
from simpleth import Blockchain, Contract, EventSearch

sender = Blockchain().address(0)
c = Contract('HelloWorld4')
c.deploy(sender, 'Hello World!')
e = EventSearch(c, 'HelloWorld4Constructed')
event = e.get_old()
print(event[0]['args']['initGreeting'])

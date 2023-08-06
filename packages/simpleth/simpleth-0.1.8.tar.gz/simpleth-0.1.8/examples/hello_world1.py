from simpleth import Blockchain, Contract

sender = Blockchain().address(0)
c = Contract('HelloWorld1')
c.deploy(sender)
greeting = c.get_var('greeting')
print(greeting)

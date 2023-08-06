from simpleth import Blockchain, Contract

sender = Blockchain().address(0)
c = Contract('HelloWorld2')
c.deploy(sender)
greeting = c.call_fcn('getGreeting')
print(greeting)

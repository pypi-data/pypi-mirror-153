from simpleth import Blockchain, Contract

sender = Blockchain().address(0)
c = Contract('HelloWorld3')
c.deploy(sender)
c.run_trx(sender, 'setGreeting', 'Hello World!')
greeting = c.call_fcn('getGreeting')
print(greeting)

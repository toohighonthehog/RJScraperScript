class Address:
  def __init__(self, street, number):
    self.street = street
    self.number = number

  def printit(abc):
    print("My Address is " + abc.street)

p1 = Address("Albert Street", 20)
p1.printit()
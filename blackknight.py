import numbers
class BlackKnight:

  def __init__(self, *args):
    self.members = list(args)
    self.comment = ['piece of cake', 'fine', 'comming', 'call it a draw']

  @property
  def members(self):
    return self.__members

  @members.setter
  def members(self, args):
    self.__members = [i for i in args if isinstance(i, numbers.Integral)]

bk = BlackKnight(1,2,3,4)
print(bk.members)

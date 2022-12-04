from nnf import Var, And, Or
from nnf import true, false
from nnf import dsharp
from config import *

vars = [Var('A'), Var('B'), Var('C')]
con = Or([And([vars[0], vars[1].negate()]), And([vars[1], vars[0].negate()]), And([vars[2]])])
con2 = Or([And([vars[0], vars[1].negate()]), And([vars[1], vars[0].negate()]), And([vars[2]])]).negate()
# cona = frozenset(And([vars[0], vars[1]]).children)
# conb = And([vars[1].negate()])
# var, = conb
# acc = {var}
# print(acc)
# conC = con.to_CNF()
# con2C = con2.to_CNF()
# print(not not cona & acc)
con = con.to_CNF()
print(con)
# models = con.to_CNF().forget_aux().models()
# for m in models:
#     print(m)
import torch
import numpy

torch.zeros([3, 4])
torch.ones([3,4,3])
x = torch.Tensor([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10 ,11, 12]])

#rint(x.size())
#print(x.shape)

#print(x[:, 1])

mask = x > 3
#print(x[mask])

y = x #по ссылке! изменения в одном повлекут изменения в другом

y = x.clone() #по значению

#print(x.dtype)

#преобразования
x = x.double()

#numpy и torch не эквивалентны, но можно приводить один к другому
#torch.from_numpy(x)
#x = x.numpy

x = torch.rand([2,3])
print(torch.cuda.is_available())

#часть с cuda выполнена с гугловским блокнотом
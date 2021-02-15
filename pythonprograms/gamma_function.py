# Taken from: https://www.rosettacode.org/wiki/Gamma_function#Python

_a = ( 1.00000000000000000000, 0.57721566490153286061, -0.65587807152025388108,
      -0.04200263503409523553, 0.16653861138229148950, -0.04219773455554433675,
      -0.00962197152787697356, 0.00721894324666309954, -0.00116516759185906511,
      -0.00021524167411495097, 0.00012805028238811619, -0.00002013485478078824,
      -0.00000125049348214267, 0.00000113302723198170, -0.00000020563384169776,
       0.00000000611609510448, 0.00000000500200764447, -0.00000000118127457049,
       0.00000000010434267117, 0.00000000000778226344, -0.00000000000369680562,
       0.00000000000051003703, -0.00000000000002058326, -0.00000000000000534812,
       0.00000000000000122678, -0.00000000000000011813, 0.00000000000000000119,
       0.00000000000000000141, -0.00000000000000000023, 0.00000000000000000002
      )
def gamma (x): 
    y  = float(x) - 1.0;
    sm = _a[-1];
    for an in _a[-2::-1]:
       sm = sm * y + an;
    return 1.0 / sm;
 
def print(*args, **kwargs):
   pass

n = 1000000
if __name__ == '__main__':
    for i in range(1,n):
       print("  %20.14e" % gamma(i/3.0))


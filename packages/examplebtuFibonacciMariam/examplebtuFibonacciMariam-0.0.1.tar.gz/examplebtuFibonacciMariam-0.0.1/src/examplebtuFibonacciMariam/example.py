def recur_fibo(n):
  if n not in [0, 1]:
    return recur_fibo(n - 1) + recur_fibo(n - 2)
  return n


def enter_data():
  nterms = int(input("Enter terms: "))
  for i in range(nterms):
    print(recur_fibo(i))


if _name_ == "_main_":
  enter_data()

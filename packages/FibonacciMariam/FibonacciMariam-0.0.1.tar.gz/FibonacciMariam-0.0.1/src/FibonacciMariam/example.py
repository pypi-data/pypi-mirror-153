def recur_fibo(n):
  if n not in [0, 1]:
    return recur_fibo(n - 1) + recur_fibo(n - 2)
  return n

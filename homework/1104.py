# お釣りの計算

insert_price = input("insert: ")
product_price = input("product: ")
change = int(insert_price) - int(product_price)

cash_list = [5000, 1000, 500, 100, 50, 10, 5, 1]

for i in cash_list:
    r = change // i
    change %= i
    print(str(i) + ": " + str(r))

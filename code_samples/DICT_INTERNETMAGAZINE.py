mydict = {}
for _ in range(int(input())):
    name, product, count = input().split()
    mydict.setdefault(name, {})
    mydict[name][product] = mydict[name].get(product, 0) + int(count)

for key, products in sorted(mydict.items()):
    print(f'{key}:')
    for product, count in sorted(products.items()):
        print(f'{product} {count}')

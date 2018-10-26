#2.1
l = [1,2,3,4]
for i in l:
    for j in l:
        for k in l:
            if (i!=j) and (i!=k) and (j!=k):
                print(i,j,k)

#2.2
a=[1,2,3,4,5]
print(a[0:5:2])
print(a[-2:])

#2.3
def filter_range(n):
    return n%2==0

print(list(filter(filter_range,[1,2,7,12,45,56,66])))
num=int(input("sheiyvane ricxvi:"))
n1,n2=0,1
ads = 0
if num<=0:
    print("miutite nulze magali:")
else:
    for i in range(0, num):
        print(ads,end=" ")
        n1=n2
        n2=ads
        ads=n1+n2
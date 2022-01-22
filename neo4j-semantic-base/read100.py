import sys

count = 0
#with open("Text_Tagged_Reddit_Data2.csv", "r") as file:
print(sys.argv[1])
with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        try:
            count = count + 1
            print(line);
        except:
            print("SKIP")
            print(line.encode("utf-8"));
            continue
            
        
        if count > 8:
            break

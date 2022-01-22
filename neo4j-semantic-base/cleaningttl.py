import sys

count = 0
skip = 0
previous_line = "start"
#with open("Text_Tagged_Reddit_Data2.csv", "r") as file:
print(sys.argv[1])
with open(sys.argv[1], "r") as file:
    with open(sys.argv[2], "w", encoding="ascii") as savefile:
        while True:
            try:
                count += 1
                content = file.readline().replace("\\", "_")
                if not content:
                    break
    
                if previous_line == "start":
                    savefile.write(content)
                    continue
                    
                if "#@" == content[:2]:
                    previous_line = content
                elif previous_line != "":
                    savefile.write(previous_line)
                    savefile.write(content)
                    previous_line = ""
                #print(line.decode("utf-8"));
            except Exception as e:
                skip = skip + 1
                previous_line = ""
                continue
print("Skips: " + str(skip))
               
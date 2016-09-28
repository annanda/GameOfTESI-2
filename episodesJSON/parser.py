import re

with open("test_a_golden_crown.txt", "r") as f:
    data = f.read()
    
data = re.sub("\n+", "\n", data)

with open("a.txt", "w") as f:
    f.write(data)
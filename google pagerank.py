import random


with open("web-Google.txt") as sample_data:
    probs = {}
    for line in sample_data:
        if line.startswith("#"): continue
        else: line = line.strip()

        nodefrom, nodeto = line.split("	")
        if nodefrom in probs:
            if nodeto not in probs[nodefrom]: probs[nodefrom].append(nodeto)
        else:
            probs[nodefrom] = [nodeto,]


time_dict = dict.fromkeys(probs, 0)

state = random.choice(list(time_dict.keys()))

for i in range(1, 500000):
    choice = random.randint(0, 100)
    if choice <= 85:
        try:
            state = random.choice(probs[state])
        except: state = random.choice(list(probs.keys()))
    else:
        state = random.choice(list(probs.keys()))
    if state not in time_dict:
        time_dict[state] = 0
    time_dict[state] += 1

#for x in range(1, len(time_dict)+1): total += time_dict[x]
new = max(time_dict, key=time_dict.get)
print(new)
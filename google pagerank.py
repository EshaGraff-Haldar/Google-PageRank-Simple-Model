import random

nodes = set()
with open("web-Google.txt") as sample_data:
    probs = {}
    for line in sample_data:
        if line.startswith("#"): continue

        nodefrom, nodeto = line.strip().split("	")
        nodes.add(nodefrom)
        nodes.add(nodeto)

        probs.setdefault(nodefrom, []).append(nodeto)


nodes = list(nodes)
time_dict = dict.fromkeys(nodes, 0)

state = random.choice(list(time_dict.keys()))

for i in range(1, 10000000):
    if random.random() <= 0.85 and state in probs:
        state = random.choice(probs[state])
    else:
        state = random.choice(nodes)
    
    time_dict[state] += 1

new = max(time_dict, key=time_dict.get)
print(new)

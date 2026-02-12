import random
import numpy as np

probs = {
        1: [1, 2, 3],
        2: [1],
        3: [2, 3]
    }


# power method
time_dict = {
    1: 0,
    2: 0,
    3: 0
}
state = 3
for i in range(1, 25000):
    choice = random.randint(0, 100)
    if choice > 85: state = random.choice(list(probs.keys()))
    else: state = random.choice(probs[state])
    time_dict[state] = time_dict[state] + 1

total = 0
for x in range(1, len(time_dict)+1): total += time_dict[x]
for key in time_dict:
    time_dict[key] = time_dict[key] / total
print(time_dict)





# eigendecompostion method

# probs into transition matrix
states = sorted(probs.keys())
size = len(states)

arr = np.zeros((size, size))
for i in range(len(states)):
    key = states[i]
    length = len(probs[states[i]])

    for new_state in probs[key]:
        j = states.index(new_state)
        arr[i, j] += 1/length


# alternate faster way to transform dict into transition matrix
'''
states = sorted(probs.keys())
n = len(states)
P = np.zeros((n, n))
for i, s in enumerate(states):
    next_states = probs[s]
    p = 1 / len(next_states)
    for ns in next_states:
        j = states.index(ns)
        P[i, j] = p
'''

#Formatting into google transition matrix
rows, cols = arr.shape
google_matrix = np.multiply(arr, 0.85) + np.multiply(np.ones((rows, cols)), (0.15/rows))

#finding eigendecomposition - to calculate stationary distribution
# usually pi*P = pi
# transpose to get left eigenvectors instead of right: (P.T)*(pi.T) = (pi.T)
# (pi.T) is now a column vector
G_T = google_matrix.T
eigenvalues, eigenvectors = np.linalg.eig(G_T)

#finding the index of the eigenvalue = 1, to get corresponding eigenvector = stationary distribution
idx = np.argmin((np.abs(eigenvalues-1.0)).real)
stationary_dist = (eigenvectors[:, idx]).real

#normalising stationary distribution
stationary_dist = stationary_dist / stationary_dist.sum()
print(stationary_dist)
print(states[np.argmax(stationary_dist)])
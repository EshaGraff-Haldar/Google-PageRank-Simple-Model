import numpy as np
from numpy.linalg import eig
from scipy import sparse

#creating transition dictionary
nodes = set()
num_of_lines = 0
with open("/Users/eshagraffhaldar/Library/Mobile Documents/com~apple~CloudDocs/KC/Google PageRank/web-Google.txt") as sample_data:
    probs = {}
    for line in sample_data:
        if line.startswith("#"): continue

        nodefrom, nodeto = line.strip().split()
        nodes.add(nodefrom)
        nodes.add(nodeto)

        probs.setdefault(nodefrom, []).append(nodeto)
        num_of_lines +=1

#Creating dictionary of node names to corresponding indices.
nodes = sorted(tuple(nodes))
nodes_indices = {}
for i, nodeid in enumerate(nodes): nodes_indices[nodeid] = i

size = len(nodes)
rows = []
cols = []
data = []
# creating array of nodes with no outbound links
dangling = np.array([n not in probs for n in nodes])
dangling_indices = np.where(dangling)[0]

#inputting data for sparse matrix
for current_node, neighbours in probs.items():
    r_index = nodes_indices[current_node]
    total = len(neighbours)
    for next_node in neighbours:
        #adding to sparse_matrix data arrays
        # We construct the matrix tranposed over here...
        # otherwise we'd need to do t.dot(arr) (tG) which is far slower than arr.dot(t) (Gt)
        #Therefore we do G^T, so that t.dot(arr) = (G^T)t = tG
        c_index = nodes_indices[next_node]
        rows.append(c_index) #here c and r are swapped
        cols.append(r_index)
        data.append(1/total)

#Creating the sparse matrix
arr = sparse.csr_matrix((data, (rows, cols)), shape=(size, size))


#Iteratively Multiplying the Google Transition Matrix
t = np.ones(size) / size
jump = 0.15 / size
for i in range(100):
    new_t = 0.85 * (arr.dot(t))

    '''Any 'missing' mass is due to dangling nodes (no outbound ) + the 0.15 teleport
    This single line below handles both
    t = (1.0 - np.sum(t)) / size'''

    #But the line below is much faster, as you don't need to calculate the sum of the whole vector
    #finding mass lost due to the dangling nodes
    dangling_mass = new_t[dangling_indices].sum()
    #redistributing dangling mass, adding jump (0.15 chance)
    new_t = new_t + dangling_mass/size + jump

    #Convergence detection
    #Finds the sum of differences between new_t and t: this is called the L1 norm/distance (also called Manhattan distance)
    if np.linalg.norm(new_t -t, 1) <= 1e-7:
        print("Broken")
        break

    t = new_t


#top node
index_of_most_visited = np.argmax(t)
top_state = nodes[index_of_most_visited]
print(top_state)


# Get top 5 nodes
top_matrix_indices = np.argsort(t)[-5:][::-1]
for i in top_matrix_indices: print(f"{nodes[i]} : {t[i]}")


''' Using eigendecomposition Method: NOT VIABLE

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
print(np.argmax(stationary_dist))
'''
## Graph embedding and clustering experiment<br />

### --- Objective ---<br />
Find the relations between node2vec’s parameters(p, q) and the embedded results in “structural role” style and “connectivity” style.

### --- node2vec model ---<br />
[node2vec: Scalable Feature Learning for Networks](https://cs.stanford.edu/people/jure/pubs/node2vec-kdd16.pdf)
![Alt text]( png/search_strategies.png?raw=true "")<br />
![Alt text]( png/bias.png?raw=true "")<br />

### Tools and Experimental steps:<br />
need node2vec, networkx, gensim.<br />

step1. Use Node2vec algorithm for embedding each vertex in a graph to a vector;<br />
step2. Use k-means algorithm to divide the vertices(vectors) into clusters;<br />
step3. Visualize the results.<br />

### --- Data description ---<br />
Text file. Each line is a edge(node1, node2) in a undirected graph.<br />
vertex#: 24;<br />
edge#: 72<br />

Visualization of graph data (Yellow ones are local hubs; Pink ones are global hubs): <br />
![Alt text]( png/graph.png?raw=true "")<br />
Nodes 3~8 are connected by node 21;<br />
Nodes 9~14 are connected by node 22;<br />
Nodes 15~20 are connected by node 23;<br />
Within any one of those three group, nodes are not connected with each other.<br />
Node 21, 22 and 23 are “local hubs” within each group respectively.<br />
Nodes 0, 1, 2 are “global hubs” that connect to all three groups except Node 21, 22 and 23.<br /><br />


### --- Embedding with connectivity ---<br />
Node2vec parameters:<br />
    embedding dimension     128<br />
    walk# per-node          300<br />
    walk length             10<br />
    window size             3<br />
    return parameter p      1<br />
    in-out parameter q      1<br /><br />
![Alt text]( png/connectivity.png?raw=true "")<br />
Explain: The three groups are clearly separated except the three global hubs.<br /><br />


### --- Embedding with structural role ---<br />
Node2vec parameters:<br />
    embedding dimension     128<br />
    walk# per-node          300<br />
    walk length             5<br />
    window size             1<br />
    return parameter p      1<br />
    in-out parameter q      1<br /><br />
![Alt text]( png/structural_role.png?raw=true "")<br />
Obsevations:<br />
The key parameters are walk length and window size (context length).<br />

BFS/DFS preference parameters p and q are not the key factors in this case. I always set p to 1. The q can be set from 0.5 to 2 and do not affect the result significantly. The result becomes unstable and meaningless when q is too high or too low.<br />

When I design the graph, I found out that within each one of the three groups, all nodes cannot connect each other but can only connect to the local hub (node 21, 22 and 23). Otherwise the result becomes  unstable, no matter how I adjust all parameters.<br /><br />


### --- Tricky behavior ---<br />
I connected some nodes with each one of three groups in original graph...<br />
modified graph(24 vertices and 9modified_structural_role0 edges):<br />
![Alt text]( png/modified_graph.png?raw=true "")<br />
Visualization of graph data (Yellow ones are local hubs; Pink ones are global hubs)<br />
The different between this graph and the original one is that I added more edge: 3-4, 4-5, 5-6, 6-7, 7-8, 8-3 within the first group, and I added more edges within other two group similarly.<br /><br />

#### Embedding with sconnectivity (same parameters as before):<br />
![Alt text]( png/modified_connectivity.png?raw=true "")<br />
Most nodes are embedded meaningless.<br />

#### Embedding with structural role (same parameters as before):<br />
![Alt text]( png/modified_structural_role.png?raw=true "")<br />
The only evidence is that the three global hubs are embedded closely. Other nodes are embedded meaningless.<br />


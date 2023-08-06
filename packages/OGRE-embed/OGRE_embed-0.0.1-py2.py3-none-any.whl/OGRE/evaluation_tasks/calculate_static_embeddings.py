"""
Main file to calculate the embeddings with OGRE/DOGRE/WOGRE, and performing link prediction and node classification task.

In order to calculate the embedding, you first must have an edge list file:
"datasets/name_of_dataset.txt" - An edge list txt file. If the graph is unweighted it consists of 2 columns: source, target (with no title, source and target share an edge).
If the graph is weighted, it consists of 3 columns: source target weight. 
Example for unweighted graph:
1 2
2 3
1 4
1 3
Example for weighted graph:
1 2 3
1 3 0.3
1 4 4.5
2 4 0.98
You can see examples for this format in "datasets" directory.

If you want to peform vertex classification task or GCN is your initial embedding, you must have labels file:
"labels/{name_of_dataset}_tags.txt" - A txt file which consists of 2 columns: node, label (no title). Notice all node must have labels!
Example:
1 0
2 0
3 1
4 2

Another possibilty is having a .mat file as in NRL_Benchmark (https://pages.github.com/). In this link, go to either `node classification`
or `link prediction` directories, where a link to datasets you can use in .mat format is avaliable. Then this .mat file is both the
edges and labels file.

If you want to perform link prediction task, you must have non edges file:
"evaluation_tasks/non_edges_{name_of_dataset}" - A csv file which consists of two columns: node1, node2 ; where there is no edge between them (again no title).
In order to produce such file, you can go to evaluation_tasks -> calculate_non_edges.py , and follow the instructions there.

When you have all the files you need (depending on what you want to perform), you can run this file.
1. First initialize DATASET parameters dict:
- name: Name of dataset (as the name of the edge list txt file) (string)
- initial_size: List of initial core sizes. (list)
- dim: Embedding dimension (int)
- is_weighted: True if the graph is weighted, else False (bool)
- choose: "degrees" if the vertices of the initial core are the ones with highest degree (as done in our experiments), else "k_core" if the vertices of the initial core are
the ones with highest k-core score. (string)
- "s_a": True if you also want to calculate state-of-the-art embeddings (node2vec/GF/HOPE/GCN), else False.
Params for OGRE:
- epsilon: Weight to the second order neighbours embedding. For more details you can go to the implementation- our_embedding_methods -> OGRE.py (float).
Params for DOGRE/WOGRE:
- "regu_val": Regularization value for regression, only for DOGRE/WOGRE. For more details you can go to the implementation- our_embedding_methods -> D_W_OGRE.py (float).
- "weighted_reg": True for weighted regression, else False.
If the initial embedding method is GCN and/or a vertex classification task is applied, a labels file is also necessary:
- "label_file": path and name (together), so it can be read directly.
2. methods_ : List of our suggested embedding methods (OGRE/DOGRE/WOGRE) with whom you want to embed the given graph. 
3. initial_methods_ : List of state-of-the-art embedding methods (node2vec/GF/HOPE/GCN) with whom the initial core will be embed.
4. params_dict_ : Parameters for state-of-the-art embeddings. These are the optimal ones (according to their papers). For more details you can go to- 
state_of_the_art -> state_of_the_art_embedding.py
5. save_: True if you want to save the embedding in a .npy format, else False.

Once you have that, you can run "calculate_static_embeddings" function to get the embeddings as dictionaries. You can see function implementation and output format in 
evaluation_tasks -> eval_utils.py . 

If you only want the embedding of the graph, you can stop here. If you also want to apply link prediction or vertex classification task you should continue.
Line 107: export_time - Export a csv file with running times of each method according to the initial core size.
Lines 123-130- Link prediction task: A csv file of non edges is needed (as explained above), you can see comments in the code. For more details you can go to
evaluation_tasks -> link_prediction.py .
Lines 132-136- Vertex classification task: You can see comments in the code. For more details you can go to evaluation_tasks -> node_classification.py .
"""

from .link_prediction import *
from .node_classification import *
import itertools as IT
from ..our_embeddings_methods.static_embeddings import *
import csv


class CalculateStaticEmbeddings:
    def __init__(self, name, datasets_path, label_file=None, initial_size=None, dim=128,
                 is_weighted=False, choose="degrees", regu_val=0,
                 weighted_reg=False, s_a=True, epsilon=0.1):

        self.initial_size = None
        self.save = None
        self.z = None
        self.G = None
        if initial_size is None:
            initial_size = [100, 1000]

        self.DATASET = {"name": name, "initial_size": initial_size, "dim": dim,
                        "is_weighted": is_weighted, "choose": choose, "s_a": s_a,
                        "regu_val": regu_val, "weighted_reg": weighted_reg,
                        "epsilon": epsilon, "label_file": label_file}

        self.datasets_path = datasets_path

    def calculate_static_embeddings(self):
        if self.DATASET["choose"] == "degrees":
            embeddings_path_ = os.path.join("embeddings_degrees")
        else:
            embeddings_path_ = os.path.join("embeddings_k_core")
        if not os.path.exists("embeddings_state_of_the_art"):
            os.makedirs("embeddings_state_of_the_art")

        if self.DATASET["s_a"]:
            if not os.path.exists(embeddings_path_):
                os.makedirs(embeddings_path_)

        # Our suggested embedding method
        methods_ = ["OGRE"]
        # state-of-the-art embedding methods
        initial_methods_ = ["node2vec"]

        # Parameters duct for state-of-the-art embedding methods
        params_dict_ = {
            "node2vec": {"dimension": self.DATASET["dim"], "walk_length": 80, "num_walks": 16, "workers": 2},
            "GF": {"dimension": self.DATASET["dim"], "eta": 0.1, "regularization": 0.1, "max_iter": 3000,
                   "print_step": 100}, "HOPE": {"dimension": 128, "beta": 0.1},
            "GCN": {"dimension": self.DATASET["dim"], "epochs": 150, "lr": 0.01, "weight_decay": 5e-4,
                    "hidden": 200,
                    "dropout": 0}}

        # if you want to save the embeddings as npy file- save_=True
        save_ = True

        # calculate dict of embeddings
        self.z, self.G, self.initial_size, list_initial_proj_nodes = \
            calculate_static_embeddings(self.datasets_path, embeddings_path_, self.DATASET,
                                        methods_, initial_methods_, params_dict_, save_=save_)

    def __set_save(self):
        if self.DATASET["choose"] == "degrees":
            self.save = "files_degrees"
        else:
            self.save = "files_k_core"
        if not os.path.exists(self.save):
            os.makedirs(self.save)

    def run_time(self):
        if self.save is None:
            self.__set_save()
        # evaluate running time
        export_time(self.z, self.DATASET["name"], self.save)

    def __pre_link_node(self):
        if self.DATASET["name"] == "Yelp":
            mapping = {i: n for i, n in zip(range(self.G.number_of_nodes()), list(self.G.nodes()))}
        else:
            mapping = None

        self.DATASET["initial_size"] = self.initial_size
        print(self.initial_size)
        n = self.G.number_of_nodes()
        return mapping, n

    def link_prediction(self, number_true_false=10000, rounds=10, test_ratio=None, number_choose=10):
        # TODO: figure out what is number_true_false and why the program fails on karate dataset
        if test_ratio is None:
            test_ratio = [0.2, 0.3, 0.5]
        if self.save is None:
            self.__set_save()

        mapping, n = self.__pre_link_node()

        # evaluate link prediction
        print("start link prediction task")
        non_edges_file = "non_edges_{}.csv".format(self.DATASET["name"])  # non edges file
        if not os.path.exists(non_edges_file):
            create_non_edges_file(self.G, self.DATASET["name"])

        # number_true_false: Number of true and false edges
        # number_choose: How many times to choose true and false edges
        params_lp_dict = {"number_true_false": number_true_false, "rounds": rounds,
                          "test_ratio": test_ratio, "number_choose": number_choose}
        dict_lp = final_link_prediction(self.z, params_lp_dict, non_edges_file)
        export_results_lp_nc_all(n, self.save, self.z, dict_lp, self.DATASET["initial_size"], self.DATASET["name"],
                                 "Link Prediction")
        print("finish link prediction")

    def node_classification(self, multi_label=False, label_files=None, rounds=10, test_ratio=None):
        # TODO: figure out what is label_files and what should this file contain
        if test_ratio is None:
            test_ratio = [0.5, 0.9]
        if self.DATASET["label_file"] is None:
            if label_files is None:
                raise ValueError("label_file is None")
            else:
                self.DATASET["label_file"] = label_files
        if self.save is None:
            self.__set_save()

        mapping, n = self.__pre_link_node()

        # Node Classification Task
        print("start node classification task")
        params_nc_dict = {"rounds": rounds, "test_ratio": test_ratio}
        # for multi-label node classification add multi=True
        dict_nc = final_node_classification(self.DATASET["name"], self.z, params_nc_dict, self.DATASET, mapping=mapping,
                                            multi=multi_label)
        export_results_lp_nc_all(n, self.save, self.z, dict_nc, self.DATASET["initial_size"], self.DATASET["name"],
                                 "Node Classification")
        print("finish node classification")


def create_non_edges_file(graph, name, path=""):
    print("First creating non edges file")
    print("Starting find non edges")

    e = graph.number_of_edges()
    n = graph.number_of_nodes()
    l = []
    print(n, e)
    nodes = list(graph.nodes())
    # could be very big so change 0.5 to smaller values if needed.
    indexes = random.sample(range(0, len(nodes)), int(len(nodes) * 0.5))
    new_nodes = []
    for j in indexes:
        new_nodes.append(nodes[j])
    missing = [pair for pair in IT.combinations(new_nodes, 2) if not graph.has_edge(*pair)]
    print(len(missing))
    for pair in missing:
        l.append((pair[0], pair[1]))

    print("Almost done, writing the csv file!")
    non_edges_path = os.path.join(path, f"non_edges_{name}.csv")
    csvfile = open(non_edges_path, 'w', newline='')
    obj = csv.writer(csvfile)
    obj.writerows(l)
    csvfile.close()
    print("Non edges file is ready!")

    return non_edges_path

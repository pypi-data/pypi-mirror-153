# FODGE - Fast Online Dynamic Graph Embedding

### Contact
********@gmail.com

## Overview

FODGE is a novel dynamic graph embedding algorithm (DGEA) to gradually shift the projection of modified vertices. FODGE optimizes CPU And memory efficacy by separating the projection of the graph densest K-core and its periphery. FODGE then smoothly updates the projection of the remaining vertices, through an iterative local update rule. As such it can be applied to extremely large dynamic graphs. Moreover, it is highly modular and can be combined with any static projection, including graph convolutional networks, and has a few hyperparameters to tune. FODGE is a stable embedding method, obtaining a better performance in an auxiliary task of link prediction and ensures a limited difference in vertex positions in following time points.

The following movie presents a typical evolution of FODGE through 19 time points on the Facebook Wall Posts dataset. We follow the colored vertices during time to see the difference in their positions. One can see that vertices that are not changing drastically through time (change neighbors, connected components), are hardly changing their positions. This demonstrates the stability of FODGE.

![caption](https://github.com/unknownuser13570/FODGE/blob/main/FODGE%20GIF.gif)

## About This Repo

This repo contains source code of the FODGE dynamic graph embedding algorithm. 

### The Directories

- `datasets` - Examples of datasets files
- `embeddings` - Path to where to save the computed embeddings
- `fodge` - The main files to run the FODGE framework
- `GEA` - State-of-the-art static graph embedding algorithms implementations, currently [node2vec](https://arxiv.org/abs/1607.00653)/[GF](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/40839.pdf)/[HOPE](https://www.kdd.org/kdd2016/papers/files/rfp0184-ouA.pdf)/[GCN](https://arxiv.org/abs/1609.02907)/[GAE](https://arxiv.org/abs/1611.07308).
- `evaluation_tasks` - Implementation of temporal link prediction tasks

#### Notes:
- The implementations of GF and HOPE were taken from [GEM toolkit](https://github.com/palash1992/GEM)
- Node2vec is implemented using [node2vec public package](https://github.com/eliorc/node2vec)
- The implementation of GCN was taken from their [public github repository](https://github.com/tkipf/pygcn)
- The implementation of GAE was taken from their [public github repository](https://github.com/tkipf/gae)

## Dependencies
- python >=3.6.8
- numpy >= 1.18.0
- scikit-learn >= 0.22.1
- heapq
- node2vec==0.3.2
- networkx==1.11
- scipy >= 1.41
- pytorch==1.7.0
- matplotlib==3.1.3
- pandas >= 1.0.5
- tensorflow == 2.4.1
- keras == 2.4.3

## Datasets
- Facebook
- Facebook Friendships
- Facebook Wall Posts
- DBLP
- Math
- Enron
- Wiki-talk

**Note:** All the datasets used can be found in this [google drive link](https://drive.google.com/drive/folders/15tlgyf3GO8s8HjCsd5S5zQ7_n28DafA7?usp=sharing) in the required format. 

If you use one of these datasets, all you have to do is choose the dataset (see name of directories) and put the appropriate `.txt` file in `datasets`directory. 

If you want to use your own dataset, you should follow this format: <br/>
Give a single `.txt` file where each row contains 3/4 columns in the form: <br/>
- **For un-weighted graphs:** from_id to_id time (e.g. 1 2 0 means there is an edge between vertices 1 and 2 at time 0).
- **For weighted graphs:** from_id to_id weight time (e.g. 1 2 0.5 0 means there is an edge of weight 0.5 between vertices 1 and 2 at time 0).

If the provided dataset is in this format, you can put it as it is in the `datasets` directory and use the `data_loader` function that is in `fodge/load_data`. <br/>
If it is not, you should build a data loader function that will convert it to this form. 

## How To Run?

To embed your temporal network with FODGE, you have to provide a `.txt` file representing the network and place it in the `datasets` directory (as explained above).

If you want to perform the fisrt temporal link prediction task as explained in the paper, you should also have a non_edges_file: "evaluation_tasks/non_edges_{name_of_dataset}" - A csv file which consists of three columns: time, node1, node2 ; where there is no edge between them (csv file has no title).
In order to produce such file, you can go to `evaluation_tasks/calculate_non_edges.py`, and follow the instructions there. In addition, you can see the example file here. Make sure to put in the `evaluation_tasks` directory!
Note you do not have to specifically provide it - if it is not provided by the user, it will be created during the run (can take a while).

The main file to run FODGE is `main.py`.

Running the following command in the terminal wll display a help message with all the optional parameters, each with an explanation and default values.

```
python main.py -h
```

```
usage: main.py [-h] [--name NAME] [--datasets_path DATASETS_PATH]
               [--save_path SAVE_PATH] [--initial_method INITIAL_METHOD]
               [--dim DIM] [--epsilon EPSILON] [--alpha ALPHA] [--beta BETA]
               [--number NUMBER] [--file_tags FILE_TAGS]
               [--link_prediction_1 LINK_PREDICTION_1]
               [--link_prediction_2 LINK_PREDICTION_2]
               [--test_ratio TEST_RATIO] [--val_ratio VAL_RATIO]
               [--non_edges_file NON_EDGES_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           Name of the dataset (str) (default:
                        facebook_friendships)
  --datasets_path DATASETS_PATH
                        Path to where the dataset file is (str) (default:
                        datasets)
  --save_path SAVE_PATH
                        Path to where to save the calculated embedding (str)
                        (default: embeddings)
  --initial_method INITIAL_METHOD
                        Initial GEA to embed the first snapshot with. Options
                        are node2vec, HOPE, GAE, GF. If thegraph has tags, GCN
                        option can also be used (str) (default: node2vec)
  --dim DIM             Embedding dimension (int) (default: 128)
  --epsilon EPSILON     Relative weight given to first and second neighbors in
                        the local update rule (float) (default: 0.01)
  --alpha ALPHA         The weight given to the recent embedding when
                        calculating the current one (float) (default: 0.2)
  --beta BETA           The rate of the exponential decay of the weights
                        (float) (default: 0.3)
  --number NUMBER       How many vertices in the cumulative initial snapshot
                        (choose a number where a 5-core exists)(int) (default:
                        1000)
  --file_tags FILE_TAGS
                        If GCN GEA is used, then one should provide the path
                        of the file of tags (str) (default: None)
  --link_prediction_1 LINK_PREDICTION_1
                        True if you want to perform temporal link prediction
                        task (type 1 with neural network), else False
                        (default: False)
  --link_prediction_2 LINK_PREDICTION_2
                        True if you want to perform temporal link prediction
                        task (type 2 with linear regression),else False
                        (default: False)
  --test_ratio TEST_RATIO
                        Test ratio for temporal link prediction tasks
                        (relevant to both) both) (default: 0.2)
  --val_ratio VAL_RATIO
                        Val ratio for temporal link prediction task (relevant
                        only to type 2- with linear regression) (default: 0.3)
  --non_edges_file NON_EDGES_FILE
                        Name of non edges csv file as explained in the readme.
                        If you do not have any, insert None (str) and it will
                        be created during the running (can take a while).
                        relevant only to type 1- with neural network (default:
                        non_edges_facebook_friendships.csv)
```

You have three options:
1. Perform an embedding of the temporal network 
```
python main.py --name facebook_friendships --datasets_path datasets --save_path embeddings --initial_method node2vec --dim 128 --epsilon 0.04 --alpha 0.2 --beta 0.7 --
number 1000
```
2. Embedding + First temporal link prediction (with neural network, as exaplained in the paper)
```
python main.py --name facebook_friendships --datasets_path datasets --save_path embeddings --initial_method node2vec --dim 128 --epsilon 0.04 --alpha 0.2 --beta 0.7 --
number 1000 --link_prediction_1 True --test_ratio 0.2 --non_edges_file None
```
Note: If you have a specific non edges file in the format explained above, provide its name

3. Embedding + Second temporal link prediction (with linear regression, as exaplained in the paper)
```
python main.py --name facebook_friendships --datasets_path datasets --save_path embeddings --initial_method node2vec --dim 128 --epsilon 0.04 --alpha 0.2 --beta 0.7 --
number 1000 --link_prediction_2 True --test_ratio 0.2 --val_ratio 0.3
```

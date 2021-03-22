import random
import time


from hash_tree import HashTree
from list_tree import BinaryListTree, LTNode


# Artificially builds a complete binary tree with the given depth
def build_hash_tree(limits, max_depth, padding, rng):
    def recurse(tree, parent, limits, depth=0):
        if depth == max_depth:
            return

        # Randomly pick a feature
        # We weight each feature by the gap between each feature's limits
        on = rng.choices(
            population=list(limits.keys()),
            weights=[limits[i][1] - limits[i][0] for i in limits],
        )[0]

        # Pick a split point while using padding to avoid narrow regions
        a = limits[on][0]
        b = limits[on][1]
        at = rng.uniform(a + padding * (b - a), b - padding * (b - a))

        l_child, r_child = tree.split_node(parent, on, at)

        tmp = limits[on]
        limits[on] = (limits[on][0], at)
        recurse(tree, l_child, limits, depth + 1)
        limits[on] = tmp

        tmp = limits[on]
        limits[on] = (at, limits[on][1])
        recurse(tree, r_child, limits, depth + 1)
        limits[on] = tmp

    tree = HashTree()
    root = tree.plant()
    recurse(tree, root, limits, 0)

    return tree


def build_list_tree(limits, max_depth, padding, rng):
    def recurse(tree, parent_index, limits, height):
        node_index = tree.add_node(parent_index)

        # Randomly pick a feature
        # We weight each feature by the gap between each feature's limits
        on = rng.choices(
            population=list(limits.keys()),
            weights=[limits[i][1] - limits[i][0] for i in limits],
        )[0]

        # Pick a split point while using padding to avoid narrow regions
        a = limits[on][0]
        b = limits[on][1]
        at = rng.uniform(a + padding * (b - a), b - padding * (b - a))

        tree.nodes.append(LTNode(on, at))

        if not height:
            return

        # Build the left child
        tmp = limits[on]
        limits[on] = (tmp[0], at)
        recurse(tree, node_index, limits, height - 1)
        limits[on] = tmp

        # Build the right node
        tmp = limits[on]
        limits[on] = (at, tmp[1])
        recurse(tree, node_index, limits, height - 1)
        limits[on] = tmp

    tree = BinaryListTree()
    recurse(tree, None, limits, max_depth)
    return tree


def eval_tree_walk(tree, n_samples, n_features):
    delta_t = 0
    for i in range(n_samples):
        x = {feat: rng.random() for feat in range(n_features)}
        start = time.time()
        tree.sort(x)
        delta_t += (time.time() - start)

    return delta_t


if __name__ == '__main__':
    n_features = 10
    n_samples = 100_000
    max_depth = 20
    padding = 0.15
    n_repetitions = 10

    # Testing
    rng = random.Random(42)
    limits = {i: (0, 1) for i in range(n_features)}
    list_tree = build_list_tree(limits, max_depth, padding, rng)

    rng = random.Random(42)
    limits = {i: (0, 1) for i in range(n_features)}
    hash_tree = build_hash_tree(limits, max_depth, padding, rng)

    print(f'Number of nodes: {list_tree.n_nodes} (list), {hash_tree.n_nodes} (hash)')

    run_list = []
    for i in range(n_repetitions):
        run_list.append(eval_tree_walk(list_tree, n_samples, n_features))

    run_hash = []
    for i in range(n_repetitions):
        run_hash.append(eval_tree_walk(hash_tree, n_samples, n_features))

    print(f'List-based tree: {sum(run_list) / n_repetitions}')
    print(f'Hash-based tree: {sum(run_hash) / n_repetitions}')
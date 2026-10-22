from algorithms import alphabeta, mcts, minimax

ALGORITHMS = {
    "minimax": minimax,
    "alphabeta": alphabeta,
    "mcts": mcts,
}


def benchmark(board, algorithm, **kwargs):
    if callable(algorithm):
        function = algorithm
        name = getattr(algorithm, "__name__", str(algorithm))
    else:
        name = str(algorithm).lower()
        if name not in ALGORITHMS:
            raise ValueError(
                f"Unknown algorithm '{algorithm}'. Choose among: {', '.join(ALGORITHMS)}"
            )
        function = ALGORITHMS[name]

    result = function(board, **kwargs)

    return {
        "name": name,
        "move": result["move"],
        "score": result["score"],
        "nodes_explored": result["nodes_explored"],
        "time": result["time"],
    }


def compare_minimax_alphabeta(depths=(1, 2, 3, 4, 5)):
    from game import create_board

    board = create_board()
    rows = []
    for depth in depths:
        mm = benchmark(board, "minimax", depth=depth)
        ab = benchmark(board, "alphabeta", depth=depth)
        rows.append((depth, mm, ab))

    header = (f"{'depth':>5} | {'algorithm':<10} | {'move':>4} | {'score':>8} | "
              f"{'nodes':>9} | {'time (s)':>9}")
    print(header)
    print("-" * len(header))
    for depth, mm, ab in rows:
        for res in (mm, ab):
            print(f"{depth:>5} | {res['name']:<10} | {str(res['move']):>4} | "
                  f"{str(res['score']):>8} | {res['nodes_explored']:>9} | "
                  f"{res['time']:>9.4f}")
        print("-" * len(header))

    # Verification
    print("\nVerification")
    for depth, mm, ab in rows:
        same_value = mm["score"] == ab["score"]
        fewer_nodes = ab["nodes_explored"] <= mm["nodes_explored"]
        ratio = ab["nodes_explored"] / mm["nodes_explored"]
        print(f"depth {depth}: same value = {same_value}, "
              f"alphabeta <= minimax nodes = {fewer_nodes}, "
              f"node ratio = {ratio:.2%}")
        assert same_value, f"Different Minimax values at depth {depth}"
        assert fewer_nodes, f"Alpha-Beta explored more nodes at depth {depth}"

    return rows


def compare_mcts(budgets=(100, 500, 1000, 2000), seed=42):
    from game import create_board

    board = create_board()
    results = [benchmark(board, "mcts", num_simulations=n, seed=seed) for n in budgets]

    header = (f"{'simulations':>11} | {'move':>4} | {'reward':>7} | "
              f"{'nodes':>7} | {'time (s)':>9}")
    print(header)
    print("-" * len(header))
    for n, res in zip(budgets, results):
        print(f"{n:>11} | {str(res['move']):>4} | {res['score']:>7.4f} | "
              f"{res['nodes_explored']:>7} | {res['time']:>9.4f}")
    return results


def run_all_experiments(depths=(1, 2, 3, 4, 5), budgets=(100, 500, 1000, 2000), seed=42):
    from game import create_board

    board = create_board()
    rows = []
    for name, label in (("minimax", "Minimax"), ("alphabeta", "Alpha-Beta")):
        for depth in depths:
            res = benchmark(board, name, depth=depth)
            rows.append({"algorithm": label, "configuration": f"Depth {depth}",
                         "param": depth, **res})
    for n in budgets:
        res = benchmark(board, "mcts", num_simulations=n, seed=seed)
        rows.append({"algorithm": "MCTS", "configuration": f"{n} simulations",
                     "param": n, **res})
    return rows


def print_table(rows):
    header = (f"{'Algorithm':<11} | {'Configuration':<17} | {'Move':>4} | "
              f"{'Nodes':>9} | {'Time (s)':>9}")
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r['algorithm']:<11} | {r['configuration']:<17} | {str(r['move']):>4} | "
              f"{r['nodes_explored']:>9} | {r['time']:>9.4f}")


def plot_results(rows, show=True):
    import matplotlib.pyplot as plt

    # Plot 1: explored nodes vs depth (Minimax and Alpha-Beta)
    plt.figure(figsize=(7, 4.5))
    for label, marker in (("Minimax", "o"), ("Alpha-Beta", "s")):
        data = [r for r in rows if r["algorithm"] == label]
        plt.plot([r["param"] for r in data], [r["nodes_explored"] for r in data],
                 marker=marker, label=label)
    plt.yscale("log")
    plt.xlabel("Search depth")
    plt.ylabel("Explored nodes (log scale)")
    plt.title("Explored nodes vs search depth")
    plt.xticks(sorted({r["param"] for r in rows if r["algorithm"] != "MCTS"}))
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("nodes_vs_depth.png", dpi=150)

    # Plot 2: execution time vs number of simulations (MCTS)
    mcts_rows = [r for r in rows if r["algorithm"] == "MCTS"]
    plt.figure(figsize=(7, 4.5))
    plt.plot([r["param"] for r in mcts_rows], [r["time"] for r in mcts_rows],
             marker="o", label="MCTS")
    plt.xlabel("Number of simulations")
    plt.ylabel("Execution time (s)")
    plt.title("MCTS execution time vs number of simulations")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("time_vs_simulations.png", dpi=150)

    if show:
        plt.show()


if __name__ == "__main__":
    print("=== Q2: Minimax vs Alpha-Beta ===")
    compare_minimax_alphabeta()
    print("\n=== Q3: MCTS budgets ===")
    compare_mcts()
    print("\n=== Q4: all experiments ===")
    all_rows = run_all_experiments()
    print_table(all_rows)
    print("\n=== Q5: plots ===")
    plot_results(all_rows)
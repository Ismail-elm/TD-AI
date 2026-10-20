"""Cost-based search algorithms for the Pokémon environment."""

from __future__ import annotations

import heapq
import random
from itertools import count

from pokemon_game import (
    GameMap,
    State,
    movement_cost,
    successors,
)


def reconstruct_path(
    parents: dict[State, State | None],
    goal: State,
) -> list[State]:
    """Reconstruct a path from a parent dictionary."""
    path: list[State] = []
    current: State | None = goal

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def path_cost(
    game_map: GameMap,
    path: list[State],
) -> int:
    """Return the total cost of a path."""
    return sum(
        movement_cost(game_map, state)
        for state in path[1:]
    )


def manhattan_distance(
    state: State,
    goal: State,
) -> int:
    """Return the Manhattan distance between two states."""
    return (
        abs(state[0] - goal[0])
        + abs(state[1] - goal[1])
    )


def generate_random_path(
    game_map: GameMap,
    start: State,
    goal: State,
    seed: int | None = None,
) -> list[State]:
    """Generate a random valid path from start to goal.

    This function is provided only to demonstrate the visualization.
    It is not guaranteed to return a minimum-cost or shortest path.

    The function performs a randomized depth-first exploration: the valid
    successor states are shuffled before being added to the frontier.

    Parameters
    ----------
    game_map : GameMap
        Weighted Pokémon map.
    start : State
        Initial trainer position.
    goal : State
        Pokémon Center position.
    seed : int or None, default=None
        Random seed used to make the result reproducible.

    Returns
    -------
    list[State]
        A valid path beginning at ``start`` and ending at ``goal``.

    Raises
    ------
    RuntimeError
        If no path exists between the start and the goal.
    """
    rng = random.Random(seed)

    frontier = [start]

    parents: dict[State, State | None] = {
        start: None,
    }

    while frontier:
        current = frontier.pop()

        if current == goal:
            return reconstruct_path(parents, goal)

        next_states = successors(game_map, current)
        rng.shuffle(next_states)

        for next_state in next_states:
            if next_state in parents:
                continue

            parents[next_state] = current
            frontier.append(next_state)

    raise RuntimeError(
        "No path exists between the start and the goal."
    )


def dijkstra(
    game_map: GameMap,
    start: State,
    goal: State,
) -> tuple[list[State], int]:

    frontier = [(0, 0, start)]
    counter = count()

    costs = {start: 0}
    parents = {start: None}
    considered_states = 0

    while frontier:
        current_cost, _, current = heapq.heappop(frontier)
        considered_states += 1

        if current_cost != costs[current]:
            continue

        if current == goal:
            return reconstruct_path(parents, goal), considered_states

        for next_state in successors(game_map, current):
            new_cost = current_cost + movement_cost(game_map, next_state)

            if next_state not in costs or new_cost < costs[next_state]:
                costs[next_state] = new_cost
                parents[next_state] = current

                heapq.heappush(
                    frontier,
                    (new_cost, next(counter), next_state),
                )

    raise RuntimeError("No path exists between the start and the goal.")


def a_star(
    game_map: GameMap,
    start: State,
    goal: State,
) -> tuple[list[State], int]:

    frontier = [
        (manhattan_distance(start, goal), 0, start)
    ]
    counter = count()

    costs = {start: 0}
    parents = {start: None}
    considered_states = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        considered_states += 1

        current_cost = costs[current]

        if current == goal:
            return reconstruct_path(parents, goal), considered_states

        for next_state in successors(game_map, current):
            new_cost = current_cost + movement_cost(game_map, next_state)

            if next_state not in costs or new_cost < costs[next_state]:
                costs[next_state] = new_cost
                parents[next_state] = current

                priority = new_cost + manhattan_distance(next_state, goal)

                heapq.heappush(
                    frontier,
                    (priority, next(counter), next_state),
                )

    raise RuntimeError("No path exists between the start and the goal.") 
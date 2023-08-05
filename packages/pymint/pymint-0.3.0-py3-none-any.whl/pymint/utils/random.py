from typing import Dict, Tuple
import networkx as nx
from parchmint.device import ValveType

from pymint.mintdevice import MINTDevice
from pymint.mintlayer import MINTLayerType
from pymint.minttarget import MINTTarget


def generate_random_graphs(
    flow_vertices, max_ports, max_valves, max_control_ports
) -> Tuple[nx.DiGraph, nx.DiGraph, Dict[str, str]]:
    """
    Generates a random graph with the given number of vertices and edges.
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(range(flow_vertices))
    graph.add_edges_from(
        nx.random_graphs.watts_strogatz_graph(flow_vertices, max_ports, 0.1).edges()
    )
    graph.add_edges_from(
        nx.random_graphs.watts_strogatz_graph(flow_vertices, max_valves, 0.1).edges()
    )
    graph.add_edges_from(
        nx.random_graphs.watts_strogatz_graph(
            flow_vertices, max_control_ports, 0.1
        ).edges()
    )
    return graph, nx.DiGraph(graph), {}


def generate_random_netlists(device_name: str) -> MINTDevice:
    """
    Generates a random netlist.
    """
    flow_graph, control_graph, valve_map = generate_random_graphs(5, 6, 7, 8)

    device = MINTDevice(device_name)
    device.create_mint_layer("FLOW", "0", "0", MINTLayerType.FLOW)
    device.create_mint_layer("CONTROL", "0", "0", MINTLayerType.CONTROL)

    # Loop through the nodes and create new components in the device.
    for node in flow_graph.nodes():

        # TODO - Decide if this is a port or something else
        mint_string = "PORT"
        device.create_mint_component(node, mint_string, {}, ["FLOW"])

    # Loop through the edges and create new connections in the device.
    connection_count = 0
    for edge in flow_graph.edges():
        device.create_mint_connection(
            "connection_{}".format(connection_count),
            "CHANNEL",
            {},
            MINTTarget(edge[0], None),
            [MINTTarget(edge[1], None)],
            "FLOW",
        )

        connection_count += 1

    # Go through the dictionary entries and add the valves to the device.
    for valve_id, connection_id in valve_map.items():
        device.create_valve(
            valve_id,
            "VALVE3D",
            {},
            ["CONTROL"],
            device.get_connection(connection_id),
            ValveType.NORMALLY_CLOSED,
        )

    return device


device = generate_random_netlists("test_device")

print(device.to_parchmint_v1_x())
print(device.to_MINT())

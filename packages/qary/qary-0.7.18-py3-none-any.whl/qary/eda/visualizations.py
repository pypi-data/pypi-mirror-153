from graphviz import Digraph
from pathlib import Path

from qary.chat.dialog import TurnsPreparation, load_dialog_turns


def graphviz_dumps(graph, format='svg', quiet=True):
    """ Dump a graphviz Graph (or Digraph) object to a unicode string """
    return graph.pipe(format=format, quiet=quiet).decode()


def graph_dialog_turns(dialog_turns, name='default_dialog_graph'):
    """ Create graphviz flow chart of a list of dicts dialog.v2 dicts

    >>> graph_dialog_turns([
    ...     {'state': 'state1', 'bot': 'All good?', 'next_condition':
    ...         {'state2': 'yes', 'state3': 'N'}},
    ...     {'state': 'state2', 'bot': 'Good!'},
    ...     {'state': 'state3', 'bot': 'Sorry...'},
    ...     ])
    <graphviz...>
    """
    # if dialog_turns is None:
    #     dialog_turns = DEFAULT_DIALOG_PATH
    if isinstance(dialog_turns, (Path, str)) and Path(dialog_turns).is_file():
        dialog_turns = load_dialog_turns(dialog_turns)

    g = Digraph(name)
    g.attr(rankdir='TB')

    for turn in dialog_turns:
        source_name = turn['state']
        next_conditions = turn.get('next_condition', {'__default__': ['']})
        for dest_name, human_statements in next_conditions.items():
            if isinstance(human_statements, str):
                human_statements = [human_statements]
            label = human_statements[0]
            g.edge(source_name, dest_name, label=label)
    return g


def draw_convoscript(graph=None, dialog_turns=None, name='qary.visualizations.draw_convoscript'):
    """ Display a finite statem machine diagram of the conversation dialog graph

    >>> draw_convoscript()
    <graphviz...
    """
    if graph is None:
        if isinstance(dialog_turns, (str, Path)) and Path(dialog_turns).is_file():
            dialog_turns = TurnsPreparation(turns_list=dialog_turns)
        if dialog_turns is not None:
            g = graph_dialog_turns(dialog_turns)
    if graph is None:
        g = Digraph(name, filename=None)
    return g

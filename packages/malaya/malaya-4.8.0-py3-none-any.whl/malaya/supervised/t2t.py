from malaya.function import (
    check_file,
    load_graph,
    generate_session,
    nodes_session,
)
from malaya.model.tf import Seq2SeqLSTM


def load_lstm(module, left_dict, right_dict, cleaning, quantized=False, **kwargs):
    path = check_file(
        file='lstm-bahdanau',
        module=module,
        keys={'model': 'model.pb'},
        quantized=quantized,
        **kwargs,
    )
    g = load_graph(path['model'], **kwargs)
    inputs = ['Placeholder']
    outputs = []
    input_nodes, output_nodes = nodes_session(
        g,
        inputs,
        outputs,
        extra={
            'greedy': 'import/decode_1/greedy:0',
            'beam': 'import/decode_2/beam:0',
        },
    )
    return Seq2SeqLSTM(
        input_nodes=input_nodes, output_nodes=output_nodes,
        sess=generate_session(graph=g, **kwargs),
        left_dict=left_dict,
        right_dict=right_dict,
        cleaning=cleaning,
    )

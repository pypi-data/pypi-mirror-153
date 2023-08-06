def create_onnx_from_keras(keras_model,
                           is_flattened: bool = True,
                           has_timestep: bool = True,
                           has_channel: bool = False,
                           is_mutex: bool = True,
                           feature: str = '',
                           filename: str = ''):
    import tf2onnx

    onnx_model, _ = tf2onnx.convert.from_keras(keras_model)
    onnx_model = replace_stateful_grus(keras_model=keras_model, onnx_model=onnx_model)
    onnx_model = add_sonusai_metadata(model=onnx_model,
                                      is_flattened=is_flattened,
                                      has_timestep=has_timestep,
                                      has_channel=has_channel,
                                      is_mutex=is_mutex,
                                      feature=feature)
    if filename:
        import onnx
        onnx.save(onnx_model, filename)
    return onnx_model


def replace_stateful_grus(keras_model, onnx_model):
    """Replace stateful GRUs with custom layers."""
    from tensorflow.keras.layers import GRU

    stateful_gru_names = []
    for i in range(len(keras_model.layers)):
        layer = keras_model.layers[i]
        if isinstance(layer, GRU):
            if layer.stateful:
                stateful_gru_names.append(layer.name)

    for node_index in range(len(onnx_model.graph.node)):
        node = onnx_model.graph.node[node_index]
        replace = False
        if node.op_type == 'GRU':
            for i in node.input:
                for n in stateful_gru_names:
                    if n in i:
                        replace = True
        if node.name in stateful_gru_names or replace:
            node.op_type = 'SGRU'

    return onnx_model


def add_sonusai_metadata(model,
                         is_flattened: bool = True,
                         has_timestep: bool = True,
                         has_channel: bool = False,
                         is_mutex: bool = True,
                         feature: str = ''):
    """Add SonusAI metadata to ONNX model.
      model           keras model
      file_pfx        filename prefix to save onnx model (do not save if empty)
      is_flattened    model feature data is flattened
      has_timestep    model has timestep dimension
      has_channel     model has channel dimension
      is_mutex        model label output is mutually exclusive
      feature         model feature type
    """
    f_flag = model.metadata_props.add()
    f_flag.key = 'is_flattened'
    f_flag.value = str(is_flattened)

    t_flag = model.metadata_props.add()
    t_flag.key = 'has_timestep'
    t_flag.value = str(has_timestep)

    c_flag = model.metadata_props.add()
    c_flag.key = 'has_channel'
    c_flag.value = str(has_channel)

    m_flag = model.metadata_props.add()
    m_flag.key = 'is_mutex'
    m_flag.value = str(is_mutex)

    feature_flag = model.metadata_props.add()
    feature_flag.key = 'feature'
    feature_flag.value = str(feature)

    return model

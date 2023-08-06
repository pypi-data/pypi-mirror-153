import numpy as np


def reshape_inputs(feature: np.ndarray,
                   truth: np.ndarray,
                   batch_size: int,
                   timesteps: int = 0,
                   flatten: bool = False,
                   add1ch: bool = False) -> (np.ndarray, np.ndarray, tuple, int, np.ndarray, str):
    """Check SonusAI feature and truth data and reshape feature of size frames x strides x bands into
    one of several options:

    If timesteps > 0: (i.e. for recurrent NNs):
      no-flatten, no-channel:   sequences x timesteps x strides       x bands     (4-dim)
      flatten, no-channel:      sequences x timesteps x strides*bands             (3-dim)
      no-flatten, add-1channel: sequences x timesteps x strides       x bands x 1 (5-dim)
      flatten, add-1channel:    sequences x timesteps x strides*bands         x 1 (4-dim)

    If timesteps == 0, then do not add timesteps dimension

    The number of samples is trimmed to be a multiple of batch_size (Keras requirement) for
    both feature and truth.
    Channel is added to last/outer dimension for channel_last support in Keras/TF

    Returns:
      f, t,       reshaped feature and truth
      in_shape    input shape for model (timesteps x feature)
      num_classes number of classes in truth = output length of nn model
      cweights    weights of each class in truth, per sklearn compute_weights()
      msg         string with report with info on data and operations done
    """

    from sonusai import SonusAIError
    from sonusai.metrics import calculate_class_weights_from_truth

    f = feature
    t = truth

    frames, strides, bands = f.shape
    truth_frames, num_classes = t.shape
    if frames != truth_frames:  # Double-check correctness of inputs
        raise SonusAIError('Frames in feature and truth do not match')

    msg = f'Training/truth shape: {frames}x{strides}x{bands}, nclass/outlen = {num_classes}\n'
    msg += f'Reshape request: timesteps {timesteps}, batchsize {batch_size}, flatten={flatten}, add1ch={add1ch}\n'

    # Compute class weights by hand as sklearn does not handle non-existent classes
    cweights = calculate_class_weights_from_truth(t)

    # calc new input shape only and return
    if batch_size == -1:
        if flatten:
            in_shape = [strides * bands]
        else:
            in_shape = [strides, bands]

        if timesteps > 0:
            in_shape = np.concatenate(([timesteps], in_shape[0:]), axis=0)

        if add1ch:
            in_shape = np.concatenate((in_shape[0:], [1]), axis=0)

        return f, t, in_shape, num_classes, cweights, msg  # quick

    if flatten:
        msg += f'Flattening {strides}x{bands} feature to {strides * bands}\n'
        f = np.reshape(f, (frames, strides * bands))

    # Reshape for Keras/TF recurrent models that require timesteps/sequence length dimension
    if timesteps > 0:
        sequences = frames // timesteps

        # Remove frames if remainder, not fitting into a multiple of new number of sequences
        frem = frames % timesteps
        brem = (frames // timesteps) % batch_size
        bfrem = brem * timesteps
        sequences = sequences - brem
        fr2drop = frem + bfrem
        if fr2drop:
            msg += f'Dropping {fr2drop} frames for new number of sequences to fit in multiple of batch_size\n'
            if f.ndim == 2:
                f = f[0:-fr2drop, ]  # Flattened input
            elif f.ndim == 3:
                f = f[0:-fr2drop, ]  # Un-flattened input

            t = t[0:-fr2drop, ]

        # Do the reshape
        msg += f'Reshape for timesteps = {timesteps}, new number of sequences (batches) = {sequences}\n'
        if f.ndim == 2:  # Flattened input
            # str=str+'Reshaping 2 dim\n'
            f = np.reshape(f, (sequences, timesteps, strides * bands))  # was frames x bands*timesteps
            t = np.reshape(t, (sequences, timesteps, num_classes))  # was frames x num_classes
        elif f.ndim == 3:  # Unflattened input
            # str=str+'Reshaping 3 dim\n'
            f = np.reshape(f, (sequences, timesteps, strides, bands))  # was frames x bands x timesteps
            t = np.reshape(t, (sequences, timesteps, num_classes))  # was frames x num_classes
    else:
        # Drop frames if remainder, not fitting into a multiple of new # sequences (Keras req)
        fr2drop = f.shape[0] % batch_size
        if fr2drop > 0:
            msg += f'Dropping {fr2drop} frames for total to be a multiple of batch_size\n'
            f = f[0:-fr2drop, ]
            t = t[0:-fr2drop, ]

    # Add channel dimension if required for input to model (i.e. for cnn type input)
    if add1ch:
        msg += 'Adding channel dimension to feature\n'
        f = np.expand_dims(f, axis=f.ndim)  # add as last/outermost dim

    in_shape = f.shape
    in_shape = in_shape[1:]  # remove frame dim size

    msg += f'Feature final shape: {f.shape}\n'
    msg += f'Input shape final (includes timesteps): {in_shape}\n'
    msg += f'Truth final shape: {t.shape}\n'

    return f, t, in_shape, num_classes, cweights, msg


def reshape_truth_predict(truth: np.ndarray, predict: np.ndarray, timesteps: int) -> (np.ndarray, np.ndarray, int):
    """Reshape truth and predict data.

    truth and predict can be either frames x num_classes, or frames x timesteps x num_classes
    In binary case, num_classes dim may not exist; detect this and set num_classes == 1
    """
    if truth.ndim == 3 or (truth.ndim == 2 and timesteps > 0):
        if truth.ndim == 2:
            # 2D but has timesteps = truth.shape[1]
            num_classes = 1
        else:
            # frames = truth.shape[0], timesteps = truth.shape[1]
            num_classes = truth.shape[2]
        # reshape to remove timestep dimension
        truth = np.reshape(truth, (truth.shape[0] * truth.shape[1], truth.shape[2]))
        predict = np.reshape(predict, (predict.shape[0] * predict.shape[1], predict.shape[2]))
    else:
        if truth.ndim == 1:
            # no timesteps dimension, = 0
            num_classes = 1
            # convert to 2D (F,1) if only 1 dim
            truth = np.expand_dims(truth, 1)
        else:
            num_classes = truth.shape[1]  # 2D input frames x num_classes

    # Support predict (and truth) when shape is (F,), just convert to (F,1)
    if predict.ndim == 1:
        predict = np.expand_dims(predict, 1)

    return truth, predict, num_classes

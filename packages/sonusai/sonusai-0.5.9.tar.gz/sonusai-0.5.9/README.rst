Sonus AI: Framework for simplified creation of deep NN models for sound, speech, and voice AI

Sonus AI includes functions for pre-processing training and validation data and
creating performance metrics reports for key types of Keras models:
- recurrent, convolutional, or a combination (i.e. RCNNs)
- binary, multiclass single-label, multiclass multi-label, and regresssion
- training with data augmentations:  noise mixing, pitch and time stretch, etc.

Sonus AI python functions are used by:
 - Aaware Inc. sonusai executable:  Easily create train/validation data, run prediction, evaluate model performance
 - Keras model scripts:             User python scripts for keras model creation, training, and prediction. These can use sonusai-specific data but also some general useful utilities for trainining rnn-based models like CRNN's, DSCRNN's, etc. in Keras

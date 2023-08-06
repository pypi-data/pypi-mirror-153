from typing import List

from sonusai import SonusAIError


def get_class_weights_threshold(mixdb: dict) -> List[float]:
    """Get the class weights threshold from a mixture database."""
    class_weights_threshold = mixdb['class_weights_threshold']
    if not isinstance(class_weights_threshold, list):
        class_weights_threshold = [class_weights_threshold] * mixdb['num_classes']
    if len(class_weights_threshold) != mixdb['num_classes']:
        raise SonusAIError(f'invalid class_weights_threshold length: {len(class_weights_threshold)}')
    return class_weights_threshold

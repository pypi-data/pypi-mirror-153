def load_mixdb(name: str) -> dict:
    import json
    from os.path import exists
    from os.path import splitext

    import h5py

    from sonusai import SonusAIError

    if not exists(name):
        raise SonusAIError(f'{name} does not exist')

    ext = splitext(name)[1]

    if ext == '.json':
        with open(file=name, mode='r', encoding='utf-8') as f:
            return json.load(f)

    if ext == '.h5':
        with h5py.File(name=name, mode='r') as f:
            return json.loads(f.attrs['mixdb'])

    raise SonusAIError(f'Do not know how to load mixdb from {name}')

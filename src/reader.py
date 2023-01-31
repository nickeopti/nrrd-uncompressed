import nrrd.reader
import numpy as np
import pydantic


class NRRDHeaderFields(pydantic.BaseModel):
    type: str
    sizes: tuple[int, ...]

    @pydantic.validator('sizes', pre=True)
    def split_sizes(cls, v):
        if isinstance(v, str):
            return v.split(' ')
        return v


def read_header(file: str) -> NRRDHeaderFields:
    header: list[str] = []
    with open(file, 'rb') as f:
        for line in f:
            line = line.decode('ascii', 'ignore').rstrip()

            if line == '':
                break

            header.append(line)

    fields = {
        line.split(':', 1)[0].strip(): line.split(':', 1)[1].strip()
        for line in header
        if ':' in line
    }

    return NRRDHeaderFields(**fields)


def read_binary_data(file: str, header: NRRDHeaderFields) -> np.ndarray:
    dtype = nrrd.reader._TYPEMAP_NRRD2NUMPY[header.type]

    data = np.fromfile(file, dtype=dtype).reshape(header.sizes[::-1]).T

    return data


def read(header_file: str, data_file: str = None) -> np.ndarray:
    if not data_file:
        data_file = f'{header_file}.b'

    header = read_header(header_file)
    data = read_binary_data(data_file, header)

    return data

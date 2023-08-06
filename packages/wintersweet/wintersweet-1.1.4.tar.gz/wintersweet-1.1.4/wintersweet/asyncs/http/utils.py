
import aiohttp


def _build_form_data(data, files):
    """
    :param data:
    :param files: {'file1': ('file1.txt', open('file1.txt')), 'file2': ('file2.txt', open('file2.txt'))}
    :return: FormData
    """
    form = aiohttp.FormData()
    if data:
        for k, v in data.items():
            form.add_field(k, str(v))

    if files:
        for name, file in files:
            form.add_field(name, value=file[1], filename=file[0])

    return form


@aiohttp.streamer
def _file_sender(writer, file_path):
    with open(file_path, 'rb') as f:
        chunk = f.read(65535)
        while chunk:
            yield from writer.write(chunk)
            chunk = f.read(65535)




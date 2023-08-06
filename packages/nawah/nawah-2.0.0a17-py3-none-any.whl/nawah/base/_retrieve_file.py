'''Provides 'retrieve_file' Base Function callable'''

import io
import logging
from typing import (TYPE_CHECKING, Any, MutableMapping, MutableSequence,
                    Optional, cast)

from PIL import Image

from nawah import data as Data
from nawah.classes import Query
from nawah.config import Config

from ._shared import FILE_ATTRS
from .exceptions import (FileNotFoundException, FileNotImageException,
                         InvalidDocException, UtilityModuleDataCallException)

if TYPE_CHECKING:
    from nawah.types import NawahEnv, Results

logger = logging.getLogger('nawah')


async def retrieve_file(
    *,
    module_name: str,
    env: 'NawahEnv',
    query: 'Query',
) -> 'Results':
    '''Finds file from doc in module, and returns it as part of results. If doc not found, raises
    'InvalidDocException'. If attr not found in doc, of file not matching file[s] in attr, raises
    'FileNotFoundException'. If a value for arg 'thumb_dims' is provided, generates a thumbnail, but
    raises 'FileNotImageException' if file not an image. If process to generate thumbnail fails, for
    any reasons, original file would be returned, error would be logged'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='retrieve_file'
        )

    attr_name = query['attr'][0]
    filename = query['filename'][0]
    thumb_dims: Optional[MutableSequence[int]] = None
    if 'thumb' in query:
        thumb_dims = [int(dim) for dim in query['thumb'][0].split('x')]

    file_results = await Data.read(
        env=env,
        collection_name=f'{module.collection}__file',
        attrs=FILE_ATTRS,
        query=Query([{'_id': query['_id'][0]}]),
    )

    if not file_results['count']:
        raise InvalidDocException(doc_id=query['_id'][0])

    retrieved_file = file_results['docs'][0]['file']

    retrieved_file['content'] = _generate_thumb(
        thumb_dims=thumb_dims,
        module_name=module_name,
        doc_id=query['_id'][0],
        attr_name=attr_name,
        filename=filename,
        retrieved_file=retrieved_file,
    )

    return {
        'status': 200,
        'msg': 'File attached to response',
        'args': {
            'return': 'file',
            'docs': [
                {
                    '_id': query['_id'][0],
                    'name': retrieved_file['name'],
                    'type': retrieved_file['type'],
                    'lastModified': retrieved_file['lastModified'],
                    'size': retrieved_file['size'],
                    'content': retrieved_file['content'],
                }
            ],
        },
    }


def _retrieve_file_from_attr(*, doc_id, attr_name, attr, filename):
    '''Attempts to find file in attr. if failed, raises 'FileNotFoundException' '''

    retrieved_file = None

    if isinstance(attr, list):
        for item in attr:
            if item['name'] == filename:
                retrieved_file = item
                break
    elif isinstance(attr, dict):
        attr = cast(MutableMapping[str, Any], attr)
        if attr['name'] == filename:
            retrieved_file = attr

    if not retrieved_file:
        # [DOC] No filename match
        raise FileNotFoundException(
            doc_id=doc_id, attr_name=attr_name, file_name=filename
        )

    return retrieved_file


def _generate_thumb(
    *, thumb_dims, module_name, doc_id, attr_name, filename, retrieved_file
):
    '''Checks 'thumb_dims' value to generate thumbnail for image. if file is not image, raises
    'FileNotImageException'. If failed while generating thumbnail, logs error, and returns
    original file'''

    if not thumb_dims:
        return retrieved_file['content']

    if retrieved_file['type'].split('/')[0] != 'image':
        raise FileNotImageException(
            doc_id=doc_id,
            attr_name=attr_name,
            file_name=filename,
            file_type=retrieved_file['type'],
        )
    try:
        image = Image.open(io.BytesIO(retrieved_file['content']))
        image.thumbnail(thumb_dims)
        stream = io.BytesIO()
        image.save(stream, format=image.format)
        stream.seek(0)
        return stream.read()
    except Exception as e:  # pylint: disable=broad-except
        logger.error('Failed to generate thumbnail for:')
        logger.error('- Module     : \'%s\'', module_name)
        logger.error('- Doc \'_id\': \'%s\'', doc_id)
        logger.error('- Attr       : \'%s\'', attr_name)
        logger.error('- File       : \'%s\'', filename)
        logger.error('- Exception message: %s', e)

    return retrieved_file['content']

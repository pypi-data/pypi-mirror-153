import logging
from typing import TYPE_CHECKING, MutableMapping, MutableSequence, Union

from nawah.config import Config
from nawah.enums import Event

if TYPE_CHECKING:
    from nawah.types import NawahDoc, NawahEnv


logger = logging.getLogger('nawah')


async def _process_file_obj(
    *,
    doc: Union['NawahDoc', MutableMapping, MutableSequence],
    env: 'NawahEnv',
):
    if isinstance(doc, dict):
        doc_iter = doc.keys()
    elif isinstance(doc, list):
        doc_iter = range(len(doc))
    for j in doc_iter:
        if isinstance(doc[j], dict):
            if '__file' in doc[j].keys():
                file_id = doc[j]['__file']
                logger.debug(
                    'Detected file in doc. Retrieving file from File module with _id: \'%s\'',
                    file_id,
                )
                try:
                    file_results = (
                        await Config.modules['file']
                        .funcs['read']
                        .callable(
                            skip_events=[Event.PERM], env=env, query=[{'_id': file_id}]
                        )
                    )
                    doc[j] = file_results['args']['docs'][0]['file']
                    file_results = (
                        await Config.modules['file']
                        .funcs['delete']
                        .callable(
                            skip_events=[Event.PERM, Event.SOFT],
                            env=env,
                            query=[{'_id': file_id}],
                        )
                    )
                    if (
                        file_results['status'] != 200
                        or file_results['args']['count'] != 1
                    ):
                        logger.warning(
                            f'Filed to delete doc _id \'{file_id}\' from File module after retrieving.'
                        )
                except Exception as e:
                    logger.error(
                        f'Failed to retrieve doc _id \'{file_id}\', with error:'
                    )
                    logger.error(e)
                    doc[j] = None
            else:
                await _process_file_obj(doc=doc[j], env=env)
        elif type(doc[j]) == list:
            await _process_file_obj(doc=doc[j], env=env)

from contextlib import contextmanager
from scrapeanything.utils.config import Config
from scrapeanything.database.repository import Repository
from scrapeanything.utils.log import Log

@contextmanager
def Connection(config: Config):

    repository = Repository(config=config)
    try:
        yield repository
        repository.commit()
        # repository.session.flush()
    except Exception as e:
        Log.error(f'Error while running database operation: {e}')
        repository.rollback()
        raise Exception()
    finally:
        repository.close()
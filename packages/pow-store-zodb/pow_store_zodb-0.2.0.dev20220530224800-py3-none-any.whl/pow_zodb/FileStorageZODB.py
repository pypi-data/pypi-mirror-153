import logging
import os

from rdflib.store import Store
import transaction
from transaction.interfaces import NoTransaction
import ZODB
from ZODB.FileStorage import FileStorage
from zc.lockfile import LockError

from .ZODB import ZODBStore


L = logging.getLogger(__name__)


class _UnopenedStore(object):
    __slots__ = ()

    def __getattr__(self, *args):
        raise Exception('This FileStorageZODBStore has not been opened')


UNOPENED_STORE = _UnopenedStore()

TM_CONFIG_KEY = 'transaction_manager'
'''
Key for transaction manager configuration option
'''


class FileStorageZODBStore(Store):
    '''
    `~ZODB.FileStorage.FileStorage`-backed Store
    '''

    context_aware = True
    formula_aware = True
    graph_aware = True
    transaction_aware = True
    supports_range_queries = True

    def __init__(self, *args, **kwargs):
        super(FileStorageZODBStore, self).__init__(*args, **kwargs)
        self._store = UNOPENED_STORE
        self._file_url = None
        self._transaction_manager = None
        self._conn = None
        self._zdb = None

    def open(self, configuration, create=True):
        if isinstance(configuration, dict):
            url = configuration.get('url', None)
            if url is None:
                raise ValueError('FileStorageZODBStore configuration dict must have a "url" key')
            openstr = os.path.abspath(url)
            # creating a new dict for params since we don't want to modify the dict given
            # to us
            params = {k: v for k, v in configuration.items()
                    if k not in ('url', TM_CONFIG_KEY)}
            if TM_CONFIG_KEY in configuration:
                tm = configuration[TM_CONFIG_KEY]
            else:
                # The default transaction manager is an appropriate fall-back since it's
                # what ZODB uses by default if you don't provide a transaction manager
                tm = transaction.manager
        elif isinstance(configuration, str):
            openstr = os.path.abspath(configuration)
            params = dict()
            tm = transaction.manager
        else:
            raise TypeError(f'Not an expected configuration type: {configuration} of type {type(configuration)}')

        try:
            # N.B.: We do not pass the `create` option to FileStorage from our `create`
            # argument because FileStorage will still create the file unless you're also
            # requesting a read_only FileStorage. I think this is super stupid, but that's
            # what it does.
            fs = FileStorage(openstr, **params)
        except IOError:
            L.exception("Failed to create a FileStorage")
            raise FileStorageInitFailed(openstr)
        except LockError:
            L.exception('Found database "{}" is locked when trying to open it. '
                    'The PID of this process: {}'.format(openstr, os.getpid()), exc_info=True)
            raise FileLocked(f'Database {openstr} locked')

        self._zdb = ZODB.DB(fs, cache_size=1600)
        self._conn = self._zdb.open(transaction_manager=tm)
        root = self._conn.root()
        if 'rdflib' not in root:
            with tm:
                root['rdflib'] = self._store = ZODBStore()
        else:
            self._store = root['rdflib']
        self._file_url = openstr
        self._transaction_manager = tm

    def close(self, commit_pending_transaction=False):
        if self._conn is None:
            raise Exception(f'Connection is not opened on {self}, so cannot close')

        if commit_pending_transaction:
            try:
                self._transaction_manager.commit()
            except NoTransaction:
                # If the transaction manager is in explicit mode, we have no transaction
                # to commit, so just chill
                L.debug('No pending transaction to commit on close with %s',
                        self._transaction_manager, exc_info=True)
            except Exception:
                # catch commit exception and close db.
                # otherwise db would stay open and follow up tests
                # will detect the db in error state
                L.warning('Forced to abort transaction on ZODB store closing', exc_info=True)
                self._transaction_manager.abort()
                raise
            else:
                L.warning('Committed pending transaction on close with %s',
                        self._transaction_manager)
        elif not self._transaction_manager.explicit:
            # If the transaction manager is explicit, then the caller should have made
            # commit or abort before closing the connection
            self._transaction_manager.abort()
            L.warning('Aborted pending transaction on close with %s',
                    self._transaction_manager)
        self._conn.close()
        self._zdb.close()

        self._conn = None
        self._zdb = None

    def bind(self, prefix, namespace, override=True):
        self._store.bind(prefix, namespace, override)

    def namespace(self, prefix):
        return self._store.namespace(prefix)

    def prefix(self, namespace):
        return self._store.prefix(namespace)

    def namespaces(self):
        return self._store.namespaces()

    def rollback(self):
        self._store.rollback()

    def commit(self):
        self._store.commit()

    def addN(self, quads):
        self._store.addN(quads)

    def add(self, triple, context, quoted=False):
        self._store.add(triple, context, quoted=quoted)

    def contexts(self, triple):
        return self._store.contexts(triple)

    def triples(self, triple, context=None):
        return self._store.triples(triple, context)

    def triples_choices(self, triple, context=None):
        return self._store.triples_choices(triple, context=context)

    def remove(self, triplepat, context=None):
        self._store.remove(triplepat, context=context)

    def __len__(self, context=None):
        return self._store.__len__(context)

    def add_graph(self, graph):
        self._store.add_graph(graph)

    def remove_graph(self, graph):
        self._store.remove_graph(graph)

    def __str__(self):
        return f'{type(self).__name__}({self._file_url})'


class OpenError(Exception):
    pass


class FileStorageInitFailed(OpenError):
    pass


class FileLocked(OpenError):
    pass

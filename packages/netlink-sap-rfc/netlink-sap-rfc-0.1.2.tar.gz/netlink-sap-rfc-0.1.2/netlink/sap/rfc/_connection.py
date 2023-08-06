import collections.abc
import getpass

import pyrfc

from .exception import LogonError, CommunicationError
from ._function import Function
from ._landscape import Landscape
from ._table import select
from netlink.logging import logger

default_landscape = Landscape()


def _get_keepass_entry(keepass_database, **kwargs):
    entries = keepass_database.find_entries(**kwargs)
    if entries:  # found at least one
        if len(entries) > 1:  # not unique -> error
            raise Exception
        return entries[0]
    return None


class Server(collections.abc.Mapping):
    PARAMETER_NAMES = ('ashost', 'sysnr', 'mshost', 'msserv', 'sysid', 'group')

    def __init__(self,
                 ashost: str = None, sysnr: str = None,  # direct Application Host
                 mshost: str = None, msserv: str = None, sysid: str = None, group: str = None,  # via message server
                 **kwargs,  # dummy to catch unsupported
                 ):
        """

        :param ashost:
        :param sysnr:
        :param mshost:
        :param msserv:
        :param sysid:
        :param group:
        """
        self.ashost = ashost
        self.sysnr = sysnr
        self.mshost = mshost
        self.msserv = msserv
        self.sysid = sysid
        self.group = group

    def __getitem__(self, item):
        if item.lower() in self.PARAMETER_NAMES:
            return self.__dict__[item.lower()]
        raise KeyError(item)

    def __getattr__(self, item):
        if item.lower() in self.PARAMETER_NAMES:
            return self[item]
        raise AttributeError(item)

    def __len__(self):
        return len([i for i in self.PARAMETER_NAMES if self[i]])

    def __iter__(self):
        return iter([i for i in self.PARAMETER_NAMES if self[i]])

    def kwargs(self):
        return {k: v for k, v in self.items()}

    def __str__(self):
        if self.ashost is not None:
            return f'{self.ashost}:32{self.sysnr}'
        else:
            return f"{self.mshost}:{self.msserv} ({self.sysid}-{self.group})"

    @property
    def is_valid(self) -> bool:
        if self.ashost is not None:
            if self.sysnr is None or (
            self.mshost is not None or self.msserv is not None or self.group is not None):
                return False
        else:
            if self.sysnr is not None or self.mshost is None or self.msserv is None or self.sysid is None or self.group is None:
                return False
        return True

    @classmethod
    def from_landscape(cls,
                       sysid: str,
                       landscape: Landscape = None) -> 'Server':
        """
        Get server info from Landscape xml

        :param sysid:
        :param landscape:
        """
        if landscape is None:
            landscape = default_landscape
        try:
            entry = landscape[sysid.upper()]
        except KeyError:
            msg = f"System ID '{sysid.upper()}' not found in Landscape."
            logger.error(msg)
            raise KeyError(msg) from None
        kwargs = {k: v for k, v in entry.items() if k in cls.PARAMETER_NAMES}
        return cls(**kwargs)


class Connection:
    def __init__(self,
                 server: Server,
                 client: str,
                 user: str = None,
                 passwd: str = None,
                 snc_qop: str = None,
                 snc_myname: str = None,
                 snc_partnername: str = None,
                 language: str = 'EN',
                 raw: bool = False):
        kwargs = server.kwargs()
        kwargs['client'] = client
        # fmt: off
        if user is not None: kwargs['user'] = user
        if passwd is not None: kwargs['passwd'] = passwd
        if snc_qop is not None: kwargs['snc_qop'] = snc_qop
        if snc_myname is not None: kwargs['snc_myname'] = snc_myname
        if snc_partnername is not None: kwargs['snc_partnername'] = snc_partnername
        # fmt: on
        kwargs.update(dict(language=language, config=dict(dtime=not raw)))
        logger.debug(f'Connecting to {server}')
        if logger.level < 10:
            for k, v in kwargs.items():
                # fmt: off
                if k == 'passwd': v = '*' * 8
                # fmt: on
                logger.trace(f'{k}: {v}')
        try:
            self._connection = pyrfc.Connection(**kwargs)
        except pyrfc.LogonError as e:
            logger.error(e.message)
            raise LogonError from None
        except pyrfc.CommunicationError as e:
            logger.error(e.message)
            raise CommunicationError from None

        self.connection_attributes = self._connection.get_connection_attributes()
        self._functions = {}

    def __getattr__(self, item):
        if item == "call":
            return self._connection.call
        if item == "get_function_description":
            return self._connection.get_function_description
        if item.upper() not in self._functions and item in self.connection_attributes:
            return self.connection_attributes[item]
        return self[item]

    def __getitem__(self, item):
        item = item.upper()
        if item not in self._functions:
            logger.debug(f"Initializing function '{item}'")
            self._functions[item] = Function(self, item)
        return self._functions[item]

    @property
    def sid(self):
        return self.sysId

    @property
    def sysid(self):
        return self.sysId

    def __str__(self):
        return f"{self.sysId}/{self.client} ({self.user})"

    def close(self):
        self._connection.close()

    def __del__(self):
        self.close()

    def select(self, table, *args, **kwargs):
        return select(self, table, *args, **kwargs)

    # def xml_select(self, table, where):
    #     return xml_select(self, table, where)

    @classmethod
    def sso(cls, sysid: str, client: str, user: str = None, language="EN", raw: bool = False):
        """
        Connect to SAP using Single-Sign-On

        :param sysid: System ID (<sid>)
        :param client: SAP Client
        :param user: User ID, defaults currently user
        :param language: Default: EN
        :param raw: Default: False
        :return: sap.rfc.Connection
        """
        sysid = sysid.upper()
        if user is None:
            user = getpass.getuser()
        user = user.upper()

        login_info = default_landscape[sysid].copy()
        if not login_info.get("sncname"):
            msg = f"SNC Name for {sysid} not found."
            logger.error(msg)
            raise AttributeError(msg)

        logger.verbose(f"Connecting using SSO to {sysid}/{client} with {user}")
        return cls(server=Server.from_landscape(sysid),
                   client=client,
                   user=user,
                   snc_qop='9',
                   snc_partnername=login_info["sncname"],
                   language=language,
                   raw=raw)

    @classmethod
    def login(cls, server: Server, client: str, passwd: str, user: str = None, language="EN", raw: bool = False):
        """
        Connect to SAP

        :param server:
        :param client:
        :param passwd:
        :param user:
        :param language:
        :param raw:
        :return:
        """
        if user is None:
            user = getpass.getuser()
        user = user.upper()

        logger.verbose(f"Connecting to {server} with {user}")
        return cls(server=server,
                   client=client,
                   user=user,
                   passwd=passwd,
                   language=language,
                   raw=raw)

    @classmethod
    def login_sid(cls, sysid: str, client: str, passwd: str, user: str = None, language="EN", raw: bool = False, landscape=None):
        """

        :param sysid:
        :param client:
        :param passwd:
        :param user:
        :param language:
        :param raw:
        :param landscape:
        :return:
        """
        sysid = sysid.upper()
        return cls.login(server=Server.from_landscape(sysid, landscape=landscape),
                         client=client,
                         user=user,
                         passwd=passwd,
                         language=language,
                         raw=raw)

    @classmethod
    def keepass(cls, keepass_database, sysid: str, client: str, user: str = None, language: str = None, raw: bool = False, landscape=None):
        """
        Connect to SAP using information from KeePass Database

        In addition to the password, any other setting might be stored (e.g. ashost)

        :param keepass_database: Opened Keepass Database
        :param sysid: Used to search  - first looks for this value in property 'logical_system'
        :param client: Used to search
        :param user: Used to search
        :param language: override possible entry
        :param raw:
        :param landscape: Used to determine connection information if not in KeePass
        :return:
        """

        # try if sysid a logical_system
        entry = _get_keepass_entry(keepass_database=keepass_database,
                                   string=dict(logical_system=sysid))
        if not entry:  # search for sysid, client, user
            entry = _get_keepass_entry(keepass_database=keepass_database,
                                       username=user.upper(),
                                       string=dict(sysid=sysid.upper(),
                                                   client=client))
            if not entry:
                raise Exception

        # try to create a server from the data in keepass
        server = Server(**entry.custom_properties)
        if not server.is_valid:  # no valid config
            server = Server.from_landscape(sysid, landscape=landscape)
        if language is None:
            language = entry.custom_properties.get('language', 'EN')

        return cls.login(server=server,
                         client=entry.get_custom_property('client'),
                         user=entry.username,
                         passwd=entry.password,
                         language=language,
                         raw=raw)


sso = Connection.sso
login = Connection.login
login_sid = Connection.login_sid
keepass = Connection.keepass

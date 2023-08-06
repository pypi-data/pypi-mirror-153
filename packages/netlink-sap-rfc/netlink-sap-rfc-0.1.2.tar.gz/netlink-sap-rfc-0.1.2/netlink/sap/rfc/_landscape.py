"""Get system information from the SAPGUI landscape configuration

For the time being, this works on Windows only, and expects that SAPGUI is installed and configured.
"""

import collections.abc
import pathlib
import winreg

from lxml import etree

from netlink.logging import logger


def _get_landscape_files():
    registry_key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
                                  r"Software\SAP\SAPLogon\LandscapeFilesLastUsed")
    result = []
    try:
        path = winreg.QueryValueEx(registry_key, "LandscapeFileOnServer")[0]
        logger.trace(f'Found SAPGUI Landscape Server File {path}')
        result.append(path)
    except FileNotFoundError:
        logger.verbose('No entry for SAPgui Landscape Server File found.')
    try:
        path = winreg.QueryValueEx(registry_key, "LandscapeFile")[0]
        logger.trace(f'Found local SAPGUI Landscape File {path}')
        result.append(path)
    except FileNotFoundError:
        logger.verbose('No entry for local SAPgui Landscape File found.')
    return tuple(result)


def _process_landscape_xml(file_handle):
    root = etree.parse(file_handle).getroot()
    if root.tag != "Landscape":
        msg = f"Wrong root tag: <{root.tag}> - expected <Landscape>"
        logger.error(msg)
        raise ValueError(msg)
    sysids = collections.defaultdict(dict)
    message_servers = {}
    for element in root:
        if element.tag == "Services":
            for child in element:
                # noinspection PyProtectedMember
                if type(child) == etree._Comment:
                    continue
                if child.tag != "Service":
                    logger.warning(f"Wrong tag: <{child.tag}> - expected <Service>")
                    continue
                if child.get("type") == "SAPGUI":
                    sid = child.get("systemid")
                    if child.get("sncname"):
                        sysids[sid]["sncname"] = child.get("sncname")
                    if child.get("mode") == "1":
                        sysids[sid]["ashost"], sysids[sid]["sysnr"] = child.get("server").split(":", 1)
                        sysids[sid]["sysnr"] = sysids[sid]["sysnr"][-2:]
                    else:
                        sysids[sid]["msid"] = child.get("msid")
                        sysids[sid]["group"] = child.get("server")
        elif element.tag == "Messageservers":
            for child in element:
                # noinspection PyProtectedMember
                if type(child) == etree._Comment:
                    continue
                if child.tag != "Messageserver":
                    logger.warning(f"Wrong tag: <{child.tag}> - expected <Messageserver>")
                    continue
                message_servers[child.get("uuid")] = {"mshost": child.get("host"), "msserv": child.get("port")}
    return sysids, message_servers


class Landscape(collections.abc.Mapping):
    """SAP System information from GUI Landscape XML files"""

    def __init__(self, landscape_file=None):
        self._data = {}
        sysids = {}
        message_servers = {}
        if landscape_file is None:
            for landscape_file in _get_landscape_files():
                logger.verbose(f"Processing {landscape_file}")
                with open(landscape_file, "r", encoding="utf-8-sig") as file_handle:
                    t_sysids, t_message_servers = _process_landscape_xml(file_handle)
                sysids.update({i: t_sysids[i] for i in t_sysids})
                message_servers.update(t_message_servers)
        else:
            if isinstance(landscape_file, str):
                file_handle = open(landscape_file, "r", encoding="utf-8-sig")
            elif isinstance(landscape_file, pathlib.Path):
                file_handle = landscape_file.open("r", encoding="utf-8-sig")
            else:
                file_handle = landscape_file
            t_sysids, t_message_servers = _process_landscape_xml(file_handle)
            if file_handle != landscape_file:
                file_handle.close()
            sysids.update({i: t_sysids[i] for i in t_sysids})
            message_servers.update(t_message_servers)
        for sysid in sysids:
            if sysids[sysid].get("msid"):
                sysids[sysid].update(message_servers[sysids[sysid].pop("msid")])
                sysids[sysid]["sysid"] = sysid
            logger.trace(f"Landscape Entry {sysid}: {sysids[sysid]}")
            self._data[sysid] = sysids[sysid]

    def __getitem__(self, item):
        return self._data[item.upper()]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)

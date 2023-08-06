# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import json
import sys as sstm
from array import array as py_array_t
from datetime import date as date_t
from datetime import datetime as date_time_t
from datetime import time as time_t
from datetime import timedelta as time_delta_t
from datetime import timezone as time_zone_t
from enum import Enum as enum_t
from io import BytesIO as io_bytes_t
from pathlib import Path as path_t
from typing import Any, Callable, Dict, GenericAlias, Optional, Tuple, Union
from uuid import UUID as uuid_t

try:
    import matplotlib.pyplot as pypl
except ModuleNotFoundError:
    pypl = None
try:
    import networkx as grph
except ModuleNotFoundError:
    grph = None
try:
    import numpy as nmpy
except ModuleNotFoundError:
    nmpy = None
if nmpy is None:
    blsc = None
    pcst = None
    sprs = None
else:
    try:
        import blosc as blsc
    except ModuleNotFoundError:
        blsc = None
    try:
        import pca_b_stream as pcst
    except ModuleNotFoundError:
        pcst = None
    try:
        import scipy.sparse as sprs
    except ModuleNotFoundError:
        sprs = None


builders_h = Dict[str, Callable[[Union[str, dict]], Any]]
description_h = Tuple[str, Any]
object_h = Any
# /!\ When a module is not found, using bytes, the first type tested while JSONing, as the main module type is a safe
# way to "disable" it.
if pypl is None:
    figure_t = bytes
else:
    figure_t = pypl.Figure
if grph is None:
    graph_t = bytes
else:
    graph_t = grph.Graph
if nmpy is None:
    array_t = bytes
else:
    array_t = nmpy.ndarray
if sprs is None:
    _SPARSE_ARRAY_CLASSES = bytes
else:
    _SPARSE_ARRAY_CLASSES = (
        sprs.bsr_array,
        sprs.coo_array,
        sprs.csc_array,
        sprs.csr_array,
        sprs.dia_array,
        sprs.dok_array,
        sprs.lil_array,
    )


_TYPES_SEPARATOR = "@"  # Must be a character forbidden in type names
_MODULE_SEPARATOR = ":"  # Must be a character forbidden in any (qualified) name
_ERROR_MARKER = "!"  # Must be a character forbidden in type names

_NUMPY_PLAIN_VERSION = "plain"
_NUMPY_COMPRESSED_VERSION = "compressed"
_BLOSC_VERSION = "blosc"
_BLOSC_HEX_VERSION = "blosc.hex"
_PCA_B_STREAM_VERSION = "pca_b_stream"
_NUMPY_NDARRAY_TO_VERSIONS = {}
_NUMPY_NDARRAY_FROM_VERSIONS = {}


def JsonStringOf(instance: Any, /, *, true_type: Union[Any, type] = None) -> str:
    """"""
    if not ((true_type is None) or (type(true_type) is type)):
        true_type = type(true_type)

    return json.dumps(_JsonDescriptionOf(instance, 0, true_type=true_type))


def _JsonDescriptionOf(
    instance: Any, calling_level: int, /, *, true_type: type = None
) -> description_h:
    """"""
    # Test for high-level classes first since they can also be subclasses of standard classes below, but only if not
    # called from the instance.AsJsonString method, which would create infinite recursion.
    if (calling_level > 0) and hasattr(instance, "AsJsonString"):
        return _JsonDescriptionOf(
            instance.AsJsonString(),
            calling_level + 1,
            true_type=_AutomaticTrueType(instance, true_type),
        )

    if dtcl.is_dataclass(instance):
        # Do not use dtcl.asdict(self) since it recurses into dataclass instances which, if they extend a "container"
        # class like list or dict, will lose the contents.
        as_dict = {
            _fld.name: getattr(instance, _fld.name) for _fld in dtcl.fields(instance)
        }
        true_type = _AutomaticTrueType(instance, true_type)

        return _JsonDescriptionOf(as_dict, calling_level + 1, true_type=true_type)

    instance_type = _DeAliasedType(instance)
    error = ""

    # /!\ Must be the first type to be tested (see unfoundable modules above)
    if issubclass(instance_type, (bytes, bytearray)):
        # bytes.decode could be used instead of bytes.hex. But which string encoding to use? Apparently, "iso-8859-1" is
        # the appropriate, dummy pass-through codec. To be tested one day...
        base_type, jsonable = instance_type.__name__, instance.hex()
    # Check datetime before date since a datetime is also a date
    elif issubclass(instance_type, date_time_t):
        base_type = "datetime_datetime"
        jsonable = _JsonDescriptionOf(
            (instance.date(), instance.timetz()), calling_level + 1
        )
    elif issubclass(instance_type, date_t):
        base_type = "datetime_date"
        jsonable = (instance.year, instance.month, instance.day)
    elif issubclass(instance_type, time_t):
        base_type = "datetime_time"
        jsonable = (
            instance.hour,
            instance.minute,
            instance.second,
            instance.microsecond,
            _JsonDescriptionOf(instance.tzinfo, calling_level + 1),
            instance.fold,
        )
    elif issubclass(instance_type, time_delta_t):
        base_type = "datetime_timedelta"
        jsonable = (instance.days, instance.seconds, instance.microseconds)
    elif issubclass(instance_type, time_zone_t):
        base_type = "datetime_timezone"
        jsonable = _JsonDescriptionOf(
            (instance.utcoffset(None), instance.tzname(None)), calling_level + 1
        )
    elif issubclass(instance_type, enum_t):
        # true_type = _AutomaticTrueType(instance, true_type)
        base_type = f"enum_Enum_{instance_type.__name__}"
        jsonable = _JsonDescriptionOf(instance.value, calling_level + 1)
    elif issubclass(instance_type, py_array_t):
        base_type, jsonable = "array_array", (instance.tolist(), instance.typecode)
    elif issubclass(instance_type, slice):
        base_type, jsonable = "slice", (instance.start, instance.stop, instance.step)
    # Check before looking for tuples since named tuples are subclasses of... tuples
    elif _IsNamedTuple(instance):
        # true_type = _AutomaticTrueType(instance, true_type)
        base_type = f"typing_NamedTuple_{instance_type.__name__}"
        jsonable = _JsonDescriptionOf(tuple(instance), calling_level + 1)
    elif issubclass(instance_type, (frozenset, list, set, tuple)):
        base_type = instance_type.__name__
        jsonable = [_JsonDescriptionOf(_elm, calling_level + 1) for _elm in instance]
    elif issubclass(instance_type, dict):
        # json does not accept non-str dictionary keys, hence the json.dumps
        base_type = "dict"
        jsonable = {
            json.dumps(_JsonDescriptionOf(_key, calling_level + 1)): _JsonDescriptionOf(
                _vle, calling_level + 1
            )
            for _key, _vle in instance.items()
        }
    elif issubclass(instance_type, path_t):
        base_type, jsonable = "pathlib_Path", str(instance)
    elif issubclass(instance_type, io_bytes_t):
        # Buffer is assumed to be open (i.e. no instance.closed check)
        base_type, jsonable = "io_BytesIO", instance.getvalue().hex()
    elif issubclass(instance_type, uuid_t):
        base_type, jsonable = "uuid_UUID", instance.hex
    elif issubclass(instance_type, array_t):
        base_type, jsonable = "numpy_ndarray", _AsMostConcise(instance)
    elif issubclass(instance_type, _SPARSE_ARRAY_CLASSES):
        base_type, jsonable = f"scipy_{instance_type.__name__}", _AsMostConcise(
            instance.toarray()
        )
    elif issubclass(instance_type, graph_t):
        edges = grph.to_dict_of_dicts(instance)
        # /!\ Node attributes are added to the edges dictionary! This must be taken into account when deJSONing. Note
        # that several attempts to avoid this have been made, including one relying on repr(node), which is based on
        # hash(node). Since the hash function gives different results across Python sessions, this could not work.
        for node, attributes in instance.nodes(data=True):
            edges[node] = (attributes, edges[node])
        base_type = f"networkx_{instance_type.__name__}"
        jsonable = _JsonDescriptionOf(edges, calling_level + 1)
    elif issubclass(instance_type, figure_t):
        fake_file = io_bytes_t()
        instance.canvas.draw()
        instance.savefig(
            fake_file,
            bbox_inches="tight",
            pad_inches=0.0,
            transparent=True,
            dpi=200.0,
            format="png",
        )
        base_type = "matplotlib_pyplot_Figure"
        jsonable = fake_file.getvalue().hex()
        fake_file.close()
    else:
        base_type = instance_type.__name__
        try:
            _ = json.dumps(instance)
            jsonable = instance
        except TypeError:
            jsonable = None
            error = _ERROR_MARKER
            print(f"{base_type}: UnJSONable type. Using None.")

    if true_type is None:
        true_type = ""
    else:
        true_type = true_type.__name__
    types = f"{instance_type.__module__}{_MODULE_SEPARATOR}{base_type}{_TYPES_SEPARATOR}{true_type}{error}"

    return types, jsonable


def ObjectFromJsonString(jsoned: str, /, *, builders: builders_h = None) -> object_h:
    """"""
    return _ObjectFromJsonDescription(json.loads(jsoned), builders=builders)


def _ObjectFromJsonDescription(
    description: description_h,
    /,
    *,
    builders: builders_h = None,
) -> object_h:
    """"""
    types, instance = description
    base_type, true_type = types.split(_TYPES_SEPARATOR, maxsplit=1)
    type_module, base_type = base_type.split(_MODULE_SEPARATOR, maxsplit=1)

    if true_type.endswith(_ERROR_MARKER):
        print(
            f"{base_type}{_TYPES_SEPARATOR}{true_type[: -_ERROR_MARKER.__len__()]}: "
            f"UnJSONable type. Returning None."
        )
        return None

    if true_type.__len__() == 0:
        true_type = None

    if builders is None:
        builders = {}

    if base_type in ("bytes", "bytearray"):
        if base_type == "bytes":
            output = bytes.fromhex(instance)
        else:
            output = bytearray.fromhex(instance)
    elif base_type == "datetime_datetime":
        date, time = _ObjectFromJsonDescription(instance)
        output = date_time_t(
            date.year,
            date.month,
            date.day,
            time.hour,
            time.minute,
            time.second,
            time.microsecond,
            time.tzinfo,
            fold=time.fold,
        )
    elif base_type == "datetime_date":
        output = date_t(*instance)
    elif base_type == "datetime_time":
        output = time_t(**_TimeDictionaryFromDescription(instance))
    elif base_type == "datetime_timedelta":
        output = time_delta_t(*instance)
    elif base_type == "datetime_timezone":
        time_delta, name = _ObjectFromJsonDescription(instance)
        output = time_zone_t(time_delta, name=name)
    elif base_type.startswith("enum_Enum_"):
        enum_type = base_type[10:]
        module = sstm.modules[type_module]
        enum_e = getattr(module, enum_type)
        output = enum_e(_ObjectFromJsonDescription(instance))
        # output = _ObjectFromJsonDescription(instance, builders=builders)
    elif base_type == "array_array":
        as_list, typecode = instance
        output = py_array_t(typecode)
        output.fromlist(as_list)
    elif base_type == "slice":
        output = slice(*instance)
    elif base_type.startswith("typing_NamedTuple_"):
        named_tuple = base_type[18:]
        module = sstm.modules[type_module]
        named_tuple_t = getattr(module, named_tuple)
        output = named_tuple_t._make(_ObjectFromJsonDescription(instance))
        # output = _ObjectFromJsonDescription(instance, builders=builders)
    elif base_type in ("frozenset", "list", "set", "tuple"):
        iterator = (
            _ObjectFromJsonDescription(_elm, builders=builders) for _elm in instance
        )
        if base_type == "frozenset":
            output = frozenset(iterator)
        elif base_type == "list":
            output = list(iterator)
        elif base_type == "set":
            output = set(iterator)
        else:
            output = tuple(iterator)
    elif base_type == "dict":
        output = {
            _ObjectFromJsonDescription(
                json.loads(_key), builders=builders
            ): _ObjectFromJsonDescription(_vle, builders=builders)
            for _key, _vle in instance.items()
        }
    elif base_type == "pathlib_Path":
        output = path_t(instance)
    elif base_type == "io_BytesIO":
        output = io_bytes_t(bytes.fromhex(instance))
    elif base_type == "uuid_UUID":
        output = uuid_t(hex=instance)
    elif base_type == "numpy_ndarray":
        output = _AsArray(*instance)
    elif base_type.startswith("scipy_"):
        sparse_type = base_type[6:]
        sparse_type_t = getattr(sprs, sparse_type)
        output = sparse_type_t(_AsArray(*instance))
    elif base_type.startswith("networkx_"):
        graph_type = base_type[9:]
        graph_type_t = getattr(grph, graph_type)

        edges_w_attributes = _ObjectFromJsonDescription(instance, builders=builders)
        attributes = {}
        edges = {}
        for node, (node_attributes, edge) in edges_w_attributes.items():
            attributes[node] = node_attributes
            edges[node] = edge

        output = grph.from_dict_of_dicts(edges, create_using=graph_type_t)
        grph.set_node_attributes(output, attributes)
    elif base_type == "matplotlib_pyplot_Figure":
        fake_file = io_bytes_t(bytes.fromhex(instance))
        image = pypl.imread(fake_file)
        fake_file.close()
        output, axes = pypl.subplots()
        axes.set_axis_off()
        axes.matshow(image)
    else:
        output = instance

    if true_type in builders:
        output = builders[true_type](output)
    elif true_type is not None:
        output = None
        print(f"{true_type}: Type without builder. Returning None.")

    return output


def _DeAliasedType(instance: Any, /) -> type:
    """"""
    if isinstance(instance, GenericAlias):
        return type(instance).__origin__

    return type(instance)


def _IsNamedTuple(instance: Any, /) -> bool:
    """"""
    instance_type = _DeAliasedType(instance)
    if hasattr(instance_type, "_make"):
        try:
            as_tuple = tuple(instance)
        except TypeError:
            return False

        return instance_type._make(as_tuple) == instance

    return False


def _AutomaticTrueType(instance: Any, true_type: Optional[type], /) -> type:
    """"""
    if true_type is None:
        return _DeAliasedType(instance)

    # This was added to support passing a true type of an object built from a subclass instance. Usage example:
    # decomposition of an instance of a class with multiple inheritance into its components built from the instance
    # itself.
    if issubclass(_DeAliasedType(instance), true_type):
        return true_type

    raise ValueError(
        f'{true_type.__name__}: Invalid true type specification for type "{type(instance).__name__}". Expected: None.'
    )


def _TimeDictionaryFromDescription(
    description: Tuple[int, int, int, int, description_h, float], /
) -> Dict[str, Any]:
    """"""
    time_zone = _ObjectFromJsonDescription(description[4])
    return dict(
        zip(
            ("hour", "minute", "second", "microsecond", "tzinfo", "fold"),
            (*description[:4], time_zone, *description[5:]),
        )
    )


def AddNumpyNDArrayRepresentation(
    name: str,
    /,
    *,
    ToVersion: Callable[[array_t], Tuple[int, str, str]] = None,
    FromVersion: Callable[[str], array_t] = None,
) -> None:
    """"""
    global _NUMPY_NDARRAY_TO_VERSIONS, _NUMPY_NDARRAY_FROM_VERSIONS

    if name in (_NUMPY_PLAIN_VERSION, _NUMPY_COMPRESSED_VERSION):
        raise ValueError(
            f"{_NUMPY_PLAIN_VERSION}, {_NUMPY_COMPRESSED_VERSION}: Reserved representation names"
        )

    if name == _BLOSC_VERSION:
        if blsc is None:
            raise ModuleNotFoundError('Module "blosc" not installed or unfoundable')
        _NUMPY_NDARRAY_TO_VERSIONS[_BLOSC_VERSION] = _BloscVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[_BLOSC_VERSION] = _FromBloscVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[_BLOSC_HEX_VERSION] = _FromBloscHexVersion
    elif name == _PCA_B_STREAM_VERSION:
        if pcst is None:
            raise ModuleNotFoundError(
                'Module "pca_b_stream" not installed or unfoundable'
            )
        _NUMPY_NDARRAY_TO_VERSIONS[_PCA_B_STREAM_VERSION] = _PCABStreamVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[_PCA_B_STREAM_VERSION] = _FromPCABStreamVersion
    else:
        if (ToVersion is None) or (FromVersion is None):
            raise ValueError(
                f'{name}: Invalid keyword-only arguments "ToVersion" and/or "FromVersion". '
                f"Actual={ToVersion}/{FromVersion}. Expected=Both non-None."
            )
        _NUMPY_NDARRAY_TO_VERSIONS[name] = ToVersion
        _NUMPY_NDARRAY_FROM_VERSIONS[name] = FromVersion


def RemoveNumpyNDArrayRepresentation(name: str, /) -> None:
    """"""
    global _NUMPY_NDARRAY_TO_VERSIONS, _NUMPY_NDARRAY_FROM_VERSIONS

    if name in (_NUMPY_PLAIN_VERSION, _NUMPY_COMPRESSED_VERSION):
        raise ValueError(
            f"{_NUMPY_PLAIN_VERSION}, {_NUMPY_COMPRESSED_VERSION}: Default representations cannot be removed"
        )

    del _NUMPY_NDARRAY_TO_VERSIONS[name]
    del _NUMPY_NDARRAY_FROM_VERSIONS[name]
    if name == _BLOSC_VERSION:
        del _NUMPY_NDARRAY_FROM_VERSIONS[_BLOSC_HEX_VERSION]


def _AsMostConcise(array: array_t, /) -> Tuple[str, str]:
    """"""
    # Is it worth implementing Numpy compressed version using io.BytesIO?
    # nmpy.savez_compressed(.npz, array=array)
    # nmpy.load(file)["array"]
    version = json.dumps((array.tolist(), array.dtype.name))
    min_length = version.__len__()

    output = (_NUMPY_PLAIN_VERSION, version)

    fake_file = io_bytes_t()
    nmpy.savez_compressed(fake_file, array=array)
    version = fake_file.getvalue().hex()
    fake_file.close()
    length = version.__len__()
    if length < min_length:
        output, min_length = (_NUMPY_COMPRESSED_VERSION, version), length

    for ToVersion in _NUMPY_NDARRAY_TO_VERSIONS.values():
        version = ToVersion(array)
        length = version[1].__len__()
        if length < min_length:
            output, min_length = version, length

    return output


def _AsArray(how: str, what: str) -> array_t:
    """"""
    if how == _NUMPY_PLAIN_VERSION:
        data, dtype = json.loads(what)
        return nmpy.array(data, dtype=dtype)
    elif how == _NUMPY_COMPRESSED_VERSION:
        fake_file = io_bytes_t(bytes.fromhex(what))
        output = nmpy.load(fake_file)["array"]
        fake_file.close()
        return output

    return _NUMPY_NDARRAY_FROM_VERSIONS[how](what)


def _BloscVersion(array: array_t, /) -> Tuple[str, str]:
    """"""
    # /!\ Do not compare packed instances of an array since blsc.pack_array(array) !=_{can be} blsc.pack_array(array)
    packed = blsc.pack_array(array)
    if isinstance(packed, bytes):
        packed = packed.hex()
        how = _BLOSC_HEX_VERSION
    else:
        how = _BLOSC_VERSION

    return how, packed


def _FromBloscVersion(blosc: str, /) -> array_t:
    """"""
    return blsc.unpack_array(blosc)


def _FromBloscHexVersion(blosc: str, /) -> array_t:
    """"""
    return blsc.unpack_array(bytes.fromhex(blosc))


def _PCABStreamVersion(array: array_t, /) -> Tuple[str, str]:
    """"""
    stream = pcst.PCA2BStream(array).hex()
    return _PCA_B_STREAM_VERSION, stream


def _FromPCABStreamVersion(pca_b_stream: str, /) -> array_t:
    """"""
    return pcst.BStream2PCA(bytes.fromhex(pca_b_stream))

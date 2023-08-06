from __future__ import annotations

import sys
from abc import ABCMeta, abstractmethod, ABC
from collections import OrderedDict
from typing import Any, TypeVar, Tuple, Optional, Dict, Type, ForwardRef, _type_check, _eval_type, Protocol, Union, runtime_checkable, _ProtocolMeta, TYPE_CHECKING

from structlib.utils import classproperty
from structlib.abc_.packing import DataclassPackableABC
from structlib.errors import PrettyNotImplementedError
from structlib.protocols.packing import StructPackable, DClassType, DClass
from structlib.protocols.typedef import native_size_of, TypeDefAlignable, align_of, AttrProtocolMeta
from structlib.typedefs.array import AnyPackableTypeDef
from structlib.typedefs.structure import Struct

T = TypeVar("T")


@runtime_checkable
class TypeDefDataclass(Protocol):
    __typedef_dclass_struct_packable__: StructPackable
    __typedef_dclass_name2type_lookup__: Dict[str, AnyPackableTypeDef]
    __typedef_dclass_name_order__: Tuple[str, ...]

    @classmethod
    @abstractmethod
    def __typedef_dclass_redefine__(cls: T, annotations: Dict[str, Any]) -> T:
        raise PrettyNotImplementedError(cls, cls.__typedef_dclass_redefine__)

    @abstractmethod
    def __typedef_dclass2tuple__(self) -> Tuple[Any, ...]:
        raise PrettyNotImplementedError(self, self.__typedef_dclass2tuple__)

    @classmethod
    @abstractmethod
    def __typedef_tuple2dclass__(cls, *args: Any) -> T:
        raise PrettyNotImplementedError(cls, cls.__typedef_tuple2dclass__)


def eval_fwd_ref(self: ForwardRef, global_namespace, local_namespace, recursive_guard=frozenset()):
    if self.__forward_arg__ in recursive_guard:
        return self
    if not self.__forward_evaluated__ or local_namespace is not global_namespace:
        if global_namespace is None and local_namespace is None:
            global_namespace = local_namespace = {}
        elif global_namespace is None:
            global_namespace = local_namespace
        elif local_namespace is None:
            local_namespace = global_namespace
        if self.__forward_module__ is not None:
            global_namespace = getattr(
                sys.modules.get(self.__forward_module__, None), '__dict__', global_namespace
            )
        type_or_obj = eval(self.__forward_code__, global_namespace, local_namespace)
        try:
            type_ = _type_check(
                type_or_obj,
                "Forward references must evaluate to types.",
                is_argument=self.__forward_is_argument__,
            )
            self.__forward_value__ = _eval_type(
                type_, global_namespace, local_namespace, recursive_guard | {self.__forward_arg__}
            )
            self.__forward_evaluated__ = True
        except TypeError:
            self.__forward_value__ = type_or_obj  # should be object
            self.__forward_evaluated__ = True
    return self.__forward_value__


def resolve_annotations(raw_annotations: Dict[str, Type[Any]], module_name: Optional[str]) -> Dict[str, Type[Any]]:
    """
    Partially taken from typing.get_type_hints.
    Resolve string or ForwardRef annotations into types OR objects if possible.
    """
    base_globals: Optional[Dict[str, Any]] = None
    if module_name:
        try:
            module = sys.modules[module_name]
        except KeyError:
            # happens occasionally, see https://github.com/samuelcolvin/pydantic/issues/2363
            pass
        else:
            base_globals = module.__dict__

    annotations = {}
    for name, value in raw_annotations.items():
        if isinstance(value, str):
            if (3, 10) > sys.version_info >= (3, 9, 8) or sys.version_info >= (3, 10, 1):
                value = ForwardRef(value, is_argument=False, is_class=True)
            else:
                value = ForwardRef(value, is_argument=False)
            try:
                value = eval_fwd_ref(value, base_globals, None)
            except NameError:
                # this is ok, it can be fixed with update_forward_refs
                pass
        annotations[name] = value
    return annotations


class TypeDefDataclassMetaclass(AttrProtocolMeta, ABCMeta, type):
    if sys.version_info < (3, 5):  # 3.5 >= is ordered by design
        @classmethod
        def __prepare__(cls, name, bases):
            return OrderedDict()

    def dclass_align_as(cls: T, alignment: int) -> T:
        if cls.__typedef_alignment__ == alignment:
            return cls
        else:
            new_cls = type(cls.__name__, cls.__bases__, dict(cls.__dict__), alignment=alignment)
            return new_cls

    def dclass_redefine(cls: T, annotations: Dict) -> T:
        _dict = dict(cls.__dict__)
        _dict["__annotations__"] = annotations
        new_cls = type(cls.__name__, cls.__bases__, _dict, alignment=align_of(cls))
        return new_cls

    def dclass_str(self: TypeDefDataclass) -> str:
        names = self.__typedef_dclass_name_order__
        cls_name = self.__class__.__name__
        pairs = [f"{name}={getattr(self, name)}" for name in names]
        return f"{cls_name}({', '.join(pairs)})"

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: Dict[str, Any], alignment: int = None):
        if not bases:
            return super().__new__(mcs, name, bases, attrs)  # Abstract Base Class; AutoStruct

        if "__str__" not in attrs:
            attrs["__str__"] = mcs.dclass_str
        if "__repr__" not in attrs:
            attrs["__repr__"] = mcs.dclass_str

        attrs["__typedef_align_as__"] = classmethod(mcs.dclass_align_as)
        attrs["__typedef_alignment__"] = classproperty(lambda self: align_of(self.__typedef_dclass_struct_packable__))

        attrs["__typedef_dclass_redefine__"] = classmethod(mcs.dclass_redefine)
        type_hints = resolve_annotations(attrs.get("__annotations__", {}), attrs.get("__module__"))
        typed_attr = {name: typing for name, typing in type_hints.items()}
        ordered_attr = [name for name in type_hints.keys() if name in typed_attr]
        ordered_structs = [type_hints[attr] for attr in typed_attr]
        attrs["__typedef_dclass_struct_packable__"] = Struct(*ordered_structs, alignment=alignment)
        attrs["__typedef_dclass_name2type_lookup__"] = typed_attr
        attrs["__typedef_dclass_name_order__"] = tuple(ordered_attr)

        attrs["__typedef_native_size__"] = classproperty(lambda self: native_size_of(self.__typedef_dclass_struct_packable__))
        return super().__new__(mcs, name, bases, attrs)


def dclass2tuple(t: Union[Type[TypeDefDataclass], Any], v: Union[TypeDefDataclass, T]) -> Union[Tuple[Any, ...], T]:
    if isinstance(t, TypeDefDataclass):
        return v.__typedef_dclass2tuple__()
    else:
        return v


def tuple2dclass(t: Type[TypeDefDataclass], v: Union[Tuple[Any, ...], T]):
    if isinstance(t, TypeDefDataclass):
        return t.__typedef_tuple2dclass__(*v)
    else:
        return v


class TypeDefDataclassABC(DataclassPackableABC, TypeDefAlignable, TypeDefDataclass, metaclass=TypeDefDataclassMetaclass):
    def __typedef_align_as__(self: T, alignment: int) -> T:
        raise PrettyNotImplementedError(self, self.__typedef_align_as__)

    def __typedef_dclass2tuple__(self) -> Tuple[Any, ...]:
        names = self.__typedef_dclass_name_order__
        types = self.__typedef_dclass_name2type_lookup__
        attrs = [dclass2tuple(types[n], getattr(self, n)) for n in names]
        return tuple(attrs)

    @classmethod
    def __typedef_tuple2dclass__(cls, *args: Any) -> T:
        names = cls.__typedef_dclass_name_order__
        types = cls.__typedef_dclass_name2type_lookup__
        kwargs = {}
        for name, arg in zip(names, args):
            t = types[name]
            if isinstance(t, TypeDefDataclass):
                kwargs[name] = tuple2dclass(t, *arg)
            else:
                kwargs[name] = arg

        # TODO figure out a proper solution
        inst = cls.__new__(cls)
        for name, value in kwargs.items():
            setattr(inst, name, value)
        return inst

    def dclass_pack(self) -> bytes:
        args = dclass2tuple(self, self)
        packable: StructPackable = self.__typedef_dclass_struct_packable__
        return packable.struct_pack(*args)

    @classmethod
    def dclass_unpack(cls: DClassType, buffer: bytes) -> DClass:
        packable: StructPackable = cls.__typedef_dclass_struct_packable__
        args = packable.struct_unpack(buffer)
        return tuple2dclass(cls, args)


class TypeDefDataclassABC(DataclassPackableABC, TypeDefAlignable, TypeDefDataclass, metaclass=TypeDefDataclassMetaclass):
    @classmethod
    def __typedef_dclass_redefine__(cls, annotations_: Dict[str, Any]):
        raise PrettyNotImplementedError(cls, cls.__typedef_dclass_redefine__)

    @classmethod
    def __typedef_align_as__(self: T, alignment: int) -> T:
        raise PrettyNotImplementedError(self, self.__typedef_align_as__)

    def __typedef_dclass2tuple__(self) -> Tuple[Any, ...]:
        names = self.__typedef_dclass_name_order__
        types = self.__typedef_dclass_name2type_lookup__
        attrs = [dclass2tuple(types[n], getattr(self, n)) for n in names]
        return tuple(attrs)

    @classmethod
    def __typedef_tuple2dclass__(cls, *args: Any) -> T:
        names = cls.__typedef_dclass_name_order__
        types = cls.__typedef_dclass_name2type_lookup__
        kwargs = {}
        for name, arg in zip(names, args):
            t = types[name]
            if isinstance(t, TypeDefDataclass):
                kwargs[name] = tuple2dclass(t, *arg)
            else:
                kwargs[name] = arg

        # TODO figure out a proper solution
        inst = cls.__new__(cls)
        for name, value in kwargs.items():
            setattr(inst, name, value)
        return inst

    def dclass_pack(self) -> bytes:
        args = dclass2tuple(self, self)
        packable: StructPackable = self.__typedef_dclass_struct_packable__
        return packable.struct_pack(*args)

    @classmethod
    def dclass_unpack(cls: DClassType, buffer: bytes) -> DClass:
        packable: StructPackable = cls.__typedef_dclass_struct_packable__
        args = packable.struct_unpack(buffer)
        return tuple2dclass(cls, args)


class DataStruct(TypeDefDataclassABC):
    ...  # Implement any ABC's


def redefine_datastruct(datastruct: T, annotations_: Dict[str, Any]) -> T:
    if TYPE_CHECKING:
        datastruct: Type[TypeDefDataclass]
    return datastruct.__typedef_dclass_redefine__(annotations_)

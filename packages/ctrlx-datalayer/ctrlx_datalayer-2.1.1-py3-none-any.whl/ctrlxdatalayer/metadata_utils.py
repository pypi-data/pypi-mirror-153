"""
    This module provides helper classes to deal with metadata flatbuffers.
"""
from enum import IntEnum

import flatbuffers
from comm.datalayer import AllowedOperations, Metadata, NodeClass, Reference, Extension, DisplayFormat

from ctrlxdatalayer.variant import Variant


class ReferenceType():
    """ List of reference types as strings. """

    @classmethod
    def read(cls):
        """ Type when reading a value (absolute node address). """
        return "readType"

    @classmethod
    def read_in(cls):
        """ Input type when reading a value. """
        return "readInType"

    @classmethod
    def read_out(cls):
        """ Output type when reading a value. """
        return "readOutType"

    @classmethod
    def write(cls):
        """ Type when writing a value (absolute node address). Input/Output type are the same. """
        return "writeType"

    @classmethod
    def write_in(cls):
        """ Input type when writing a value. """
        return "writeInType"

    @classmethod
    def write_out(cls):
        """ Output type when writing a value. """
        return "writeOutType"

    @classmethod
    def create(cls):
        """ Type when creating a value (absolute node address). """
        return "createType"

    @classmethod
    def uses(cls):
        """ Referenced (list of) absolute node addresses. """
        return "uses"

    @classmethod
    def has_save(cls):
        """
        Reference to a save node address which needs to be called after
        node change to persist the new value (must be <technology>/admin/cfg/save).
        """
        return "hasSave"


class AllowedOperation(IntEnum):
    """
    Allowed Operation Flags
    """
    NONE = 0x00000
    READ = 0x00001
    WRITE = 0x00010
    CREATE = 0x00100
    DELETE = 0x01000
    BROWSE = 0x10000
    ALL = READ | WRITE | CREATE | DELETE | BROWSE


class MetadataBuilder():
    """ Builds a flatbuffer provided with the metadata information for a Data Layer node. """

    @staticmethod
    def create_metadata(
            name: str, description: str, unit: str, description_url: str,
            node_class: NodeClass,
            read_allowed: bool, write_allowed: bool,  create_allowed: bool,  delete_allowed: bool, browse_allowed: bool,
            type_path: str):
        """
            create metadata
        """
        builder = MetadataBuilder(allowed=AllowedOperation.NONE,
                                  description=description, description_url=description_url)
        allowed = AllowedOperation.NONE
        if read_allowed:
            allowed = allowed | AllowedOperation.READ
            if len(type_path) != 0:
                builder.add_reference(ReferenceType.read(), type_path)
        if write_allowed:
            allowed = allowed | AllowedOperation.WRITE
            if len(type_path) != 0:
                builder.add_reference(ReferenceType.write(), type_path)
        if create_allowed:
            allowed = allowed | AllowedOperation.CREATE
            if len(type_path) != 0:
                builder.add_reference(ReferenceType.create(), type_path)
        if delete_allowed:
            allowed = allowed | AllowedOperation.DELETE
        if browse_allowed:
            allowed = allowed | AllowedOperation.BROWSE

        builder.set_operations(allowed)
        builder.set_display_name(name)
        builder.set_node_class(node_class)
        builder.set_unit(unit)

        return builder.build()

    def __init__(self, allowed: AllowedOperation = AllowedOperation.BROWSE, description: str = "", description_url: str = ""):
        """
        generate MetadataBuilder
        """
        self.__name = ""
        self.__description = description
        self.__description_url = description_url
        self.__unit = ""
        self.__node_class = NodeClass.NodeClass.Node
        self.__allowed = AllowedOperation.ALL
        self.__displayformat = DisplayFormat.DisplayFormat.Auto
        self.set_operations(allowed)
        self.__references = dict([])
        self.__extensions = dict([])

    def build(self) -> Variant:
        """
        build function
        """
        builder = flatbuffers.Builder(1024)

        # Serialize AllowedOperations data
        operations = self.__buildoperations(builder)

        references = self.__buildreferences(builder)

        extensions = self.__buildextensions(builder)

        # Prepare strings
        description_builder_string = builder.CreateString(self.__description)
        url_builder_string = builder.CreateString(self.__description_url)
        name_builder_string = builder.CreateString(self.__name)
        unit_builder_string = builder.CreateString(self.__unit)

        # Serialize Metadata data
        Metadata.MetadataStart(builder)
        Metadata.MetadataAddNodeClass(builder, self.__node_class)
        Metadata.MetadataAddOperations(builder, operations)
        Metadata.MetadataAddDescription(builder, description_builder_string)
        Metadata.MetadataAddDescriptionUrl(builder, url_builder_string)
        Metadata.MetadataAddDisplayName(builder, name_builder_string)
        Metadata.MetadataAddUnit(builder, unit_builder_string)
        Metadata.MetadataAddDisplayFormat(builder, self.__displayformat)
        # Metadata reference table
        Metadata.MetadataAddReferences(builder, references)
        Metadata.MetadataAddExtensions(builder, extensions)
        metadata_internal = Metadata.MetadataEnd(builder)

        # Closing operation
        builder.Finish(metadata_internal)

        metadata = Variant()
        metadata.set_flatbuffers(builder.Output())
        return metadata

    def set_unit(self, unit: str):
        """
        set the unit
        """
        self.__unit = unit
        return self

    def set_display_name(self, name: str):
        """
        set the display name
        """
        self.__name = name
        return self

    def set_node_class(self, node_class: NodeClass):
        """
        set the node class
        """
        self.__node_class = node_class
        return self

    def set_operations(self, allowed: AllowedOperation = AllowedOperation.NONE):
        """
        set allowed operations
        """
        self.__allowed = allowed
        return self

    def set_displayFormat(self, f: DisplayFormat.DisplayFormat.Auto):
        """
        set display format
        """
        self.__displayformat = f
        return self

    def add_reference(self, t: ReferenceType, addr: str):
        """
        add reference
        """
        self.__references[t] = addr

    def add_extensions(self, key: str, val: str):
        """
        add extension
        """
        self.__extensions[key] = val

    def __is_allowed(self, allowed: AllowedOperation) -> bool:
        return (self.__allowed & allowed) == allowed

    def __buildoperations(self, builder: flatbuffers.Builder):
        AllowedOperations.AllowedOperationsStart(builder)
        AllowedOperations.AllowedOperationsAddRead(builder, self.__is_allowed(
                                                   AllowedOperation.READ))
        AllowedOperations.AllowedOperationsAddWrite(builder, self.__is_allowed(
            AllowedOperation.WRITE))
        AllowedOperations.AllowedOperationsAddCreate(builder, self.__is_allowed(
            AllowedOperation.CREATE))
        AllowedOperations.AllowedOperationsAddDelete(builder, self.__is_allowed(
            AllowedOperation.DELETE))
        AllowedOperations.AllowedOperationsAddBrowse(builder,  self.__is_allowed(
            AllowedOperation.BROWSE))
        return AllowedOperations.AllowedOperationsEnd(builder)

    def __add_reference(self, builder: flatbuffers.Builder, t: ReferenceType, addr: str):
        tbs = builder.CreateString(t)
        tabs = builder.CreateString(addr)
        Reference.ReferenceStart(builder)
        Reference.ReferenceAddType(builder, tbs)
        Reference.ReferenceAddTargetAddress(builder, tabs)
        return Reference.ReferenceEnd(builder)

    def __buildreferences(self, builder: flatbuffers.Builder):
        refs = []
        for key in sorted(self.__references):
            addr = self.__references[key]
            ref = self.__add_reference(builder, key, addr)
            refs.append(ref)

        Metadata.MetadataStartReferencesVector(builder, len(refs))
        for i in reversed(range(len(self.__references))):
            builder.PrependUOffsetTRelative(refs[i])
        return builder.EndVector(len(refs))

    def __add_extension(self, builder: flatbuffers.Builder, key: str, val: str):
        keybs = builder.CreateString(key)
        valbs = builder.CreateString(val)
        Extension.ExtensionStart(builder)
        Extension.ExtensionAddKey(builder, keybs)
        Extension.ExtensionAddValue(builder, valbs)
        return Extension.ExtensionEnd(builder)

    def __buildextensions(self, builder: flatbuffers.Builder):
        exts = []
        for key in sorted(self.__extensions):
            val = self.__extensions[key]
            ref = self.__add_extension(builder, key, val)
            exts.append(ref)

        Metadata.MetadataStartExtensionsVector(builder, len(exts))
        for i in reversed(range(len(self.__extensions))):
            builder.PrependUOffsetTRelative(exts[i])
        return builder.EndVector(len(exts))

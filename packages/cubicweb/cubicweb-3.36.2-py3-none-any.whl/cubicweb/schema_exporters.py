# copyright 2021 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.
"""some schema exporters"""

import json
import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

from cubicweb.schema import (
    CubicWebSchema,
    CubicWebEntitySchema,
    CubicWebRelationDefinitionSchema,
)


class SchemaExporter(ABC):
    """Used as base class for classes which exports the schema as a string."""

    @abstractmethod
    def export(self, schema: CubicWebSchema) -> str:
        raise NotImplementedError()


class JSONSchemaExporter(SchemaExporter):
    """Export schema as a json"""

    def _entity_to_json(self, entity: CubicWebEntitySchema):
        return {
            "type": entity.type,
            "description": entity.description,
            "final": entity.final,
        }

    def _relation_definition_to_json(self, rdef: CubicWebRelationDefinitionSchema):
        schema_json = {
            "type": rdef.relation_type.type,
            "description": rdef.description,
            "final": rdef.final,
            "subject": rdef.subject.type,
            "object": rdef.object.type,
            "cardinality": rdef.cardinality,
        }
        if hasattr(rdef, "default"):
            schema_json["default"] = rdef.default
        return schema_json

    def export_as_dict(self, schema: CubicWebSchema) -> dict:
        """
        Export the schema as a Python dict.
        """
        entities_json = [self._entity_to_json(entity) for entity in schema.entities()]
        rdefs_json = [
            self._relation_definition_to_json(rdef)
            for rel in schema.relations()
            for rdef in rel.relation_definitions.values()
        ]
        return {
            "entities": entities_json,
            "relations_definitions": rdefs_json,
        }

    def export(self, schema: CubicWebSchema) -> str:
        """
        Export the schema as a JSON dump.
        """
        return json.dumps(
            self.export_as_dict(schema),
            indent=2,
        )


class TypescriptSchemaExporter(SchemaExporter):
    """Export schema as a typescript interface"""

    def __init__(self, interface_name: str):
        super().__init__()
        self._name = interface_name

    def _named_export(self, schema):
        json_exporter = JSONSchemaExporter()
        return f"export interface {self._name} {json_exporter.export(schema)};"

    def _default_export(self, schema):
        json_exporter = JSONSchemaExporter()
        return (
            f"interface InstanceSchema {json_exporter.export(schema)};\n\n"
            "export default InstanceSchema;"
        )

    def _ts_module(self, schema):
        if self._name == "default":
            return self._default_export(schema)
        return self._named_export(schema)

    def export(self, schema: CubicWebSchema) -> str:
        generation_time = datetime.utcnow().isoformat()
        content = textwrap.wrap(
            "This file is generated. Manual modifications will be overwritten "
            "next time you run `cubicweb-ctl export-schema`.",
            width=80,
            initial_indent="// ",
            subsequent_indent="// ",
        )
        content.append(f"// Generated at: {generation_time}\n")
        content.append(self._ts_module(schema))
        return "\n".join(content)

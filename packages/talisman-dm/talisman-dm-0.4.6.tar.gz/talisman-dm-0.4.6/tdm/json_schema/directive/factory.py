from typing import TypeVar

from tdm.abstract.datamodel.directive import AbstractDirective, DirectiveType
from tdm.json_schema.directive import CreateConceptDirectiveModel
from tdm.json_schema.directive.abstract import AbstractDirectiveModel


_AbstractDirective = TypeVar('_AbstractDirective', bound=AbstractDirective)


_DIRECTIVE_MODELS = {
    DirectiveType.CREATE_CONCEPT: CreateConceptDirectiveModel
}


def build_directive_model(directive: _AbstractDirective) -> AbstractDirectiveModel:
    return _DIRECTIVE_MODELS[directive.directive_type].build(directive)

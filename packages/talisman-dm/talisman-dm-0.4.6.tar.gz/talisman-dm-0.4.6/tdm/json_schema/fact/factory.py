from tdm.abstract.datamodel import AbstractFact, AbstractTreeDocumentContent, FactType
from tdm.json_schema.fact.common import AbstractFactModel, SpanModel
from tdm.json_schema.fact.concept import ConceptFactModel
from tdm.json_schema.fact.property import PropertyFactModel
from tdm.json_schema.fact.relation import RelationFactModel
from tdm.json_schema.fact.value import ValueFactModel

_FACT_MODELS = {
    FactType.CONCEPT: ConceptFactModel,
    FactType.VALUE: ValueFactModel,
    FactType.PROPERTY: PropertyFactModel,
    FactType.RELATION: RelationFactModel
}


def build_fact_model(fact: AbstractFact, doc: AbstractTreeDocumentContent) -> AbstractFactModel:
    model_type = _FACT_MODELS[fact.fact_type]

    mention = tuple(SpanModel.build(span, doc) for span in fact.mention) if fact.mention is not None else None
    value = model_type.build_value(fact.value)
    return model_type.construct(id=fact.id, status=fact.status, type_id=fact.type_id, value=value, mention=mention,
                                metadata=fact.metadata)

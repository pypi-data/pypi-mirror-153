import json
import re
from pathlib import Path

import pytest
from dirty_equals import HasLen, IsPartialDict, IsStr, IsList
from pymultirole_plugins.v1.schema import Document, Annotation
from pyprocessors_afp_entities.afp_entities import (
    AFPEntitiesProcessor,
    AFPEntitiesParameters,
    ConsolidationType,
    group_annotations,
)


def test_model():
    model = AFPEntitiesProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AFPEntitiesParameters


# Arrange
@pytest.fixture
def original_doc():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


# Arrange
@pytest.fixture
def original_doc_en():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_en-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


def by_linking(a: Annotation):
    if a.terms:
        links = sorted({t.lexicon.split("_")[0] for t in a.terms})
        return "+".join(links)
    else:
        return "candidate"


def test_afp_entities_linker(original_doc):
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso, by_linking)
    assert len(conso_groups["candidate"]) == 8
    assert len(conso_groups["person"]) == 2
    persons = [r.value.dict() for r in conso_groups["person"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="Frank Garnier",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        IsPartialDict(
            label="AFPPerson",
            text="Werner Baumann",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        length=2,
    )
    assert len(conso_groups["wikidata"]) == 10
    assert len(conso_groups["location+wikidata"]) == 1
    assert len(conso_groups["organization+wikidata"]) == 2


def test_afp_entities_whitelist():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test-whitelist.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso, by_linking)
    assert len(conso_groups["candidate"]) == 7
    assert len(conso_groups["person"]) == 2
    persons = [r.value.dict() for r in conso_groups["person"].ranges()]
    assert persons == IsList(
        IsPartialDict(
            label="AFPPerson",
            text="reine Maxima",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        IsPartialDict(
            label="AFPPerson",
            text="Letizia",
            terms=IsList(
                IsPartialDict(identifier=IsStr(regex=r"^afpperson.*")), length=1
            ),
        ),
        length=2,
    )
    assert len(conso_groups["wikidata"]) == 1
    assert len(conso_groups["location"]) == 2


def test_afp_entities_linker_en(original_doc_en):
    # linker
    doc = original_doc_en.copy(deep=True)
    processor = AFPEntitiesProcessor()
    parameters = AFPEntitiesParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )

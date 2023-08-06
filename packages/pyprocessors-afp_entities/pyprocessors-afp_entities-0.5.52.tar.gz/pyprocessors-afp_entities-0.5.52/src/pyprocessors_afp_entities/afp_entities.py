import logging
from collections import defaultdict
from enum import Enum
from itertools import groupby, chain
from typing import Type, cast, List, Optional, Dict

from collections_extended import RangeMap, MappedRange
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation, AltText

logger = Logger("pymultirole")


class ConsolidationType(str, Enum):
    linker = "linker"
    unknown = "unknown"


class AFPEntitiesParameters(ProcessorParameters):
    type: ConsolidationType = Field(
        ConsolidationType.linker,
        description="""Type of consolidation, use<br />
    <li>**default** deduplicate and if overlap keeps only the longest match<br />
    <li>**linker** to retain only known entities<br />
    <li>**unknown** to retain all but prepending the `unknown_prefix` to the label of unknown entities<br />""",
    )
    kill_label: Optional[str] = Field("kill", description="Label name of the kill list")
    eurovoc_label: Optional[str] = Field(
        "eurovoc", description="Label name of the Eurovoc thesaurus"
    )
    as_altText: str = Field(
        "fingerprint",
        description="""If defined generate the fingerprint as an alternative text of the input document.""",
    )


class AFPEntitiesProcessor(ProcessorBase):
    """AFPEntities processor ."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: AFPEntitiesParameters = cast(AFPEntitiesParameters, parameters)
        for document in documents:
            with add_logging_context(docid=document.identifier):
                if document.annotations:
                    mark_whitelisted(document)
                    ann_groups = group_annotations(document, by_lexicon)
                    # 1. Compute document fingerprint
                    fingerprints = compute_fingerprint(ann_groups)
                    if params.as_altText is not None and len(params.as_altText):
                        document.altTexts = document.altTexts or []
                        altTexts = [
                            alt
                            for alt in document.altTexts
                            if alt.name != params.as_altText
                        ]
                        altTexts.append(
                            AltText(name=params.as_altText, text=" ".join(fingerprints))
                        )
                        document.altTexts = altTexts
                    # 2. Consolidate & links against KB and Wikidata
                    conso_anns = consolidate_and_link(ann_groups, params.kill_label)
                    document.annotations = conso_anns
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AFPEntitiesParameters


EUROVOC_NS = "http://eurovoc.europa.eu/"


def compute_fingerprint(ann_groups):
    def get_sort_key(r: MappedRange):
        return -r.start, r.stop - r.start

    fingerprints = []
    sorted_ann = sorted(
        chain(ann_groups["wikidata"].ranges(), ann_groups["eurovoc"].ranges()),
        key=get_sort_key,
        reverse=True,
    )
    for r in sorted_ann:
        ann = r.value
        if ann.terms and len(ann.terms):
            if ann.terms[0].lexicon == "wikidata":
                fingerprints.append(ann.terms[0].identifier)
                fingerprint = ann.terms[0].properties.get("fingerprint", None)
                if fingerprint:
                    props_vals = [
                        (p, v)
                        for p, v in [
                            pv.split(":", maxsplit=1) for pv in fingerprint.split(",")
                        ]
                    ]
                    ann.terms[0].properties["fingerprint"] = props_vals
                    try:
                        fingerprints.extend(
                            [v for p, v in props_vals if v.startswith("Q")]
                        )
                    except BaseException:
                        logging.exception()
            elif ann.terms[0].lexicon == "eurovoc" and ann.terms[
                0
            ].identifier.startswith(EUROVOC_NS):
                fingerprints.append("E" + ann.terms[0].identifier[len(EUROVOC_NS) :])
    return fingerprints


def mark_whitelisted(document):
    for a in document.annotations:
        if is_whitelist(
            a
        ):  # Consider whitelisted terms as entities coming from the model
            if a.label.startswith("AFP"):
                a.label = a.label[3:]
                a.labelName = a.labelName[3:]
                a.terms = None


def consolidate_and_link(ann_groups, kill_label):
    conso_anns = []
    for model_r in ann_groups[""].ranges():
        model_ann = model_r.value
        gname = model_ann.labelName

        kill_r = annotation_in_group(model_ann, ann_groups, kill_label)
        perfect, kill_match = one_match(model_ann, kill_r)
        if perfect and kill_match:
            logger.warning("Kill annotation")
            logger.warning(f"=> {model_ann}")
            continue

        kb_r = annotation_in_group(model_ann, ann_groups)
        perfect, kb_match = one_match(model_ann, kb_r)
        if kb_match:
            if perfect:
                model_ann.labelName = kb_match.labelName
                model_ann.label = kb_match.label
                model_ann.terms = model_ann.terms or []
                model_ann.terms.extend(kb_match.terms)
            else:
                logger.warning("Found larger annotation in KB")
                logger.warning(f"=> {model_ann}")
                logger.warning("and")
                logger.warning(f" -{kb_match}")
        elif kb_r and len(kb_r) > 1:
            logger.warning("Found overlapping annotations in KB")
            logger.warning(f"=> {model_ann}")
            logger.warning("and")
            for r in kb_r.values():
                logger.warning(f" -{r}")

        wiki_r = annotation_in_group(model_ann, ann_groups, "wikidata")
        perfect, wiki_match = one_match(model_ann, wiki_r)
        if wiki_match:
            if validate_wiki_type(wiki_match, gname):
                if perfect:
                    model_ann.terms = model_ann.terms or []
                    wiki_match.terms[0].properties.pop("fingerprint", None)
                    model_ann.terms.extend(wiki_match.terms)
                else:
                    logger.warning("Found larger annotation in Wikidata")
                    logger.warning(f"=> {model_ann}")
                    logger.warning("and")
                    logger.warning(f" -{wiki_match}")
        elif wiki_r and len(wiki_r) > 1:
            logger.warning("Found overlapping annotations in Wikidata")
            logger.warning(f"=> {model_ann}")
            logger.warning("and")
            for r in wiki_r.values():
                logger.warning(f" -{r}")
        conso_anns.append(model_ann)
    return conso_anns


def group_annotations(doc: Document, keyfunc):
    def get_sort_key(a: Annotation):
        return a.end - a.start, -a.start

    groups = defaultdict(RangeMap)
    for k, g in groupby(sorted(doc.annotations, key=keyfunc), keyfunc):
        sorted_group = sorted(g, key=get_sort_key, reverse=True)
        groups[k] = RangeMap((a.start, a.end, a) for a in sorted_group)
    return groups


def has_knowledge(a: Annotation):
    return a.terms is not None


def is_whitelist(a: Annotation):
    if has_knowledge(a):
        for term in a.terms:
            props = term.properties or {}
            status = props.get("status", "")
            if "w" in status.lower():
                return True
    return False


def by_lexicon(a: Annotation):
    if a.terms:
        lex = a.terms[0].lexicon.split("_")
        return lex[0]
    else:
        return ""


def by_label(a: Annotation):
    return a.labelName


def one_match(a: Annotation, matches: RangeMap):
    match = None
    perfect = False
    if matches and len(matches) == 1:
        match = matches.get(a.start) or matches.get(a.end)
        if match:
            perfect = a.start == match.start and a.end == match.end
    return perfect, match


# noqa: W503
def annotation_in_group(
    a: Annotation, ann_groups: Dict[str, RangeMap], gname: str = None
):
    gname = gname or a.labelName
    if (
        gname in ann_groups
        and a.start in ann_groups[gname]
        or a.end in ann_groups[gname]
    ):
        return ann_groups[gname][a.start : a.end]
    return None


# noqa: W503
def validate_wiki_type(w: Annotation, gname: str):
    match = None
    if w.terms and len(w.terms) and w.terms[0].properties:
        fingerprint = w.terms[0].properties.get("fingerprint", None)
        if fingerprint:
            if gname == "person":
                match = next(
                    filter(lambda pv: pv[0] == "P31" and pv[1] == "Q5", fingerprint),
                    None,
                )
            elif gname == "location":
                match = next(filter(lambda pv: pv[0] == "P1566", fingerprint), None)
            elif gname == "organization":
                match = next(
                    filter(
                        lambda pv: (pv[0] == "P452")
                        or (
                            pv[0] == "P31"
                            and pv[1]
                            in [
                                "Q6881511",
                                "Q4830453",
                                "Q891723",
                                "Q484652",
                                "Q43229",
                                "Q245065",
                                "Q7210356",
                                "Q2085381",
                                "Q11691",
                                "Q161726",
                                "Q484652",
                                "Q4120211",
                                "Q748720",
                                "Q11422536",
                                "Q29300714",
                                "Q15911314",
                                "Q17127659",
                                "Q1788992",
                                "Q327333",
                                "Q15991290",
                                "Q163740",
                                "Q4438121",
                                "Q1530022",
                                "Q20746389",
                                "Q48204",
                            ]
                        ),
                        fingerprint,
                    ),
                    None,
                )
    if not match:
        logger.warning(f"Wikidata annotation discarded as {gname}")
        logger.warning(f"=> {w}")
    return match

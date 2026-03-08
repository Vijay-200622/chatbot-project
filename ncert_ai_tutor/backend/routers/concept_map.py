"""Concept map API router."""

from fastapi import APIRouter

from backend.models.schemas import ConceptMapRequest, ConceptMapResponse
from backend.services.concept_map import generate_concept_map

router = APIRouter(prefix="/api/concept-map", tags=["Concept Map"])


@router.post("", response_model=ConceptMapResponse)
async def concept_map(request: ConceptMapRequest):
    """Generate a concept relationship map for a topic."""
    result = generate_concept_map(request.topic)
    return ConceptMapResponse(
        svg=result["svg"],
        edges=[list(edge) for edge in result["edges"]],
        dot_source=result["dot_source"],
    )

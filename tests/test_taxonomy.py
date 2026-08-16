"""1. Taxonomy schema: categories.yaml structure + profile merging."""

EXPECTED_CATEGORIES = {
    "decision-making", "investing-finance", "business-strategy",
    "psychology-behavior", "research-science", "learning-education",
    "writing", "communication-negotiation", "productivity",
    "leadership-management", "technology-engineering", "creativity-design",
    "philosophy-thinking", "health-performance", "reference-knowledge",
    "other",
}


def test_categories_yaml_structure(taxonomy):
    assert taxonomy.validate() == []
    assert set(taxonomy.category_ids()) == EXPECTED_CATEGORIES


def test_every_category_has_a_distillation_profile(taxonomy):
    for cid in taxonomy.category_ids():
        profile = taxonomy.profile(cid)
        assert profile["focus"], f"{cid}: empty focus"
        assert profile["skill_sections"], f"{cid}: no skill sections"
        # base sections must survive unless explicitly overridden
        if not profile["skill_sections_override"]:
            base = taxonomy.base["skill_sections"]
            assert all(s in profile["skill_sections"] for s in base)


def test_profiles_differ_across_categories(taxonomy):
    """Classification must change the distillation strategy."""
    dm = taxonomy.profile("decision-making")
    inv = taxonomy.profile("investing-finance")
    assert dm["focus"] != inv["focus"]


def test_invalid_category_raises(taxonomy):
    import pytest
    from book_to_agent_skill.taxonomy import TaxonomyError

    with pytest.raises(TaxonomyError):
        taxonomy.get("not-a-category")
    with pytest.raises(TaxonomyError):
        taxonomy.profile("not-a-category")


def test_eval_minimums(taxonomy):
    m = taxonomy.eval_minimums()
    assert m["positive_trigger"] == 5
    assert m["negative_trigger"] == 5
    assert m["application"] == 5
    assert m["edge_case"] == 3

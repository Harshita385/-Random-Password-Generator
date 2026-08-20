import pytest

from password_generator import (
    build_character_pool,
    classify_strength,
    generate_password,
    validate_inputs,
)


@pytest.mark.parametrize(
    "length, selected_types, expected",
    [
        (7, ["uppercase", "lowercase"], "Length must be at least 8 characters."),
        (10, [], "Select at least 2 character types."),
        (10, ["uppercase"], "Select at least 2 character types."),
    ],
)
def test_validate_inputs_rejects_invalid_values(length, selected_types, expected):
    result = validate_inputs(length, selected_types)
    assert result == expected


def test_generate_password_requires_each_selected_type():
    password = generate_password(12, ["uppercase", "lowercase", "numbers", "symbols"])
    assert len(password) == 12
    assert any(ch.isupper() for ch in password)
    assert any(ch.islower() for ch in password)
    assert any(ch.isdigit() for ch in password)
    assert any(not ch.isalnum() for ch in password)


def test_generate_password_can_exclude_ambiguous_characters():
    password = generate_password(
        14,
        ["uppercase", "lowercase", "numbers"],
        exclude_ambiguous=True,
    )
    ambiguous = set("0O1l")
    assert not any(ch in ambiguous for ch in password)


def test_strength_rating_is_consistent():
    assert classify_strength(12, ["uppercase", "lowercase", "numbers", "symbols"]) == "Strong"
    assert classify_strength(10, ["uppercase", "lowercase"]) == "Medium"
    assert classify_strength(8, ["uppercase", "lowercase"]) == "Weak"


def test_build_character_pool_omits_ambiguous_chars():
    pool = build_character_pool(["uppercase", "lowercase", "numbers"], exclude_ambiguous=True)
    assert "O" not in pool["uppercase"]
    assert "l" not in pool["lowercase"]
    assert "0" not in pool["numbers"]

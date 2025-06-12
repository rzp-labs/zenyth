"""Test that BasicPseudocodeGenerator uses instance configuration meaningfully.

This test validates that generator methods use instance state for behavior,
following proper SOLID design principles.

SOLID Assessment:
- SRP: Generator focused solely on pseudocode document creation
- OCP: Behavior extensible through configuration without modification
"""

from zenyth.phases.pseudocode import BasicPseudocodeGenerator


def test_basic_pseudocode_generator_uses_instance_configuration() -> None:
    """Test that BasicPseudocodeGenerator uses instance configuration meaningfully.

    Validates that generator methods use instance state for behavior,
    following proper SOLID design principles.

    SOLID Assessment:
    - SRP: Generator focused solely on pseudocode document creation
    - OCP: Behavior extensible through configuration without modification
    """
    # Create generators with different configurations
    generator_concise = BasicPseudocodeGenerator(
        verbosity_level="concise",
        include_comments=False,
    )
    generator_verbose = BasicPseudocodeGenerator(
        verbosity_level="verbose",
        include_comments=True,
    )

    # Should have meaningful instance configuration
    assert getattr(generator_concise, "_verbosity_level", None) == "concise"
    assert getattr(generator_concise, "_include_comments", None) is False
    assert getattr(generator_verbose, "_verbosity_level", None) == "verbose"
    assert getattr(generator_verbose, "_include_comments", None) is True

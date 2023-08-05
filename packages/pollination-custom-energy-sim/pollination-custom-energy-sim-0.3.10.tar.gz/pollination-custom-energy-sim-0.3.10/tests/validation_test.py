from pollination.custom_energy_sim.entry import CustomEnergySimEntryPoint
from queenbee.recipe.dag import DAG


def test_annual_energy_use():
    recipe = CustomEnergySimEntryPoint().queenbee
    assert recipe.name == 'custom-energy-sim-entry-point'
    assert isinstance(recipe, DAG)

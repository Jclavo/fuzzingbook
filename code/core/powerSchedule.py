import numpy as np

class PowerSchedule(object):    
    def assignEnergy(self, population):
        """Assigns each seed the same energy"""
        for seed in population:
            seed.energy = 1

    def normalizedEnergy(self, population):
        """Normalize energy"""
        energy = list(map(lambda seed: seed.energy, population))
        sum_energy = sum(energy)  # Add up all values in energy
        norm_energy = list(map(lambda nrg: nrg/sum_energy, energy))
        return norm_energy

    def choose(self, population):
        """Choose weighted by normalized energy."""
        import numpy as np

        self.assignEnergy(population)
        norm_energy = self.normalizedEnergy(population)
        seed = np.random.choice(population, p=norm_energy)
        return seed
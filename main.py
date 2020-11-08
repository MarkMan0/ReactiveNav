from Simulation import Simulation

if __name__ == '__main__':
    sim = Simulation("resources/Scenario_1.yaml")
    sim.setup()
    while sim.running:
        sim.tick()


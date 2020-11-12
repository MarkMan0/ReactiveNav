from Simulation import Simulation
import time


def main():
    sim = Simulation("resources/Scenario_1.yaml", True)
    sim.setup()
    cnt = 0
    while sim.running:
        sim.tick()
        cnt += 1
        sim.camera.get_cam_view()
    sim.cleanup()
    print(f"Goal reached: {sim.result}, score: {cnt}")


if __name__ == '__main__':
    main()

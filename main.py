from Simulation import Simulation

if __name__ == '__main__':
    sim = Simulation("resources/Scenario_1.yaml")
    sim.setup()
    cnt = 0
    while sim.running:
        sim.tick()
        cnt += 1
        sim.camera.get_cam_view()
    print(f"Goal reached: {sim.result}, score: {cnt}")

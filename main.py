from Simulation import Simulation
import time
import neat
import visualize
import pickle
import numpy as np


def check_camera(image: np.array) -> tuple:
    sz_x, sz_y = image.shape
    """
    _________________________
    |   1   |   2   |   3   |
    _________________________
    |   4   |   5   |   6   |
    _________________________
    |   7   |   8   |   9   |
    _________________________
    """
    x_div = (0, int(sz_x*1/3), int(sz_x*2/3), sz_x)
    y_div = (0, int(sz_y*1/3), int(sz_y*2/3), sz_y)
    ret = ()
    for i in range(1, 4):
        for j in range(1, 4):
            if np.any(image[x_div[j-1]:x_div[j], y_div[i-1]:y_div[i]] > 1000):
                ret += (1,)
            else:
                ret += (0,)
    return ret


def do_sim(path: str, net: neat.nn.FeedForwardNetwork, draw: bool = False) -> tuple:
    """Simulates a given scenario"""
    sim = Simulation(path, drawing=draw)
    sim.setup()
    cnt = 0
    sim.tick()
    min_dist = sim.get_dist_to_goal()
    cnt_th = 2000
    while sim.running and cnt < cnt_th:
        cam = sim.camera.get_cam_arr()
        in1 = check_camera(cam)
        dist = sim.get_dist_to_goal()
        min_dist = min(min_dist, dist)
        net_in = (dist, sim.get_direction_to_target()/180) + in1  # 1652
        res = net.activate(net_in)
        sim.set_car_ang_spd(3*res[0])
        cnt += 1
        sim.tick()
    sim.cleanup()
    timeout = False
    if cnt >= cnt_th:
        timeout = True
    return cnt, timeout, sim.result, sim.get_dist_to_goal(), min_dist


def eval_genome(genome, config) -> float:
    """Fitness function for 1 genome"""
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    cnt, timeout, reached, dist, min_dist = do_sim("resources/Scenario_1.yaml", net, False)
    fit = 0
    if timeout:
        fit -= 100000
    if reached:
        fit += 2000 - 20*dist - 10*min_dist - cnt
    else:
        fit = -20*dist - 10*min_dist + cnt
    print(fit)
    return fit


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def evolve_net():
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "resources/net_config.ini")

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5, filename_prefix='checkpoints/checkpoint_'))

    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(12, eval_genome)
    winner = p.run(pe.evaluate, 10)
    save_tup = (winner, p)
    pickle.dump(save_tup, open("save.p", "wb"))

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    input("Press Enter to continue...")
    input("Press Enter to continue...")
    input("Press Enter to continue...")
    do_sim("resources/Scenario_1.yaml", winner_net, True)

    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


def main():
    sim = Simulation("resources/Scenario_1.yaml", drawing=True)
    sim.setup()
    cnt = 0
    sim.tick()
    while sim.running:
        cam = sim.camera.get_cam_arr()
        in1 = tuple(cam.reshape(1, -1)[0])  # 1650
        cnt += 1
        sim.tick()

    sim.cleanup()
    print(f"Goal reached: {sim.result}, score: {cnt}, dist_to_goal: {sim.get_dist_to_goal()}")


def from_file():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "resources/net_config.ini")
    winner, pop = pickle.load(open("save.p", "rb"))
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    do_sim("resources/Scenario_1.yaml", net, True)


if __name__ == '__main__':
    start = time.perf_counter()
    evolve_net()
    end = time.perf_counter()
    print(f"Took: {end-start}")

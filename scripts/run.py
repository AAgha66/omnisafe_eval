import clearml
from omnisafe.common.experiment_grid import ExperimentGrid
from omnisafe.utils.exp_grid_tools import train


def main(env: str, algo: str, seed: int):
    eg = ExperimentGrid(exp_name="Benchmark_Safety_Velocity")
    mujoco_envs = [env]

    eg.add("env_id", mujoco_envs)
    # Set the device.
    gpu_id = [0]

    eg.add("algo", algo)
    eg.add("logger_cfgs:use_wandb", [False])
    eg.add("logger_cfgs:use_tensorboard", [True])
    eg.add("train_cfgs:vector_env_nums", [1])
    eg.add("train_cfgs:torch_threads", [1])
    eg.add("algo_cfgs:steps_per_epoch", [5000])
    eg.add("train_cfgs:total_steps", [1000000])
    eg.add("seed", [seed])

    # total experiment num must can be divided by num_pool
    # meanwhile, users should decide this value according to their machine
    eg.run(train, num_pool=1, gpu_id=gpu_id)

    # just fill in the name of the parameter of which value you want to compare.
    # then you can specify the value of the parameter you want to compare,
    # or you can just specify how many values you want to compare in single graph at most,
    # and the function will automatically generate all possible combinations of the graph.
    # but the two mode can not be used at the same time.
    eg.analyze(parameter="env_id", values=None, compare_num=6, cost_limit=25)
    eg.render(num_episodes=1, render_mode="rgb_array", width=256, height=256)
    eg.evaluate(num_episodes=5)


if __name__ == "__main__":
    task = clearml.Task.init()
    task_logger = task.get_logger()
    task_params = task.get_parameters_as_dict(cast=True)
    d = task_params["internal"]
    print(d)
    main(
        seed=d["seed"],
        env=d["env"],
        algo=d["algo"],
    )

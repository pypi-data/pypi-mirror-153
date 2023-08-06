from omegaconf import OmegaConf

OmegaConf.register_new_resolver("mul", lambda x, y: x * y)

OmegaConf.register_new_resolver("int", lambda x: int(x))

OmegaConf.register_new_resolver("slurm", lambda x: f"_{x}" if x else "_interactive")

import os
import wandb
from pyresearchutils import logger
from pyresearchutils.seed import set_seed
from pyresearchutils.log_folder import generate_log_folder
from pyresearchutils.config_reader import ConfigReader
from pyresearchutils import constants


def initialized_log(project_name: str, config_reader: ConfigReader = None,
                    enable_wandb: bool = False):
    args = config_reader.get_user_arguments()

    os.makedirs(args.base_log_folder, exist_ok=True)
    run_log_dir = generate_log_folder(args.base_log_folder)

    logger.set_log_folder(run_log_dir)
    set_seed(args.seed)
    if config_reader is not None:
        config_reader.save_config(run_log_dir)
    logger.info(f"Log Folder Set to {run_log_dir}")
    if enable_wandb:
        wandb.init(project=project_name, dir=args.base_log_folder)  # Set WandB Folder to log folder
        wandb.config.update(config_reader.get_user_arguments())  # adds all of the arguments as config variables®
    if constants.FOUND_PYTORCH:
        from pyresearchutils.torch.working_device import get_working_device
        constants.DEVICE = get_working_device()
    return args, run_log_dir

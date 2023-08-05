from pathlib import Path
import shutil
import subprocess
import json
from pprint import pprint
from copy import deepcopy
from deepdiff import DeepDiff


def rerun_cmd(cmd, outfile, max_ntry=2, subdir_failures='failed_outputs', **run_kwargs):
    """
    rerun r0_to_dl1 process given by `cmd` as long as the exit code is 0 and number of try < max_ntry
    move the failed output file to subdir failed_outputs

    Parameters
    ----------
    cmd: str
    simtel_file: Path
    subdir_failures: str
    outfile: Path
        path to the cmd output file
    max_ntry: int
    run_kwargs: kwargs for subprocess.run

    Returns
    -------
    ntry: int
        number of tries actually run
    """
    outfile = Path(outfile)
    ret = -1
    ntry = 1
    while ret != 0 and ntry <= max_ntry:
        ret = subprocess.run(cmd, **run_kwargs).returncode
        if ret != 0:
            failed_jobs_subdir = outfile.parent.joinpath(subdir_failures)
            if outfile.exists():
                failed_jobs_subdir.mkdir(exist_ok=True)
                outfile_target = failed_jobs_subdir.joinpath(outfile.name)
                print(f"Move failed output file from {outfile} to {outfile_target}. try #{ntry}")
                shutil.move(outfile, outfile_target)

        ntry += 1
    return ntry-1



def dump_lstchain_std_config(filename='lstchain_config.json', allsky=False, overwrite=False):
    from lstchain.io.config import get_standard_config
    
    filename = Path(filename)

    if filename.exists() and not overwrite:
        raise FileExistsError(f"{filename} exists already")

    std_cfg = get_standard_config()
    cfg = deepcopy(std_cfg)

    cfg['LocalPeakWindowSum']['apply_integration_correction'] = True
    cfg['GlobalPeakWindowSum']['apply_integration_correction'] = True
    cfg['source_config']['EventSource']['allowed_tels'] = [1]
    cfg['random_forest_energy_regressor_args']['min_samples_leaf'] = 10
    cfg['random_forest_disp_regressor_args']['min_samples_leaf'] = 10
    cfg['random_forest_disp_classifier_args']['min_samples_leaf'] = 10
    cfg['random_forest_particle_classifier_args']['min_samples_leaf'] = 10
    cfg['random_forest_energy_regressor_args']['n_jobs'] = -1
    cfg['random_forest_disp_regressor_args']['n_jobs'] = -1
    cfg['random_forest_disp_classifier_args']['n_jobs'] = -1
    cfg['random_forest_particle_classifier_args']['n_jobs'] = -1
    if allsky:
        for rf_feature in ['energy_regression_features', 'disp_regression_features',
                           'disp_classification_features', 'particle_classification_features']:
            cfg[rf_feature] = std_cfg[rf_feature]
            if 'alt_tel' not in cfg[rf_feature]:
                cfg[rf_feature].append('alt_tel')
            if 'az_tel' not in cfg[rf_feature]:
                cfg[rf_feature].append('az_tel')

    extra_msg = "for AllSky prod" if allsky else ""
    print(f"Updating std lstchain config {extra_msg} with")
    diff = DeepDiff(std_cfg, cfg)
    pprint(diff)
    
    with open(filename, 'w') as file:
        json.dump(cfg, file, indent=4)
    print(f"\nModified lstchain config dumped in {filename}. Check full config thoroughly.")

import logging
import os
import shutil

from midas.util.runtime_config import RuntimeConfig

LOG = logging.getLogger("midas.cli")


def download_smart_nord(data_path, tmp_path, if_necessary, force):
    """Download and convert the Smart Nord dataset.

    The dataset is stored inside of gitlab and will be downloaded from
    there and converted afterwards.

    """
    import subprocess
    import tarfile

    LOG.info("Preparing Smart Nord datasets...")
    token = "fDaPqqSuMBhsXD8nQ_Nn"  # read only Gitlab token for midas_data

    # There is only one dataset
    config = RuntimeConfig().data["smart_nord"][0]
    if if_necessary and not config.get("load_on_start", False):
        return
    output_path = os.path.abspath(os.path.join(data_path, config["name"]))
    if os.path.exists(output_path):
        LOG.debug("Found existing datasets at %s.", output_path)
        if not force:
            return

    zip_path = os.path.join(
        tmp_path, "smart_nord_data", "HouseholdProfiles.tar.gz"
    )
    if not os.path.exists(zip_path):
        LOG.debug("Downloading dataset...")
        subprocess.check_output(
            [
                "git",
                "clone",
                f"https://midas:{token}@gitlab.com/midas-mosaik/"
                "midas-data.git",
                os.path.join(tmp_path, "smart_nord_data"),
            ]
        )
        LOG.debug("Download complete.")
    LOG.debug("Extracting...")
    with tarfile.open(zip_path, "r:gz") as tar_ref:
        tar_ref.extractall(tmp_path)
    LOG.debug("Extraction complete.")

    tmp_name = os.path.join(tmp_path, "HouseholdProfiles.hdf5")
    shutil.move(tmp_name, output_path)
    LOG.info("Successfully created database for Smart Nord datasets.")

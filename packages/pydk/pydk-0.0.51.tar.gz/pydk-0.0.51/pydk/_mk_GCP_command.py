import re
from ._flexible_multilevel_mkdir import _flexible_multilevel_mkdir

def _add_multithread_flag(command):
    return re.sub("gsutil", "gsutil -m", command)


def _mk_GCP_command(destination_path, bucket_path, command, multithreaded=True):

    """
    Create a gsutil cinnabd

    Parameters:
    -----------
    destination

    bucket_path

    Returns:
    --------
    gcp_command

    Notes:
    ------
    (1) It would be great to eventually replace this with a more streamlined API
        for performing gsutil-based commands from a python notebook interface.
    """

    _flexible_multilevel_mkdir(destination_path)
    gcp_command = "gsutil {} -r gs://{} {}".format(
        command, bucket_path, destination_path
    )
    if multithreaded:
        gcp_command = _add_multithread_flag(gcp_command)

    return gcp_command
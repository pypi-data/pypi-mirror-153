import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post287"
version_tuple = (0, 3, 0, 287)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post287")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post145"
data_version_tuple = (0, 3, 0, 145)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post145")
except ImportError:
    pass
data_git_hash = "f1c1500f126f6cdc5fa60c047bd46e9fd73ac1c7"
data_git_describe = "0.3.0-145-gf1c1500f"
data_git_msg = """\
commit f1c1500f126f6cdc5fa60c047bd46e9fd73ac1c7
Merge: c27b73db c081b107
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Mon May 30 07:41:49 2022 +0200

    Merge pull request #557 from Silabs-ArjanB/ArjanB_ae
    
    Documented Atomics extension

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn

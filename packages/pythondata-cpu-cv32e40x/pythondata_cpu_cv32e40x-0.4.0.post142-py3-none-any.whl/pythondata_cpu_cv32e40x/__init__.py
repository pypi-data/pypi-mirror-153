import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post142"
version_tuple = (0, 4, 0, 142)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post142")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post0"
data_version_tuple = (0, 4, 0, 0)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post0")
except ImportError:
    pass
data_git_hash = "df030b15727e5d3f7070bec9257bf6c539275244"
data_git_describe = "0.4.0-0-gdf030b15"
data_git_msg = """\
commit df030b15727e5d3f7070bec9257bf6c539275244
Merge: 728ef777 ca2cca8f
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Thu Jun 2 12:38:00 2022 +0200

    Merge pull request #564 from Silabs-ArjanB/ArjanB_dcsrt
    
    Fixed comment related to dcsr.mprven value

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

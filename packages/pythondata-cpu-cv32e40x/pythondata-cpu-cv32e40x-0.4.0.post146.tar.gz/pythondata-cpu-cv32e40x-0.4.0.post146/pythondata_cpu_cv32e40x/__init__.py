import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post146"
version_tuple = (0, 4, 0, 146)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post146")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post4"
data_version_tuple = (0, 4, 0, 4)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post4")
except ImportError:
    pass
data_git_hash = "ef6540683b9fcba91411368adeaafd16468f4f7d"
data_git_describe = "0.4.0-4-gef654068"
data_git_msg = """\
commit ef6540683b9fcba91411368adeaafd16468f4f7d
Merge: cbb63d0c 3a3d619f
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Fri Jun 3 11:26:17 2022 +0200

    Merge pull request #566 from Silabs-ArjanB/ArjanB_clicu1
    
    Unifying interrupt controllers; aligning cs registers syntax with cor…

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

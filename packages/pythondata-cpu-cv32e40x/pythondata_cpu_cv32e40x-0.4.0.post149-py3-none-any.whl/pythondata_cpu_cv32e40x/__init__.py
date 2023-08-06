import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post149"
version_tuple = (0, 4, 0, 149)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post149")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post7"
data_version_tuple = (0, 4, 0, 7)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post7")
except ImportError:
    pass
data_git_hash = "f45ed637d34d817e04a8be5612f9f4ce2dd6c396"
data_git_describe = "0.4.0-7-gf45ed637"
data_git_msg = """\
commit f45ed637d34d817e04a8be5612f9f4ce2dd6c396
Merge: ef654068 a7132365
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Fri Jun 3 13:19:44 2022 +0200

    Merge pull request #567 from silabs-oysteink/silabs-oysteink_mret-dbg-exc
    
    Fix for issue #558

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

def get_ptcu_code():
    from torch import __version__
    torch_version = "".join(__version__.split(".")[:2])
    cuda_version = __version__.split("+cu")[-1]
    return "pt" + torch_version + "cu" + cuda_version

def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, imp
    __file__ = pkg_resources.resource_filename(__name__, '__torchcontentareaext.cpython-39-x86_64-linux-gnu.so.' + get_ptcu_code())
    __loader__ = None; del __bootstrap__, __loader__
    imp.load_dynamic(__name__,__file__)
__bootstrap__()

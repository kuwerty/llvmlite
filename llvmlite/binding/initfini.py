from ctypes import c_uint, POINTER, c_char, c_int, create_string_buffer, cast

from llvmlite.binding import ffi

LP_c_char = POINTER(c_char)
LP_LP_c_char = POINTER(LP_c_char)

ffi.lib.LLVMPY_ParseCommandLineOptions.argtypes = (c_int, LP_LP_c_char)


def parse_options(argv):
    argc = len(argv)
    p = (LP_c_char*argc)()
    for i, arg in enumerate(argv):  # not sys.argv, but argv!!!
        enc_arg = arg.encode('utf-8')
        p[i] = create_string_buffer(enc_arg)

    na = cast(p, LP_LP_c_char)

    ffi.lib.LLVMPY_ParseCommandLineOptions(argc, na)

def initialize():
    """
    Initialize the LLVM core.
    """
    ffi.lib.LLVMPY_InitializeCore()


def initialize_all_targets():
    """
    Initialize all targets. Necessary before targets can be looked up
    via the :class:`Target` class.
    """
    ffi.lib.LLVMPY_InitializeAllTargetInfos()
    ffi.lib.LLVMPY_InitializeAllTargets()
    ffi.lib.LLVMPY_InitializeAllTargetMCs()


def initialize_all_asmprinters():
    """
    Initialize all code generators. Necessary before generating
    any assembly or machine code via the :meth:`TargetMachine.emit_object`
    and :meth:`TargetMachine.emit_assembly` methods.
    """
    ffi.lib.LLVMPY_InitializeAllAsmPrinters()


def initialize_native_target():
    """
    Initialize the native (host) target.  Necessary before doing any
    code generation.
    """
    ffi.lib.LLVMPY_InitializeNativeTarget()


def initialize_native_asmprinter():
    """
    Initialize the native ASM printer.
    """
    ffi.lib.LLVMPY_InitializeNativeAsmPrinter()


def initialize_native_asmparser():
    """
    Initialize the native ASM parser.
    """
    ffi.lib.LLVMPY_InitializeNativeAsmParser()


def shutdown():
    ffi.lib.LLVMPY_Shutdown()


# =============================================================================
# Set function FFI

ffi.lib.LLVMPY_GetVersionInfo.restype = c_uint


def _version_info():
    v = []
    x = ffi.lib.LLVMPY_GetVersionInfo()
    while x:
        v.append(x & 0xff)
        x >>= 8
    return tuple(reversed(v))


llvm_version_info = _version_info()

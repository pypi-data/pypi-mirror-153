from pylabview.LVrsrcontainer import VI

from contextlib import contextmanager, redirect_stderr

class _PyLabVIEWParseOptions:
    """pylabview expects an Options argument to be passed in
    to everything containing the configuration the user specified.
    Its not intended to be used directly as classes.
    """

    def __init__(self, file):
        self.file = file

    @property
    def verbose(self):
        return 0

    @property
    def print_map(self):
        return False

    @property
    def typedesc_list_limit(self):
        return 4095

    @property
    def array_data_limit(self):
        return (2**28) - 1

    @property
    def store_as_data_above(self):
        return 4095

    @property
    def store_as_data_above(self):
        return 4095

    @property
    def filebase(self):
        return os.path.splitext(os.path.basename(self.file))[0]

    @property
    def rsrc(self):
        return self.file

    @property
    def xml(self):
        return self.file

    @property
    def keep_names(self):
        return True

    @property
    def raw_connectors(self):
        return True

@contextmanager
def suppress_stderr():
    """A context manager that redirects stderr to devnull.
       pylabview outputs a lot of warnings to stderr. """
    with open(os.devnull, "w") as fnull:
        with redirect_stderr(fnull) as err:
            yield (err)


def get_vi(vi_path, parse_diagrams=True, parse_save_record=False):
    with open(vi_path, "rb") as rsrc_fh:
        parse_options = _PyLabVIEWParseOptions(vi_path)
        vi = VI(parse_options)
        # HACK: skipping part of the ctor here to avoid parsing all sections of the file
        # pylabview can't parse everything and over half our VIs throw while parsing sections
        # that we don't care about in most use cases, instead only parse when asked
        vi.dataSource = "rsrc"
        vi.rsrc_fh = rsrc_fh
        vi.src_fname = rsrc_fh.name
        vi.rsrc_map = []
        vi.readRSRCList(rsrc_fh)
        block_headers = vi.readRSRCBlockInfo(rsrc_fh)

        filtered_block_headers = []
        for header in block_headers:
            section_name = bytearray(header.ident).decode("ascii")
            if section_name == "vers":  # Version
                filtered_block_headers.append(header)
            if section_name == "LVSR" and parse_save_record:  # Save Record
                filtered_block_headers.append(header)
            if parse_diagrams:
                if "FPH" in section_name:  # Front panel
                    filtered_block_headers.append(header)
                elif "BDH" in section_name:  # Block Diagram
                    filtered_block_headers.append(header)
        if filtered_block_headers:
            vi.readRSRCBlockData(rsrc_fh, filtered_block_headers)
            vi.checkSanity()
        return vi



import os

KEY = 'System\CurrentControlSet\Control\Session Manager\Environment'

DISCARD_KEYWORDS = tuple([
   'awscli',
   'azure',
   'coverity',
   'dnvm',
   'mspec',
   'nunit',
   'odbc',
   'privateassemblies',
   'python27',
   'ruby193',
   'service fabric',
   'sql',
   'subversion',
   'testwindow',
   'xunit',
])

# TODOs:
# - Also get raw unexpanded values from registry to reduce length, and
#   merge them with the current PATH which AppVeyor has populated
# - also fetch and filter user env vars, also de-duplicate wrt system vars
#   (see https://github.com/reider-roque/pathvar)
# - Replace \\ and \.\ with \


def get_tidy_path(original):
    parts = []
    dups = set()
    discard_matches = set()

    for part in original.split(';'):
        # This will break directories with a trailing space
        part = part.strip().rstrip('\\')
        if part in parts:
            dups.add(part)
            continue

        part_lower = part.lower()
        for word in DISCARD_KEYWORDS:
            if word in part_lower:
                discard_matches.add(word)
                break
        else:
            parts.append(part)

    if dups:
        print('Discarded dups:\n  {}'.format('\n  '.join(sorted(dups))))

    if discard_matches:
        print('Discarded keyword matches: '
              '{}'.format(', '.join(sorted(discard_matches))))

    return ';'.join(parts)


def set_path_in_registry(value):
    try:
        import winreg
    except ImportError:
        import _winreg as winreg

    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    with winreg.OpenKey(reg, KEY, 0, winreg.KEY_ALL_ACCESS) as regkey:
        winreg.SetValueEx(regkey, 'Path', 0, winreg.REG_EXPAND_SZ, value)


if __name__ == '__main__':
    original = os.environ['PATH']
    value = get_tidy_path(original)
    print('PATH (len %d) set to:\n%s' % (len(value), value))
    set_path_in_registry(value)

from pkg_resources import VersionConflict

try:
    from cwtags import __pkginfo__
except ImportError:
    pass
else:
    if __pkginfo__.numversion < (1, 2, 3):
        raise VersionConflict(
            "This version ({}) of cwtags is incompatible with CubicWeb >= 3.32. "
            "Please, upgrade your version of cwtags to >= 1.2.3 before running "
            "this migration.".format(__pkginfo__.version)
        )

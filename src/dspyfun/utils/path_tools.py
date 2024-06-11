from pathlib import Path


def project_dir() -> Path:
    """Get the root for project directory."""
    return Path(__file__).parent.parent.parent.parent.absolute()


def src_dir() -> Path:
    return Path(__file__).parent.parent.absolute()


def subcommand_dir() -> Path:
    return Path(__file__).parent.parent / 'subcommands'


def config_dir() -> Path:
    """Get the root for project directory."""
    return project_dir() / 'config'


if __name__ == '__main__':
    print(subcommand_dir())

# print(Path(__file__).parent.parent.parent.parent)

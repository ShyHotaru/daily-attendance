import sys


def main() -> None:
    if "--run" in sys.argv:
        import runner
        runner.run()
    elif "--uninstall" in sys.argv:
        import uninstaller
        uninstaller.run()
    else:
        import installer
        installer.run()


if __name__ == "__main__":
    main()

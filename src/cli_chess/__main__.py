from cli_chess.core.main import MainModel, MainPresenter


def main() -> None:
    """Main entry point"""
    MainPresenter(MainModel()).run()


if __name__ == "__main__":
    main()

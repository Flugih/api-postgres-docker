from CLI import CommandLineInterface


def main():
    cli = CommandLineInterface()
    args = cli.parse_args()
    cli.execute_command(args)


if __name__ == '__main__':
    main()

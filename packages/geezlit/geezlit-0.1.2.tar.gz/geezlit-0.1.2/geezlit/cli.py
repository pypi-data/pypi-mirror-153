from .lit import geezlit


def main():
    import argparse

    parser = argparse.ArgumentParser("GeezLit")
    parser.add_argument("geez", type=str, help="Geez text to convert to latex encoding!")
    args = parser.parse_args()

    if args.geez:
        res = geezlit(args.geez)
        print(res)
    else:
        print("!! Provide text to convert with `-g` !!")


if "__main__" == __name__:
    main()

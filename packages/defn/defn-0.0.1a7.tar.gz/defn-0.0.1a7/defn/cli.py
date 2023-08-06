from defn.init import once


""" init must run before cdktf """


import typer


cli = typer.Typer()


@cli.command()
def synth():
    once()

    from cdktf import App

    from defn.stack.demo import DemoStack

    app = App()

    full_accounts = ["net", "log", "lib", "ops", "sec", "hub", "pub", "dev", "dmz"]
    env_accounts = ["net", "lib", "hub"]

    DemoStack(
        app,
        org="spiral",
        domain="defn.us",
        sso_region="us-west-2",
        accounts=full_accounts,
    )

    DemoStack(
        app,
        org="helix",
        domain="defn.sh",
        sso_region="us-east-2",
        accounts=full_accounts,
    )

    DemoStack(
        app,
        org="coil",
        domain="defn.us",
        sso_region="us-east-1",
        accounts=env_accounts,
    )

    DemoStack(
        app,
        org="curl",
        domain="defn.us",
        sso_region="us-west-2",
        accounts=env_accounts,
    )

    DemoStack(
        app, org="gyre", domain="defn.us", sso_region="us-east-2", accounts=["ops"]
    )

    app.synth()


@cli.command()
def version():
    import pkgutil

    print(pkgutil.get_data("defn", "VERSION").decode("utf-8").strip())  # type: ignore


def main():
    cli()


if __name__ == "__main__":
    main()

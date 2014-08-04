def upgrade_jrnl_if_necessary(config_path):
    with open(config_path) as f:
        config = f.read()
    if not config.strip().startswith("{"):
        return

    util.prompt("Welcome to jrnl {}".format(__version__))
    util.prompt("jrnl will now upgrade your configuration and journal files.")
    util.prompt("Please note that jrnl 1.x is NOT forward compatible with this version of jrnl.")
    util.prompt("If you choose to proceed, you will not be able to use your journals with")
    util.prompt("older versions of jrnl anymore.")
    cont = util.yesno("Continue upgrading jrnl?", default=False)
    if not cont:
        util.prompt("jrnl NOT upgraded, exiting.")
        sys.exit(1)

    util.prompt("")

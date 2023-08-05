from optparse import OptionParser


def get_options(args=None):
    parser = OptionParser()

    parser.add_option("-p", "--profile", dest='profile', default='default', help="profile selection")

    parser.add_option("--tests", action='store_true', dest='test', default=False, help="print logs to console")
    parser.add_option("--log", action='store_true', dest='log', help="print logs to console")

    (options, _) = parser.parse_args(args)

    return options
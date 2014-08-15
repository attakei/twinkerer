import sys
import argparse
import datetime


class DateStringAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        formats_ = [
            '%Y-%m-%d',
            '%Y/%m/%d',
        ]
        for format_ in formats_:
            try:
                dt_ = datetime.datetime.strptime(values, format_).date()
                setattr(namespace, self.dest, dt_)
                return
            except:
                continue
        parser.error('"%s" must be string to parse as datetime.' % self.dest)


class UnsignedIntegerAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value = int(values)
        if value > 0:
            setattr(namespace, self.dest, value)
            return
        else:
            parser.error('"%s" must be plus integer.' % self.dest)


def build_args(args):
    args.from_date = args.to_date - datetime.timedelta(days=(args.days - 1))
    args.from_datetime = datetime.datetime(
        args.from_date.year,
        args.from_date.month,
        args.from_date.day,
    )
    args.to_datetime = datetime.datetime(
        args.to_date.year,
        args.to_date.month,
        args.to_date.day,
    ) + datetime.timedelta(days=1)


def main(argv=None):
    """console script
    """
    if not argv:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--date', dest='to_date',
        action=DateStringAction,
        default=(datetime.date.today() - datetime.timedelta(days=1)),
    )
    parser.add_argument(
        '--days', dest='days',
        action=UnsignedIntegerAction,
        default=7,
    )

    args = parser.parse_args(argv)
    build_args(args)

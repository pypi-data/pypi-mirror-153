import asyncio
from argparse import ArgumentParser


def job_events(args):
    from levrt.core import events
    try:
        asyncio.run(events(args.user, args.job_id))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    parser = ArgumentParser("levrt")
    sub = parser.add_subparsers(title="Sub commands")
    events_parser = sub.add_parser("events", help="minitor job events")
    events_parser.add_argument("user", type=str)
    events_parser.add_argument("job_id", type=int)
    events_parser.set_defaults(func=job_events)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()

#!/usr/bin/env python3

import gather_stats

import argparse
import sys


class Config:
    def __init__(self):
        args = self.parse_args()
        self._cores = args.cores
        self.feature = args.feature

        if args.feature == 'gather':
            self.output = args.output

        elif args.feature == 'analyze':
            self.data_file = args.data_file

    @property
    def cores(self):
        if self._cores <= 0:
            return None
        return self._cores

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Gather statistics about system-related ELFs")

        parser.add_argument('--cores', '-j', default=1, type=int,
                            help=("Use N cores for processing. Defaults to "
                                  "1. 0 to use up all cores."))

        subparsers = parser.add_subparsers(help='Subcommands')

        # Gather stats
        parser_gather = subparsers.add_parser(
            'gather',
            help=('Gather system data into a file, to allow multiple '
                  'analyses without re-scanning the whole system.'))
        parser_gather.set_defaults(feature='gather')
        parser_gather.add_argument('--output', '-o',
                                   default='elf_data',
                                   help=('Output data to this file. Defaults '
                                         'to "elf_data"'))

        # Analyze stats
        parser_analyze = subparsers.add_parser(
            'analyze',
            help='Analyze data gathered by a previous run.')
        parser_analyze.set_defaults(feature='analyze')
        parser_analyze.add_argument('data_file',
                                    default='elf_data',
                                    help=('Analyze this data file. Defaults '
                                          'to "elf_data".'))
        # TODO histogram?

        out = parser.parse_args()
        if 'feature' not in out:
            print("No subcommand specified.", file=sys.stderr)
            parser.print_usage(file=sys.stderr)
            sys.exit(1)

        return out


def main():
    config = Config()

    if config.feature == 'gather':
        stats_accu = gather_stats.gather_system_files(config)
        stats_accu.serialize(config.output)

    elif config.feature == 'analyze':
        # TODO
        print("Not implemented", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
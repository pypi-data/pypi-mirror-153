#!/usr/bin/env python3

"""
\033[1;33mpicoslave\033[0m a CLI tool to control the \033[1;33mPicoSlave\033[0m I2C slave simulator.

PicoSlave USB devices have the vid/pid \033[0;33mC001:012C\033[0m and are automatically detected
by this tool if only one is present. The \033[1;39mscan\033[0m command lists devices showing an
index and the device serial number, by which a specific device can be selected
using \033[1;39m-i\033[0m or \033[1;39m-s\033[0m.

\033[1;33mPicoSlave\033[0m supports 2 I2C slaves to be each configured via the \033[1;39mconfig\033[0m command
for an I2C slave address to operate on a register space of configurable size
starting at address 0x00. Slave operation can be disabled by configuring a slave
for the I2C address 0x00. Slaves 0 or 1 are selected using the \033[1;39miface\033[0m argument
for all slave specific commands.

The register spaces of the slaves can be written into (\033[1;39mwrite\033[0m) and read from (\033[1;39mread\033[0m).
This can be done when slaves are enabled or disabled. \033[1;39mclear\033[0m resets the entire
configured register space to 0x00 or a given value.
"""  # pylint: disable=line-too-long  # noqa

import argparse
import logging
import sys
from typing import Any

import picoslave as ps
from picoslave.picoslave import PicoSlave, UsbPicoSlave
from picoslave.picoslave import bytestr
from picoslave.picoslave import DeviceNotFoundError


def config_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:

    function = PicoSlave.Protocol.SlaveFunction[args.function.upper()]

    if function == PicoSlave.Protocol.SlaveFunction.SLAVE:
        assert args.slave_addr is not None, "slave operation requires argument 'slave_addr'"
        slave_addr = args.slave_addr

        if args.eightbit:
            print(f"converting 8-bit address '{slave_addr:02X}h' to 7-bit address "
                  f'{slave_addr >> 1:02X}h')
            slave_addr >>= 1
        assert 1 <= slave_addr <= PicoSlave.Protocol.SlaveFunction.SLAVE.value, \
            f'I2C address out of range [1..{PicoSlave.Protocol.SlaveFunction.SLAVE:02X}h]'

        print(f'configuring I2C-{args.iface} for address {args.slave_addr:02X}h, '
              f'size {args.size} and word width {args.width}')
        picoslave.config_slave(args.iface, args.slave_addr, args.size, args.width)
        return

    if function == PicoSlave.Protocol.SlaveFunction.BLOCKER:
        assert args.signals, "'blocker' function requires '--signals' option (non-empty)."
        print(f'configuring I2C-{args.iface} as blocker ({"|".join(set(args.signals))})')
        picoslave.config_blocker(args.iface, scl='scl' in args.signals, sda='sda' in args.signals)
        return

    if function == PicoSlave.Protocol.SlaveFunction.RESET:
        args.slave_addr = PicoSlave.Protocol.SlaveFunction.RESET
        print(f'deactivating I2C-{args.iface}')
        picoslave.config_reset(args.iface)
        return


def read_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'reading from I2C-{args.iface}: {args.size} bytes from address {args.addr:02X}h')
    response_data = picoslave.read(args.iface, args.addr, args.size)
    print('response:')
    print(bytestr(response_data))


def write_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'writing to I2C-{args.iface}: {len(args.data)} '
          f'{"bytes" if len(args.data) > 1 else "byte"} to address {args.addr:02X}h:')
    print(bytestr(args.data))
    picoslave.write(args.iface, args.addr, args.data)


def clear_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'clearing memory of I2C-{args.iface} with value {args.value:02x}h')
    picoslave.clear(args.iface, args.value)


def stat_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print(f'reading statistics from I2C-{args.iface}: {args.size} entries '
          f'from address {args.addr:02X}h')
    statistics = picoslave.statistics(args.iface, args.addr, args.size)
    print('  ADDR  READ  WRITE')
    for addr in statistics:
        if statistics[addr][0] or statistics[addr][1]:
            print(f'   {addr:02X}h  {statistics[addr][0]:4}   {statistics[addr][1]:4}')


def info_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    info = picoslave.info()
    print(info)


def reset_cmd(args: argparse.Namespace, picoslave: PicoSlave) -> None:
    print('resetting target')
    picoslave.reset()


def main() -> None:

    loglevels = ['debug', 'info', 'warning', 'error', 'critical']
    ifaces = [0, 1]

    def auto_int(x: str) -> int:
        return int(x, 0)

    def mem_addr8(x: str) -> int:
        addr = auto_int(x)
        if addr >= 2**8:
            raise argparse.ArgumentTypeError(f'address must be in range [0..{2**8-1}]')
        return addr

    def mem_addr16(x: str) -> int:
        addr = auto_int(x)
        if addr >= 2**16:
            raise argparse.ArgumentTypeError(f'address must be in range [0..{2**16-1}]')
        return addr

    def byte_str(x: str) -> bytes:
        try:
            return bytes.fromhex(x)
        except Exception:
            raise argparse.ArgumentTypeError(f'not a valid byte string: "{x}"')

    class Formatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
        def add_usage(self, usage: Any, actions: Any, groups: Any, prefix: Any = None) -> None:
            if prefix is None:
                prefix = '\033[1;32mUsage: \033[0m'
            super().add_usage(usage, actions, groups, prefix)

    parser = argparse.ArgumentParser(description=__doc__,
                                     prog='\033[1;34mpicoslave\033[0m',
                                     formatter_class=Formatter)
    parser.add_argument(
        '-l', '--loglevel',
        metavar='L',
        type=str,
        default='Warning',
        choices=loglevels,
        help=f'log level: L={loglevels}\n'
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help="shortcut for '--loglevel debug'"
    )
    device_group = parser.add_mutually_exclusive_group()
    device_group.add_argument(
        '-i', '--index',
        type=int,
        metavar='X',
        help="Device index to select a specific PicoSlave device\n"
             "(see cmd='scan')"
    )
    device_group.add_argument(
        '-s', '--serial',
        type=str,
        metavar='S',
        help='Device serial number to select a specific PicoSlave\n'
             "device (see cmd='scan')"
    )
    parser.add_argument(
        '-V', '--version',
        action='store_true',
        help='show the program version'
    )

    # subparsers
    sub = parser.add_subparsers(
        title='\033[1;34mCMD\033[0m',
        dest='command',
        metavar='\033[1;34mCMD\033[0m',
        description='Command to execute on PicoSlave. See CMD -h for help.',
    )
    iface_parser = argparse.ArgumentParser(add_help=False, formatter_class=Formatter)
    iface_parser.add_argument(
        'iface',
        type=int,
        metavar='iface',
        choices=ifaces,
        help=f'I2C interface number ({ifaces})',
    )

    # config
    sub_parser = sub.add_parser(
        'config',
        aliases=['c'],
        parents=[iface_parser],
        help='configure an I2C slave',
        formatter_class=Formatter,
    )
    sub_parser.add_argument(
        '-f', '--function',
        metavar='FUNC',
        type=str,
        default='slave',
        choices=[e.name.lower() for e in PicoSlave.Protocol.SlaveFunction],
        help='Function to configure the given interface.\n'
             "    slave:   (default) operate as I2C slave\n"
             "             requires 1 <= 'slave_addr' <= 127\n"
             "    blocker: block SCL, SDA or both to a LOW signal level\n"
             "             requires '--signals' option\n"
             "    reset:   reset configuration for no operation\n",
    )
    sub_parser.add_argument(
        'slave_addr',
        type=auto_int,
        nargs='?',
        help='Memory or 7-bit slave address (use -8 for 8-bit addresses)',
    )
    sub_parser.add_argument(
        '-8',
        dest='eightbit',
        action='store_true',
        help='Set to interpret I2C addresses as 8-bit (default is 7-bit)\n',
    )
    sub_parser.add_argument(
        'size',
        type=int,
        nargs='?',
        default=256,
        help='size of the configured I2C memory, at which it will overflow\n'
             '(max 256). Note that the I2C memory size is given in words\n'
             '(of size [width]), not bytes.',
    )
    sub_parser.add_argument(
        'width',
        type=int,
        nargs='?',
        default=1,
        choices=[1, 2, 4],
        metavar='width',
        help='width of data words in I2C memory (1, 2 or 4)',
    )
    sub_parser.add_argument(
        '--signals',
        type=str,
        nargs='*',
        choices=['sda', 'scl'],
        metavar='S',
        help='todo',
    )
    sub_parser.set_defaults(func=config_cmd)

    # read
    sub_parser = sub.add_parser(
        'read',
        aliases=['r'],
        parents=[iface_parser],
        help='read from the slaves I2C memory',
        formatter_class=Formatter,
    )
    sub_parser.add_argument(
        'addr',
        type=mem_addr16,
        help='address to start reading from',
    )
    sub_parser.add_argument(
        'size',
        type=int,
        nargs='?',
        default=1,
        help='number of words to read from [addr] (max 256 * [width])',
    )
    sub_parser.set_defaults(func=read_cmd)

    # write
    sub_parser = sub.add_parser(
        'write',
        aliases=['w'],
        parents=[iface_parser],
        help='write data to the slaves I2C memory',
        formatter_class=Formatter,
    )
    sub_parser.add_argument(
        'addr',
        type=mem_addr16,
        help='address to start writing into',
    )
    sub_parser.add_argument(
        'data',
        type=byte_str,
        help='data to write to the I2C memory at [addr].\n'
             'Data format is a little endian hex string without spaces,\n'
             'e.g.: 03ab7fE0 (4 bytes). Note that data length must be a\n'
             'multiple of the configured word [width]. (see "config -h")',
    )
    sub_parser.set_defaults(func=write_cmd)

    # clear
    sub_parser = sub.add_parser(
        'clear',
        aliases=['C'],
        parents=[iface_parser],
        help='clear the I2C memory to 0 or an initial value',
        formatter_class=Formatter,
    )
    sub_parser.add_argument(
        'value',
        type=auto_int,
        nargs='?',
        default=0x00,
        help='initialize with this value',
    )
    sub_parser.set_defaults(func=clear_cmd)

    # stat
    sub_parser = sub.add_parser(
        'stat',
        aliases=['s'],
        parents=[iface_parser],
        help='retrieve read/write statistics from I2C memory',
        formatter_class=Formatter,
    )
    sub_parser.add_argument(
        'addr',
        type=mem_addr8,
        nargs='?',
        default=0x00,
        help='start memory address for reading statistics',
    )
    sub_parser.add_argument(
        'size',
        type=int,
        nargs='?',
        default=256,
        help='number of addresses/words to get r/w statistics for (max 256)',
    )
    sub_parser.set_defaults(func=stat_cmd)

    # scan
    sub_parser = sub.add_parser(
        'scan',
        aliases=['S'],
        help='scan for PicoSlave devices on USB',
        formatter_class=Formatter,
    )
    sub_parser.set_defaults(func='scan_cmd')

    # info
    sub_parser = sub.add_parser(
        'info',
        aliases=['I'],
        help='print info for the selected device',
        formatter_class=Formatter,
    )
    sub_parser.set_defaults(func=info_cmd)

    # reset
    sub_parser = sub.add_parser(
        'reset',
        aliases=['R'],
        help='reset the PicoSlave device',
        formatter_class=Formatter,
    )
    sub_parser.set_defaults(func=reset_cmd)

    args = parser.parse_args()

    if args.version:
        print(f'PicoSlave {ps.__version__}')
        exit(0)

    if args.debug:
        args.loglevel = 'debug'

    log_format = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.getLevelName(args.loglevel.upper()), format=log_format)

    try:
        import coloredlogs  # type: ignore
        coloredlogs.install(level=logging.getLevelName(args.loglevel.upper()), fmt=log_format)
    except ModuleNotFoundError:
        pass

    if 'func' not in args:
        parser.print_help()
        exit(1)

    if args.func == 'scan_cmd':
        devices = UsbPicoSlave.scan()
        sys.exit(1 if not devices else 0)

    assert args.index is None or args.index > 0, 'Device index must not be 0'
    args.index = args.index - 1 if args.index is not None else None

    picoslave = PicoSlave(index=args.index, serial=args.serial)

    try:
        args.func(args, picoslave)
    except (AssertionError, DeviceNotFoundError) as e:
        if str(e):
            print(f'\033[1;31mError:\033[0m {e}')
            sys.exit(1)
        raise


if __name__ == '__main__':
    main()

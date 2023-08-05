#!/usr/bin/python3
"""
Synopsis: watch dnsmasq-forwarders and adjust dnsmasq configuration dynamically

Usage: {appname} [-hVv][-l log]
       -h, --help           this message
       -V, --version        print version and exit
       -v, --verbose        verbose mode (cumulative)
       -l, --logfile=fname  log to this file

Defaults (supply deviating values via environment):
FORWARDERS: {forwarders}
VPNDNSCONF: {vpndnsconf}
DNSSERVICE: {dnsservice}

Copyright:
(c)2021 by {author}

License:
{license}
"""
#
# vim:set et ts=8 sw=4:
#

__version__ = '0.0.3'
__author__ = 'Hans-Peter Jansen <hans-peter.jansen@suse.com>'
__license__ = 'GNU GPL v2 - see http://www.gnu.org/licenses/gpl2.txt for details'
__homepage__ = 'https://github.com/frispete/vpndnshelper'


import os
import re
import sys
import time
import getopt
import signal
import logging
import ipaddress
import pyinotify
import subprocess

# exit codes
OPT_ERROR = 1
IO_ERROR = 2
INTR_ERROR = 4

class gpar:
    """Global parameter class"""
    appdir, appname = os.path.split(sys.argv[0])
    if appdir == '.':
        appdir = os.getcwd()
    if appname.endswith('.py'):
        appname = appname[:-3]
    version = __version__
    author = __author__
    license = __license__
    homepage = __homepage__
    loglevel = logging.WARNING
    logfile = '-'
    pid = os.getpid()
    forwarders = os.environ.get('FORWARDERS', '/run/dnsmasq-forwarders.conf')
    vpndnsconf = os.environ.get('VPNDNSCONF', '/etc/dnsmasq.d/vpndnshelper.conf')
    dnsservice = os.environ.get('DNSSERVICE', 'systemctl restart dnsmasq.service')
    # internal
    vpn_ns_start_tag = '# VPN DNS server'
    vpn_ns_end_tag = '# VPN DNS revres'

    ns_pattern = re.compile('''
        ^                   # anchor at start
        nameserver          # nameserver entry
        \s+                 # space(s)
        (?P<ip>[\d\.:]+)    # ip address
        $                   # anchor at end
    ''', re.VERBOSE)

    vpn_ns_pattern = re.compile('''
        ^                   # anchor at start
        (?P<enable>[#]?)    # optional #
        (?P<tag>server=)    # server entry
        (?P<names>/.*/+)    # /vpndomain.tld/
        (?P<ip>[\d\.:]+)    # ip address
        $                   # anchor at end
    ''', re.VERBOSE)

    local_server = set()


log = logging.getLogger(gpar.appname)


stdout = lambda *msg: print(*msg, file = sys.stdout, flush = True)
stderr = lambda *msg: print(*msg, file = sys.stderr, flush = True)


def exit(ret = 0, msg = None, usage = False):
    """Terminate process with optional message and usage """
    if msg:
        stderr('{}: {}'.format(gpar.appname, msg))
    if usage:
        stderr(__doc__.format(**gpar.__dict__))
    sys.exit(ret)


def setup_logging(loglevel, logfile):
    """Setup various aspects of logging facility"""
    logconfig = dict(
        level = loglevel,
        format = '%(asctime)s %(levelname)5s: [%(name)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
    )
    if not logfile == '-':
        logconfig['filename'] = logfile
    logging.basicConfig(**logconfig)


def rstrip(line, lst = ' \t\r\n'):
    """Strip whitespace and line breaks from line end"""
    items = list(lst)
    while line and line[-1] in items:
        line = line[:-1]
    return line


def sstrlist(it, sep = ', '):
    """Return a sorted string with it elements mapped to str, concatenated by sep"""
    return sep.join(sorted(map(str, it)))


def ts2time(ts):
    """Convert a timestamp since epoch into human readable form"""
    return time.asctime(time.localtime(ts))


def get_ns(fname):
    """Fetch nameserver entries from a file, e.g. /etc/resolv.conf"""
    log.debug('fetch nameserver from {}'.format(fname))
    ns = set()
    with open(fname) as fd:
        for line in fd:
            m = gpar.ns_pattern.match(line)
            if m:
                try:
                    ip = ipaddress.ip_address(m['ip'])
                except ipaddress.AddressValueError as e:
                    log.error('{} is not a valid ip-address'.format(m['ip']))
                else:
                    ns.add(ip)
    if ns:
        log.debug('nameserver: {}'.format(sstrlist(ns)))
    return ns


def update_vpn_ns(enable, nameserver = set()):
    """Update nameserver entries in dnsmasq config file and restart dnsmasq"""
    if enable and not nameserver:
        log.error('cannot enable without any nameserver')
        return
    fname = gpar.vpndnsconf
    if enable:
        log.info('enable vpn nameserver {} in {}'.format(sstrlist(nameserver), fname))
    else:
        log.info('disable vpn nameserver in {}'.format(fname))
    vpn_ns = False
    vpn_ns_done = False
    vpn_ns_match = None
    lines = []
    with open(fname) as fd:
        for line in fd:
            line = rstrip(line)
            if vpn_ns:
                if enable and not vpn_ns_done:
                    # we process all enabled ns at once here
                    if not vpn_ns_match:
                        # use the first matching ns pattern as template
                        vpn_ns_match = gpar.vpn_ns_pattern.match(line)
                    if vpn_ns_match:
                        fdict = vpn_ns_match.groupdict()
                        for ns in sorted(nameserver):
                            fdict['ip'] = str(ns)
                            lines.append('{tag}{names}{ip}'.format(**fdict))
                        vpn_ns_done = True
                        continue
                else:
                    # handle disabling / suppress further enabled entries
                    m = gpar.vpn_ns_pattern.match(line)
                    if m:
                        if not enable:
                            # disable: we let pass matching entries (but disabled)
                            fdict = m.groupdict()
                            fdict['enable'] = '#'
                            lines.append('{enable}{tag}{names}{ip}'.format(**fdict))
                        # else
                            # enable: suppress further matches
                        continue

            elif line.startswith(gpar.vpn_ns_start_tag):
                vpn_ns = True
                vpn_ns_match = None
            elif line.startswith(gpar.vpn_ns_end_tag):
                vpn_ns = False
                vpn_ns_match = None
            lines.append(line)

    if lines:
        # rewrite dnsmasq config file
        log.info('replace {}'.format(fname))
        os.rename(fname, fname + '~')
        open(fname, 'w').write('\n'.join(lines) + '\n')
        # restart dnsmasq service
        log.info('execute "{}"'.format(gpar.dnsservice))
        subprocess.call(gpar.dnsservice.split())


class ForwardHandler(pyinotify.ProcessEvent):
    """Process specific pyinotify events, kick vpn ns updates, and restart dnsmasq"""
    def my_init(self, par):
        self.forwarders = par.forwarders
        self.forwarders_ts = os.path.getmtime(self.forwarders)
        log.debug('forwarders ts: {}'.format(ts2time(self.forwarders_ts)))
        self.local_server = par.local_server
        self.vpn = False

    def check_forwarders(self):
        if self.forwarders_ts != os.path.getmtime(self.forwarders):
            ns = get_ns(self.forwarders)
            if ns != self.local_server:
                # nameserver were added, remove local ns
                ns -= self.local_server
                log.debug('new nameserver found: {}'.format(sstrlist(ns)))
                update_vpn_ns(True, ns)
                self.vpn = True
            elif self.vpn:
                log.debug('vpn nameserver disappeared')
                update_vpn_ns(False)
                self.vpn = False
            self.forwarders_ts = os.path.getmtime(self.forwarders)
            log.debug('forwarders ts: {}'.format(ts2time(self.forwarders_ts)))

    def process_event(self, event):
        if event.pathname == self.forwarders:
            # on fast systems, avoid a race between inotify events and ts actualization 
            time.sleep(0.1)
            log.debug('check {}'.format(event.pathname))
            self.check_forwarders()

    def process_IN_CLOSE_WRITE(self, event):
        log.debug('close_write {}'.format(event.pathname))
        self.process_event(event)

    def process_IN_CLOSE_NOWRITE(self, event):
        log.debug('close_nowrite {}'.format(event.pathname))
        self.process_event(event)


def run():
    """Watch /run for close events"""
    log.info('started with pid {pid} in {appdir}'.format(**gpar.__dict__))
    # assume VPN is NOT active (TODO: check openconnect/openvpn process, hard!)
    gpar.local_server = get_ns(gpar.forwarders)
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CLOSE_NOWRITE
    handler = ForwardHandler(par = gpar)
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch(os.path.dirname(gpar.forwarders), mask)
    notifier.loop()


def cleanup():
    """Cleanup: make sure, redirection is disabled on exit, and dnsmasq is restarted"""
    update_vpn_ns(False)


def sighandler(signum, frame):
    """Signal handler to gracefully exit the process"""
    if signum == signal.SIGTERM:
        signum = 0
    else:
        log.warning('process interrupted: %s', signum)
    cleanup()
    # avoid signal loop
    os._exit(signum)


def main(argv = None):
    """Command line interface and console script entry point."""
    if argv is None:
        argv = sys.argv[1:]

    try:
        optlist, args = getopt.getopt(argv, 'hVvl:',
            ('help', 'version', 'verbose', 'logfile=')
        )
    except getopt.error as msg:
        exit(OPT_ERROR, msg, True)

    for opt, par in optlist:
        if opt in ('-h', '--help'):
            exit(usage = True)
        elif opt in ('-V', '--version'):
            exit(msg = 'version {}'.format(gpar.version))
        elif opt in ('-v', '--verbose'):
            if gpar.loglevel > logging.DEBUG:
                gpar.loglevel -= 10
        elif opt in ('-l', '--logfile'):
            gpar.logfile = par

    setup_logging(gpar.loglevel, gpar.logfile)

    for fn, mode, err in (
            (gpar.forwarders, os.R_OK, 'readable'),
            (gpar.vpndnsconf, os.W_OK, 'writable'),
        ):
        if not os.access(fn, mode):
            exit(IO_ERROR, 'mandatory file {} isn\'t {}'.format(fn, err))

    for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGQUIT,
                signal.SIGPIPE, signal.SIGTERM):
        signal.signal(sig, sighandler)

    ret = 0
    try:
        run()
    except SystemExit:
        pass
    except:
        log.exception('internal error:')
        cleanup()
        ret = INTR_ERROR
    return ret


if __name__ == '__main__':
    sys.exit(main())


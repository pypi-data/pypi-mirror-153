VPN DNS Helper
==============
This tool allows local DNS server to coexist with corporate VPN DNS server by
adjusting the dnsmasq configuration dynamically.

Description
-----------
If you want to set up a split DNS corporate VPN on a Linux system that is itself
included in an advanced local network environment with its own DNS server, you
may encounter an **unpleasant issue**: once the VPN connection is established, you
can no longer resolve local systems/services because the VPN **overwrites** the
local nameserver with the **company VPN nameserver**.

A simple solution would be to add the local systems to `/etc/hosts`, but what if
there are many, or if they change frequently?

A better solution to this problem is presented here: on the system, that needs
to access the corporate VPN (*vpn system*), we use `dnsmasq` as a resolver on
localhost, and instruct `dnsmasq` to resolve VPN destinations only with the
VPN nameserver. This should work even if your corporate DNS uses public domains
with private subdomains.

Prerequisites
-------------
Install `dnsmasq` on the *vpn system* in such a way that nameserver changes on VPN
start (e.g. triggered by the NetworkManager) do not end up in /etc/resolv.conf
but in another file (e.g. `/run/dnsmasq-resolvers.conf`). We do not supply this
file directly to `dnsmasq`, but adjust a `dnsmasq` config file dynamically
(e.g. `/etc/dnsmasq.d/vpndnshelper.conf`).

On a SUSE system, the network setup is done with `netconfig`. For our specific
needs, please check/adjust `/etc/sysconfig/network/config`:

```
NETCONFIG_DNS_POLICY="auto"
NETCONFIG_DNS_FORWARDER="dnsmasq"
NETCONFIG_DNS_FORWARDER_FALLBACK="no"
NETCONFIG_DNS_STATIC_SEARCHLIST=""
NETCONFIG_DNS_STATIC_SERVERS=""
```

Installation
------------
Create a config file with the name `/etc/dnsmasq.d/vpndnshelper.conf`:
```
# force primary interface
interface=lo
bind-interfaces
domain-needed

# disable dhcp
no-dhcp-interface=

# VPN DNS server
#server=/vpndomain.tld/othervpn.tld/12.34.56.78
# VPN DNS revres

# local DNS server
server=12.34.56.78
```

In this file, the section between the VPN DNS comments is adjusted dynamically.
The VPN domain names and the local server need to be set up correctly. Before
the VPN is started, it's a good idea to keep the VPN DNS server disabled.

The paths of `/run/dnsmasq-forwarders.conf` and `/etc/dnsmasq.d/vpndnshelper.conf`,
as well as the `dnsmasq` restart command can be changed via the environment.
See `vpndnshelper --help` for further configurability.

After installation checks
-------------------------
After a restart of the *vpn system*, `/etc/resolv.conf` should not contain any
nameserver entries. That forces the resolver to resolve via `localhost`, which is
handled by `dnsmasq`. `/run/dnsmasq-forwarders.conf` should only contain the local
nameserver, which must be manually assigned to the local DNS server in
`/etc/dnsmasq.d/vpndnshelper.conf`.

Operation
---------
When the VPN tunnel is established, netconfig will add the VPN nameserver with
higher priority to `/run/dnsmasq-forwarders.conf`. We monitor any changes to this
file, adjust `/etc/dnsmasq.d/vpndnshelper.conf` and restart `dnsmasq`.

When the VPN is started, we will rewrite VPN DNS `server=` lines. If multiple VPN
nameserver are supplied, the first `server=` line is used as a template for all
entries, and the comments are removed.

When the VPN is shut down, the `server=` entries are simply commented out again.

Issues and Caveats
------------------
We monitor filesystem changes to `/run/dnsmasq-forwarders.conf` with `pyinotify`.
During development, we noticed a race between `IN_CLOSE_WRITE` and file mtime
changes.

Another option to get noticed from VPN state changes is `dbus`, but this would
make us depending harder on `NetworkManager` and comes with its own can of worms.

For now, we rely on being started with a teared down VPN tunnel in order to
collect the local nameserver. If you need to restart `vpndnshelper` during
operation, tear down the VPN tunnel first. `vpndnshelper` will reset the VPN
DNS server on restart, but will not be able to catch up with current state with
an open VPN tunnel.


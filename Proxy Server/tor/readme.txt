curl --proxy "socks5://159.65.156.237:1300" "ipinfo.io/json"
curl --proxy "socks5://159.65.156.237:1300" "https://api.ipify.org"
curl --proxy "socks5://159.65.156.237:1310" "https://api.ipify.org?format=json"

#Http Proxy faster than socks5
curl --proxy "159.65.156.237:1322" "https://api.ipify.org?format=json"


torsocks wget -qO - https://api.ipify.org; echo

tor -f /etc/tor/torrc_pub

https://tor.stackexchange.com/questions/9934/tor-is-only-assigning-circuits-from-a-very-limited-subset-of-exit-nodes


#config from one source
"--NewCircuitPeriod 15",
"--MaxCircuitDirtiness 15",
"--NumEntryGuards 8",
"--CircuitBuildTimeout 5",
"--ExitNodes {us}",
"--ExitRelay 0",
"--RefuseUnknownExits 0",
"--ClientOnly 1",
"--StrictNodes 1",
"--AllowSingleHopCircuits 1",


#############config source 2####################
User tor
RunAsDaemon 1
PidFile /var/run/tor/tor.pid
DataDirectory /var/lib/tor
Log notice file /var/log/tor/tor.log

SafeSocks 1
TestSocks 1

CircuitBuildTimeout 2
KeepalivePeriod 2
NewCircuitPeriod 15
NumEntryGuards 8

SocksPort 9050
SocksListenAddress 127.0.0.1

ControlPort 9051
HashedControlPassword <TOR_GENERATED_HASH_HERE>
###################################






https://github.com/milesrichardson/rotating-proxy

https://github.com/noobpk/auto-change-tor-ip

https://github.com/seevik2580/tor-ip-changer
#sudo pkill -SIGHUP tor
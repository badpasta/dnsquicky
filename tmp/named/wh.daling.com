$ORIGIN .
$TTL 60	; 1 minute
wh.daling.com		IN SOA	a.ns.wh.daling.com. root.wh.daling.com. (
				2016072342 ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				3600000    ; expire (5 weeks 6 days 16 hours)
				3600       ; minimum (1 hour)
				)
$TTL 600	; 10 minutes
			NS	b.ns.wh.daling.com.
			NS	a.ns.wh.daling.com.
$ORIGIN wh.daling.com.
$TTL 60	; 1 minute
bj1-msr1		A	172.16.0.1
$ORIGIN ns.wh.daling.com.
a			A	119.254.119.155
b			A	119.254.119.156

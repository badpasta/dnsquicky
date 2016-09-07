;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.fe.daling.com. root.fe.daling.com.(
                        2016072101	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.fe.daling.com.
@       60      IN      NS    b.ns.fe.daling.com.

$ORIGIN fe.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156

area-tool	IN	A	10.36.4.54

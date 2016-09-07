;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.dc.daling.com. root.dc.daling.com.(
                        2015082003	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.dc.daling.com.
@       60      IN      NS    b.ns.dc.daling.com.

$ORIGIN dc.daling.com.

;; glue records
a.ns IN A 119.254.116.71
b.ns IN A 119.254.116.72

ad	IN	A	10.36.4.60
;; dc.daling.com
$ORIGIN test.dc.daling.com.
l-test1	IN	A	10.0.0.99

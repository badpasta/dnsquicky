;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.dev.daling.com. root.dev.daling.com.(
                        2016072601	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.dev.daling.com.
@       60      IN      NS    b.ns.dev.daling.com.

$ORIGIN dev.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156


wx		IN	A	223.223.192.86
pay		IN	A	223.223.192.86
l-erpdev1	IN	A	10.36.4.19
l-erpdev2	IN	A	10.36.4.20
l-erpdev3	IN	A	10.36.4.21
passport	IN	A	10.36.4.85
push		IN	A	10.36.4.10

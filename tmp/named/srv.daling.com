;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.srv.daling.com. root.srv.daling.com.(
                        2016090702	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.srv.daling.com.
@       60      IN      NS    b.ns.srv.daling.com.



$ORIGIN srv.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156

wx	IN	A	10.0.31.240
wx	IN	A	10.0.31.241
erp	IN	A	10.0.31.240
erp	IN	A	10.0.31.241
qp	IN	A	10.0.31.240
qp	IN	A	10.0.31.241

activity 	IN	A	10.0.31.240
activity 	IN	A	10.0.31.241
zin	IN	A	10.0.31.240
zin	IN	A	10.0.31.241

recommend	IN	A	10.0.31.240
recommend	IN	A	10.0.31.241

passport	IN	A	10.0.31.240
passport	IN	A	10.0.31.241

sms	IN	A	10.0.31.240
sms	IN	A	10.0.31.241

api.erp	IN	A	10.0.31.240	
api.erp	IN	A	10.0.31.241

alert	IN	A	10.0.31.240
alert	IN	A	10.0.31.241

app	IN	A	10.0.8.32
app	IN	A	10.0.8.33

search	IN	A	10.0.31.240
search	IN	A	10.0.31.241

solr	IN	A	10.0.31.240
solr	IN	A	10.0.31.241

captcha	IN	A	10.0.31.240
captcha	IN	A	10.0.31.241

pushagent	IN	A	10.0.31.240
pushagent	IN	A	10.0.31.241

push	IN	A	10.0.31.240
push	IN	A	10.0.31.241

cart    IN      A       10.0.31.240
cart    IN      A       10.0.31.241

goods    IN      A       10.0.31.240
goods    IN      A       10.0.31.241

vrm    IN      A       10.0.31.240
vrm    IN      A       10.0.31.241

wallet	IN	A	10.0.31.240
wallet	IN	A	10.0.31.241

status-ng	IN	A	10.0.31.240
status-ng	IN	A	10.0.31.241
cdnpush		IN	A	10.0.31.16
;;vip 
mq2.vip	IN	A	10.0.8.32
mq2.vip	IN	A	10.0.8.33
erpdbm1.vip	IN	A	10.0.3.241
mfsmaster.vip	IN	A	10.0.3.230
ucdbm.vip	IN	A	10.0.24.249
coupondbm.vip	IN	A	10.0.24.246
wmsdbm.vip	IN	A	10.0.24.247
syslog.vip	IN	A	10.0.3.17
coupon		IN	A	10.0.31.240
coupon		IN	A	10.0.31.241
idstore		IN	A	10.0.31.240
idstore		IN	A	10.0.31.241
erpdbm2.vip	IN	A	10.0.24.248
gpmstore	IN	A	10.0.31.27
storage		IN	A	10.0.31.26

;;ntp
pool1.ntp	IN	A	10.0.31.16
pool2.ntp	IN	A	10.0.31.17
pool3.ntp	IN	A	10.0.31.18

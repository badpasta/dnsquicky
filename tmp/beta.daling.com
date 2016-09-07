;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.beta.daling.com. root.beta.daling.com.(
                        2016081701	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.beta.daling.com.
@       60      IN      NS    b.ns.beta.daling.com.



$ORIGIN beta.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156

;; root records
;beta.daling.com.	IN	A	119.254.116.73
;beta.daling.com.	IN	A	119.254.116.74


;; beta service
*.hotconfig	IN	A	10.36.4.30
;m		IN	A	175.25.24.15
;m		IN	A	119.253.46.146
m		IN	A	223.223.192.86
;;app	IN	A	122.112.10.90
;app		IN	A	175.25.24.15
app		IN	A	223.223.192.86
captcha		IN	A	10.36.4.30
;app		IN	A	119.253.46.146
;erp.api		IN	A	119.253.46.146
erp.api		IN	A	223.223.192.86
;app		IN	CNAME	app.beta.sec.daling.com.
ymall		IN	CNAME	ymall.beta.daling.com.he2.aqb.so.
*.erp		IN	A	10.36.4.30
l-qa2		IN	A	10.36.2.77
l-qa3		IN	A	10.36.4.4
l-qa4		IN	A	10.36.2.78
l-qa5		IN	A	10.36.4.7
l-qa6		IN	A	10.36.4.16
l-qa7		IN	A	10.36.4.17
l-qa9		IN	A	10.36.4.23
l-qa10		IN	A	10.36.4.24
l-qa11		IN	A	10.36.4.25
l-qa12		IN	A	10.36.4.26
l-nginx1	IN	A	10.36.4.6
l-nginx2	IN	A	10.36.4.12
web		IN	A	175.25.24.15
cps		IN	A	175.25.24.15
l-db1		IN	A	10.36.4.15
l-php1		IN	A	10.36.4.13
l-php2		IN	A	10.36.4.14
l-qa8		IN	A	10.36.4.18
a.erp.corp	IN	A	10.36.4.30
b.erp.corp	IN	A	10.36.4.30
c.erp.corp	IN	A	10.36.4.30
a.cart		IN	A	10.36.4.30
b.cart		IN	A	10.36.4.38
c.cart		IN	A	10.36.4.10
d.cart		IN	A	10.36.4.85
a.mbr-growth	IN	A	10.36.4.30
b.mbr-growth	IN	A	10.36.4.38
c.mbr-growth	IN	A	10.36.4.10
d.mbr-growth	IN	A	10.36.4.85
a.mbr-wallet	IN	A	10.36.4.30
b.mbr-wallet	IN	A	10.36.4.38
c.mbr-wallet	IN	A	10.36.4.10
d.mbr-wallet	IN	A	10.36.4.85

zin		IN	A	10.36.4.30 
crm		IN	A	10.36.4.30
qadb		IN	CNAME	l-opdb2.ops.bj0.daling.com

l-tools1        IN      A       10.36.2.206
sms		IN	A	10.36.4.30
a.coupon		IN	A	10.36.4.30
b.coupon		IN	A	10.36.4.38
c.coupon		IN	A	10.36.4.10
d.coupon		IN	A	10.36.4.85

a.solr		IN	A	10.36.4.30
b.solr		IN	A	10.36.4.38
c.solr		IN	A	10.36.4.10
d.solr		IN	A	10.36.4.85

a.app		IN	A	10.36.4.30
b.app		IN	A	10.36.4.38
c.app		IN	A	10.36.4.10
d.app		IN	A	10.36.4.85

*.oauth		IN	A	10.36.4.30
*.goods		IN	A	10.36.4.30
*.vrm		IN	A	10.36.4.30
*.wms		IN	A	10.36.4.30

recommend	IN	A	10.36.4.10
img		IN	A	10.36.4.30

a.admin		IN	A	10.36.4.30
a.shop		IN	A	10.36.4.30
a.activity		IN	A	10.36.4.30

b.admin		IN	A	10.36.4.38
b.shop		IN	A	10.36.4.38
b.activity		IN	A	10.36.4.38

c.admin		IN	A	10.36.4.10
c.shop		IN	A	10.36.4.10
c.activity		IN	A	10.36.4.10

d.admin		IN	A	10.36.4.85
d.shop		IN	A	10.36.4.85
d.activity		IN	A	10.36.4.85

e.admin		IN	A	10.36.4.67
e.shop		IN	A	10.36.4.67
e.activity		IN	A	10.36.4.67

f.activity		IN	A	10.36.4.72
f.admin		IN	A	10.36.4.72
f.shop		IN	A	10.36.4.72
a.zin		IN	A	10.36.4.30
b.zin		IN	A	10.36.4.38
dschedule	IN	A	10.36.4.30


;;tasks for tianfu
goods.x		IN	A	10.36.12.120
passport.x	IN	A	10.36.12.120
wallet.x	IN	A	10.36.12.120
cart.x		IN	A	10.36.12.120

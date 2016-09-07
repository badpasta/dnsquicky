;;$TTL 1800      ; 1 day
$TTL 60
@		IN SOA  ns1.daling.com. root.daling.com.(
			2015080601	; Serial
			3600            ; Refresh (1 hour)
			900             ; Retry (15 minutes)
			3600000         ; Expire (5 weeks 6 days 16 hours)
			3600            ; Minimum (1 hour)
			)
@	90	IN	NS    ns1.daling.com.
@	90	IN	NS    ns2.daling.com.


;; NS
corp.daling.com.		IN	NS    a.ns.corp.daling.com.
corp.daling.com.		IN	NS    b.ns.corp.daling.com.
beta.daling.com.		IN	NS    a.ns.beta.daling.com.
beta.daling.com.		IN	NS    b.ns.beta.daling.com.
bj1.daling.com.			IN	NS    a.ns.bj1.daling.com.
bj1.daling.com.			IN	NS    b.ns.bj1.daling.com.
wh.daling.com.			IN	NS    a.ns.wh.daling.com.
wh.daling.com.			IN	NS    b.ns.wh.daling.com.
dev.daling.com.			IN	NS    a.ns.dev.daling.com.
dev.daling.com.			IN	NS    b.ns.dev.daling.com.
paycenter.daling.com.			IN	NS    a.ns.paycenter.daling.com.
paycenter.daling.com.			IN	NS    b.ns.paycenter.daling.com.
daling.com.	IN	A	119.254.116.73
daling.com.	IN	A	119.254.116.74
$ORIGIN daling.com.
;; mail domain

@  IN  MX  5   mxwcom.263xmail.com.
@  IN  MX  10  mxcom.263xmail.com.
@  IN  TXT "v=spf1 include:spf.263xmail.com -all"
pop   IN  CNAME   popcom.263xmail.com.
smtp  IN  CNAME   smtpcom.263xmail.com.
imap  IN  CNAME   imapcom.263xmail.com.
mail  IN  CNAME   mm.263.com.

;; glue records
a.ns.corp IN A 119.254.116.71
b.ns.corp IN A 119.254.116.72
a.ns.beta IN A 119.254.116.71
b.ns.beta IN A 119.254.116.72
a.ns.bj1 IN A 119.254.116.71
b.ns.bj1 IN A 119.254.116.72
a.ns.wh IN A 119.254.116.71
b.ns.wh IN A 119.254.116.72
a.ns.dev IN A 119.254.116.71
a.ns.paycenter IN A 119.254.116.71
b.ns.dev IN A 119.254.116.72
b.ns.paycenter IN A 119.254.116.72
;; prod domail
mirrors	IN	A	10.0.3.17
s	IN	A	119.254.116.73
s	IN	A	119.254.116.74
act	IN	A	119.254.116.74
act	IN	A	119.254.116.73
tools	IN	A	119.254.116.70
ns1	IN	A	119.254.116.71
ns2	IN	A	119.254.116.72

;;erp
erp		IN	A	10.0.3.18
samba.erp		IN	A	10.0.0.34
erp		IN	A	10.0.3.19
api.erp		IN	A	119.254.116.73
api.erp		IN	A	119.254.116.74
;;www
www	IN	A	119.254.116.73
www	IN	A	119.254.116.74
wx    	IN  A    182.92.187.191
wx2    	IN  A    119.254.116.73
wx2    	IN  A    119.254.116.74
;;classify
meihu		IN	CNAME	www
lingshi		IN	CNAME	www
shenghuo		IN	CNAME	www
peishi		IN	CNAME	www
bao		IN	CNAME	www
jingxuan		IN	CNAME	www
new		IN	CNAME	www
hot		IN	CNAME	www
;;touch
touch		IN	A	119.254.116.73
touch		IN	A	119.254.116.74
t       	IN      CNAME   touch
;;wx
wxgame    	IN  A    119.254.116.73
wxgame    	IN  A    119.254.116.74
;;pay
paycenter    	IN  A    119.254.116.74
paycenter    	IN  A    119.254.116.73
;;video
v                IN      A       119.254.116.73
v                IN      A       119.254.116.74
m                IN      A       119.254.116.73
m                IN      A       119.254.116.74
video.cdn        IN      A       119.254.116.73
video.cdn        IN      A       119.254.116.74
img1.cdn        IN      CNAME       img1.cdn.daling.com.wscdns.com.
download.cdn        IN      CNAME       download.cdn.daling.com.wscdns.com.
;;touch class
$ORIGIN touch.daling.com.
meihu		IN	CNAME	touch.daling.com.
lingshi		IN	CNAME	touch.daling.com.
shenghuo		IN	CNAME	touch.daling.com.
peishi		IN	CNAME	touch.daling.com.
bao		IN	CNAME	touch.daling.com.
jingxuan		IN	CNAME	touch.daling.com.
new		IN	CNAME	touch.daling.com.
hot		IN	CNAME	touch.daling.com.
summer		IN	CNAME	touch.daling.com.
;;passport
passport	IN	A	119.254.116.73
passport	IN	A	119.254.116.74


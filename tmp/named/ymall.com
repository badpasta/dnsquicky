;;$TTL 1800      ; 1 day
$TTL	60
@		IN SOA  ns1.ymall.com. root.ymall.com.(
			2015052501	; Serial
;			3600            ; Refresh (1 hour)
			60
			900             ; Retry (15 minutes)
			3600000         ; Expire (5 weeks 6 days 16 hours)
			3600            ; Minimum (1 hour)
			)
@	60	IN	NS    ns1.ymall.com.
@	60	IN	NS    ns2.ymall.com.
;;ymall.com. 60	IN	A	59.151.3.136
ymall.com. 60	IN	A	119.254.116.73
ymall.com. 60	IN	A	119.254.116.74
$ORIGIN ymall.com.

;; basic service
ns1     IN      A       119.254.116.71
ns2     IN      A       119.254.116.72
;; prod domail
;;www    900 	IN      A 59.151.3.136
;;www	60	IN	A 59.151.3.136
www	60	IN	A	119.254.116.73
www	60	IN	A	119.254.116.74
brand 		IN      CNAME	www
store 		IN      CNAME   www
bag 		IN      CNAME   www
duds 		IN      CNAME   www
fashion 	IN      CNAME   www
shoe 		IN      CNAME   www
special 	IN      CNAME   www
watch 		IN      CNAME   www
cosmetics	IN      CNAME   www
paycenter	IN 	CNAME   www
3g 		IN 	CNAME   3g.yoka.com.
;;mobile 900 	IN 	A 59.151.3.136
;;mobile	60	IN	A 59.151.3.136
mobile		IN	A	119.254.116.73
mobile		IN	A	119.254.116.74
m 		IN 	CNAME mobile
shop    	IN      CNAME   mobile
;;touch   	IN      CNAME www
touch		IN	A	119.254.116.73
touch		IN	A	119.254.116.74
v 		IN 	CNAME   v.ymall.com.wscdns.com.
;;v		IN	A	119.254.116.73
;;V		IN	A	119.254.116.74
t       	IN      CNAME   touch
;;cdn domain
img1.cdn 60        IN      A       119.254.116.73
img1.cdn 60        IN      A       119.254.116.74
;;beta damain
test            IN      A       119.254.116.73
test            IN      A       119.254.116.74
;; js&css domain
static 60            IN      A       119.254.116.73
static 60            IN      A       119.254.116.74

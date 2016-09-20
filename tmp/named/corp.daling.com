;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.corp.daling.com. root.corp.daling.com.(
                        2016091301	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.corp.daling.com.
@       60      IN      NS    b.ns.corp.daling.com.

$ORIGIN corp.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156

;;corp
csm	IN	A	10.0.8.32
csm	IN	A	10.0.8.33
zin	IN	A	10.0.8.32
zin	IN	A	10.0.8.33
dalingbot	IN	A	10.0.8.33
dalingbot	IN	A	10.0.8.32
act	IN	A	10.0.8.32
act	IN	A	10.0.8.33
sysmon IN	A	10.0.3.37
asset IN	A	10.0.3.37
push IN		A	10.0.8.32
push IN		A	10.0.8.33
netmon	IN	A	10.36.2.245
betaerp    IN      A       119.254.116.73
betaerp    IN      A       119.254.116.74
redmine    IN      A       10.36.2.20
printers    IN      A       10.36.15.100
wiki       IN      A       10.0.26.28
jenkins    IN      A       10.0.8.32
jenkins    IN      A       10.0.8.33
project    IN      A       10.36.4.30
cacti      IN      A       10.36.4.30
nexus      IN      A       10.36.2.7
gitlab-tmp	IN	A	10.0.26.26
gitlab     IN      A       10.0.26.26
qa         IN      A       10.36.4.30
smtp1              IN      A       10.36.3.202
smokeping          IN      A 10.36.4.145
erpreport          IN      A       10.0.8.32 
erpreport          IN      A       10.0.8.33
appreport          IN      A       10.0.20.173
files1     IN      A       10.36.2.248

a.erp        IN      A       10.36.4.30
b.erp        IN      A       10.36.4.30
c.erp        IN      A       10.36.4.30
erp        IN      A       10.0.8.32
erp        IN      A       10.0.8.33
app        IN      A       10.0.8.32
app        IN      A       10.0.8.33
vpn        IN      A       119.254.116.70
monitor   IN      CNAME   l-core2.ops.bj2.daling.com.
cloud   IN      A	10.36.3.36
test1   IN      A	10.36.4.7
test2   IN      A	10.36.4.6
ors     IN      A       10.0.8.19
cache   IN      CNAME  l-core1.ops.bj1.daling.com.       
*.cache IN CNAME cache.corp.daling.com.
l-radius1	IN	A	10.36.4.22
l-erpdevt	IN	A	10.36.2.7
l-svn		IN	A	10.36.2.170
l-opcpu1	IN	A	10.36.3.37
l-opcpu2	IN	A	10.36.3.39
l-opcpu3	IN	A	10.36.3.38
l-opctl1	IN	A	10.36.3.36
l-opdb2		IN	A	10.36.2.22
upload		IN	A	10.0.20.64
sell-up		IN	A	10.0.3.17

;; other
oauth		IN	A	10.0.8.32
oauth		IN	A	10.0.8.33

pypi		IN	A	10.0.8.32
pypi		IN	A	10.0.8.33

notifycenter		IN	A	10.0.8.32
notifycenter		IN	A	10.0.8.33

erptools		IN	A	10.0.8.32
erptools		IN	A	10.0.8.33

kibana		IN	A	10.0.8.32
kibana		IN	A	10.0.8.33

custom		IN	A	10.0.8.32
custom		IN	A	10.0.8.33

auth		IN	A	10.0.8.32
auth		IN	A	10.0.8.33

hotconfig		IN	A	10.0.8.32
hotconfig		IN	A	10.0.8.33
sip		IN	A	10.36.56.20
voip		IN	A	10.36.56.21

crm		IN	A	10.0.8.32
crm		IN	A	10.0.8.33

api		IN	A	10.0.8.32
api		IN	A	10.0.8.33
passport		IN	A	10.0.8.32
passport		IN	A	10.0.8.33
;; test environment 

a.passport	IN	A	10.36.4.30
b.passport	IN	A	10.36.4.38
c.passport	IN	A	10.36.4.10
*.passport	IN	A	10.36.4.85

soc1		IN	A	10.36.4.32

order		IN	A	10.0.8.32
order		IN	A	10.0.8.33

wx		IN	A	10.0.8.32
wx		IN	A	10.0.8.33

stat		IN	A	10.0.8.32
stat		IN	A	10.0.8.33
netplan		IN	A	10.0.31.16

rsp		IN	A	10.0.8.32
rsp		IN	A	10.0.8.33
oa		IN	A	10.36.4.11

mbr		IN	A	10.0.8.32
mbr		IN	A	10.0.8.33
cc		IN	A	119.254.168.95

slowquery	IN	A	10.0.8.32
slowquery	IN	A	10.0.8.33

dschedule	IN	A	10.0.8.32
dschedule	IN	A	10.0.8.33

npm-registry	IN	A	10.0.8.32
npm-registry	IN	A	10.0.8.33

statdb		IN	A	10.0.8.32
statdb		IN	A	10.0.8.33

tpm.fe		IN	A	10.0.8.32
tpm.fe		IN	A	10.0.8.33

searchtool      IN      A       10.0.20.234
it              IN      A       10.36.2.248
invcost         IN      A       10.0.8.32
invcost         IN      A       10.0.8.33

status-ng         IN      A       10.0.8.32
status-ng         IN      A       10.0.8.33

wallet         IN      A       10.0.8.32
wallet         IN      A       10.0.8.33

etherpad         IN      A       10.0.8.32
etherpad         IN      A       10.0.8.33

sentry         IN      A       10.0.8.32
sentry         IN      A       10.0.8.33
opsdb         IN      A       10.0.8.32
opsdb         IN      A       10.0.8.33
;;tasks for tianfu
app.x		IN	A	10.36.12.120

;;pTTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.bj1.daling.com. root.bj1.daling.com.(
                        2016072101	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.bj1.daling.com.
@       60      IN      NS    b.ns.bj1.daling.com.

$ORIGIN bj1.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156

;;ops business
cloud	IN	A	10.0.3.24
;;proxy 
snort	IN	A	10.0.8.33


$ORIGIN erp.bj1.daling.com.
l-erpreport3	IN	A	10.0.8.34
l-erpreport4	IN	A	10.0.8.35
l-erptools1       IN      A    10.0.8.27
l-erptools2       IN      A    10.0.8.40
l-salesagent1       IN      A    10.0.8.26
l-notifycenter1	IN	A	10.0.8.24
l-notifycenter2	IN	A	10.0.8.39
l-tms2	IN	A	10.0.8.23
l-tms1	IN	A	10.0.8.22
l-erpautotask1	IN	A	10.0.8.21
l-wms1	IN	A	10.0.8.17
l-wms2	IN	A	10.0.8.20
l-erp5 IN	A	10.0.8.36



$ORIGIN ops.bj1.daling.com.
;;network device
csr1	IN 	A 	10.0.3.1
csr2	IN 	A 	10.0.3.254
msr1	IN 	A 	10.0.3.253
st1.b	IN 	A 	172.16.0.3
st1.m	IN 	A 	172.16.0.2
st1.as	IN	A	172.16.0.228

;; prod server
l-tengine1	IN	A	10.0.3.10
l-tengine2	IN	A	10.0.3.11
l-kvm3	IN	A	10.0.3.20
l-kvm4	IN	A	10.0.3.21
l-kvm5	IN	A	10.0.3.24
l-kvm6	IN	A	10.0.3.25
l-kvm7	IN	A	10.0.3.26
l-db1	IN	A	10.0.3.12
l-db2	IN	A	10.0.3.13
l-erpdb1        IN      A       10.0.3.27
l-erpdb2        IN      A       10.0.3.23
l-erpdb3        IN      A       10.0.3.22
l-tools	IN	A	10.0.3.14
l-nginx1	IN	A	10.0.3.15
l-nginx2	IN	A	10.0.3.16
l-mfs1	IN	A	10.0.3.17
l-ngvip1	IN	A	10.0.3.18
l-ngvip2	IN	A	10.0.3.19
l-gpm1		IN	A	10.0.3.36
l-gpm2		IN	A	10.0.3.29
l-gp1		IN	A	10.0.3.30
l-gp2		IN	A	10.0.3.31
l-gp3		IN	A	10.0.3.32
l-gp4		IN	A	10.0.3.33
l-gp5		IN	A	10.0.3.34
l-gp6		IN	A	10.0.3.35
l-core1		IN	A	10.0.3.37
;; prod vm server
l-hadooptest3	IN	A	10.0.8.46
l-hadooptest2	IN	A	10.0.8.44
l-hadooptest1	IN	A	10.0.8.45
l-yadmin	IN	A	10.0.0.6
l-erp1 IN	A	10.0.0.28
l-erp2 IN	A	10.0.0.17
l-erp3 IN	A	10.0.8.13
l-erp4 IN	A	10.0.8.12

l-puppet IN	A	10.0.0.26
l-activemq1 IN	A	10.0.8.8
l-activemq2 IN	A	10.0.8.7
l-activemq3 IN	A	10.0.8.14
l-report1 IN	A	10.0.0.33
l-nagios1	IN	A	10.0.0.32
l-appstat1      IN      A       10.0.8.16
l-kafka1        IN      A    	10.0.8.15
l-zk1	IN	A	10.0.8.25
l-zk2	IN	A	10.0.8.31
l-zk3	IN	A	10.0.8.30
l-statdb1 IN A 10.0.8.28
l-openreport1 IN A 10.0.8.19
l-nginx4	IN	A	10.0.8.10
l-nginx3	IN	A	10.0.8.9
l-opsdev1	IN	A	10.0.8.18
l-dnscache1	IN	A	10.0.8.43
l-dnscache2	IN	A	10.0.8.38
l-localdns1	IN	A	10.0.8.41
l-localdns2	IN	A	10.0.8.42

l-mha3		IN	A	10.0.8.11
l-mha4		IN	A	10.0.8.29

;; ilo server
i-db1 IN A  10.0.4.12
i-db2 IN A  10.0.4.13
i-erpdb1 IN A  10.0.4.27
i-erpdb2 IN A  10.0.4.23
i-erpdb3 IN A  10.0.4.22
i-gp1 IN A  10.0.4.30
i-gp2 IN A  10.0.4.31
i-gp3 IN A  10.0.4.32
i-gp4 IN A  10.0.4.33
i-gp5 IN A  10.0.4.34
i-gp6 IN A  10.0.4.35
i-gpm1 IN A  10.0.4.36
i-gpm2 IN A  10.0.4.29
i-kvm3 IN A  10.0.4.20
i-kvm4 IN A  10.0.4.21
i-kvm5 IN A  10.0.4.24
i-kvm6 IN A  10.0.4.25
i-kvm7 IN A  10.0.4.26
i-mfs1 IN A  10.0.4.17
i-nginx1 IN A  10.0.4.15
i-nginx2 IN A  10.0.4.16
i-tengine1 IN A  10.0.4.10
i-tengine2 IN A  10.0.4.11
i-tools IN A  10.0.4.14
i-core1 IN A  10.0.4.37


;; network area
l-jxqas01	IN	A	10.0.3.252
l-jxqhx02	IN	A	10.0.3.254
l-jxqhx01	IN	A	10.0.3.2
l-jxqmsr02 	IN	A	10.0.3.251

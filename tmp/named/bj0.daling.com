;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.bj0.daling.com. root.bj0.daling.com.(
                        2016081701	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.bj0.daling.com.
@       60      IN      NS    b.ns.bj0.daling.com.

$ORIGIN bj0.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156
l-uc1.stage	IN	A	10.36.4.102
l-uc2.stage	IN	A	10.36.4.103
cloud		IN	A	10.36.3.36

;; ops.bj0.daling.com
$ORIGIN ops.bj0.daling.com.
l-smokeping1	IN	A	10.36.4.145
l-pushtest1	IN	A	10.36.4.144
l-localdns5	IN	A	10.36.4.137
l-opstest1	IN	A	10.36.4.135
l-optest	IN	A	10.36.99.3
l-qatools  IN	A	10.36.4.85
l-task1	  IN    A       10.36.4.61
l-qa1     IN	A	10.36.4.30
l-qa2     IN	A	10.36.4.38
l-qa3     IN	A	10.36.4.10
l-hadooptest1 IN	A	10.36.4.141
l-hadooptest2 IN	A	10.36.4.142
l-hadooptest3 IN	A	10.36.4.143
	
l-opdb2   IN	A	10.36.2.22
l-opcpu2  IN    A       10.36.3.39 
l-opcpu3  IN    A       10.36.3.38

l-pgtest1 IN	A	10.36.4.39
l-pgtest2 IN	A	10.36.4.40

l-nginx1  IN	A	10.36.4.77
l-cacti1  IN	A	10.36.4.94
l-cacti19  IN	A	10.36.4.199

l-testdb1	IN	A	10.36.4.5
l-testdb2	IN	A	10.36.4.44
l-testdb3	IN	A	10.36.4.45
l-testdb4	IN	A	10.36.4.46

l-tengine1	IN	A	10.36.4.48
l-tengine2	IN	A	10.36.4.60

l-rabbitmq1	IN	A	10.36.4.50
l-rabbitmq2	IN	A	10.36.4.51
l-rabbitmq3	IN	A	10.36.4.52
l-solr1   	IN	A	10.36.4.53
l-solr2   	IN	A	10.36.4.59

l-fedev1        IN	A	10.36.4.54
l-fedev2        IN	A	10.36.4.55
l-fedev3        IN	A	10.36.4.56

l-oa1		IN	A	10.36.4.65

l-opsdev1	IN	A	10.36.4.74
l-opsdev2	IN	A	10.36.4.73
l-opsdev3	IN	A	10.36.4.36
l-opsdev4	IN	A	10.36.4.68
l-opsdev5	IN	A	10.36.4.69
l-opsdev6	IN	A	10.36.4.70
l-opsdev7	IN	A	10.36.4.71
l-opsdev8	IN	A	10.36.4.98
l-opsdev9	IN	A	10.36.4.99
l-opsdev10	IN	A	10.36.4.101
l-opsdev11	IN	A	10.36.4.102
l-opsdev12	IN	A	10.36.4.103
l-opsdev13	IN	A	10.36.4.133
l-opsdev14	IN	A	10.36.4.131
l-opsdev15	IN	A	10.36.4.132
l-opsdev16	IN	A	10.36.4.136

l-datadev1	IN	A	10.36.4.100
l-vrmupload1	IN	A	10.36.4.134

l-coupondb1	IN	A	10.36.4.126
l-coupondb2	IN	A	10.36.4.127
l-hbtest	IN	A	10.36.4.104
l-dnscache1	IN	A	10.36.4.105
l-dnscache2	IN	A	10.36.4.155

l-hd1		IN	A	10.36.4.135
l-hd2		IN	A	10.36.4.137
l-hd3		IN	A	10.36.4.138


;; kvm-server
l-opcpu4	IN	A	10.36.3.40
l-opcpu5	IN	A	10.36.3.41
l-opcpu6	IN	A	10.36.3.42
l-opcpu7	IN	A	10.36.3.43
l-opcpu8 	IN	A	10.36.2.21




;; qa.bj0.daling.com
$ORIGIN qa.bj0.daling.com.
l-php1   	IN    	A       10.36.4.42
l-php2   	IN    	A       10.36.4.41
l-php3   	IN    	A       10.36.4.43
l-php4    	IN    	A       10.36.4.49
l-php5    	IN    	A       10.36.4.92
l-php6    	IN    	A       10.36.4.93
l-cache1	IN	A	10.36.4.66
l-solr1		IN	A	10.36.4.67
l-solr2		IN	A	10.36.4.72

l-jenkins1    IN    A       10.36.4.57

l-qa13		IN	A	10.36.4.12
l-qa14		IN	A	10.36.4.27
l-qa15		IN	A	10.36.4.28
l-qa16		IN	A	10.36.4.29
l-qa17		IN	A	10.36.4.31
l-qa18		IN	A	10.36.4.32
l-qa19		IN	A	10.36.4.33
l-qa20		IN	A	10.36.4.34
l-qa21		IN	A	10.36.4.108
l-qa22		IN	A	10.36.4.109
l-qa23		IN	A	10.36.4.110
l-qa24		IN	A	10.36.4.111
l-qa25		IN	A	10.36.4.112
l-qa26		IN	A	10.36.4.113
l-qa27		IN	A	10.36.4.114
l-qa28		IN	A	10.36.4.115
l-qa29		IN	A	10.36.4.116
l-qa30		IN	A	10.36.4.117
l-qa31		IN	A	10.36.4.118
l-qa32		IN	A	10.36.4.119
l-qa33		IN	A	10.36.4.120
l-qa34		IN	A	10.36.4.121
l-qa35		IN	A	10.36.4.122
l-qa36		IN	A	10.36.4.123
l-qa37		IN	A	10.36.4.124
l-qa38		IN	A	10.36.4.125
l-qa39		IN	A	10.36.4.128
l-qa40		IN	A	10.36.4.129


l-oldererp	IN	A	10.36.4.84


;; prod.bj0.daling.com
$ORIGIN prod.bj0.daling.com.
l-nginx          IN      A       10.36.4.86
l-solr           IN      A       10.36.4.87
l-cache          IN      A       10.36.4.88
l-uc             IN      A       10.36.4.89
l-rabbitmq       IN      A       10.36.4.90
l-php1           IN      A       10.36.4.96
l-php2           IN      A       10.36.4.78
l-php3           IN      A       10.36.4.91
l-php4           IN      A       10.36.4.97
;;dev.bj0.daling.com
$ORIGIN dev.bj0.daling.com.
l-phpdev1	IN	A	10.36.4.130

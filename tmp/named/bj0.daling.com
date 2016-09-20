$ORIGIN .
$TTL 60	; 1 minute
bj0.daling.com		IN SOA	a.ns.bj0.daling.com. root.bj0.daling.com. (
				2016081762 ; serial
				3600       ; refresh (1 hour)
				900        ; retry (15 minutes)
				3600000    ; expire (5 weeks 6 days 16 hours)
				3600       ; minimum (1 hour)
				)
			NS	a.ns.bj0.daling.com.
			NS	b.ns.bj0.daling.com.
$ORIGIN bj0.daling.com.
cloud			A	10.36.3.36
l-phpdev1.dev		A	10.36.4.130
$ORIGIN ns.bj0.daling.com.
a			A	119.254.119.155
b			A	119.254.119.156
$ORIGIN ops.bj0.daling.com.
l-cacti1		A	10.36.4.94
l-cacti19		A	10.36.4.199
l-coupondb1		A	10.36.4.126
l-coupondb2		A	10.36.4.127
l-datadev1		A	10.36.4.100
l-dnscache1		A	10.36.4.105
l-dnscache2		A	10.36.4.155
l-fedev1		A	10.36.4.54
l-fedev2		A	10.36.4.55
l-fedev3		A	10.36.4.56
l-hadooptest1		A	10.36.4.141
l-hadooptest2		A	10.36.4.142
l-hadooptest3		A	10.36.4.143
l-hbtest		A	10.36.4.104
l-hd1			A	10.36.4.135
l-hd2			A	10.36.4.137
l-hd3			A	10.36.4.138
l-localdns5		A	10.36.4.137
l-nginx1		A	10.36.4.77
l-oa1			A	10.36.4.65
l-opcpu2		A	10.36.3.39
l-opcpu3		A	10.36.3.38
l-opcpu4		A	10.36.3.40
l-opcpu5		A	10.36.3.41
l-opcpu6		A	10.36.3.42
l-opcpu7		A	10.36.3.43
l-opcpu8		A	10.36.2.21
l-opdb2			A	10.36.2.22
l-opsdev1		A	10.36.4.74
l-opsdev10		A	10.36.4.101
l-opsdev11		A	10.36.4.102
l-opsdev12		A	10.36.4.103
l-opsdev13		A	10.36.4.133
l-opsdev14		A	10.36.4.131
l-opsdev15		A	10.36.4.132
l-opsdev16		A	10.36.4.136
l-opsdev2		A	10.36.4.73
l-opsdev3		A	10.36.4.36
l-opsdev4		A	10.36.4.68
l-opsdev5		A	10.36.4.69
l-opsdev6		A	10.36.4.70
l-opsdev7		A	10.36.4.71
l-opsdev8		A	10.36.4.98
l-opsdev9		A	10.36.4.99
l-opstest1		A	10.36.4.135
l-optest		A	10.36.99.3
l-pgtest1		A	10.36.4.39
l-pgtest2		A	10.36.4.40
l-pushtest1		A	10.36.4.144
l-qa1			A	10.36.4.30
l-qa2			A	10.36.4.38
l-qa3			A	10.36.4.10
l-qatools		A	10.36.4.85
l-rabbitmq1		A	10.36.4.50
l-rabbitmq2		A	10.36.4.51
l-rabbitmq3		A	10.36.4.52
l-smokeping1		A	10.36.4.145
l-solr1			A	10.36.4.53
l-solr2			A	10.36.4.59
l-task1			A	10.36.4.61
l-tengine1		A	10.36.4.48
l-tengine2		A	10.36.4.60
l-testdb1		A	10.36.4.5
l-testdb2		A	10.36.4.44
l-testdb3		A	10.36.4.45
l-testdb4		A	10.36.4.46
l-vrmupload1		A	10.36.4.134
$ORIGIN prod.bj0.daling.com.
l-cache			A	10.36.4.88
l-nginx			A	10.36.4.86
l-php1			A	10.36.4.96
l-php2			A	10.36.4.78
l-php3			A	10.36.4.91
l-php4			A	10.36.4.97
l-rabbitmq		A	10.36.4.90
l-solr			A	10.36.4.87
l-uc			A	10.36.4.89
$ORIGIN qa.bj0.daling.com.
l-cache1		A	10.36.4.66
l-jenkins1		A	10.36.4.57
l-oldererp		A	10.36.4.84
l-php1			A	10.36.4.42
l-php2			A	10.36.4.41
l-php3			A	10.36.4.43
l-php4			A	10.36.4.49
l-php5			A	10.36.4.92
l-php6			A	10.36.4.93
l-qa13			A	10.36.4.12
l-qa14			A	10.36.4.27
l-qa15			A	10.36.4.28
l-qa16			A	10.36.4.29
l-qa17			A	10.36.4.31
l-qa18			A	10.36.4.32
l-qa19			A	10.36.4.33
l-qa20			A	10.36.4.34
l-qa21			A	10.36.4.108
l-qa22			A	10.36.4.109
l-qa23			A	10.36.4.110
l-qa24			A	10.36.4.111
l-qa25			A	10.36.4.112
l-qa26			A	10.36.4.113
l-qa27			A	10.36.4.114
l-qa28			A	10.36.4.115
l-qa29			A	10.36.4.116
l-qa30			A	10.36.4.117
l-qa31			A	10.36.4.118
l-qa32			A	10.36.4.119
l-qa33			A	10.36.4.120
l-qa34			A	10.36.4.121
l-qa35			A	10.36.4.122
l-qa36			A	10.36.4.123
l-qa37			A	10.36.4.124
l-qa38			A	10.36.4.125
l-qa39			A	10.36.4.128
l-qa40			A	10.36.4.129
l-solr1			A	10.36.4.67
l-solr2			A	10.36.4.72
$ORIGIN stage.bj0.daling.com.
l-uc1			A	10.36.4.102
l-uc2			A	10.36.4.103

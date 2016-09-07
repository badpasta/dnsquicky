;;$TTL 1800      ; 1 day
$TTL 60
@                    IN SOA  a.ns.bj2.daling.com. root.bj2.daling.com.(
                        2016080101	; Serial
                        3600            ; Refresh (1 hour)
                        900             ; Retry (15 minutes)
                        3600000         ; Expire (5 weeks 6 days 16 hours)
                        3600            ; Minimum (1 hour)
                        )
@       60      IN      NS    a.ns.bj2.daling.com.
@       60      IN      NS    b.ns.bj2.daling.com.

$ORIGIN bj2.daling.com.

;; glue records
a.ns IN A 119.254.119.155
b.ns IN A 119.254.119.156

cloud		IN		CNAME	l-kvm8.ops.bj2.daling.com.
$ORIGIN daling.com.

$ORIGIN ops.bj2.daling.com.

l-pushmaster4	IN		A	10.0.26.176
l-pushmaster5	IN		A	10.0.26.177
l-pushmaster3	IN		A	10.0.26.173
l-pushmaster2	IN		A	10.0.26.169
l-pushagent4	IN		A	10.0.26.170
l-pushagent5	IN		A	10.0.26.171
l-pushagent6	IN		A	10.0.26.172
l-pushagent3	IN		A	10.0.26.168
l-pushmaster1	IN		A	10.0.26.167
l-captcha2	IN		A	10.0.26.166
l-captcha1	IN		A	10.0.26.165
l-jenkins	IN		A	10.0.20.13
l-vpnauth	IN		A	10.0.26.144
l-gitlab1	IN		A	10.0.26.26
l-wiki1		IN		A	10.0.26.28
l-erpdb4 	IN	 	A	10.0.24.11
l-db3 		IN	 	A	10.0.24.13
l-db4 		IN	 	A	10.0.24.14
l-db5 		IN	 	A	10.0.24.15
l-db6 		IN	 	A	10.0.24.16
l-db7 		IN	 	A	10.0.24.17
l-db8 		IN	 	A	10.0.24.18
l-db9		IN	 	A	10.0.24.19
l-db10 		IN	 	A	10.0.24.20
l-db11 		IN	 	A	10.0.24.21
l-db12 		IN	 	A	10.0.24.22
l-db13 		IN	 	A	10.0.24.23
l-erpdb6 		IN	 	A	10.0.24.24
l-erpdb7 		IN	 	A	10.0.24.25
l-erpdb8		IN		A	10.0.24.33
l-core2 	IN	 	A	10.0.31.16
l-hd5 		IN	 	A	10.0.25.11
l-hd6 		IN	 	A	10.0.25.12
l-hd3 		IN	 	A	10.0.25.13
l-hd4 		IN	 	A	10.0.25.14
l-hd1 		IN	 	A	10.0.25.15
l-hd2 		IN	 	A	10.0.25.16
l-kvm8 		IN	 	A	10.0.16.11
l-kvm9 		IN	 	A	10.0.16.12
l-kvm10 	IN	 	A	10.0.16.13
l-kvm11 	IN	 	A	10.0.16.14
l-kvm12 	IN	 	A	10.0.16.15
l-kvm13 	IN	 	A	10.0.16.16
l-kvm14 	IN	 	A	10.0.16.17
l-kvm15 	IN	 	A	10.0.16.18
l-kvm16 	IN	 	A	10.0.16.19
l-kvm17 	IN	 	A	10.0.16.20
l-kvm18 	IN	 	A	10.0.16.21
l-kvm19 	IN	 	A	10.0.16.22
l-kvm20 	IN	 	A	10.0.16.23
l-kvm21 	IN	 	A	10.0.16.24
l-kvm22 	IN	 	A	10.0.16.25
l-kvm23 	IN	 	A	10.0.16.26
l-kvm24 	IN	 	A	10.0.16.27
l-kvm25 	IN	 	A	10.0.16.28
l-kvm26 	IN	 	A	10.0.16.29
l-kvm27 	IN	 	A	10.0.16.30
l-kvm28 	IN	 	A	10.0.16.31
l-kvm29 	IN	 	A	10.0.16.32
l-kvm30 	IN	 	A	10.0.16.33
l-kvm31 	IN	 	A	10.0.16.34
l-kvm32		IN	 	A	10.0.16.35
l-kvm33		IN	 	A	10.0.16.36
l-kvm34		IN	 	A	10.0.16.37
l-kvm37		IN	 	A	10.0.16.40
l-kvm40		IN	 	A	10.0.16.43
l-kvm41		IN	 	A	10.0.16.44
l-kvm42		IN	 	A	10.0.16.45
l-pxetest		IN	 	A	10.0.16.38
l-tpm           IN              A       10.0.20.235
l-prestodb2	IN	 	A	10.0.16.39
l-prestodb3	IN	 	A	10.0.16.41
l-prestodb4	IN	 	A	10.0.16.42
l-hb1		IN		A	10.0.25.17
l-hb2		IN		A	10.0.25.18
l-hb3		IN		A	10.0.25.19
l-hb4		IN		A	10.0.25.20
l-hb5		IN		A	10.0.25.21
l-hb6		IN		A	10.0.16.63
l-db14		IN		A	10.0.24.26
l-db15		IN		A	10.0.24.27
l-db16  	IN	 	A	10.0.24.12
l-kvm50		IN		A	10.0.16.53
l-kvm51		IN		A	10.0.16.54
l-kvm48		IN		A	10.0.16.51
l-kvm49		IN		A	10.0.16.52
l-db17		IN		A	10.0.24.28
l-db18		IN		A	10.0.24.29
l-db19		IN		A	10.0.24.30
l-db20		IN		A	10.0.24.31
l-db21		IN		A	10.0.24.32
l-kvm43		IN		A	10.0.16.46
l-kvm44		IN		A	10.0.16.47
l-kvm45		IN		A	10.0.16.48
l-kvm46		IN		A	10.0.16.49
l-kvm47		IN		A	10.0.16.50
l-tengine3	IN		A	10.0.31.17
l-tengine4	IN		A	10.0.31.18
l-tengine5	IN		A	10.0.31.19
l-tengine6	IN		A	10.0.31.20
l-kvm52		IN		A	10.0.16.55
l-kvm53		IN		A	10.0.16.56
l-kvm54		IN		A	10.0.16.57
l-kvm55		IN		A	10.0.16.58
l-kvm56		IN		A	10.0.16.59
l-codis2		IN		A	10.0.16.60
l-kvm58		IN		A	10.0.16.61
l-kvm59		IN		A	10.0.16.62
l-kvm60		IN		A	10.0.16.63
l-codis1		IN		A	10.0.16.64
l-kvm62		IN		A	10.0.16.65
l-tengine7		IN		A	10.0.31.21
l-tengine8		IN		A	10.0.31.22
l-db23		IN		A	10.0.24.34
l-db24		IN		A	10.0.24.35
l-db25		IN		A	10.0.24.36
l-db26		IN		A	10.0.24.37
l-sentry	IN		A	10.0.26.88
l-opsdb		IN		A	10.0.26.100



;;vm-server
l-pushagent1	IN		A	10.0.20.90
l-pushagent2	IN		A	10.0.20.82
l-eauth1	IN		A	10.0.20.92
l-eauth2	IN		A	10.0.20.94
l-devdb1	IN		A	10.0.20.3
l-devphp1	IN		A	10.0.20.7
l-php1		IN		A	10.0.20.208
l-php2		IN		A	10.0.20.36
l-php3		IN		A	10.0.20.37
l-php4		IN		A	10.0.20.38
l-php5		IN		A	10.0.20.40
l-php6		IN		A	10.0.20.41
l-php7		IN		A	10.0.20.42
l-php8		IN		A	10.0.20.58
l-php9		IN		A	10.0.20.59
l-php10		IN		A	10.0.20.153
l-php11		IN		A	10.0.20.163
l-php12		IN		A	10.0.20.164
l-php13		IN		A	10.0.20.168
l-php14		IN		A	10.0.20.10
l-php15		IN		A	10.0.20.16
l-php16		IN		A	10.0.20.197
l-php17		IN		A	10.0.20.199
l-php18		IN		A	10.0.20.14
l-php19		IN		A	10.0.20.17
l-php20		IN		A	10.0.20.15
l-php21		IN		A	10.0.20.19
l-php22		IN		A	10.0.20.29
l-php23		IN		A	10.0.20.20
l-php24		IN		A	10.0.20.21
l-php25		IN		A	10.0.20.24
l-php26		IN		A	10.0.20.25
l-php27		IN		A	10.0.20.23
l-php28		IN		A	10.0.20.26
l-php29		IN		A	10.0.20.31
l-php30		IN		A	10.0.20.27
l-php31		IN		A	10.0.20.28
l-php32		IN		A	10.0.20.5
l-yadmin1	IN		A	10.0.20.232
l-etl1		IN		A	10.0.20.35
l-upload1	IN		A	10.0.20.64
l-upload2	IN		A	10.0.20.221

l-channel1	IN		A	10.0.20.12
l-channel2	IN		A	10.0.20.18

l-erp1		IN		A	10.0.20.254
l-erp2		IN		A	10.0.26.6
l-wms1		IN		A	10.0.26.36
l-wms2		IN		A	10.0.26.37

l-rabbitmq1	IN		A	10.0.20.48
l-rabbitmq2	IN		A	10.0.20.49
l-rabbitmq3	IN		A	10.0.20.50
l-rabbitmq4	IN		A	10.0.26.155
l-rabbitmq5	IN		A	10.0.26.156
l-rabbitmq6	IN		A	10.0.26.158

l-credis1	IN		A	10.0.20.51
l-credis2	IN		A	10.0.20.52
l-credis3	IN		A	10.0.20.54
l-credis4	IN		A	10.0.20.53
l-credis5	IN		A	10.0.20.56
l-credis6	IN		A	10.0.20.57

l-zk1		IN		A	10.0.26.83
l-zk2		IN		A	10.0.26.97
l-zk3		IN		A	10.0.26.98

l-point1	IN		A	10.0.20.176
l-point2	IN		A	10.0.20.177
l-report2	IN		A	10.0.20.174
l-report3	IN		A	10.0.20.173

l-varnish1	IN		A	10.0.20.186
l-varnish2	IN		A	10.0.20.187

l-auditor1	IN		A	10.0.20.213
l-auditor2	IN		A	10.0.26.48
	

l-qp1		IN		A	10.0.20.60
l-qp2		IN		A	10.0.20.63

l-radius	IN		A	10.0.20.65
l-pypi1		IN		A	10.0.20.66
l-pyapp1	IN		A	10.0.20.67
l-pyapp2	IN		A	10.0.20.68

l-push1		IN		A	10.0.20.69		
l-push2		IN		A	10.0.20.70

l-smartpush1	IN		A	10.0.20.71
l-smartpush2	IN		A	10.0.20.72

l-uc1           IN              A       10.0.20.9
l-uc2           IN              A       10.0.20.43
l-uc3           IN              A       10.0.20.159
l-uc4           IN              A       10.0.20.161
l-uc5           IN              A       10.0.26.22
l-uc6           IN              A       10.0.26.23
l-uc7           IN              A       10.0.26.24
l-uc8           IN              A       10.0.26.25
l-uc9		IN		A	10.0.26.74
l-uc10		IN		A	10.0.26.75
l-uc11		IN		A	10.0.26.76
l-uc12		IN		A	10.0.26.77
l-uc13		IN		A	10.0.26.78
l-uc14		IN		A	10.0.26.79
l-uc15		IN		A	10.0.26.80

l-dnscache3	IN		A	10.0.20.222
l-dnscache4	IN		A	10.0.20.224
l-localdns3	IN		A	10.0.26.116
l-localdns4	IN		A	10.0.26.117
l-localdns6	IN		A	10.0.26.147

l-kafka1	IN		A	10.0.20.236
l-kafka2	IN		A	10.0.20.34
l-kafka3	IN		A	10.0.20.73

l-elastic1	IN		A	10.0.20.32
l-elastic2	IN		A	10.0.26.35
l-logstash1	IN		A	10.0.20.39
l-logstash2     IN		A	10.0.20.149
l-kibana1       IN		A	10.0.20.237
l-ngelk1	IN		A	10.0.26.81

l-zin1		IN		A	10.0.20.76
l-zin2		IN		A	10.0.20.61
l-zin3		IN		A	10.0.20.62
l-zin4		IN		A	10.0.20.44
l-zin5		IN		A	10.0.20.45

l-zinstat1	IN		A	10.0.20.166
l-zinstat2	IN		A	10.0.20.167
l-zinstatpy1	IN		A	10.0.20.200


l-ucdbsync3     IN		A	10.0.26.86
l-cartsync1     IN		A	10.0.20.22
l-cartsync2     IN		A	10.0.26.88

l-cart1         IN		A	10.0.26.95
l-cart2         IN		A	10.0.26.96
l-cart3         IN		A	10.0.26.84
l-cart4         IN		A	10.0.26.85
l-cart5         IN		A	10.0.26.90
l-cart6         IN		A	10.0.26.91
l-cart7         IN		A	10.0.26.93
l-cart8         IN		A	10.0.26.94
l-cart9         IN		A	10.0.26.70
l-cart10        IN		A	10.0.26.72
l-cart11        IN		A	10.0.26.73
l-cart12        IN		A	10.0.26.112
l-cart13        IN		A	10.0.26.113
l-cart14        IN		A	10.0.26.114
l-cart15        IN		A	10.0.26.115
l-cart16        IN              A       10.0.20.189
l-cart17        IN              A       10.0.20.192
l-cart18        IN              A       10.0.20.194
l-cart19        IN              A       10.0.20.195
l-cart20        IN              A       10.0.20.196
l-cart21        IN              A       10.0.20.198
l-cart22        IN              A       10.0.26.39
l-cart23        IN              A       10.0.26.41
l-cart24        IN              A       10.0.26.44
l-cart25        IN              A       10.0.26.47
l-cart26        IN              A       10.0.26.50
l-cart27        IN              A       10.0.26.52
l-cart28        IN              A       10.0.26.54
l-cart29        IN              A       10.0.26.56
l-cart30        IN              A       10.0.26.58



l-paycenter1	IN A 10.0.20.142
l-paycenter2	IN A 10.0.20.143
l-paycenter3	IN A 10.0.20.144
l-paycenter4	IN A 10.0.20.145
l-paycenter5	IN A 10.0.20.146
l-paycenter6	IN A 10.0.20.182
l-paycenter7	IN A 10.0.20.184
l-paycenter8	IN A 10.0.20.190
l-mem6 IN A 10.0.20.137
l-mem7 IN A 10.0.20.138
l-mem8 IN A 10.0.20.139
l-mem9 IN A 10.0.20.140
l-mem10 IN A 10.0.20.141

l-solr1 IN A 10.0.20.178
l-solr2 IN A 10.0.20.179
l-solr3 IN A 10.0.20.147
l-solr4 IN A 10.0.20.170
l-solr5 IN A 10.0.26.106
l-solr6 IN A 10.0.26.107
l-solr7 IN A 10.0.26.108
l-solr8 IN A 10.0.26.109
l-pysolr IN A 10.0.20.234
l-invcost1	IN A 10.0.20.238
l-invcost2	IN A 10.0.20.239

l-buffer1 IN A 10.0.26.137
l-buffer2 IN A 10.0.26.138
l-buffer3 IN A 10.0.26.139
l-buffer4 IN A 10.0.26.140
l-buffer5 IN A 10.0.26.110
l-buffer6 IN A 10.0.26.111
l-buffer7 IN A 10.0.26.135
l-buffer8 IN A 10.0.26.136

l-sms1	IN	A	10.0.20.229
l-sms2	IN	A	10.0.20.230
l-sms3	IN	A	10.0.20.74
l-sms4	IN	A	10.0.26.87
l-sms5	IN	A	10.0.26.82

l-php33 IN A 10.0.20.77
l-php34 IN A 10.0.20.79
l-php35 IN A 10.0.26.16
l-php36 IN A 10.0.20.84
l-php37 IN A 10.0.20.86
l-php38 IN A 10.0.20.87
l-php39 IN A 10.0.20.88
l-php40 IN A 10.0.20.89
l-php41 IN A 10.0.26.19
l-php42 IN A 10.0.20.91
l-php43 IN A 10.0.26.20
l-php44 IN A 10.0.20.93
l-php45 IN A 10.0.26.21
l-php46 IN A 10.0.20.95
l-php47 IN A 10.0.20.96
l-php48 IN A 10.0.20.97
l-php49 IN A 10.0.20.98
l-php50 IN A 10.0.20.99
l-php51 IN A 10.0.20.100
l-php52 IN A 10.0.20.101
l-php53 IN A 10.0.20.102
l-php54 IN A 10.0.20.103
l-php55 IN A 10.0.20.104
l-php56 IN A 10.0.20.105
l-php57 IN A 10.0.20.106
l-php58 IN A 10.0.20.148
l-php59 IN A 10.0.20.107
l-php60 IN A 10.0.20.109
l-php61 IN A 10.0.20.110
l-php62 IN A 10.0.20.111
l-php63 IN A 10.0.20.112
l-php64 IN A 10.0.20.114
l-php65 IN A 10.0.20.115
l-php66 IN A 10.0.20.116
l-php67 IN A 10.0.20.117
l-php68 IN A 10.0.20.118
l-php69 IN A 10.0.20.120
l-php70 IN A 10.0.20.121
l-php71 IN A 10.0.20.122
l-php72 IN A 10.0.20.123
l-php73 IN A 10.0.20.124
l-php74 IN A 10.0.20.125
l-php75 IN A 10.0.20.127
l-php76 IN A 10.0.20.128
l-php77 IN A 10.0.20.129
l-php78 IN A 10.0.20.130
l-php79 IN A 10.0.20.131
l-php80 IN A 10.0.20.133
l-php81 IN A 10.0.20.134
l-php82 IN A 10.0.20.135
l-php83 IN A 10.0.20.136
l-php84 IN A         10.0.20.201 
l-php85 IN A         10.0.20.202 
l-php86 IN A         10.0.20.203 
l-php87 IN A         10.0.20.204 
l-php88 IN A         10.0.20.205 
l-php89 IN A         10.0.20.206 
l-php90 IN A         10.0.20.207 
l-yadmin3	IN	A	10.0.20.150
l-prestodev	IN	A	10.0.20.219	
l-etherpad	IN	A	10.0.26.127

l-vcodis1	IN	A	10.0.20.214
l-vcodis2	IN	A	10.0.20.217
l-vcodis3	IN	A	10.0.20.223


l-vrm1		IN	A	10.0.26.29
l-vrm2		IN	A	10.0.26.30
l-midsolr1	IN	A	10.0.26.31
l-midsolr2	IN	A	10.0.26.32

l-alert1	IN	A	10.0.26.33
l-alert2	IN	A	10.0.26.34
l-dschedule1	IN	A	10.0.20.227
l-dschedule2	IN	A	10.0.20.228
l-npm1		IN	A	10.0.20.231

l-rdrbd1	IN	A	10.0.20.151
l-rdrbd2	IN	A	10.0.20.152


l-mha1		IN	A	10.0.20.154
l-mha2		IN	A	10.0.20.156

l-recommend1	IN	A	10.0.20.157
l-recommend2	IN	A	10.0.20.155

l-app1	        IN	A	10.0.20.158
l-app2          IN	A	10.0.20.160
l-zintask	IN	A	10.0.20.165
l-slowquery1	IN	A	10.0.20.181

;; newvlan vm server
l-img1		IN	A	10.0.26.10
l-img2		IN	A	10.0.26.8
l-crm1		IN	A	10.0.26.14
l-crm2		IN	A	10.0.26.15

l-taxzz		IN	A	10.0.26.17
l-taxsz		IN	A	10.0.26.18


;;ilo server
i-core2 IN A  10.0.18.16
i-db10 IN A  10.0.18.50
i-db11 IN A  10.0.18.51
i-db12 IN A  10.0.18.52
i-db13 IN A  10.0.18.53
i-db3 IN A  10.0.18.13
i-db4 IN A  10.0.18.14
i-db5 IN A  10.0.18.15
i-db6 IN A  10.0.18.46
i-db7 IN A  10.0.18.47
i-db8 IN A  10.0.18.48
i-db9 IN A  10.0.18.49
i-erpdb4 IN A  10.0.18.11
i-erpdb6 IN A  10.0.18.54
i-erpdb7 IN A  10.0.18.55
i-hd1 IN A  10.0.18.21
i-hd2 IN A  10.0.18.22
i-hd3 IN A  10.0.18.19
i-hd4 IN A  10.0.18.20
i-hd5 IN A  10.0.18.17
i-hd6 IN A  10.0.18.18
i-kvm10 IN A  10.0.18.25
i-kvm11 IN A  10.0.18.26
i-kvm12 IN A  10.0.18.27
i-kvm13 IN A  10.0.18.28
i-kvm14 IN A  10.0.18.29
i-kvm15 IN A  10.0.18.30
i-kvm16 IN A  10.0.18.31
i-kvm17 IN A  10.0.18.32
i-kvm18 IN A  10.0.18.33
i-kvm19 IN A  10.0.18.34
i-kvm20 IN A  10.0.18.35
i-kvm21 IN A  10.0.18.36
i-kvm22 IN A  10.0.18.37
i-kvm23 IN A  10.0.18.38
i-kvm24 IN A  10.0.18.39
i-kvm25 IN A  10.0.18.40
i-kvm26 IN A  10.0.18.41
i-kvm27 IN A  10.0.18.42
i-kvm28 IN A  10.0.18.43
i-kvm29 IN A  10.0.18.44
i-kvm30 IN A  10.0.18.45
i-kvm31 IN A  10.0.18.56
i-kvm32 IN A  10.0.18.57
i-kvm33 IN A  10.0.18.58
i-kvm34 IN A  10.0.18.59
i-kvm37 IN A  10.0.18.62
i-kvm40 IN A  10.0.18.65
i-kvm41 IN A  10.0.18.66
i-kvm42 IN A  10.0.18.67
i-kvm8 IN A  10.0.18.23
i-kvm9 IN A  10.0.18.24
i-prestodb2 IN A  10.0.18.61
i-prestodb3 IN A  10.0.18.63
i-prestodb4 IN A  10.0.18.64
i-pxetest IN A  10.0.18.60
i-hb1		IN		A	10.0.18.68
i-hb2		IN		A	10.0.18.69
i-hb3		IN		A	10.0.18.70
i-hb4		IN		A	10.0.18.71
i-hb5		IN		A	10.0.18.72
i-hb6		IN		A	10.0.18.106
i-db14		IN		A	10.0.18.73
i-db15		IN		A	10.0.18.74
i-db16		IN  		A  	10.0.18.12
i-kvm50		IN		A	10.0.18.75
i-kvm51		IN		A	10.0.18.76
i-kvm48		IN		A	10.0.18.77
i-kvm49		IN		A	10.0.18.78
i-db17		IN		A	10.0.18.79
i-db18		IN		A	10.0.18.80
i-db19		IN		A	10.0.18.81
i-db20		IN		A	10.0.18.82
i-db21		IN		A	10.0.18.83
i-kvm43		IN		A	10.0.18.84
i-kvm44		IN		A	10.0.18.85
i-kvm45		IN		A	10.0.18.86
i-kvm46		IN		A	10.0.18.87
i-kvm47		IN		A	10.0.18.88
i-tengine3 IN A  10.0.18.89
i-tengine4 IN A  10.0.18.90
i-tengine5 IN A  10.0.18.91
i-tengine6 IN A  10.0.18.92
i-kvm52 IN A  10.0.18.93
i-kvm53 IN A  10.0.18.94
i-kvm54 IN A  10.0.18.95
i-kvm55 IN A  10.0.18.96
i-kvm56 IN A  10.0.18.97
i-codis2 IN A  10.0.18.98
i-erpdb8 IN A  10.0.18.99
i-db23 IN A  10.0.18.100
i-db24 IN A  10.0.18.101
i-db25 IN A  10.0.18.102
i-db26 IN A  10.0.18.103
i-kvm58 IN A  10.0.18.104
i-kvm59 IN A  10.0.18.105
i-kvm60 IN A  10.0.18.106
i-codis1 IN A  10.0.18.107
i-kvm62 IN A  10.0.18.108
i-tengine7 IN A  10.0.18.109
i-tengine8 IN A  10.0.18.110




;;Network service
l-yjhx01	IN		A	10.0.30.2
l-yjhx02	IN		A	10.0.30.3
l-yjac01	IN		A	10.0.30.4
l-yjac02	IN		A	10.0.30.5
l-yjac03	IN		A	10.0.30.6
l-yjac04	IN		A	10.0.30.7
l-yjac05	IN		A	10.0.30.8
l-yjac06	IN		A	10.0.30.9
l-yjac07	IN		A	10.0.30.10
l-yjac08	IN		A	10.0.30.11
l-yjac09	IN		A	10.0.30.12
l-yjac10	IN		A	10.0.30.13
l-yjac11	IN		A	10.0.30.14
l-yjac12	IN		A	10.0.30.15
l-yjisp01	IN		A	10.0.30.201
l-yjisp02	IN		A	10.0.30.202
l-yjmsr01	IN		A	119.254.119.148
l-yjmsr02	IN		A	119.254.119.149

$ORIGIN app.bj2.daling.com.
l-innerproxy1	IN		A	10.0.26.151
l-innerproxy2	IN		A	10.0.26.152
l-innerproxy3	IN		A	10.0.26.146
l-innerproxy4	IN		A	10.0.26.153
l-coupon8	IN		A	10.0.26.143
l-coupon7	IN		A	10.0.26.142
l-coupon6	IN		A	10.0.26.141
l-coupon5	IN		A	10.0.26.140
l-coupon4	IN		A	10.0.26.136
l-coupon3	IN		A	10.0.26.135
l-coupon2	IN		A	10.0.26.111
l-coupon1	IN		A	10.0.26.110
l-tdapi1	IN		A	10.0.20.188
l-tdapi2	IN		A	10.0.20.218
l-goods1	IN		A	10.0.20.220
l-goods2	IN		A	10.0.26.121
l-goods3	IN		A	10.0.26.122
l-goods4	IN		A	10.0.26.123
l-wallet1	IN		A	10.0.20.212
l-wallet2	IN		A	10.0.20.209
l-wallet3	IN		A	10.0.20.210
l-wallet4	IN		A	10.0.20.211
l-push1		IN		A	10.0.26.119
l-push2		IN		A	10.0.26.125
l-collect1	IN		A	10.0.26.128
l-collect2	IN		A	10.0.26.129
l-solrindex	IN		A	10.0.26.130
l-loadtest	IN		A	10.0.26.131
l-loadtest2	IN		A	10.0.26.132
l-special4      IN              A       10.0.26.105
l-special3      IN              A       10.0.26.103
l-special2      IN              A       10.0.26.102
l-special1      IN              A       10.0.26.101
$ORIGIN erp.bj2.daling.com.
l-vrmopenapi	IN		A	10.0.26.174
l-pay1		IN		A	10.0.26.63
l-pay2		IN		A	10.0.26.164
l-deeplucky1	IN		A	10.0.26.59
l-deeplucky2	IN		A	10.0.26.60
l-deeplucky3	IN		A	10.0.26.61
l-deeplucky4	IN		A	10.0.26.62
l-workform2	IN		A	10.0.20.162
l-workform1	IN		A	10.0.20.170
l-activiti2	IN		A	10.0.20.147
l-activiti1	IN		A	10.0.26.154
l-erp1          IN              A       10.0.20.254
l-erp2          IN              A       10.0.26.6
l-erp3          IN              A       10.0.26.64
l-erp4          IN              A       10.0.26.65
l-erp5          IN              A       10.0.26.66
l-erp6          IN              A       10.0.26.67
l-wms1          IN              A       10.0.26.36
l-wms2          IN              A       10.0.26.37
l-wms3          IN              A       10.0.26.68
l-wms4          IN              A       10.0.26.69
l-oauth1	IN		A	10.0.20.75
l-oauth2	IN		A	10.0.20.169	
l-activiti	IN		A	10.0.26.150
l-workform	IN		A	10.0.26.149
$ORIGIN	dba.bj2.daling.com.
l-mysqltest	IN		A	10.0.26.99
l-goodssync	IN		A	10.0.20.22
$ORIGIN zin.bj2.daling.com.
l-solrindex1 IN A 10.0.26.133
l-solrindex2 IN A 10.0.26.134

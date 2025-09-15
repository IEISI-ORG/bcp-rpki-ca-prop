# PostgreSQL

Some quick work to load the data from the python script (rpki_error_analyzer.py) for analysis later.

```
Timestamp,Host,Error_Type,Severity,Message
Sep 15 07:58:27,rpki-repo.canops.org,tls_handshake_failed,LOW,Sep 15 07:58:27 rpki-client: https://rpki-repo.canops.org/rrdp/notification.xml (23.140.52.8): TLS handshake: certificate verification failed: unable to get local issuer certificate
Sep 15 07:58:48,repo.kagl.me,tls_handshake_failed,HIGH,Sep 15 07:58:48 rpki-client: https://repo.kagl.me/rpki/notification.xml (104.37.40.237): TLS handshake: certificate verification failed: certificate has expired
Sep 15 07:58:27,rpki-repo.canops.org,fallback_to_rsync,LOW,"Sep 15 07:58:27 rpki-client: https://rpki-repo.canops.org/rrdp/notification.xml: load from network failed, fallback to rsync"
Sep 15 07:58:35,oto.wakuwaku.ne.jp,fallback_to_rsync,LOW,"Sep 15 07:58:35 rpki-client: https://oto.wakuwaku.ne.jp/pki/oshirase.xml: load from network failed, fallback to rsync"
```


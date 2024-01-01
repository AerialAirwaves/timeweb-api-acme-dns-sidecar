# ACME DNS Timeweb Sidecar
A simple sidecar, that mimics an [acme-dns](https://github.com/joohoi/acme-dns) API server
and allows to easily automate LetsEncrypt DNS-01 challenge for domains with Timeweb Cloud managed nameservers

Written with FastAPI, AioHTTP and AioTinyDB 

# Installation
1. Build it with docker:
```
docker build . -t ${DOCKER_IMAGE_FULL_NAME}
```

2. Fill env file (see .env.example)

**Security warning**: keep cloud access token as safe as possible, 
as it currently have no limitations and allows access to all cloud infrastructure of your account, not just DNS

3. Start:
```
docker run -d --env-file .env -p 8000:8000 -v ./data/:/data/ ${DOCKER_IMAGE_FULL_NAME} --name 'acme-dns-timeweb-sidecar'
```

4. Then fill your `registration.json` with pattern below, according to configuration:
```
{
	"${MANAGED_DOMAIN}": {
		"username":"${UPDATE_USERNAME}",
		"password":"${UPDATE_PASSWORD}",
		"fulldomain":"_acme-challenge.${MANAGED_DOMAIN}",
		"subdomain":"_acme-challenge",
		"allowfrom":["0.0.0.0/0"]
	}
}
```
5. Use a standard acme-dns plugin for certbot (or whatever you use) to obtain the certificate
6. Enjoy a wildcard certificate

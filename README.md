# ACME DNS Timeweb Sidecar
A simple sidecar, that mimics an [acme-dns](https://github.com/joohoi/acme-dns) API server
and allows to easily automate LetsEncrypt DNS-01 challenge for domains with Timeweb Cloud managed nameservers

Written with FastAPI, AioHTTP and AioTinyDB

# Purpose
To obtain a wildcard TLS Let's Encrypt certificate with a minimal effort using managed cloud DNS, without messing up
with deploying own nameservers - it's your only choice if you don't want to deploy your own DNS server, as at the moment
cloud managed DNS API does not give you an option to add NS records for subdomains, 
and therefore you cannot delegate it to acme-dns.

This sidecar automatically manage acme challenge TXT records for a single domain and optionally its subdomains:
it keeps created TXT records IDs in a small database and deletes old records automatically during the next renewal.
Moreover, it mimics acme-dns API semantic, and therefore you don't need to reinvent a new plugin for certbot.


# Installation
1. Build it with docker:
```
docker build . -t ${DOCKER_IMAGE_FULL_NAME}
```

2. Fill env file (see .env.example)

**Security warning**: keep cloud access token as safe as possible, 
as the PaaS currently have no option to limit its permissions and allows access to all cloud infrastructure of your account, not just DNS

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
		"subdomain":"${MANAGED_DOMAIN}",
		"allowfrom":["0.0.0.0/0"]
	}
}
```
**Notice**: You can use it for subdomains of `${MANAGED_DOMAIN}` as well - just set `subdomain` key's value
to something like `foo.bar.example.com` assuming `${MANAGED_DOMAIN}` is `example.com`.

Just keep in mind, you'll need to add additional records to those subdomains if it was set via wildcard,
as once this automation will create TXT record for subdomain, it will no longer be resolved via parent wildcard's records.
For example, if you've added `foo.example.com`, and earlier had it via A record for `*.example.com` pointing to somewhere,
`foo.example.com` will no longer resolve unless you explicitly add A records `foo.example.com` 
and optionally `*.foo.example.com`


5. Use a standard acme-dns plugin for certbot (or whatever you use) to obtain the certificate
6. Enjoy a wildcard certificate

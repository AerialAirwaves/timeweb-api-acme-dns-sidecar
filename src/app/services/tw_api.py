import logging

import aiohttp


class TimewebAPIService:
    BASE_URL = "https://api.timeweb.cloud"

    def __init__(self, token: str) -> None:
        self._token = token

    @property
    def _headers(self) -> dict:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {self._token}"}

    async def check_token(self) -> dict:
        request_url = f"{self.BASE_URL}/api/v1/account/status"
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url, headers=self._headers) as response:
                response.raise_for_status()
                return await response.json()

    async def create_acme_record(self, domain: str, acme_validation_token: str) -> int:
        request_url = f"{self.BASE_URL}/api/v1/domains/{domain}/dns-records"
        request_body = {"subdomain": "_acme-challenge", "type": "TXT", "value": acme_validation_token}

        async with aiohttp.ClientSession() as session:
            async with session.post(request_url, headers=self._headers, json=request_body) as response:
                response.raise_for_status()

                response_json = await response.json()
                record_id = response_json["dns_record"]["id"]

                logging.info(f"Created ACME DNS-01 challenge DNS record {record_id} for domain {domain}")
                return record_id

    async def delete_acme_record(self, domain: str, record_id: int) -> None:
        request_url = f"{self.BASE_URL}/api/v1/domains/{domain}/dns-records/{record_id}"
        async with aiohttp.ClientSession() as session:
            async with session.delete(request_url, headers=self._headers) as response:
                match response.status:
                    case 204:
                        logging.info(f"DNS Record {record_id} deleted for domain {domain}")
                    case 404:
                        logging.warning(f"Failed to delete DNS record {record_id} for domain {domain} - not exist")
                        pass
                    case _:
                        response.raise_for_status()

from typing import List
from ekp_sdk.dto.moralis_nft_dto import MoralisNftDto
from ekp_sdk.services.limiter import Limiter
from ekp_sdk.services.rest_client import RestClient


class MoralisApiService:
    def __init__(
        self,
        api_key: str,
        rest_client: RestClient
    ):
        self.base_url = "https://deep-index.moralis.io/api/v2"
        self.api_key = api_key
        self.rest_client = rest_client
        self.limiter = Limiter(250, 4)

    # -----------------------------------------------------------------

    async def get_token_usd_price(
        self,
        chain: str,
        address: str,
        to_block_number: int = None
    ):

        url = f"{self.base_url}/erc20/{address}/price?chain={chain}"

        if to_block_number:
            url += f"&to_block={to_block_number}"
        
        def handle_response(data, text):
            if "usdPrice" in data:
                return data["usdPrice"]
            
            return 0
            
        result = await self.__get(
            url, 
            handle_response, 
            allowed_response_codes = [200, 400]
        )

        return result
    
    # -----------------------------------------------------------------

    async def get_token_metadata(
        self,
        chain: str,
        address: str,
    ):

        url = f"{self.base_url}/erc20/metadata?chain={chain}&addresses={address}"

        result = await self.__get(url, fn=lambda data,text: data[0])

        return result
    # -----------------------------------------------------------------

    async def get_nfts_by_owner_and_token_address(
        self,
        owner_address: str,
        token_address: str,
        chain: str
    ) -> List[MoralisNftDto]:

        url = f"{self.base_url}/{owner_address}/nft/{token_address}?chain={chain}&format=decimal"

        result = await self.__get(url)

        return result

    # -----------------------------------------------------------------

    async def __get(self, url, fn=lambda data, text: data["result"], allowed_response_codes = [200]):
        headers = {"X-API-Key": self.api_key}

        result = await self.rest_client.get(
            url,
            fn,
            limiter=self.limiter,
            headers=headers,
            allowed_response_codes=allowed_response_codes
        )

        return result

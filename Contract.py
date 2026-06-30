# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from dataclasses import dataclass
from genlayer import *

@allow_storage
@dataclass
class NFT:
    owner: Address
    metadata_url: str
    description: str
    price: u256
    is_listed: u256  # عدد 0 یعنی برای فروش نیست، عدد 1 یعنی برای فروشه


class Contract(gl.Contract):
    nfts: TreeMap[u256, NFT]
    token_counter: u256

    def __init__(self):
        self.token_counter = u256(0)

    # ۱. ضرب توکن
    @gl.public.write
    def mint_nft(self, metadata_url: str, description: str) -> u256:
        self.token_counter = u256(int(self.token_counter) + 1)
        token_id = self.token_counter
        
        self.nfts[token_id] = NFT(
            owner=gl.message.sender_address,
            metadata_url=metadata_url,
            description=description,
            price=u256(0),
            is_listed=u256(0)
        )
        return token_id

    # ۲. قیمت‌گذاری برای فروش
    @gl.public.write
    def list_for_sale(self, token_id: u256, price: u256) -> None:
        nft = self.nfts[token_id]
        assert nft.owner == gl.message.sender_address, "Not the owner"
        
        nft.price = price
        nft.is_listed = u256(1)

    # ۳. خرید و انتقال مالکیت
    @gl.public.write
    def buy_nft(self, token_id: u256) -> None:
        nft = self.nfts[token_id]
        assert nft.is_listed == u256(1), "Not for sale"
        
        nft.owner = gl.message.sender_address
        nft.is_listed = u256(0)
        nft.price = u256(0)

    # ۴. مشاهده جزئیات توکن
    @gl.public.view
    def get_nft_details(self, token_id: u256) -> NFT:
        return self.nfts[token_id]

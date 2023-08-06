ETH_CHAIN = 'ETHERIUM'
POLYGON_CHAIN = 'POLYGON'
SOLANA_CHAIN = 'SOLANA'

CHAINS_SUPPORT = [ETH_CHAIN, POLYGON_CHAIN, SOLANA_CHAIN]

ETHNET = "https://api.etherscan.io"
POLYGONNET = "https://api.polygonscan.com"
BSCNET = "https://api.bscscan.com/"

COIN_GECHO_CHAIN_DATA = {
    ETH_CHAIN: {
        "chain_id": "ethereum",
        "coin_id": "ethereum",
    },
    POLYGON_CHAIN: {
        "chain_id": "polygon-pos",
        "coin_id": "matic-network",
    },
    SOLANA_CHAIN: {
        "chain_id": "solana",
        "coin_id": "solana",
    }
}
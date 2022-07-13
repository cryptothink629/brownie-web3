// SPDX-License-Identifier: MIT
// by Cryptothink

pragma solidity ^0.8.0;

import "./ERC721.sol";

contract Nft is ERC721 {
    uint public MAX_SUPPLY = 10000;

    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_){
    }

    function mint(address to, uint tokenId) external {
        require(tokenId >= 0 && tokenId < MAX_SUPPLY, "tokenId out of range");
        _mint(to, tokenId);
    }
}
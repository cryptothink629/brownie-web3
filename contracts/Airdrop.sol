pragma solidity ^0.8.4;

import "./IERC20.sol";

contract Airdrop {

    function airdrop(address _token, address[] calldata to, uint256[] calldata _amounts) external {
        require(to.length == _amounts.length, "Lengths of Addresses and Amounts NOT EQUAL");

        IERC20 token = IERC20(_token);

        for (uint8 i; i < to.length; i++) {
            token.transferFrom(msg.sender, to[i], _amounts[i]);
        }
    }
}
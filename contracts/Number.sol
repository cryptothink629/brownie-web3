pragma solidity ^0.8.0;

contract Number {
    uint public number;
	event Add(uint number);

    constructor () public {
        number = 1;
    }

    function set(uint v) public {
        number += v;
		emit Add(v);
    }

    function get() public view returns (uint) {
        return number;
    }

}

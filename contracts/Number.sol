pragma solidity ^0.8.0;

contract Number {
    uint public number;
	event Add(uint number);

    constructor (uint v) public {
        number = v;
    }

    function set(uint v) public {
        number += v;
		emit Add(v);
    }

    function get() public view returns (uint) {
        return number;
    }

}

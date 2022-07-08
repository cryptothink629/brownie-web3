pragma solidity ^0.8.0;

contract Number {
    uint public number;
    address owner;
	event Add(uint number);
	error NotOwner();

	modifier onlyOwner {
      if(owner != msg.sender){
            revert NotOwner();
        }
      _;
   }

    constructor () public {
        number = 1;
        owner = msg.sender;
    }

    function set(uint v) public onlyOwner {
        number += v;
		emit Add(v);
    }

    function get() public view returns (uint) {
        return number;
    }

    function testError() public {
        revert NotOwner();
    }

}

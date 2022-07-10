pragma solidity ^0.8.0;

contract Number {

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

}

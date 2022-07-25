// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ERC721.sol";
import "./Ownable.sol";

contract CuZuki is ERC721, Ownable {
    //Imports
    using Strings for uint256;

    //Token count 
    uint256 private supply = 0;

    //Token URI generation
    string baseURI;
    string public baseExtension = ".json";

    //Supply code
    uint256 public constant MAX_SUPPLY = 4444;

    //Pausing functionality
    bool public paused = true;

    //Price
    uint256 private _price = 0 ether;


    //--------------------------------------constructor--------------------------------------

    constructor(
        string memory _name,
        string memory _symbol,
        string memory _initBaseURI
    ) ERC721(_name, _symbol){
        //Set base uri
        baseURI = _initBaseURI;

        //Create 1 nft so that the collection gets listed on opensea
        _mint(msg.sender, supply);
        supply += 1;

    }

    //=========================================PUBLIC=========================================================
    //------------------------------------------count functions---------------------------

    // How many left
    function remainingSupply() public view returns (uint256) {
        return MAX_SUPPLY - supply;
    }

    // How many minted
    function tokenSupply() public view returns (uint256) {
        return supply;
    }


    //-----------------------------------------Price and amount functions--------------------------------------
    function Price() public view returns (uint256 _cost){
        return _price;
    }


    // --------------------------------------------------Minting functions---------------------------------------------------
    function MintCuZuki(uint256 _mintAmount) public payable {

        require(!paused, "CuZuki is paused!");
        require(_mintAmount > 0, "Cant order negative number");
        require(supply + _mintAmount <= MAX_SUPPLY, "This order would exceed the max supply");

        require(msg.value >= Price() * _mintAmount, "This order doesn't meet the price requirement for the current stage");


        for (uint256 i = 0; i < _mintAmount; i++) {
            _mint(msg.sender, supply);
            supply += 1;
        }
    }

    //------------------------------------------------------------Metadata---------------------------------------
    //Generate uri for metadata
    function tokenURI(uint256 tokenId) public view virtual override returns (string memory)
    {
        uint256 tokenId_ = tokenId + 1;
        string memory currentBaseURI = _baseURI();
        return bytes(currentBaseURI).length > 0
        ? string(abi.encodePacked(currentBaseURI, tokenId_.toString(), baseExtension))
        : "";
    }

    //=========================================================PRIVATE and OWNER=====================================
    //-------------------------------------------------------------------uri-------------------------------------------------------
    //returns the base uri for URI generation
    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    //Only Owner
    function setBaseURI(string memory _newBaseURI) public onlyOwner {
        baseURI = _newBaseURI;
    }

    //Pause the contract, if paused = true will not be able to mint
    function pause(bool _state) public onlyOwner {
        paused = _state;
    }

    //Change the price
    function setPrice(uint256 price) public onlyOwner {
        _price = price;
    }

    //Withdraw money from minting
    function withdraw() public payable onlyOwner {
        uint balance = address(this).balance;
        payable (msg.sender).transfer(balance);
    }
}
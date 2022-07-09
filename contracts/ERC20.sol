pragma solidity ^0.8.4;

import "./IERC20.sol";

contract ERC20 is IERC20 {
    mapping(address => uint256) private  _balances;
    mapping(address => mapping(address => uint256)) private  _allowances;
    uint256 private  _total_supply;

    string private _name;
    string private _symbol;

    uint8 private _decimals = 18;

    constructor(string memory name_, string memory symbol_){
        _name = name_;
        _symbol = symbol_;
    }

    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function decimals() public view returns (uint8) {
        return _decimals;
    }

    function totalSupply() external view override returns (uint256) {
        return _total_supply;
    }

    function balanceOf(address account) public view override returns (uint256) {
        return _balances[account];
    }

    function transfer(address to, uint amount) external override returns (bool) {
        _balances[msg.sender] -= amount;
        _balances[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function allowance(address owner, address spender) public view override returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint amount) external override returns (bool) {
        _allowances[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint amount) external override returns (bool){
        _allowances[from][msg.sender] -= amount;  // msg.sender is a contract generally

        _balances[from] -= amount;
        _balances[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }

    function _mint(address account, uint256 amount) internal {
        _total_supply += amount;
        _balances[account] += amount;
        emit Transfer(address(0), account, amount);
    }
}
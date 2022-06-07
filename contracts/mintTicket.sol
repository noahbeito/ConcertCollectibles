pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract ConcertToken is ERC721Full {
    constructor() public ERC721Full("ConcertToken", "CRT") { }

    struct Ticket {
        string name;
        string artist;
        uint256 value;
    }

    mapping(uint256 => Ticket) public ticketCollection;

    event TicketValuation(uint256 ticket_id, uint256 ticketValue, string reportURI)

// function to register new ticket
    function registerTicket(address owner, string memory name, string memory artist, uint256 initialTicketValue, string memory tokenURI)
        public returns (uint256) {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        ticketCollection[tokenId] = Ticket(name, artist, initialTicketValue)

        return tokenId;
    }
// function to give new value to tickets 
    function newTicketValuation(uint256 tokenId, uint256 newTicketValue, string memory reportURI) 
    public returns (uint256) {
        ticketCollection[tokenId].value = newTicketValue;
        emit TicketValuation(tokenId, newTicketValue, reportURI);
        return ticketCollection[tokenId].value;
    }
}

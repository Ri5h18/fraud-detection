// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FraudLog {
struct Record {
string txId;
bool isFraud;
uint timestamp;
}
Record[] public records;

event FraudRecorded(string txId, bool isFraud, uint timestamp);

function logFraud(string memory _txId, bool _isFraud) public {
    records.push(Record(_txId, _isFraud, block.timestamp));
    emit FraudRecorded(_txId, _isFraud, block.timestamp);
}

function getRecord(uint index) public view returns (string memory, bool, uint) {
    require(index < records.length, "Invalid index");
    Record memory r = records[index];
    return (r.txId, r.isFraud, r.timestamp);
}

function totalRecords() public view returns (uint) {
    return records.length;
}
}
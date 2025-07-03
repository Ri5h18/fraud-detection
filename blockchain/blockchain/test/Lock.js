const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FraudLog", function () {
let fraudLog;

beforeEach(async () => {
const FraudLog = await ethers.getContractFactory("FraudLog");
fraudLog = await FraudLog.deploy(); // no .deployed() needed
});

it("should start with zero records", async () => {
const count = await fraudLog.totalRecords();
expect(count).to.equal(0n); // note the 'n' because it's a BigInt
});

it("should log a new fraud record", async () => {
const txId = "TX123";
const isFraud = true;

const tx = await fraudLog.logFraud(txId, isFraud);
await tx.wait();

const count = await fraudLog.totalRecords();
expect(count).to.equal(1n);

const [storedTxId, storedIsFraud, timestamp] = await fraudLog.getRecord(0);
expect(storedTxId).to.equal(txId);
expect(storedIsFraud).to.equal(isFraud);
expect(timestamp).to.be.a("bigint");
});
});
const hre = require("hardhat");

async function main() {
const FraudLog = await hre.ethers.getContractFactory("FraudLog");
const fraudLog = await FraudLog.deploy();

// await fraudLog.deployed();
// 
console.log("✅ FraudLog deployed to:", fraudLog.target);
}



main().catch((error) => {
console.error(error);
process.exitCode = 1;
});
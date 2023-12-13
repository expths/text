const ether = require('ethers');
const { Worker, isMainThread, parentPort } = require('worker_threads')

function* addressGenerator() {
    while (true) {
        wallet = ether.Wallet.createRandom()
        if (/^0x114514/.test(wallet.address)) { yield wallet }
    }
}


if (isMainThread) {
    const workers = [1, 2, 3, 4, 5, 6, 7, 8];
    workers.forEach((i) => {
        console.log(`Start thread ${i}`)
        const worker = new Worker('./index.js')
        worker.on('message', (result) => {
            console.log(result)
        })
    })
} else {
    const aG = addressGenerator()
    parentPort.postMessage(aG.next())
}

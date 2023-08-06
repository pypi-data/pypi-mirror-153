const bc = new BroadcastChannel('nprompt_channel');

document.addEventListener('keydown', logKey);

const handledKeys = new Set([
    27, 32, 37, 39, 38, 40, 70, 77, 85,68, 80, 79,
]);

function logKey(e) {
    bc.postMessage(e.keyCode);
    if(handledKeys.has(e.keyCode))
    {
        e.preventDefault();
    }
}
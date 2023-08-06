const bc = new BroadcastChannel('nprompt_channel');

document.addEventListener('keydown', logKey);
document.addEventListener('wheel', handleScroll, {
    passive: false
});

document.addEventListener('click', toggleScrolling);

const manualScrollAmount = 10;
const fontSizeIncrease = 2;
const paddingSizeIncrease = 10;
const maxScrollSpeed = 200;
const scrollSpeedIncrease = 3;
const maxPadding = 250;
const maxFontSize = 200;
const content = $("#content");
const debug = $("#debug");
let fontSize = parseInt(content.css("font-size"));
let paddingSize = parseInt(content.css("padding-left"));
let isScrolling = false;
let scrollSpeed = 10;
let scrollTimer = 0;

/* Get the documentElement (<html>) to display the page in fullscreen */
const elem = document.documentElement;

function pageScroll() {
    window.scrollBy(0, 1); // horizontal and vertical scroll increments
    scrollTimer = setTimeout('pageScroll()', scrollSpeed);
}

/* View in fullscreen */
function openFullscreen() {
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) {
        /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
        /* IE11 */
        elem.msRequestFullscreen();
    }
}

/* Close fullscreen */
function closeFullscreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
        /* Safari */
        document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
        /* IE11 */
        document.msExitFullscreen();
    }
}

function toggleScrolling() {
    if (isScrolling === false) {
        pageScroll();
        isScrolling = true;
    } else {
        clearTimeout(scrollTimer);
        isScrolling = false;
    }
}

bc.onmessage = function(ev) {
    handleKeyCode(ev.data);
}


function handleKeyCode(keyCode) {
    let handled = true;

    switch (keyCode) {
        case 27: // Escape
            window.scrollTo(0, 0);
            break;
        case 32: // Space
            toggleScrolling();
            break;
        case 37: // Right arrow - Slow scroll
            scrollSpeed = Math.min(maxScrollSpeed, scrollSpeed + scrollSpeedIncrease)
            break;
        case 39: // Left arrow - Fast scroll
            scrollSpeed = Math.max(0, scrollSpeed - scrollSpeedIncrease)
            break;
        case 38: // Up arrow
            window.scrollBy(0, -1 * manualScrollAmount);
            break;
        case 40: // Down arrow
            window.scrollBy(0, manualScrollAmount);
            break;
        case 70: // F
            openFullscreen();
            break;
        case 77: // M
            $("#content").toggleClass("mirrored");
            break;
        case 85: // U - Increase font size
            fontSize = Math.min(maxFontSize, fontSize + fontSizeIncrease);
            content.css({
                'font-size': fontSize
            });
            break;
        case 68: // D - Decrease font size
            fontSize = Math.max(0, fontSize - fontSizeIncrease);
            content.css({
                'font-size': fontSize
            });
            break;
        case 80: // P - Increase padding
            paddingSize = Math.min(maxPadding, paddingSize + paddingSizeIncrease);
            content.css({
                'padding-left': paddingSize,
                'padding-right': paddingSize
            });
            break;
        case 79: // O - Decrease padding
            paddingSize = Math.max(0, paddingSize - paddingSizeIncrease);
            content.css({
                'padding-left': paddingSize,
                'padding-right': paddingSize
            });
            break;
        case 66: // B - Debug mode
            $("#debug").toggle();
            break
        default:
            handled = false;
            break;
    }
    if (handled) {
        updateDebug();
    }
    return handled;
}

function updateDebug() {
    debug.text(`Padding: ${paddingSize} | Font Size ${fontSize} | Scroll speed ${scrollSpeed}`);
}

function handleScroll(wheelEvent) {
    if (wheelEvent.deltaX != 0) {
        wheelEvent.preventDefault()
        const delta = parseInt(wheelEvent.deltaX)

        if (delta < 0) {
            scrollSpeed = Math.max(0, scrollSpeed - scrollSpeedIncrease)
        } else {
            scrollSpeed = Math.min(maxScrollSpeed, scrollSpeed + scrollSpeedIncrease)
        }

        updateDebug();
    }
}

function logKey(e) {
    const keyCode = e.keyCode;
    if (handleKeyCode(keyCode)) {
        e.preventDefault();
    }
}

updateDebug();

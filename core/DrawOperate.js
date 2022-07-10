let metricFlow;
let isDrag = false;
let isDown = false;
let nodes = [];
let moveTracks = [];
let lastPathX;
let lastPathY;
let lastNodeMinX = null;
let lastNodeMinY = null;
let lastNodeMaxX = null;
let lastNodeMaxY = null;
let menuMap = new Map();
let clickNodeId = null;
let clickLineId = null;

function drawRectangle(minX, minY, maxX, maxY, color) {
    let id = "node1" + guid();
    nodes.push(id);
    lastNodeMinX = minX;
    lastNodeMinY = minY;
    lastNodeMaxX = maxX;
    lastNodeMaxY = maxY;
    let node1 = {
        "x": minX,
        "y": minY,
        "id": id,
        "contextmenu": "nodeMenuClick",
        "dblclick": "dblClick",
        "style": {
            "node-type": "rectangle",
            'node-width': (maxX - minX) + 'px',
            'node-height': (maxY - minY) + 'px',
            'border-width': '3px',
            'border-color': (color == null || color == undefined) ? '#25264c' : color,
            'title-color': (color == null || color == undefined) ? '#25264c' : color,
        },
        "title": {'name': ""}
    }
    metricFlow.createNode(node1);
}

function drawTextRectangle(minX, minY, maxX, maxY, color) {
    let id = "node1" + guid();
    nodes.push(id);
    lastNodeMinX = minX;
    lastNodeMinY = minY;
    lastNodeMaxX = maxX;
    lastNodeMaxY = maxY;
    let node1 = {
        "x": minX,
        "y": minY,
        "id": id,
        "contextmenu": "nodeMenuClick",
        "dblclick": "dblClick",
        "style": {
            "node-type": "rectangle",
            'node-width': (maxX - minX) + 'px',
            'node-height': (maxY - minY) + 'px',
            'title-font-color': '#030531',
            'title-font-size': '14px',
            'border-width': '2px',
            'border-color': '#25264c',
            'title-color': (color == null || color == undefined) ? '#fafafc' : color,
        },
        "title": {'name': "text"}
    }
    metricFlow.createNode(node1);
}

function drawCircle(minX, minY, maxX, maxY, color) {
    let id = "node1" + guid();
    nodes.push(id);
    lastNodeMinX = minX;
    lastNodeMinY = minY;
    lastNodeMaxX = maxX;
    lastNodeMaxY = maxY;
    let node1 = {
        "x": minX,
        "y": minY,
        "id": id,
        "contextmenu": "nodeMenuClick",
        "dblclick": "dblClick",
        "style": {
            "node-type": "circle",
            'node-width': (maxX - minX) + 'px',
            'node-height': (maxX - minX) + 'px',
            'border-width': '3px',
            'border-color': (color == null || color == undefined) ? '#177854' : color,
            'title-color': (color == null || color == undefined) ? '#177854' : color
        },
        "title": {'name': ""}
    }
    metricFlow.createNode(node1);
}

function getLineStartIndex() {
    let minStartD = Number.MAX_VALUE;
    let minStartDIndex = 0;
    let lineStartX = moveTracks[0][0];
    let lineStartY = moveTracks[0][1];
    for (let i = 0; i < nodes.length; i++) {
        let nodeInfo = metricFlow.getNodeInfo(nodes[i]);
        let nodeXY = [nodeInfo['x'], nodeInfo['y'], nodeInfo['x'] + nodeInfo['width'], nodeInfo['y'] + nodeInfo['height']];
        let centerX = (nodeXY[0] + nodeXY[2]) / 2;
        let centerY = (nodeXY[1] + nodeXY[3]) / 2;
        let d = Math.sqrt(Math.pow(centerX - lineStartX, 2) + Math.pow(centerY - lineStartY, 2));
        if (d < minStartD) {
            minStartD = d;
            minStartDIndex = i;
        }
    }
    if (minStartD > 100) {
        return -1;
    }
    ;
    return minStartDIndex
}

function getLineEndIndex() {
    let minEndD = Number.MAX_VALUE;
    let minEndDIndex = 0;
    let lineEndX = moveTracks[moveTracks.length - 1][0];
    let lineEndY = moveTracks[moveTracks.length - 1][1];
    for (let i = 0; i < nodes.length; i++) {
        let nodeInfo = metricFlow.getNodeInfo(nodes[i]);
        let nodeXY = [nodeInfo['x'], nodeInfo['y'], nodeInfo['x'] + nodeInfo['width'], nodeInfo['y'] + nodeInfo['height']];
        let centerX = (nodeXY[0] + nodeXY[2]) / 2;
        let centerY = (nodeXY[1] + nodeXY[3]) / 2;
        let d = Math.sqrt(Math.pow(centerX - lineEndX, 2) + Math.pow(centerY - lineEndY, 2));
        if (d < minEndD) {
            minEndD = d;
            minEndDIndex = i;
        }
    }
    if (minEndD > 100) {
        return -1;
    }
    ;
    return minEndDIndex;
}

function drawLine(ex, ey) {
    let minStartDIndex = getLineStartIndex();
    let minEndDIndex = getLineEndIndex();
    if (minStartDIndex == -1 || minEndDIndex == -1) {
        return
    }
    ;
    metricFlow.createLink(document.getElementById(nodes[minStartDIndex]), document.getElementById(nodes[minEndDIndex]));
    metricFlow.bindLinkEvent(nodes[minStartDIndex], nodes[minEndDIndex], 'oncontextmenu', 'lineMenuClick');
}

function guid() {
    return 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function preventDefault(e) {
    window.event.cancelBubble = true;
    e.preventDefault();
}

function nodeMenuClick(e) {
    preventDefault(e);
    clickNodeId = metricFlow.getNodeId(e);
    let nodeMenu = document.querySelector("#node-menu");
    nodeMenu.style.display = 'block';
    nodeMenu.style.left = (e.x + 20) + 'px';
    nodeMenu.style.top = (e.y - 10) + 'px';
}

function lineMenuClick(e) {
    preventDefault(e);
    clickLineId = e.currentTarget.id;
    let nodeMenu = document.querySelector("#line-menu");
    nodeMenu.style.display = 'block';
    nodeMenu.style.left = (e.x + 20) + 'px';
    nodeMenu.style.top = (e.y - 30) + 'px';
}

function rayMenuClick(e) {
    preventDefault(e);
    clickLineId = e.currentTarget.id;
    let nodeMenu = document.querySelector("#ray-menu");
    nodeMenu.style.display = 'block';
    nodeMenu.style.left = (e.x + 20) + 'px';
    nodeMenu.style.top = (e.y - 30) + 'px';
}

function dblClick(e) {
    preventDefault(e);
    clickNodeId = metricFlow.getNodeId(e);
    let nodeInput = document.querySelector("#node-input");
    nodeInput.style.display = 'block';
    nodeInput.style.left = e.x + 'px';
    nodeInput.style.top = e.y + 'px';
    nodeInput.value = metricFlow.getTitle(clickNodeId);
    nodeInput.focus();
}

function setNodeTitle(value) {
    metricFlow.setTitle(clickNodeId, value);
    let info = metricFlow.getNodeInfo(clickNodeId);
    if (info['nodeType'] != 'circle') {
        metricFlow.stretchWidth(clickNodeId, value.length * 15);
    }
    ;
    let nodeInput = document.querySelector("#node-input");
    nodeInput.value = '';
    nodeInput.style.display = 'none';
    clickNodeId = null;
}

function removeNode() {
    metricFlow.removeNode(clickNodeId);
    let nodeInput = document.querySelector("#node-menu");
    nodeInput.style.display = 'none';
    for (let i = 0; i < nodes.length; i++) {
        if (nodes[i] == clickNodeId) {
            nodes.splice(i, 1);
        }
    }
    clickNodeId = null;
}

function newNode(e, nodeType) {
    if (nodeType == 'circle') {
        drawCircle(e.x - 30, e.y - 30, e.x + 30, e.y + 30);
    } else if (nodeType == 'rectangle') {
        drawRectangle(e.x - 40, e.y - 20, e.x + 40, e.y + 20);
    } else if (nodeType == 'textRectangle') {
        drawTextRectangle(e.x - 40, e.y - 20, e.x + 40, e.y + 20);
    }
    let nodeInput = document.querySelector("#back-menu");
    nodeInput.style.display = 'none';
}

function cloneRightNode() {
    let info = metricFlow.getNodeInfo(clickNodeId);
    let x = info['x'];
    let y = info['y'];
    let width = info['width'] - 6;
    let height = info['height'] - 6;
    let nx = x + width + width / 2 + 30;
    if (info['nodeType'] == 'circle') {
        drawCircle(nx, y, nx + width, y + height, info['titleBackgroundColor']);
    } else if (info['nodeType'] == 'rectangle') {
        let conNode = document.querySelector(`#${clickNodeId}-node`);
        if ("#fafafc" == conNode.style.backgroundColor || "rgb(250, 250, 252)" == conNode.style.backgroundColor) {
            width = info['width'] - 4;
            height = info['height'] - 4;
            drawTextRectangle(nx, y, nx + width, y + height, info['titleBackgroundColor']);
        } else {
            drawRectangle(nx, y, nx + width, y + height, info['titleBackgroundColor']);
        }
    }
    let nodeInput = document.querySelector("#node-menu");
    nodeInput.style.display = 'none';
    clickNodeId = null;
}

function cloneDownNode() {
    let info = metricFlow.getNodeInfo(clickNodeId);
    let x = info['x'];
    let y = info['y'];
    let width = info['width'] - 6;
    let height = info['height'] - 6;
    let ny = y + height + height / 2 + 30;
    if (info['nodeType'] == 'circle') {
        drawCircle(x, ny, x + width, ny + height, info['titleBackgroundColor']);
    } else if (info['nodeType'] == 'rectangle') {
        let conNode = document.querySelector(`#${clickNodeId}-node`);
        if ("#fafafc" == conNode.style.backgroundColor || "rgb(250, 250, 252)" == conNode.style.backgroundColor) {
            width = info['width'] - 4;
            height = info['height'] - 4;
            drawTextRectangle(x, ny, x + width, ny + height, info['titleBackgroundColor']);
        } else {
            drawRectangle(x, ny, x + width, ny + height, info['titleBackgroundColor']);
        }
    }
    let nodeInput = document.querySelector("#node-menu");
    nodeInput.style.display = 'none';
    clickNodeId = null;
}

function removeLine() {
    let lineIdSplit = clickLineId.split("-");
    metricFlow.removeLink(lineIdSplit[1], lineIdSplit[2]);
    lineIdSplit = null;
    let nodeInput = document.querySelector("#line-menu");
    nodeInput.style.display = 'none';
    clickLineId = null;
}

function removeRay() {
    metricFlow.removeRay(clickLineId);
    lineIdSplit = null;
    let nodeInput = document.querySelector("#ray-menu");
    nodeInput.style.display = 'none';
    clickLineId = null;
}

function setNodeColor(e) {
    let colorContainer = document.querySelector("#color-container");
    colorContainer.style.display = 'flex';
    colorContainer.style.left = (e.x + 30) + 'px';
    colorContainer.style.top = (e.y - 5) + 'px';

    let nodeMenu = document.querySelector("#node-menu");
    nodeMenu.style.display = 'none';
    let color = ColorPicker(
        document.getElementById('color-slide'),
        document.getElementById('color-picker'),
        function (hex, hsv, rgb) {
            if (clickNodeId != null) {
                metricFlow.setColor(clickNodeId, hex, hex);
            }
        });
}

function setLineColor(e) {
    let colorContainer = document.querySelector("#color-container");
    colorContainer.style.display = 'flex';
    colorContainer.style.left = (e.x + 30) + 'px';
    colorContainer.style.top = (e.y - 5) + 'px';

    let lineMenu = document.querySelector("#line-menu");
    lineMenu.style.display = 'none';

    let color = ColorPicker(
        document.getElementById('color-slide'),
        document.getElementById('color-picker'),
        function (hex, hsv, rgb) {
            if (clickLineId != null) {
                let lineIdSplit = clickLineId.split("-");
                metricFlow.setLinkColor(lineIdSplit[1], lineIdSplit[2], hex);
            }
        });
}

function clearAll() {
    metricFlow.clearAll();
    nodes = [];
    let backMenu = document.querySelector("#back-menu");
    backMenu.style.display = 'none';
}

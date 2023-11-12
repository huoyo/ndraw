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
let clickNodeId = null;
let clickLineId = null;
let clickFileName = null;

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
            'title-color': (color == null || color == undefined) ? '#25264c' : color
        },
        "title": {'name': ""}
    }
    nodeInfoList.push(deepClone(node1));
    metricFlow.createNode(node1);
}

function deepClone(obj) {
    let _obj = JSON.stringify(obj);
    let objClone = JSON.parse(_obj);
    return objClone;
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
            'title-color': (color == null || color == undefined) ? '#fafafc' : color
        },
        "title": {'name': "text"}
    }
    nodeInfoList.push(deepClone(node1));
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
    nodeInfoList.push(deepClone(node1));
    metricFlow.createNode(node1);
}

function getLineStartIndex() {
    let minStartD = Number.MAX_VALUE;
    let minStartDIndex = 0;
    let lineStartX = moveTracks[0][0];
    let lineStartY = moveTracks[0][1];
    let lineEndX = moveTracks[moveTracks.length - 1][0];
    for (let i = 0; i < nodes.length; i++) {
        let nodeInfo = metricFlow.getNodeInfo(nodes[i]);
        let nodeXY = [nodeInfo['x'], nodeInfo['y'], nodeInfo['x'] + nodeInfo['width'], nodeInfo['y'] + nodeInfo['height']];
        let centerX = (nodeXY[0] + nodeXY[2]) / 2;
        let centerY = (nodeXY[1] + nodeXY[3]) / 2;
        if ((lineEndX - lineStartX) > 10) {
            centerX = nodeXY[2];
            centerY = (nodeXY[1] + nodeXY[3]) / 2;
        } else if ((lineEndX - lineStartX) < 10) {
            centerX = nodeXY[0];
            centerY = (nodeXY[1] + nodeXY[3]) / 2;
        }

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
    let lineStartX = moveTracks[0][0];
    let lineEndX = moveTracks[moveTracks.length - 1][0];
    let lineEndY = moveTracks[moveTracks.length - 1][1];
    for (let i = 0; i < nodes.length; i++) {
        let nodeInfo = metricFlow.getNodeInfo(nodes[i]);
        let nodeXY = [nodeInfo['x'], nodeInfo['y'], nodeInfo['x'] + nodeInfo['width'], nodeInfo['y'] + nodeInfo['height']];
        let centerX = (nodeXY[0] + nodeXY[2]) / 2;
        let centerY = (nodeXY[1] + nodeXY[3]) / 2;
        if ((lineEndX - lineStartX) > 10) {
            centerX = nodeXY[0];
            centerY = (nodeXY[1] + nodeXY[3]) / 2;
        } else if ((lineEndX - lineStartX) < 10) {
            centerX = nodeXY[2];
            centerY = (nodeXY[1] + nodeXY[3]) / 2;
        }
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
    linkInfoList.push([nodes[minStartDIndex], nodes[minEndDIndex]])
    linkColorList.push('#3f6c53')
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
            nodeInfoList.splice(i, 1);
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
                for (let i = 0; i < linkInfoList.length; i++) {
                    let linkArray = linkInfoList[i]
                    if (lineIdSplit[1] === linkArray[0] && lineIdSplit[2] === linkArray[1]) {
                        linkColorList.splice(i, 1, hex);
                        break;
                    }
                }
            }
        });
}

function clearAll() {
    metricFlow.clearAll();
    nodes = [];
    nodeInfoList = [];
    linkInfoList = [];
    linkColorList = [];
    let backMenu = document.querySelector("#back-menu");
    backMenu.style.display = 'none';
}

function initFiles() {
    let fileMenu = document.querySelector("#file-menu");
    fileMenu.innerHTML = '';
    let li = document.createElement("li");
    li.innerHTML = 'Saved Files';
    li.style.borderBottom = 'border-bottom: 1px solid #3b3d3b;'
    fileMenu.appendChild(li);
    for (let i = 0; i < files.length; i++) {
        let li = document.createElement("li");
        li.innerHTML = files[i];
        li.setAttribute("onclick", `loadFileHtml('${files[i]}')`);
        li.setAttribute("oncontextmenu", `navMenuClick(event)`);
        fileMenu.appendChild(li);
    }
}

function loadFileHtml(fileName) {
    fetch('/getHtml', {
        method: 'post',
        body: JSON.stringify({'name': fileName}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(json => {
            let content = json['content'];
            let html = content['content'];
            let nodeList = content['nodes'];
            let links = content['links'];
            let linkColors = content['linkColors'];
            nodeInfoList = [];
            metricFlow.clearAll();
            nodes = [];
            for (let i = 0; i < nodeList.length; i++) {
                nodes.push(nodeList[i]['id'])
                nodeInfoList.push(deepClone(nodeList[i]));
                metricFlow.createNode(nodeList[i]);
            }
            linkInfoList = [];
            linkColorList = [];
            for (let i = 0; i < links.length; i++) {
                metricFlow.createLink(document.getElementById(links[i][0]), document.getElementById(links[i][1]));
                if (linkColors) {
                    metricFlow.setLinkColor(links[i][0], links[i][1], linkColors[i]);
                }
                metricFlow.bindLinkEvent(links[i][0], links[i][1], 'oncontextmenu', 'lineMenuClick');
                linkInfoList.push([links[i][0], links[i][1]]);
                linkColorList.push(linkColors[i]);
            }
            clickFileName = fileName;
        }).catch(e => {
    })
}

function showFileInput(e) {
    createMask();
    let fileInput = document.getElementById('file-input');
    fileInput.value = clickFileName;
    let fileModel = document.getElementById('file-model');
    fileModel.style.display = 'block';
    let backMenu = document.getElementById("back-menu");
    backMenu.style.display = 'none';

}

function enterpress(e) {
    if (e.keyCode == 13) {
        let fileInput = document.getElementById('file-input');
        if (fileInput.value) {
            saveAll(fileInput.value);
        } else {
            fileInput.value = 'please type a file name...'
        }
    }

}

function navMenuClick(e) {
    preventDefault(e);
    clickFileName = e.currentTarget.innerHTML;
    let nodeMenu = document.querySelector("#nav-menu");
    nodeMenu.style.display = 'block';
    nodeMenu.style.left = (e.x) + 'px';
    nodeMenu.style.top = (e.y) + 'px';
}


function removeFile() {
    preventDefault(event);
    for (let i = 0; i < files.length; i++) {
        if (files[i] == clickFileName) {
            files.splice(i, 1);
        }
    }
    fetch('/deleteHtml', {
        method: 'post',
        body: JSON.stringify({
            'name': clickFileName
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(json => {
            clearAll();
            initFiles();
            let nodeMenu = document.querySelector("#nav-menu");
            nodeMenu.style.display = 'none';
        }).catch(e => {
    })
}

function saveAll(name) {
    for (let i = 0; i < nodeInfoList.length; i++) {
        let nodeInfo = metricFlow.getNodeInfo(nodeInfoList[i]['id']);
        nodeInfoList[i]['x'] = nodeInfo['x'];
        nodeInfoList[i]['y'] = nodeInfo['y'];
        nodeInfoList[i]['title']['name'] = nodeInfo['title'];
        nodeInfoList[i]['style']['title-color'] = nodeInfo['titleBackgroundColor'];
        nodeInfoList[i]['style']['border-color'] = nodeInfo['borderColor'];
        nodeInfoList[i]['style']['node-width'] = `${nodeInfo['width']}px`;
        nodeInfoList[i]['style']['node-height'] = `${nodeInfo['height']}px`;
    }
    let graph = document.getElementById('graph');
    fetch('/saveHtml', {
        method: 'post',
        body: JSON.stringify({
            'nodes': nodeInfoList,
            'links': linkInfoList,
            'linkColors': linkColorList,
            'content': graph.innerHTML,
            'name': name
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(json => {
            let nodeInput = document.getElementById("file-input");
            nodeInput.value = '';
            let fileModel = document.getElementById('file-model');
            fileModel.style.display = 'none';
            closeMask();
            let nodeMenu = document.querySelector("#node-menu");
            nodeMenu.style.display = 'none';
            if (files.indexOf(name) == -1) {
                files.push(name);
            }
            initFiles();
        }).catch(e => {
    })
}

function closeMask() {
    let back = document.querySelector(".mask-back");
    if (back) {
        back.remove();
        let fileModel = document.getElementById('file-model');
        fileModel.style.display = 'none';
    }

}

function createMask() {
    let back = document.createElement("div");
    back.className = 'mask-back';
    back.addEventListener("click", function () {
        let back = document.querySelector(".mask-back");
        if (back) {
            back.remove();
            let fileModel = document.getElementById('file-model');
            fileModel.style.display = 'none';
        }
    });
    document.querySelector("body").appendChild(back);
}
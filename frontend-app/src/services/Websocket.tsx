let socket = null

export const connectWebsocket = (onMessage) => {
    const socket = new WebSocket('ws://' + '127.0.0.1:8000' + '/ws/mavlink/');

    socket.onopen = () => {
        console.log('Websocket connected')
    }

    socket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        onMessage(payload)
    }

    socket.onerror = (error) => {
        console.log('error:', error)
    }

    socket.onclose = () => {
        console.log('Websocket closed')
    }
}

export const disconnectWebsocket = () => {
    if (socket) {
        socket.close()
        socket = null
    }
}


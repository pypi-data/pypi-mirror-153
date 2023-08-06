import { nanoid } from 'https://cdn.jsdelivr.net/npm/nanoid/nanoid.js'
const { ref, reactive } = Vue;
const { useWebSocket } = window.VueUse;

class WSock {
    // Control debug message printing
    DEBUG = false

    constructor(path) {
        // A list of created routes and their callback methods
        this.cbRoutes = {}

        // Determine the correct protocol string
        let protocol_string = 'ws://';
        if (location.protocol == 'https:') {
            protocol_string = 'wss://';
        }

        const wsUrl = protocol_string + document.domain + ':' + location.port + path;

        this.socket = reactive(useWebSocket(wsUrl, {
            // Callback methods cannot be class methods in JavaScript
            // ... Because we loose access to `this`.
            // ... So use an arrow functions instead
            // ... Note that only arrow functions do not create a new context for `this`
            onConnected: (ws) => this.onConnected(ws),
            onMessage: (ws, evt) => this.onMessage(ws, evt),
        }));
    }

    onConnected(ws) {
        if (this.DEBUG) console.log("WS Connect:", ws);
    }

    onMessage(ws, evt) {
        let msg = JSON.parse(evt.data);
        let cmd = `${msg.route}>${msg.cmd}`;

        if (cmd in this.cbRoutes) {
            if (this.DEBUG) console.log(`WS Command[in] for [${msg.route}] cmd [${msg.cmd}]:`, msg.data);
            this.cbRoutes[cmd](msg);
        }
        else if (msg.route in this.cbRoutes) {
            if (this.DEBUG) console.log(`WS Message for [${msg.route}] cmd [${msg.cmd}]:`, msg.data);
            this.cbRoutes[msg.route](msg);
        }
        else {
            console.log("WS Message for Unknown Route:", msg);
        }
    }

    sendCmd(route, cmd, data = {}) {
        let message = {route: route, cmd: cmd, data: data};
        if (this.DEBUG) console.log("WS Command[out]:", message);
        return this.socket.send(JSON.stringify(message));
    }

    getCmdResponse(socketid, routeid, cmd, data = {}) {
        return new Promise((resolve, reject) => {
            // Add a uniqe response identifier to the command
            // ... The leading underscore (_) is used to mitigate the chance of conflicts with real command data
            const uuid = nanoid()
            data._rID = uuid

            const refThis = ref(this)

            // The callback function used for the response message
            function cbFunc(msg) {
                // A command response is a one-time event
                // ... Delete the route when the response is received
                delete refThis.value.cbRoutes[`${msg.route}>${msg.cmd}`]

                // Resolve the promise
                resolve(msg)
            }

            // This Create a new command with a callback linked to this unique identifier
            const cmdRoute = this.setCmdHandler(routeid, uuid, cbFunc);
            this.sendCmd(socketid, cmd, data);
        })
    }

    // Generate a unique route identifier
    // Save the callback function for received messages
    // Notify the server of this route identifier
    // Return the identifier
    getRoute(route, cbFunc) {
        let routeid = nanoid();
        this.cbRoutes[routeid] = cbFunc;
        this.sendCmd(route, 'connect', {route: routeid});
        return routeid
    }

    setCmdHandler(route, cmd, cbFunc) {
        let cmdRoute = `${route}>${cmd}`
        this.cbRoutes[cmdRoute] = cbFunc
        return cmdRoute
    }
}
export { WSock };

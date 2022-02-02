from fastapi import APIRouter
from fastapi.responses import HTMLResponse


test_page_router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <form action="" onsubmit="ackNotification(event)">
            <input type="text" id="ackMessage" autocomplete="off"/>
            <button>Ack</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/1");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                
                console.log("onMessage " + event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                console.log("sendMessage " + input.value)
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            };
            function ackNotification(even) {
                var input = document.getElementById("ackMessage")
                console.log("ackNotification " + input.value)
                ws.send(JSON.stringify({tx_hash: input.value}))
                input.value = ''
                event.preventDefault()
            };
        </script>
    </body>
</html>
"""


@test_page_router.get("/")
async def get():
    return HTMLResponse(html)

import React, { useState, useContext } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { AuthContext } from "../contexts/AuthContext";
import { useParams } from "react-router-dom";


export function Chat() {
  const [welcomeMessage, setWelcomeMessage] = useState("");
  const [messageHistory, setMessageHistory] = useState<any>([]);
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");
  const { user } = useContext(AuthContext);
  const { conversationName } = useParams();


  const { readyState, sendJsonMessage } = useWebSocket(
    user ? `ws://127.0.0.1:8000/chats/${conversationName}/` : null,
    {
      queryParams: {
        token: user ? user.token : "",
      },

      onOpen: () => {
        console.log("Connected!");
      },
      onClose: () => {
        console.log("Disconnected!");
      },
      onMessage: (e) => {
        const data = JSON.parse(e.data);
        console.log(e.data);
        switch (data.type) {
          case "welcome_message":
            setWelcomeMessage(data.message);
            break;
          case "chat_message_echo":
            setMessageHistory((prev: any) => prev.concat(data));
            break;
          case "greeting_response_echo":
            setMessageHistory((prev: any) => prev.concat(data));
            break;
          case "like_response_echo":
            setMessageHistory((prev: any) => prev.concat(data));
            break;
          case "save_response_echo":
            setMessageHistory((prev: any) => prev.concat(data));
            break;
          case "comment_response_echo":
            setMessageHistory((prev: any) => prev.concat(data));
            break;
          case "upload_response_echo":
            setMessageHistory((prev: any) => prev.concat(data));
            break;
          default:
            console.error("Unknown message type!");
            break;
        }
      },
    }
  );

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  function handleChangeMessage(e: any) {
    setMessage(e.target.value);
  }

  function handleChangeName(e: any) {
    setName(e.target.value);
  }

  function handleSubmit() {
    const data = { type: "chat_message", message, name };
    console.log(data);
    sendJsonMessage(data);
    setName("");
    setMessage("");
  }

  return (
    <div>
      <span>The WebSocket is currently {connectionStatus}</span>
      <p>{welcomeMessage}</p>

      {/* Test Button */}
      <button
        className="bg-gray-300 px-3 py-1"
        onClick={() => {
          sendJsonMessage({
            type: "greeting",
            message: "Hi Django from ReactApp!",
          });
        }}
      >
        GreetingWithBackend
      </button>

      {/* Like Post Button and Function */}
      <div>
        <button
          className="bg-gray-300 px-3 py-1"
          onClick={() => {
            sendJsonMessage({
              type: "Like",
              message: "I Like This Post!",
              token: "userAccessToken",
              post: "postID",
            });
          }}
        >
          Like
        </button>
      </div>

      {/* Save Post Button and Function */}
      <div>
        <button
          className="bg-gray-300 px-3 py-1"
          onClick={() => {
            sendJsonMessage({
              type: "Save",
              message: "I Want Save This Post!",
              token: "userAccessToken",
              post: "postID",
            });
          }}
        >
          Save
        </button>
      </div>

      {/* Comment Post Button and Function */}
      <div>
        <button
          className="bg-gray-300 px-3 py-1"
          onClick={() => {
            sendJsonMessage({
              type: "Comment",
              message: "I Write Comment !!!",
              token: "userAccessToken",
              post: "postID",
            });
          }}
        >
          Comment
        </button>
      </div>

      {/* Upload Button and Function */}
      <div>
        <button
          className="bg-gray-300 px-3 py-1"
          onClick={() => {
            sendJsonMessage({
              type: "Upload",
              message: "I Upload Post With This Category !!!",
              token: "userAccessToken",
              post: "postID",
            });
          }}
        >
          Upload
        </button>
      </div>
      <input
        name="name"
        placeholder="Name"
        onChange={handleChangeName}
        value={name}
        className="shadow-sm sm:text-sm border-gray-300 bg-gray-100 rounded-md"
      />
      <input
        name="message"
        placeholder="Message"
        onChange={handleChangeMessage}
        value={message}
        className="ml-2 shadow-sm sm:text-sm border-gray-300 bg-gray-100 rounded-md"
      />
      <button className="ml-3 bg-gray-300 px-3 py-1" onClick={handleSubmit}>
        Submit
      </button>
      <hr />
      <ul>
        {messageHistory.map((message: any, idx: number) => (
          <div className="border border-gray-200 py-3 px-3" key={idx}>
            {message.name}: {message.message}
          </div>
        ))}
      </ul>
    </div>
  );
}

"use client";

import React from "react";

export default function AgentResult({ result }:any) {
    if (!result || !result.messages) {
        return <div>No results found.</div>;
      }
    
      const getMessageType = (message:any) => {
        if (message.tool_call_id) return "tool";
        if (message.tool_calls) return "ai";
        if (message.content && !message.tool_calls && !message.tool_call_id) return "human";
        return "unknown";
      };
    
      return (
        <div className="p-6 bg-white rounded-lg shadow space-y-4 text-black">
          <h2 className="text-2xl font-bold mb-4">Agent Execution Result</h2>
    
          {result.messages.map((message:any, index:any) => {
            const type = getMessageType(message);
    
            return (
              <div
                key={index}
                className="p-4 border rounded space-y-2 bg-gray-50"
              >
                <div className="text-sm text-gray-500">Type: {type}</div>
    
                {type === "human" && (
                  <div>
                    <strong>User:</strong> {message.content}
                  </div>
                )}
    
                {type === "ai" && (
                  <div>
                    <strong>AI Response:</strong> {message.content}
                    {message.tool_calls?.length > 0 && (
                      <div className="mt-2">
                        <strong>Tool Calls:</strong>
                        <ul className="list-disc list-inside">
                          {message.tool_calls.map((toolCall:any, i:any) => (
                            <li key={i}>
                              <strong>{toolCall.name}</strong> — Arguments:{" "}
                              {JSON.stringify(toolCall.args)}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
    
                {type === "tool" && (
                  <div>
                    <strong>Tool Result:</strong> {message.content} <br />
                    <strong>Tool Name:</strong> {message.name}
                  </div>
                )}
    
                {type === "unknown" && (
                  <div>
                    <strong>Unknown message type:</strong> {JSON.stringify(message)}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      );
}

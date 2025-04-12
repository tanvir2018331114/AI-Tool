import { useState } from "react";
import { runTask } from "../lib/api";
import Router from "next/router";
import WorkflowTrace from "@/components/WorkflowTrace";
import AgentResult from "@/components/AgentResult";

export default function Home() {
  const [task, setTask] = useState("");
  const [trace, setTrace] = useState<any>(null);

  const handleRun = async () => {
    const res = await runTask(task);
    setTrace(res.data.trace);
  };

  return (
    <div className="p-6">
      <h1 className="text-xl mb-4">Tool Automator Agent</h1>
      <input
        className="border p-2 w-full mb-2"
        value={task}
        onChange={(e) => setTask(e.target.value)}
        placeholder="Enter task..."
      />
      <div className="flex items-center gap-2">
        <button onClick={handleRun} className="bg-blue-500 text-white px-4 py-2 rounded">
          Run
        </button>
        <button onClick={() => Router.push("/register")}>Add Tool</button>
      </div>

      <div className="flex items-center gap-2 mt-6">
        <div className="max-w-5xl">
          <h2 className="text-lg">Agent Result</h2>
          {trace && <div className="max-w-5xl mx-auto p-6">
            <AgentResult result={trace.result} />
          </div>}
        </div>

        <div className="w-full">
          <h2 className="text-lg">Workflow Trace</h2>
          {trace &&
            <WorkflowTrace nodes={trace.nodes} edges={trace.edges} />
          }

        </div>
      </div>


    </div>
  );
}

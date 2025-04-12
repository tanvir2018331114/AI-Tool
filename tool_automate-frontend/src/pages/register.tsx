import { useState } from "react";
import { registerTool } from "../lib/api";
import Router from "next/router";

export default function Register() {
  const [form, setForm] = useState<any>({
    name: "",
    description: "",
    input_params: "",
    output_type: "",
    code: "",
  });

  const handleSubmit = async () => {
    const tool = {
      ...form,
      input_params: JSON.parse(form.input_params),
    };
    await registerTool(tool);
    alert("Tool registered!");
  };

  return (
    <div className="p-6">
      <div>
        <button className="underline" onClick={()=>Router.push("/")}>{"<"} Back</button>
        <h1 className="text-xl mb-4">Register New Tool</h1>
      </div>
      
      {["name", "description", "output_type",].map((field) => (
        <input
          key={field}
          className="border p-2 w-full mb-2"
          placeholder={field}
          value={form[field]}
          onChange={(e) => setForm({ ...form, [field]: e.target.value })}
        />
      ))}
      <textarea
        className="border p-2 w-full mb-2"
        placeholder='Input Params (e.g., [{"name": "url", "type": "str"}])'
        value={form.input_params}
        onChange={(e) => setForm({ ...form, input_params: e.target.value })}
      />
      <textarea
      className="border p-2 w-full mb-2"
      rows={5}
      placeholder="Code"
      value={form.code}
      onChange={(e) => setForm({ ...form, code: e.target.value })}
      >

      </textarea>
      <button onClick={handleSubmit} className="bg-green-500 text-white px-4 py-2 rounded">
        Register Tool
      </button>
    </div>
  );
}

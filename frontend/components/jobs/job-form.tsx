"use client";

import React, { Dispatch, SetStateAction, useState } from "react";
import { 
  Button 
} from "@/components/ui/button";
import {
    Input,
} from "@/components/ui/input";
import {
    Label,
} from "@/components/ui/label";
import {
    Select,
} from "@/components/ui/select";
import {
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { BACKEND_URL } from "@/lib/config";
import { useJobStore } from "@/stores/useJobsStore";

type props = {
  setOpen: Dispatch<SetStateAction<boolean>>;
}
type FormData = {
  dataset_repo_id: string;
  model_id: string;
  gpu_type: string;
  policy_name: string;
  mode: "fine_tuning" | "from_scratch";
  steps: number;
  save_freq: number;
  log_freq: number;
  batch_size?: number | null;
};

export default function JobForm({ setOpen }: props) {
  const [form, setForm] = useState<FormData>({
    dataset_repo_id: "DanqingZ/filtered_pick_yellow_pink",
    model_id: "lerobot/pi0",
    gpu_type: "A100",
    policy_name: "Job name",
    mode: "fine_tuning",
    steps: 20,
    save_freq: 200000,
    log_freq: 100,
    batch_size: null,
  });
  const [loading, setLoading] = useState(false);

  const {addJob} = useJobStore();

  function handleChange<K extends keyof FormData>(key: K, value: FormData[K]) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    // Hit the fastapi backend
    await fetch(`${BACKEND_URL}/submit-job`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const newJob: Job = data.job as Job;
        console.log("New Job:", newJob);
        addJob(newJob);
        setOpen(false);
      })
      .catch((error) => {
        console.error("Error submitting job:", error);
      });
      setLoading(false);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 w-full mx-auto p-4">
      <div>
        <Label htmlFor="dataset_repo_id">Dataset Repo ID</Label>
        <Input
          id="dataset_repo_id"
          type="text"
          value={form.dataset_repo_id}
          onChange={(e) => handleChange("dataset_repo_id", e.target.value)}
          required
          placeholder="e.g. DanqingZ/filtered_pick_yellow_pink"
        />
      </div>

      <div>
        <Label htmlFor="model_id">Model ID</Label>
        <Input
          id="model_id"
          type="text"
          value={form.model_id}
          onChange={(e) => handleChange("model_id", e.target.value)}
          required
          placeholder="e.g. lerobot/pi0"
        />
      </div>

      <div>
        <Label htmlFor="gpu_type">GPU Type</Label>
        <Select
          value={form.gpu_type}
          onValueChange={(value) => handleChange("gpu_type", value as string)}
        >
          <SelectTrigger id="gpu_type">
            <SelectValue placeholder="Select GPU Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="A100">A100</SelectItem>
            <SelectItem value="H100">H100</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label htmlFor="policy_name">Policy Name</Label>
        <Input
          id="policy_name"
          type="text"
          value={form.policy_name}
          onChange={(e) => handleChange("policy_name", e.target.value)}
          required
          placeholder="Job name"
        />
      </div>

      <div>
        <Label htmlFor="mode">Mode</Label>
        <Select
          value={form.mode}
          onValueChange={(value) =>
            handleChange("mode", value as "fine_tuning" | "from_scratch")
          }
        >
          <SelectTrigger id="mode">
            <SelectValue placeholder="Select Mode" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="fine_tuning">Fine Tuning</SelectItem>
            <SelectItem value="from_scratch">From Scratch</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label htmlFor="steps">Steps</Label>
        <Input
          id="steps"
          type="number"
          min={1}
          value={form.steps}
          onChange={(e) => handleChange("steps", Number(e.target.value))}
          required
        />
      </div>

      <div>
        <Label htmlFor="save_freq">Save Frequency</Label>
        <Input
          id="save_freq"
          type="number"
          min={1}
          value={form.save_freq}
          onChange={(e) => handleChange("save_freq", Number(e.target.value))}
          required
        />
      </div>

      <div>
        <Label htmlFor="log_freq">Log Frequency</Label>
        <Input
          id="log_freq"
          type="number"
          min={1}
          value={form.log_freq}
          onChange={(e) => handleChange("log_freq", Number(e.target.value))}
          required
        />
      </div>

      <div>
        <Label htmlFor="batch_size">Batch Size (optional)</Label>
        <Input
          id="batch_size"
          type="number"
          min={1}
          value={form.batch_size ?? ""}
          onChange={(e) =>
            handleChange("batch_size", e.target.value ? Number(e.target.value) : null)
          }
          placeholder="e.g. 64"
        />
      </div>

      <Button type="submit" disabled={loading} className="w-full">
        Submit Job
      </Button>
    </form>
  );
}

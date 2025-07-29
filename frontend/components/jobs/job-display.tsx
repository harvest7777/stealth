import { IoIosInformationCircleOutline } from "react-icons/io";
import { LuRotateCcw } from "react-icons/lu";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { BACKEND_URL } from "@/lib/config";
import Link from "next/dist/client/link";

type props = {
    job: Job;
    className?: string;
}

const statusColors: Record<string, { bg: string; text: string }> = {
  pending: { bg: "bg-gray-100", text: "text-gray-700" },
  training: { bg: "bg-yellow-100", text: "text-yellow-700" },
  completed: { bg: "bg-green-100", text: "text-green-700" },
  failed: { bg: "bg-red-100", text: "text-red-700" },
};

export default function JobDisplay({job, className}:props) {
  async function handleRetry() {
    // You should only be able to retry if a job has failed
    if (job.status !== "failed") {
      console.warn("Job is not in a failed state, cannot retry.");
      return;
    }
    await fetch(`${BACKEND_URL}/retry-job`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ job_id: job.id }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const newJob: Job = data.job as Job;
        console.log("Retrying Job:", newJob);
      })
      .catch((error) => {
        console.error("Error retrying job:", error);
      });
  }
    return (
        <div className={`flex items-center align-middle ${className}`}>
            {job.upload_repo ? (
                <Link className="w-2/3 text-cyan-600 underline hover:cursor-pointer" href={`https://huggingface.co/${job.upload_repo}`} target="_blank">
                    <span>{job.policy_name}</span>
                </Link>
            ):(

                <span className="w-2/3">{job.policy_name}</span>
            )}
        <span className="w-2/3">{job.policy_name}</span>
        <div className="w-1/3">
            <span className={`px-2 rounded-md ${statusColors[job.status].bg} ${statusColors[job.status].text}`}>{job.status}</span>
        </div>

        <div className="flex gap-x-2 items-center align-middle">
            <LuRotateCcw onClick={()=>handleRetry()} className={`text-xl  ${job.status === "failed" ? "text-red-500 hover:cursor-pointer" : "text-gray-200 hover:cursor-not-allowed"}`}/>
            <Popover>
                <PopoverTrigger asChild>
                    <IoIosInformationCircleOutline className="text-2xl hover:cursor-pointer"/>
                </PopoverTrigger>
                <PopoverContent>
                    <dl className="grid grid-cols-2 gap-x-4 gap-y-2">
                    {Object.entries(job).map(([key, value]) => (
                        <div key={key} className="flex flex-col">
                        <dt className="font-semibold text-gray-700 capitalize truncate">{key.replace(/_/g, " ")}</dt>
                        <dd className="text-gray-900 truncate">
                            {value === null ? (
                            <span className="italic text-gray-500 truncate">null</span>
                            ) : (
                            value.toString()
                            )}
                        </dd>
                        </div>
                    ))}
                    </dl>
                </PopoverContent>
            </Popover>
        </div>
        </div>
    )

}
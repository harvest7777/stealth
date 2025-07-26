import { IoIosInformationCircleOutline } from "react-icons/io";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

type props = {
    job: Job
}

const statusColors: Record<string, { bg: string; text: string }> = {
  pending: { bg: "bg-gray-100", text: "text-gray-700" },
  training: { bg: "bg-yellow-100", text: "text-yellow-700" },
  completed: { bg: "bg-green-100", text: "text-green-700" },
  failed: { bg: "bg-red-100", text: "text-red-700" },
};

export default function JobDisplay({job}:props) {
    return (
        <div className="flex gap-x-2 p-2 items-center align-middle">
            <h2>{job.policy_name}</h2>
            <span className={`px-2 rounded-md ${statusColors[job.status].bg} ${statusColors[job.status].text}`}>{job.status}</span>
        <Popover>
        <PopoverTrigger>
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
    )

}
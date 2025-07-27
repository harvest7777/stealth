import { useJobStore } from "@/stores/useJobsStore";
import Spinner from "../ui/spinner";
import JobDisplay from "./job-display";

type props = {
    className?: string;
}
export default function JobList ({className}: props ) {
    const {jobs} = useJobStore();

    return (
        <div className={`flex flex-col ${className}`}>
            {jobs ? (
                <ul className="divide-y divide-gray-200">
                    {jobs.map(job => (
                        <JobDisplay className="py-4" key={job.id} job={job} />
                    ))}
                </ul>
            ) : (
                <Spinner/>
            )}
        </div>
    )

}

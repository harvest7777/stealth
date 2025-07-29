import { useJobStore } from "@/stores/useJobsStore";
import Spinner from "../ui/spinner";
import JobDisplay from "./job-display";

type props = {
    className?: string;
}
export default function JobList ({className}: props ) {
    const {jobs} = useJobStore();

    return (
        <div className={`flex flex-col ${className} justify-center items-center align-middle`}>
            {jobs ? (
                jobs.length > 0 ? (
                    <ul className="divide-y divide-gray-200 w-full">
                        {jobs.map(job => (
                            <JobDisplay className="py-4" key={job.id} job={job} />
                        ))}
                    </ul>
                ) : (
                    <h2 className="">No jobs available</h2>
                ) 
            ) : (
                <Spinner/>
            )}
        </div>
    )

}

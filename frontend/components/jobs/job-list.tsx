import { useJobStore } from "@/stores/useJobsStore";
import Spinner from "../ui/spinner";
import JobDisplay from "./job-display";

export default function JobList () {
    const {jobs} = useJobStore();

    return (
        <div>
            <h1>Jobs</h1>
            {jobs ? (
                <ul>
                    {jobs.map(job => (
                        <JobDisplay key={job.id} job={job} />
                    ))}
                </ul>
            ) : (
                <Spinner/>
            )}
        </div>
    )

}
